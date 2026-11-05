"""TV page: settings, page without login, live data, starting it on the TVs."""

from __future__ import annotations

import json
import sys
import types
from unittest.mock import MagicMock

from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ServiceValidationError
from homeassistant.helpers import device_registry as dr, entity_registry as er
from homeassistant.setup import async_setup_component
import pytest
from pytest_homeassistant_custom_component.common import async_mock_service

from custom_components.autodarts.const import DOMAIN

from .conftest import board_mock


async def _dienst(hass: HomeAssistant, dienst: str, **daten):
    return await hass.services.async_call(DOMAIN, dienst, daten, blocking=True, return_response=dienst == "spieler_anlegen")


def _tv(hass: HomeAssistant) -> dict:
    return hass.states.get("sensor.autodarts_board_players").attributes["tv"]


def _url(hass: HomeAssistant) -> str:
    return hass.config_entries.async_entries(DOMAIN)[0].runtime_data.fernseher.url()


def _token(hass: HomeAssistant) -> str:
    return _url(hass).rsplit("/", 1)[1]


def _geraet(hass: HomeAssistant, plattform: str, name: str, mock_entry) -> str:
    return er.async_get(hass).async_get_or_create("media_player", plattform, name, suggested_object_id=name).entity_id


@pytest.fixture
async def mit_http(hass: HomeAssistant, aioclient_mock, mock_entry):
    """Integration with the web server, so the page can be fetched."""
    assert await async_setup_component(hass, "http", {})
    board_mock(aioclient_mock)
    mock_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(mock_entry.entry_id)
    await hass.async_block_till_done()
    yield mock_entry
    await hass.config_entries.async_unload(mock_entry.entry_id)
    await hass.async_block_till_done()


async def test_einstellungen(hass: HomeAssistant, geladen) -> None:
    tv = _tv(hass)
    assert tv["geraete"] == [] and tv["auto"] is False
    assert "/autodarts/tv/" in _url(hass) and len(_token(hass)) == 32
    alt = _token(hass)
    await _dienst(hass, "fernseher_setzen", geraete=["media_player.a", "media_player.a", "media_player.b"], auto=True)
    tv = _tv(hass)
    assert tv["geraete"] == ["media_player.a", "media_player.b"] and tv["auto"] is True and _token(hass) == alt
    await _dienst(hass, "fernseher_setzen", neuer_link=True)
    assert _tv(hass)["url"] == _url(hass) and _token(hass) != alt and _tv(hass)["geraete"] == ["media_player.a", "media_player.b"]
    await _dienst(hass, "fernseher_setzen", geraete=[])
    assert _tv(hass)["geraete"] == []


async def test_seite_und_live(hass: HomeAssistant, mit_http, hass_client_no_auth) -> None:
    client = await hass_client_no_auth()
    assert (await client.get("/autodarts/tv/falsch")).status == 404
    assert (await client.get("/autodarts/tv/falsch/live")).status == 404
    token = _token(hass)
    r = await client.get(f"/autodarts/tv/{token}")
    assert r.status == 200 and "DartNest" in await r.text() and "EventSource" in await r.text()

    anna = (await _dienst(hass, "spieler_anlegen", name="Anna"))["id"]
    ben = (await _dienst(hass, "spieler_anlegen", name="Ben"))["id"]
    r = await client.get(f"/autodarts/tv/{token}/live")
    assert r.status == 200 and r.headers["Content-Type"].startswith("text/event-stream")
    zeile = (await r.content.readuntil(b"\n\n")).decode()
    assert zeile.startswith("data: ")
    daten = json.loads(zeile[6:])
    assert {"spiel", "rang", "verlauf", "sprache"} <= daten.keys()
    assert [x["name"] for x in daten["rang"]] == ["Anna", "Ben"] and "phase" not in daten["spiel"]

    # a started game arrives as the next message
    await _dienst(hass, "spiel_starten", spieler=[anna, ben], startwert=301)
    zeile = (await r.content.readuntil(b"\n\n")).decode()
    daten = json.loads(zeile[6:])
    assert daten["spiel"]["phase"] == "laeuft" and [p["rest"] for p in daten["spiel"]["spieler"]] == [301, 301]
    r.close()

    # a new link locks out the old one
    await _dienst(hass, "fernseher_setzen", neuer_link=True)
    assert (await client.get(f"/autodarts/tv/{token}")).status == 404
    assert (await client.get(f"/autodarts/tv/{_token(hass)}")).status == 200


async def test_fire_tv(hass: HomeAssistant, geladen) -> None:
    an = async_mock_service(hass, "media_player", "turn_on")
    adb = async_mock_service(hass, "androidtv", "adb_command")
    tv = _geraet(hass, "androidtv", "fire", geladen)
    with pytest.raises(ServiceValidationError) as fehler:
        await _dienst(hass, "fernseher_zeigen")
    assert fehler.value.translation_key == "no_tv"
    await _dienst(hass, "fernseher_setzen", geraete=[tv])
    await _dienst(hass, "fernseher_zeigen")
    assert an[0].data["entity_id"] == tv
    befehl = adb[0].data["command"]
    assert _url(hass) in befehl and "pm list packages -e com.amazon.cloud9" in befehl and "android.intent.action.VIEW" in befehl
    await _dienst(hass, "fernseher_beenden")
    assert adb[1].data == {"entity_id": tv, "command": "HOME"}


async def test_fire_tv_ohne_silk(hass: HomeAssistant, geladen) -> None:
    async_mock_service(hass, "media_player", "turn_on")
    tv = _geraet(hass, "androidtv", "fire", geladen)
    antwort = {"text": "DARTNEST_SILK_OFF"}

    async def adb(call) -> None:
        hass.states.async_set(tv, "idle", {"adb_response": antwort["text"]})

    hass.services.async_register("androidtv", "adb_command", adb)
    with pytest.raises(ServiceValidationError) as fehler:
        await _dienst(hass, "fernseher_zeigen", geraete=[tv])
    assert fehler.value.translation_key == "tv_silk_off"
    antwort["text"] = "Starting: Intent\nError: Activity not started, unable to resolve Intent"
    with pytest.raises(ServiceValidationError) as fehler:
        await _dienst(hass, "fernseher_zeigen", geraete=[tv])
    assert fehler.value.translation_key == "tv_failed" and "unable to resolve" in fehler.value.translation_placeholders["error"]
    antwort["text"] = "Starting: Intent { act=android.intent.action.VIEW }"
    await _dienst(hass, "fernseher_zeigen", geraete=[tv])


async def test_google_tv(hass: HomeAssistant, geladen) -> None:
    an = async_mock_service(hass, "media_player", "turn_on")
    spielen = async_mock_service(hass, "media_player", "play_media")
    senden = async_mock_service(hass, "remote", "send_command")
    reg, dreg = er.async_get(hass), dr.async_get(hass)
    geraet = dreg.async_get_or_create(config_entry_id=geladen.entry_id, identifiers={("test", "gtv")})
    tv = reg.async_get_or_create("media_player", "androidtv_remote", "gtv", suggested_object_id="gtv", device_id=geraet.id).entity_id
    fb = reg.async_get_or_create("remote", "androidtv_remote", "gtv", suggested_object_id="gtv", device_id=geraet.id).entity_id
    await _dienst(hass, "fernseher_zeigen", geraete=[tv])
    assert len(an) == 1 and spielen[0].data == {"entity_id": tv, "media_content_type": "url", "media_content_id": _url(hass)}
    await _dienst(hass, "fernseher_beenden", geraete=[tv])
    assert senden[0].data["entity_id"] == fb and senden[0].data["command"] in ("HOME", ["HOME"])


async def test_chromecast(hass: HomeAssistant, geladen, monkeypatch) -> None:
    aus = async_mock_service(hass, "media_player", "turn_off")
    tv = _geraet(hass, "cast", "wohnzimmer", geladen)
    with pytest.raises(ServiceValidationError) as fehler:
        await _dienst(hass, "fernseher_zeigen", geraete=[tv])
    assert fehler.value.translation_key == "tv_failed"

    dash = MagicMock()
    modul = types.ModuleType("pychromecast.controllers.dashcast")
    modul.DashCastController = lambda: dash  # type: ignore[attr-defined]
    for name in ("pychromecast", "pychromecast.controllers"):
        monkeypatch.setitem(sys.modules, name, types.ModuleType(name))
    monkeypatch.setitem(sys.modules, "pychromecast.controllers.dashcast", modul)
    entitaet = types.SimpleNamespace(_chromecast=MagicMock())
    komponente = types.SimpleNamespace(get_entity=lambda eid: entitaet if eid == tv else None)
    monkeypatch.setitem(hass.data, "media_player", komponente)
    await _dienst(hass, "fernseher_zeigen", geraete=[tv])
    entitaet._chromecast.register_handler.assert_called_once_with(dash)
    dash.load_url.assert_called_once_with(_url(hass), force=True)
    await _dienst(hass, "fernseher_beenden", geraete=[tv])
    assert aus[0].data["entity_id"] == tv


async def test_falsches_geraet_und_fehler(hass: HomeAssistant, geladen) -> None:
    hass.states.async_set("media_player.radio", "idle")
    with pytest.raises(ServiceValidationError) as fehler:
        await _dienst(hass, "fernseher_zeigen", geraete=["media_player.radio"])
    assert fehler.value.translation_key == "tv_unsupported"

    async def kaputt(call):
        from homeassistant.exceptions import HomeAssistantError

        raise HomeAssistantError("aus")

    hass.services.async_register("media_player", "turn_on", kaputt)
    tv = _geraet(hass, "androidtv", "fire", geladen)
    with pytest.raises(ServiceValidationError) as fehler:
        await _dienst(hass, "fernseher_zeigen", geraete=[tv])
    assert fehler.value.translation_key == "tv_failed"


async def test_von_selbst_beim_spielstart(hass: HomeAssistant, geladen) -> None:
    async_mock_service(hass, "media_player", "turn_on")
    adb = async_mock_service(hass, "androidtv", "adb_command")
    tv = _geraet(hass, "androidtv", "fire", geladen)
    anna = (await _dienst(hass, "spieler_anlegen", name="Anna"))["id"]
    await _dienst(hass, "fernseher_setzen", geraete=[tv])
    await _dienst(hass, "spiel_starten", spieler=[anna], startwert=101)
    await hass.async_block_till_done()
    assert adb == []  # off by default
    await _dienst(hass, "spiel_abbrechen")
    await _dienst(hass, "fernseher_setzen", auto=True)
    await _dienst(hass, "spiel_starten", spieler=[anna], startwert=101)
    await hass.async_block_till_done()
    assert len(adb) == 1

    # a TV that is off or unreachable does not break the game
    adb.clear()
    hass.services.async_remove("androidtv", "adb_command")
    await _dienst(hass, "spiel_abbrechen")
    await _dienst(hass, "spiel_starten", spieler=[anna], startwert=101)
    await hass.async_block_till_done()
    assert hass.states.get("sensor.autodarts_board_game").attributes["phase"] == "laeuft"
