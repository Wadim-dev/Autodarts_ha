"""Light effects on game events."""

from __future__ import annotations

import asyncio
from typing import Any
from unittest.mock import patch

from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import ServiceValidationError
from homeassistant.helpers import device_registry as dr, entity_registry as er
import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry, async_mock_service

from custom_components.autodarts import lichter as lichter_modul
from custom_components.autodarts.const import DOMAIN

FARBIG = {"supported_color_modes": ["hs"], "color_mode": "hs", "hs_color": [30.0, 50.0], "brightness": 120}
WEISS = {"supported_color_modes": ["color_temp"], "color_mode": "color_temp", "color_temp_kelvin": 3000, "brightness": 200}


@pytest.fixture
def lampen(hass: HomeAssistant) -> list[tuple[str, str, dict[str, Any]]]:
    """Fake light services that change the state like a real light."""
    aufrufe: list[tuple[str, str, dict[str, Any]]] = []

    async def dienst(call: ServiceCall) -> None:
        for e in call.data["entity_id"]:
            aufrufe.append((call.service, e, dict(call.data)))
            alt = hass.states.get(e)
            hass.states.async_set(e, "on" if call.service == "turn_on" else "off", alt.attributes if alt else {})

    hass.services.async_register("light", "turn_on", dienst)
    hass.services.async_register("light", "turn_off", dienst)
    hass.states.async_set("light.bunt", "on", FARBIG)
    hass.states.async_set("light.weiss", "on", WEISS)
    hass.states.async_set("light.aus", "off", {"supported_color_modes": ["onoff"]})
    hass.states.async_set("light.weg", "unavailable", {})
    return aufrufe


async def _setzen(hass: HomeAssistant, regeln: list[dict[str, Any]]) -> None:
    await hass.services.async_call(DOMAIN, "lichteffekte_setzen", {"regeln": regeln}, blocking=True)


async def _fertig(hass: HomeAssistant, show: lichter_modul.Lichtshow) -> None:
    await asyncio.gather(*show._laeufe.values(), return_exceptions=True)
    await hass.async_block_till_done()


@pytest.fixture(autouse=True)
def schnell():
    with patch.object(lichter_modul, "TAKT", 0.05):
        yield


async def test_regeln_speichern_und_lesen(hass: HomeAssistant, geladen, hass_ws_client, hass_storage) -> None:
    await _setzen(hass, [{"ereignis": "one_eighty", "lichter": ["light.bunt"], "effekt": "regenbogen"}])
    show = geladen.runtime_data.lichter
    assert show.regeln[0]["dauer"] == 3 and show.regeln[0]["aktiv"] and len(show.regeln[0]["id"]) == 8
    assert hass_storage["autodarts.lichter"]["data"]["regeln"] == show.regeln
    ws = await hass_ws_client(hass)
    await ws.send_json({"id": 1, "type": "autodarts/lichteffekte"})
    antwort = await ws.receive_json()
    assert antwort["result"]["regeln"][0]["effekt"] == "regenbogen"
    assert "bust" in antwort["result"]["ereignisse"] and "pulsieren" in antwort["result"]["effekte"]
    with pytest.raises(ServiceValidationError):
        await _setzen(hass, [{"ereignis": "gibtsnicht", "lichter": ["light.bunt"]}])
    with pytest.raises(ServiceValidationError):
        await _setzen(hass, [{"ereignis": "bust", "lichter": ["switch.x"]}])
    # rules are loaded again after a restart; broken ones are skipped
    hass_storage["autodarts.lichter"]["data"]["regeln"].append({"ereignis": "kaputt"})
    await show.laden()
    assert len(show.regeln) == 1


async def test_ws_ohne_eintrag(hass: HomeAssistant, geladen, hass_ws_client) -> None:
    await hass.config_entries.async_unload(geladen.entry_id)
    ws = await hass_ws_client(hass)
    await ws.send_json({"id": 1, "type": "autodarts/lichteffekte"})
    assert (await ws.receive_json())["result"]["regeln"] == []


@pytest.mark.parametrize("effekt", [e for e in lichter_modul.EFFEKTE if e not in ("lampe", "preset")])
async def test_effekte_und_zurueck(hass: HomeAssistant, geladen, lampen, effekt: str) -> None:
    show = geladen.runtime_data.lichter
    await _setzen(hass, [{"ereignis": "bust", "lichter": ["light.bunt", "light.weiss", "light.aus", "light.weg"],
                          "effekt": effekt, "farbe": [0, 0, 255], "dauer": 1, "helligkeit": 80},
                         {"ereignis": "bust", "lichter": ["light.weg"], "aktiv": True},
                         {"ereignis": "bust", "lichter": ["light.bunt"], "aktiv": False}])
    with patch.object(lichter_modul.asyncio, "sleep", side_effect=_kurz):
        show.ereignis("dart", {})
        assert not show._laeufe
        show.ereignis("bust", {})
        await _fertig(hass, show)
    farbe = [a for a in lampen if a[0] == "turn_on" and a[1] == "light.bunt" and "rgb_color" in a[2]]
    assert farbe and "rgb_color" not in next(a for a in lampen if a[1] == "light.aus" and a[0] == "turn_on")[2]
    # everything back as before
    assert lampen[-3:] == [
        ("turn_on", "light.bunt", {"entity_id": ["light.bunt"], "brightness": 120, "hs_color": [30.0, 50.0]}),
        ("turn_on", "light.weiss", {"entity_id": ["light.weiss"], "brightness": 200, "color_temp_kelvin": 3000}),
        ("turn_off", "light.aus", {"entity_id": ["light.aus"]}),
    ]
    assert not show._vorher and not show._besitz


_echt = asyncio.sleep


async def _kurz(sekunden: float) -> None:
    await _echt(min(sekunden, 0.05))


async def test_uebernahme_und_testen(hass: HomeAssistant, geladen, lampen) -> None:
    show = geladen.runtime_data.lichter
    await hass.services.async_call(DOMAIN, "lichteffekt_testen", {"regel": {"ereignis": "bust", "lichter": ["light.bunt", "light.weiss"],
                                                                             "effekt": "blinken", "dauer": 5}}, blocking=True)
    await asyncio.sleep(0.1)
    # a second effect takes over one light: the first run gives it back only to the new run
    show.abspielen(lichter_modul.regel_pruefen({"ereignis": "checkout", "lichter": ["light.bunt"], "effekt": "farbe", "dauer": 1}))
    await asyncio.sleep(0.05)
    await show.beenden()
    await hass.async_block_till_done()
    assert hass.states.get("light.bunt").state == "on"
    zurueck = [a for a in lampen if a[1] == "light.bunt" and "hs_color" in a[2]]
    assert len(zurueck) == 1 and not show._vorher
    with pytest.raises(ServiceValidationError):
        await hass.services.async_call(DOMAIN, "lichteffekt_testen", {"regel": {"ereignis": "bust", "lichter": []}}, blocking=True)
    # no usable light: nothing runs
    show.abspielen(lichter_modul.regel_pruefen({"ereignis": "bust", "lichter": ["light.weg"]}))
    assert not show._laeufe


async def test_fehler_stoert_nicht(hass: HomeAssistant, geladen, lampen, caplog) -> None:
    show = geladen.runtime_data.lichter

    async def kaputt(call: ServiceCall) -> None:
        raise RuntimeError("weg")

    hass.services.async_register("light", "turn_on", kaputt)
    show.abspielen(lichter_modul.regel_pruefen({"ereignis": "bust", "lichter": ["light.bunt"], "dauer": 1}))
    await _fertig(hass, show)
    assert "Light effect failed" in caplog.text and "Could not restore" in caplog.text


async def test_spiel_ereignis_loest_aus(hass: HomeAssistant, geladen, lampen) -> None:
    show = geladen.runtime_data.lichter
    await _setzen(hass, [{"ereignis": "one_eighty", "lichter": ["light.aus"], "dauer": 1}])
    geladen.runtime_data.spiel._ereignis("one_eighty", {})
    assert show._laeufe
    await show.beenden()


@pytest.fixture
def wled(hass: HomeAssistant, lampen) -> MockConfigEntry:
    """A WLED strip with preset select and speed/intensity numbers (as the WLED integration registers them)."""
    eintrag = MockConfigEntry(domain="wled")
    eintrag.add_to_hass(hass)
    geraet = dr.async_get(hass).async_get_or_create(config_entry_id=eintrag.entry_id, identifiers={("wled", "aa")})
    reg = er.async_get(hass)
    for domain, uid, key, oid in [("light", "l", None, "streifen"), ("select", "p", "preset", "streifen_preset"),
                                  ("number", "s", "speed", "streifen_speed"), ("number", "i", "intensity", "streifen_intensity"),
                                  ("select", "x", "playlist", "streifen_playlist")]:
        reg.async_get_or_create(domain, "wled", uid, device_id=geraet.id, translation_key=key, suggested_object_id=oid)
    hass.states.async_set("light.streifen", "on", {**FARBIG, "effect_list": ["Solid", "Fireworks"], "effect": "Solid"})
    hass.states.async_set("select.streifen_preset", "Abend", {"options": ["Abend", "Party"]})
    hass.states.async_set("number.streifen_speed", "128")
    hass.states.async_set("number.streifen_intensity", "100")
    return eintrag


async def test_wled_effekt_und_preset(hass: HomeAssistant, geladen, lampen, wled, hass_ws_client) -> None:
    show = geladen.runtime_data.lichter
    zahlen = async_mock_service(hass, "number", "set_value")
    auswahl = async_mock_service(hass, "select", "select_option")
    ws = await hass_ws_client(hass)
    await ws.send_json({"id": 1, "type": "autodarts/lichteffekte"})
    assert (await ws.receive_json())["result"]["wled"] == {"light.streifen": {"presets": ["Abend", "Party"], "tempo": True}}

    with patch.object(lichter_modul.asyncio, "sleep", side_effect=_kurz):
        show.abspielen(lichter_modul.regel_pruefen({"ereignis": "bust", "lichter": ["light.streifen", "light.weiss"], "effekt": "lampe",
                                                    "lampen_effekt": "Fireworks", "tempo": 200, "staerke": 50, "dauer": 1}))
        await asyncio.sleep(0)
        hass.states.async_set("light.streifen", "on", {**FARBIG, "effect_list": ["Solid", "Fireworks"], "effect": "Fireworks"})
        await _fertig(hass, show)
    an = [a for a in lampen if a[1] == "light.streifen" and a[0] == "turn_on"]
    assert an[0][2]["effect"] == "Fireworks" and an[-1][2]["effect"] == "Solid"
    assert "effect" not in next(a for a in lampen if a[1] == "light.weiss")[2]
    assert sorted((c.data["entity_id"], c.data["value"]) for c in zahlen) == [
        ("number.streifen_intensity", 50), ("number.streifen_intensity", 100.0), ("number.streifen_speed", 128.0), ("number.streifen_speed", 200)]

    with patch.object(lichter_modul.asyncio, "sleep", side_effect=_kurz):
        show.abspielen(lichter_modul.regel_pruefen({"ereignis": "bust", "lichter": ["light.streifen", "light.weiss"], "effekt": "preset",
                                                    "preset": "Party", "dauer": 1}))
        await _fertig(hass, show)
    assert [c.data for c in auswahl] == [{"entity_id": "select.streifen_preset", "option": "Party"}]
    # a light that is not WLED gets the colour instead
    assert any(a[1] == "light.weiss" and a[0] == "turn_on" and a[2].get("brightness_pct") for a in lampen)
    assert not show._vorher and not show._besitz
    assert lichter_modul.wled_teile(hass, "light.weiss") == {}
