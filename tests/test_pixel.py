"""Pixel displays: find AWTRIX 3 / PixelIt by address, score during the game, effects, give the display back."""

from __future__ import annotations

import asyncio
import json

from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ServiceValidationError
import pytest

from custom_components.autodarts import pixel as pixel_modul
from custom_components.autodarts.const import DOMAIN

AWTRIX = "http://192.0.2.10"
PIXELIT = "http://192.0.2.11"
ATTR = "sensor.autodarts_board_players"


async def _dienst(hass: HomeAssistant, dienst: str, **daten):
    antwort = dienst in ("spieler_anlegen", "pixel_hinzufuegen")
    return await hass.services.async_call(DOMAIN, dienst, daten, blocking=True, return_response=antwort)


def _posts(aioclient_mock, basis: str, pfad: str) -> list:
    return [json.loads(c[2]) if isinstance(c[2], (str, bytes)) and c[2] else c[2]
            for c in aioclient_mock.mock_calls if c[0] == "POST" and str(c[1]).startswith(f"{basis}/api/{pfad}")]


def test_host_pruefen() -> None:
    assert pixel_modul.host_pruefen(" http://192.168.1.5/ ") == "192.168.1.5"
    assert pixel_modul.host_pruefen("awtrix.local:8080") == "awtrix.local:8080"
    for falsch in ("", "a b", "192.168.1.5;rm", "http://"):
        with pytest.raises(ServiceValidationError):
            pixel_modul.host_pruefen(falsch)


def test_anzeige() -> None:
    a = {"phase": "laeuft", "art": "x01", "am_zug": 1, "spieler": [{"name": "Anna", "rest": 501}, {"name": "Benjamin", "rest": 321}],
         "aufnahme": {"darts": []}}
    assert pixel_modul.anzeige(a, "en") == [{"t": "BENJAM ", "c": pixel_modul.WEISS}, {"t": "321", "c": pixel_modul.ORANGE}]
    a["art"], a["spieler"][1] = "atc", {"name": "Ben", "ziel": "S7"}
    assert pixel_modul.anzeige(a, "en")[1]["t"] == "S7"
    a["aufnahme"] = {"darts": [], "bust": True}
    assert pixel_modul.anzeige(a, "en")[1]["t"] == "BUST"
    assert pixel_modul.anzeige({"phase": "beendet", "gewinner": 0, "spieler": a["spieler"]}, "de")[1]["t"] == " GEWINNT"
    assert pixel_modul.anzeige({"phase": "bulloff"}, "en") == [{"t": "BULL-OFF", "c": pixel_modul.ORANGE}]
    assert pixel_modul.anzeige({}, "en") is None


async def test_pixel_anzeigen(hass: HomeAssistant, geladen, aioclient_mock, monkeypatch) -> None:
    monkeypatch.setattr(pixel_modul, "EFFEKT_DAUER", 0.2)
    aioclient_mock.get(f"{AWTRIX}/api/stats", json={"version": "0.98", "app": "Time", "uptime": 12})
    aioclient_mock.get(f"{PIXELIT}/api/stats", status=404)
    aioclient_mock.get(f"{PIXELIT}/api/matrixinfo", json={"pixelitVersion": "2.5.0"})
    aioclient_mock.get("http://192.0.2.12/api/stats", exc=TimeoutError)
    aioclient_mock.get("http://192.0.2.12/api/matrixinfo", exc=TimeoutError)
    for basis in (AWTRIX, PIXELIT):
        for pfad in ("custom", "switch", "notify", "screen"):
            aioclient_mock.post(f"{basis}/api/{pfad}", json={})
    attr = lambda: hass.states.get(ATTR).attributes["pixel"]  # noqa: E731

    assert attr()["geraete"] == [] and attr()["an"] is True
    with pytest.raises(ServiceValidationError) as err:
        await _dienst(hass, "pixel_testen")
    assert err.value.translation_key == "pixel_none"

    neu = await _dienst(hass, "pixel_hinzufuegen", adresse="192.0.2.10")
    assert neu == {"host": "192.0.2.10", "typ": "awtrix", "name": "AWTRIX 3", "version": "0.98"}
    assert (await _dienst(hass, "pixel_hinzufuegen", adresse="http://192.0.2.11/"))["typ"] == "pixelit"
    for adresse, schluessel in (("192.0.2.12", "pixel_not_found"), ("192.0.2.10", "pixel_exists"), ("nix da", "pixel_bad_address")):
        with pytest.raises(ServiceValidationError) as err:
            await _dienst(hass, "pixel_hinzufuegen", adresse=adresse)
        assert err.value.translation_key == schluessel
    assert [g["typ"] for g in attr()["geraete"]] == ["awtrix", "pixelit"] and attr()["geraete"][0]["online"] is True
    # greeting on adding
    assert _posts(aioclient_mock, AWTRIX, "notify")[0]["text"][0]["t"] == "DARTNEST"

    # game: score of the player at the oche, DartNest app switched to
    anna, ben = [(await _dienst(hass, "spieler_anlegen", name=n))["id"] for n in ("Anna", "Ben")]
    await _dienst(hass, "spiel_starten", spieler=[anna, ben], startwert=501)
    await asyncio.sleep(0.5)
    await hass.async_block_till_done()
    app = _posts(aioclient_mock, AWTRIX, "custom")
    assert app[-1]["text"] == [{"t": "ANNA ", "c": "#FFFFFF"}, {"t": "501", "c": "#FF8A4C"}] and app[-1]["lifetime"] == 900
    assert _posts(aioclient_mock, AWTRIX, "switch") == [{"name": "dartnest"}]
    assert _posts(aioclient_mock, PIXELIT, "screen")[-1]["text"]["textString"] == "ANNA 501"
    assert attr()["vorschau"][1]["t"] == "501"

    # 180: one effect (rainbow), afterwards Ben with his rest
    for i in range(3):
        await _dienst(hass, "wurf_aendern", dart=i, feld="T20")
    await _dienst(hass, "weiter")
    await asyncio.sleep(0.6)
    await hass.async_block_till_done()
    effekte = [n for n in _posts(aioclient_mock, AWTRIX, "notify") if n["text"][0]["t"] == "180!"]
    assert len(effekte) == 1 and effekte[0]["rainbow"] is True
    assert _posts(aioclient_mock, AWTRIX, "custom")[-1]["text"][0]["t"] == "BEN "
    # PixelIt: effect, then the score again
    texte = [s["text"]["textString"] for s in _posts(aioclient_mock, PIXELIT, "screen") if "text" in s]
    assert "180!" in texte and texte[-1] == "BEN 501"

    # switched off: the displays are given back (AWTRIX app removed, PixelIt clock)
    await _dienst(hass, "pixel_setzen", an=False)
    await hass.async_block_till_done()
    assert _posts(aioclient_mock, AWTRIX, "custom")[-1] is None
    assert "clock" in _posts(aioclient_mock, PIXELIT, "screen")[-1]
    assert attr()["vorschau"] is None

    await _dienst(hass, "pixel_entfernen", adresse="192.0.2.11")
    assert [g["host"] for g in attr()["geraete"]] == ["192.0.2.10"]
    await _dienst(hass, "spiel_abbrechen")


async def test_sieger_dann_freigeben(hass: HomeAssistant, geladen, aioclient_mock, monkeypatch) -> None:
    monkeypatch.setattr(pixel_modul, "SIEGER_ZEIT", 0.5)
    aioclient_mock.get(f"{AWTRIX}/api/stats", json={"version": "0.98"})
    for pfad in ("custom", "switch", "notify"):
        aioclient_mock.post(f"{AWTRIX}/api/{pfad}", json={})
    await _dienst(hass, "pixel_hinzufuegen", adresse="192.0.2.10")
    (anna,) = [(await _dienst(hass, "spieler_anlegen", name=n))["id"] for n in ("Anna",)]
    await _dienst(hass, "spiel_starten", spieler=[anna], startwert=101)
    for i, feld in enumerate(("T20", "T7", "D10")):
        await _dienst(hass, "wurf_aendern", dart=i, feld=feld)
    await asyncio.sleep(0.4)
    await hass.async_block_till_done()
    assert _posts(aioclient_mock, AWTRIX, "custom")[-1]["text"][0]["t"] == "ANNA"
    assert any(n["text"][0]["t"] == "ANNA WINS" and n["rainbow"] for n in _posts(aioclient_mock, AWTRIX, "notify"))
    # a moment later the display is given back
    await asyncio.sleep(1.2)
    await hass.async_block_till_done()
    assert _posts(aioclient_mock, AWTRIX, "custom")[-1] is None
