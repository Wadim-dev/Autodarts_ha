"""Cricket, training and party games inside Home Assistant: start, board darts, bot, statistics, events."""

from __future__ import annotations

from unittest.mock import patch

from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ServiceValidationError
import pytest
import voluptuous as vol

from custom_components.autodarts.spiel import modus_text

from .test_ereignisse import _sammeln
from .test_spiel import SPIEL, SPIELER, _attr, _board, _dienst, _spieler


async def test_cricket_mit_board(hass: HomeAssistant, geladen) -> None:
    anna, ben = await _spieler(hass, "Anna", "Ben")
    await _dienst(hass, "spiel_starten", spieler=[anna, ben], spiel="cricket", variante="standard", zahlen="classic", legs=1)
    assert _attr(hass, "art") == "cricket"
    assert _attr(hass, "modus") == "Cricket · Standard"
    assert _attr(hass, "zahlen") == [20, 19, 18, 17, 16, 15, 25]
    _board(hass, geladen, [])
    _board(hass, geladen, ["T20", "T20", "S19"])
    a = _attr(hass, "spieler")[0]
    assert a["marks"][:2] == [3, 1]
    assert a["rest"] == 60
    assert _attr(hass, "ansage") == "7 Marks"
    _board(hass, geladen, [])
    assert _attr(hass, "am_zug") == 1
    # a later x01 game still works with the old settings merged in
    await _dienst(hass, "spiel_starten", spiel="x01", startwert=301)
    assert _attr(hass, "art") == "x01"
    assert _attr(hass, "spieler")[0]["rest"] == 301


async def test_ungueltige_spielart(hass: HomeAssistant, geladen) -> None:
    (anna,) = await _spieler(hass, "Anna")
    with pytest.raises(vol.Invalid):
        await _dienst(hass, "spiel_starten", spieler=[anna], spiel="poker")
    geladen.runtime_data.spiel.daten["letzte"]["spiel"] = "poker"
    with pytest.raises(ServiceValidationError):
        await _dienst(hass, "spiel_starten", spieler=[anna])


async def test_statistik_je_spielart(hass: HomeAssistant, geladen) -> None:
    (anna,) = await _spieler(hass, "Anna")
    await _dienst(hass, "spiel_starten", spieler=[anna], spiel="shanghai", runden=7)
    for f in ("S1", "D1", "T1"):
        await _dienst(hass, "wurf_aendern", dart=["S1", "D1", "T1"].index(f), feld=f)
    assert hass.states.get(SPIEL).state == "finished"
    ges = geladen.runtime_data.spiel.daten["statistik"][anna]["arten"]["shanghai"]
    assert ges["spiele"] == 1 and ges["siege"] == 1 and ges["darts"] == 3 and ges["best"] == 6
    assert "punkte" not in geladen.runtime_data.spiel.daten["statistik"][anna]
    assert hass.states.get(SPIELER).attributes["verlauf"][0]["modus"] == "Shanghai"
    # undo after the end takes the statistics back
    await _dienst(hass, "rueckgaengig")
    ges = geladen.runtime_data.spiel.daten["statistik"][anna]["arten"]["shanghai"]
    assert ges["spiele"] == 0 and ges["siege"] == 0 and ges["darts"] == 0


async def test_killer_ereignisse(hass: HomeAssistant, geladen) -> None:
    anna, ben = await _spieler(hass, "Anna", "Ben")
    liste = _sammeln(geladen)
    await _dienst(hass, "spiel_starten", spieler=[anna, ben], spiel="killer", leben=1)
    a, b = _attr(hass, "spieler")
    _board(hass, geladen, [])
    _board(hass, geladen, [f"D{a['nummer']}", f"D{b['nummer']}"])
    typen = [t for t, _ in liste]
    assert "killer" in typen and "eliminated" in typen and typen[-1] == "match_won"
    assert hass.states.get(SPIEL).state == "finished"


async def test_bot_cricket_und_golf(hass: HomeAssistant, geladen) -> None:
    with patch("custom_components.autodarts.spiel._pause"), patch(
        "custom_components.autodarts.x01.streuung", return_value=0.001
    ):
        await _dienst(hass, "spiel_starten", spieler=["bot:60"], spiel="cricket", zahlen="classic")
        await hass.async_block_till_done()
        assert hass.states.get(SPIEL).state == "finished"
        # 6 triples and the bull: 3 visits
        assert len(_attr(hass, "verlauf")) == 3
        await _dienst(hass, "spiel_starten", spieler=["bot:60"], spiel="golf", runden=9)
        await hass.async_block_till_done()
        assert hass.states.get(SPIEL).state == "finished"
        sp = _attr(hass, "spieler")[0]
        assert sp["rest"] == 9  # hole in one everywhere, the bot stops after the first dart
        assert sp["darts"] == 9


def test_modus_text_spielarten() -> None:
    assert modus_text({"spiel": "cricket", "variante": "cut_throat", "zahlen": "tactics", "legs": 3}) == "Cricket · Cut-Throat · Tactics · Erster bis 3 Legs"
    assert modus_text({"spiel": "golf", "legs": 1}) == "Golf"
