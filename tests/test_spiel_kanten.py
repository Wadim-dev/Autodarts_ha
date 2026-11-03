"""Edge cases of the local game: board corrections, bot timing, errors while talking to the board."""

from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock, patch

from aioautodarts import AutodartsConnectionError
from homeassistant.core import HomeAssistant

from custom_components.autodarts import x01

from .test_spiel import SPIEL, _attr, _board, _dienst, _spieler


async def _ewig(sekunden: float) -> None:
    """The bot's first wait never ends; all other waits are skipped."""
    if sekunden == 2.0:
        await asyncio.sleep(3600)


async def test_ohne_spiel(hass: HomeAssistant, geladen) -> None:
    spiel = geladen.runtime_data.spiel
    assert spiel._dart_annehmen({"f": "T20"}, vom_board=True) is False
    assert spiel._aufnahme_schliessen() is False
    with patch("custom_components.autodarts.spiel._pause"):
        await spiel._bot_werfen()  # nothing to do without a game


async def test_vier_darts_auf_einmal(hass: HomeAssistant, geladen) -> None:
    (anna,) = await _spieler(hass, "Anna")
    await _dienst(hass, "spiel_starten", spieler=[anna], startwert=501)
    _board(hass, geladen, [])
    # the board reports four darts at once: only three count
    _board(hass, geladen, ["T20", "T20", "T20", "S1"])
    await hass.async_block_till_done()
    assert _attr(hass, "spieler")[0]["rest"] == 321
    # a further dart on a full visit is ignored as well
    _board(hass, geladen, ["T20", "T20", "T20", "S1", "S5"])
    assert _attr(hass, "spieler")[0]["rest"] == 321


async def test_aufnahme_schliessen_varianten(hass: HomeAssistant, geladen) -> None:
    (anna,) = await _spieler(hass, "Anna")
    await _dienst(hass, "spiel_starten", spieler=[anna], startwert=501)
    spiel = geladen.runtime_data.spiel
    # darts pulled before any visit: nothing to close
    assert spiel._aufnahme_schliessen(nur_wenn_darts=True) is False
    # open visit without darts is not closed by pulling darts
    spiel._offene_aufnahme()
    assert spiel._aufnahme_schliessen(nur_wenn_darts=True) is False
    # "next" without an open visit records an empty visit, undo removes it again
    spiel._laufend["aufnahmen"].clear()
    await _dienst(hass, "weiter")
    assert len(spiel._laufend["aufnahmen"]) == 1
    await _dienst(hass, "rueckgaengig")
    assert spiel._laufend["aufnahmen"] == []
    # a player without statistics yet is skipped when statistics are taken back
    spiel._statistik_abziehen()


async def test_bot_wird_abgebrochen(hass: HomeAssistant, geladen) -> None:
    with patch("custom_components.autodarts.spiel._pause", side_effect=_ewig), patch(
        "custom_components.autodarts.x01.streuung", return_value=0.001
    ):
        await _dienst(hass, "spiel_starten", spieler=["bot:60"], startwert=501)
        spiel = geladen.runtime_data.spiel
        aufgabe = spiel._bot_aufgabe
        assert aufgabe is not None and not aufgabe.done()
        # a second check while the bot is waiting does not start another one
        spiel._bot_pruefen()
        assert spiel._bot_aufgabe is aufgabe
        # board darts are ignored while the bot is on
        _board(hass, geladen, ["T20"])
        assert spiel._laufend["aufnahmen"] == []
        await _dienst(hass, "spiel_abbrechen")
        await asyncio.sleep(0)
        assert aufgabe.cancelled()


async def test_bot_ganze_aufnahme(hass: HomeAssistant, geladen) -> None:
    (anna,) = await _spieler(hass, "Anna")
    with patch("custom_components.autodarts.spiel._pause"), patch(
        "custom_components.autodarts.x01.streuung", return_value=0.001
    ):
        await _dienst(hass, "spiel_starten", spieler=["bot:60", anna], startwert=501)
        for _ in range(20):
            await asyncio.sleep(0)
        await hass.async_block_till_done()
    # the bot threw T20 T20 T20 and closed its visit, Anna is on
    assert _attr(hass, "spieler")[0]["rest"] == 321
    assert _attr(hass, "am_zug") == 1


async def test_board_fehler_beim_start_und_weiter(hass: HomeAssistant, geladen) -> None:
    (anna,) = await _spieler(hass, "Anna")
    spiel = geladen.runtime_data.spiel
    _board(hass, geladen, ["T20"], laeuft=False)
    fehler = AsyncMock(side_effect=AutodartsConnectionError("weg"))
    with patch.object(spiel.board, "start", fehler), patch.object(spiel.board, "reset", fehler):
        # detection stopped and the board does not take the start: the game starts anyway
        await _dienst(hass, "spiel_starten", spieler=[anna], startwert=501)
        assert hass.states.get(SPIEL).state == "running"
        _board(hass, geladen, ["T20", "S20"])
        # reset fails: the visit is still closed
        await _dienst(hass, "weiter")
    assert spiel._laufend["aufnahmen"][-1]["zu"] is True


async def test_darts_nach_checkout_zaehlen_nicht(hass: HomeAssistant, geladen) -> None:
    (anna,) = await _spieler(hass, "Anna")
    await _dienst(hass, "spiel_starten", spieler=[anna], startwert=101)
    for feld in ("T17", "S1", "S1"):
        await _dienst(hass, "wurf_aendern", dart=9, feld=feld)
    assert _attr(hass, "spieler")[0]["rest"] == 48
    await _dienst(hass, "wurf_aendern", aufnahme=0, dart=1, feld="D25")
    assert hass.states.get(SPIEL).state == "finished"


def test_bot_ziel_ohne_weg() -> None:
    assert x01.bot_ziel(1, 1, True, "straight", "double") == "S1"
    assert x01.bot_ziel(99, 1, True, "straight", "double") == "T20"
