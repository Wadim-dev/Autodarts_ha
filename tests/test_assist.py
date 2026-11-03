"""Assist sentences: score, ranking, start, tournament, undo, cancel (German, English, Russian)."""

from __future__ import annotations

from homeassistant.components import conversation
from homeassistant.core import Context, HomeAssistant
from homeassistant.setup import async_setup_component
import pytest

from custom_components.autodarts.assist import spiel_aus_text

from .conftest import board_mock
from .test_spiel import _dienst, _spieler


@pytest.fixture
async def mit_assist(hass, aioclient_mock, mock_entry):
    assert await async_setup_component(hass, "homeassistant", {})
    assert await async_setup_component(hass, "conversation", {})
    board_mock(aioclient_mock)
    mock_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(mock_entry.entry_id)
    await hass.async_block_till_done()
    yield mock_entry
    await hass.config_entries.async_unload(mock_entry.entry_id)
    await hass.async_block_till_done()


async def _sag(hass: HomeAssistant, text: str, sprache: str = "de") -> str:
    r = await conversation.async_converse(hass, text, None, Context(), language=sprache)
    return r.response.speech["plain"]["speech"]


def test_spielnamen() -> None:
    assert spiel_aus_text("501") == {"spiel": "x01", "startwert": 501}
    assert spiel_aus_text("Cricket") == {"spiel": "cricket"}
    assert spiel_aus_text("шанхай") == {"spiel": "shanghai"}
    assert spiel_aus_text("poker") is None


async def test_saetze(hass: HomeAssistant, mit_assist) -> None:
    assert await _sag(hass, "Wie steht es beim Darts") == "Gerade läuft kein Darts-Spiel."
    assert await _sag(hass, "who is winning at darts", "en") == "No darts game is running."
    assert await _sag(hass, "какой счёт в дартс", "ru") == "Сейчас игры в дартс нет."
    assert await _sag(hass, "starte darts spiel") == "Das geht gerade nicht."  # nobody chosen yet
    anna, ben = await _spieler(hass, "Anna", "Ben")
    await _dienst(hass, "spiel_starten", spieler=[anna, ben], startwert=301)
    await _dienst(hass, "spiel_abbrechen")
    antwort = await _sag(hass, "starte darts 501")
    assert antwort.startswith("Los geht's: 501")
    assert await _sag(hass, "wer ist dran beim darts") == "Anna 501 Rest, Ben 501 Rest. Anna ist dran."
    await _dienst(hass, "wurf_aendern", dart=0, feld="T20")
    assert await _sag(hass, "darts rückgängig") == "Letzter Dart ist zurückgenommen."
    assert await _sag(hass, "starte darts poker") == "Das Spiel poker kenne ich nicht."
    assert await _sag(hass, "darts spiel abbrechen") == "Spiel abgebrochen."
    assert await _sag(hass, "darts rangliste") == "Es gibt noch keine Spieler mit Wertung."
    assert await _sag(hass, "nächstes darts match") == "Das geht gerade nicht."
    cem = (await _spieler(hass, "Cem"))[0]
    await _dienst(hass, "turnier_starten", spieler=[anna, ben, cem], spiel="highscore", runden=1)
    assert "Ben" in await _sag(hass, "wer führt beim darts")
