"""Tests for local X01 games: actions, board throws, bull-off, bot, statistics."""

from __future__ import annotations

from unittest.mock import patch

from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ServiceValidationError
import pytest
import voluptuous as vol

from custom_components.autodarts.const import DOMAIN
from custom_components.autodarts.coordinator import OFFLINE
from custom_components.autodarts.spiel import modus_text

SPIEL = "sensor.autodarts_board_game"
SPIELER = "sensor.autodarts_board_players"


async def _dienst(hass: HomeAssistant, dienst: str, **daten):
    return await hass.services.async_call(DOMAIN, dienst, daten, blocking=True, return_response=dienst == "spieler_anlegen")


def _board(hass: HomeAssistant, entry, felder: list[str], laeuft: bool = True) -> None:
    """Simulate the board: `felder` are the darts currently on the board."""
    wuerfe = []
    for f in felder:
        zahl = 0 if f == "M" else int(f[1:])
        faktor = {"S": 1, "D": 2, "T": 3}.get(f[0], 0)
        wuerfe.append({"feld": f, "zahl": zahl, "faktor": faktor, "punkte": zahl * faktor, "bereich": "", "x": 0.0, "y": 0.5,
                       "abpraller": False, "fehlgeschlagen": False, "methode": ""})
    entry.runtime_data.zustand.async_set_updated_data(
        {"verbindung": "Online", "status": "Throw", "ereignis": "-", "laeuft": laeuft, "wuerfe": wuerfe}
    )


def _attr(hass: HomeAssistant, name: str):
    return hass.states.get(SPIEL).attributes[name]


async def _spieler(hass: HomeAssistant, *namen: str) -> list[str]:
    return [(await _dienst(hass, "spieler_anlegen", name=n))["id"] for n in namen]


async def test_ganzes_spiel(hass: HomeAssistant, geladen) -> None:
    anna, ben = await _spieler(hass, "Anna", "Ben")
    assert hass.states.get(SPIELER).state == "2"
    assert hass.states.get(SPIEL).state == "idle"

    await _dienst(hass, "spiel_starten", spieler=[anna, ben], startwert=101, auswurf="double")
    await hass.async_block_till_done()
    assert hass.states.get(SPIEL).state == "running"
    assert _attr(hass, "modus") == "101 · Double Out · Erster bis 1 Leg"

    # Anna: three darts from the board, then the darts are pulled
    _board(hass, geladen, [])
    _board(hass, geladen, ["T20"])
    _board(hass, geladen, ["T20", "S1"])
    _board(hass, geladen, ["T20", "S1", "M"])
    await hass.async_block_till_done()
    assert _attr(hass, "spieler")[0]["rest"] == 40
    # board corrects the second dart afterwards
    _board(hass, geladen, ["T20", "S5", "M"])
    assert _attr(hass, "spieler")[0]["rest"] == 36
    _board(hass, geladen, [])
    assert _attr(hass, "am_zug") == 1

    # Ben by hand, then "next"
    await _dienst(hass, "wurf_aendern", dart=0, feld="t19")
    await _dienst(hass, "wurf_aendern", dart=1, feld="25")
    await _dienst(hass, "weiter")
    assert _attr(hass, "spieler")[1]["rest"] == 19
    # correct Ben's first visit afterwards, remove a dart again
    await _dienst(hass, "wurf_aendern", aufnahme=1, dart=1, feld="BULL")
    assert _attr(hass, "spieler")[1]["rest"] == 101  # bust
    await _dienst(hass, "wurf_aendern", aufnahme=1, dart=1, feld="")
    assert _attr(hass, "spieler")[1]["rest"] == 44

    # Anna checks out 36 with D18
    await _dienst(hass, "wurf_aendern", dart=0, feld="D18")
    await hass.async_block_till_done()
    assert hass.states.get(SPIEL).state == "finished"
    assert _attr(hass, "gewinner") == 0
    stat = {s["name"]: s for s in hass.states.get(SPIELER).attributes["spieler"]}
    assert stat["Anna"]["siege"] == 1 and stat["Anna"]["spiele"] == 1 and stat["Anna"]["finish"] == 36
    assert stat["Ben"]["siege"] == 0 and stat["Ben"]["spiele"] == 1
    assert hass.states.get(SPIELER).attributes["verlauf"][0]["gewinner"] == "Anna"

    # undo after the end: game runs again and statistics are taken back
    await _dienst(hass, "rueckgaengig")
    assert hass.states.get(SPIEL).state == "running"
    stat = {s["name"]: s for s in hass.states.get(SPIELER).attributes["spieler"]}
    assert stat["Anna"]["spiele"] == 0 and stat["Anna"]["siege"] == 0
    assert hass.states.get(SPIELER).attributes["verlauf"] == []

    await _dienst(hass, "spiel_abbrechen")
    assert hass.states.get(SPIEL).state == "idle"
    assert hass.states.get(SPIEL).attributes == {"quelle": "HA", "friendly_name": "Autodarts Board Game", "device_class": "enum", "options": ["idle", "bull_off", "running", "finished"]}


async def test_bull_off(hass: HomeAssistant, geladen) -> None:
    anna, ben = await _spieler(hass, "Anna", "Ben")
    await _dienst(hass, "spiel_starten", spieler=[anna, ben], startwert=301, einwurf="double", legs=3, sets=2, bull_off=True)
    assert hass.states.get(SPIEL).state == "bull_off"
    assert _attr(hass, "modus") == "301 · Double In · Double Out · Erster bis 2 Sets à 3 Legs"
    # both hit the bull: tie, both throw again
    await _dienst(hass, "wurf_aendern", dart=0, feld="50")
    await _dienst(hass, "wurf_aendern", dart=1, feld="D25")
    assert _attr(hass, "gleichstand") == 1
    # undo restores the first round minus the last dart
    await _dienst(hass, "rueckgaengig")
    assert _attr(hass, "gleichstand") == 0
    assert _attr(hass, "bulloff")[0]["dart"]["f"] == "D25"
    await _dienst(hass, "rueckgaengig")
    assert _attr(hass, "bulloff")[0]["dart"] is None
    # Anna from the board, Ben misses ("next")
    _board(hass, geladen, [])
    _board(hass, geladen, ["S25"])
    await _dienst(hass, "wurf_aendern", dart=0, feld="D25")
    await _dienst(hass, "weiter")
    assert hass.states.get(SPIEL).state == "running"
    assert _attr(hass, "reihenfolge") == [0, 1]
    # undo with no visit yet: back to bull-off
    await _dienst(hass, "rueckgaengig")
    assert hass.states.get(SPIEL).state == "bull_off"


async def test_bot(hass: HomeAssistant, geladen) -> None:
    (anna,) = await _spieler(hass, "Anna")
    with patch("custom_components.autodarts.spiel._pause"), patch(
        "custom_components.autodarts.x01.streuung", return_value=0.001
    ):
        await _dienst(hass, "spiel_starten", spieler=["bot:60", anna], startwert=101, bull_off=True)
        await hass.async_block_till_done()
        # bot throws its bull-off dart, Anna misses
        assert _attr(hass, "bulloff")[0]["dart"]["f"] == "D25"
        await _dienst(hass, "weiter")
        await hass.async_block_till_done()
        # bot won the bull-off and plays its visit: T20 T20 ... aims at the checkout
        assert hass.states.get(SPIEL).state in ("running", "finished")
        verlauf = _attr(hass, "verlauf")
        assert verlauf and verlauf[0]["s"] == 0
        # board darts are ignored while the bot is on
        assert _attr(hass, "spieler")[1]["rest"] == 101


async def test_fehler(hass: HomeAssistant, geladen) -> None:
    (anna,) = await _spieler(hass, "Anna")
    faelle = [
        ("spiel_starten", {"spieler": [anna], "startwert": 123}, "invalid_start_value"),
        ("spiel_starten", {"spieler": ["gibtsnicht"]}, "no_player"),
        ("weiter", {}, "no_game"),
        ("rueckgaengig", {}, "no_game"),
        ("wurf_aendern", {"dart": 0, "feld": "T20"}, "no_game"),
        ("spieler_anlegen", {"name": "  "}, "name_missing"),
        ("spieler_anlegen", {"name": "anna"}, "name_exists"),
        ("spieler_aendern", {"id": "x"}, "player_not_found"),
    ]
    for dienst, daten, schluessel in faelle:
        with pytest.raises(ServiceValidationError) as err:
            await _dienst(hass, dienst, **daten)
        assert err.value.translation_key == schluessel
    await _dienst(hass, "spiel_starten", spieler=[anna])
    for daten, schluessel in (({"dart": 0, "feld": "X9"}, "unknown_field"), ({"aufnahme": 5, "dart": 0, "feld": "T20"}, "unknown_visit")):
        with pytest.raises(ServiceValidationError) as err:
            await _dienst(hass, "wurf_aendern", **daten)
        assert err.value.translation_key == schluessel
    # wrong mode is stopped by the schema already
    with pytest.raises(vol.Invalid):
        await _dienst(hass, "spiel_starten", einwurf="triple")


async def test_ungueltiger_modus_aus_speicher(hass: HomeAssistant, geladen) -> None:
    leiter = geladen.runtime_data.spiel
    leiter.daten["letzte"]["einwurf"] = "falsch"
    with pytest.raises(ServiceValidationError) as err:
        await _dienst(hass, "spiel_starten", spieler=["bot:50"])
    assert err.value.translation_key == "invalid_mode"


async def test_spieler_verwalten(hass: HomeAssistant, geladen) -> None:
    anna, ben = await _spieler(hass, "Anna", "Ben")
    await _dienst(hass, "spieler_aendern", id=anna, name="Anna-Lena")
    namen = [s["name"] for s in hass.states.get(SPIELER).attributes["spieler"]]
    assert namen == ["Anna-Lena", "Ben"]
    leiter = geladen.runtime_data.spiel
    leiter.daten["statistik"] = {anna: {"punkte": 300, "darts": 9}, ben: {"punkte": 30, "darts": 3}}
    leiter.daten["verlauf"] = [{"gewinner": "Ben"}]
    await _dienst(hass, "statistik_loeschen", id=anna)
    assert list(leiter.daten["statistik"]) == [ben]
    await _dienst(hass, "statistik_loeschen", verlauf=True)
    assert leiter.daten["statistik"] == {} and leiter.daten["verlauf"] == []
    await _dienst(hass, "spieler_aendern", id=ben, loeschen=True)
    assert hass.states.get(SPIELER).state == "1"


async def test_spiel_bleibt_nach_neustart(hass: HomeAssistant, geladen, hass_storage) -> None:
    (anna,) = await _spieler(hass, "Anna")
    await _dienst(hass, "spiel_starten", spieler=[anna], startwert=170)
    await hass.config_entries.async_reload(geladen.entry_id)
    await hass.async_block_till_done()
    assert hass.states.get(SPIEL).state == "running"
    assert hass_storage["autodarts.spiel"]["data"]["spiel"]["einstellungen"]["startwert"] == 170


async def test_board_offline_ignoriert(hass: HomeAssistant, geladen) -> None:
    (anna,) = await _spieler(hass, "Anna")
    await _dienst(hass, "spiel_starten", spieler=[anna])
    geladen.runtime_data.zustand.async_set_updated_data(dict(OFFLINE))
    assert _attr(hass, "aufnahmen") == 0


async def test_dienst_ohne_integration(hass: HomeAssistant, geladen) -> None:
    await hass.config_entries.async_unload(geladen.entry_id)
    with pytest.raises(ServiceValidationError) as err:
        await _dienst(hass, "spiel_abbrechen")
    assert err.value.translation_key == "not_set_up"


def test_modus_text() -> None:
    e = {"startwert": 501, "einwurf": "master", "auswurf": "straight", "legs": 3, "sets": 0}
    assert modus_text(e) == "501 · Master In · Straight Out · Erster bis 3 Legs"
