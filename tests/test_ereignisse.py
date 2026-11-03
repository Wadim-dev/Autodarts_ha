"""Game events for automations: darts, 180, bust, checkout, leg and match."""

from __future__ import annotations

from homeassistant.core import HomeAssistant

from .test_spiel import _board, _dienst, _spieler

EREIGNIS = "event.autodarts_board_game_event"


def _sammeln(geladen) -> list[tuple[str, dict]]:
    liste: list[tuple[str, dict]] = []
    geladen.runtime_data.spiel.ereignis_hoerer(lambda typ, daten: liste.append((typ, daten)))
    return liste


async def test_180_und_checkout(hass: HomeAssistant, geladen) -> None:
    anna, ben = await _spieler(hass, "Anna", "Ben")
    liste = _sammeln(geladen)
    await _dienst(hass, "spiel_starten", spieler=[anna, ben], startwert=301, auswurf="double")
    assert liste == []
    _board(hass, geladen, [])
    _board(hass, geladen, ["T20"])
    _board(hass, geladen, ["T20", "T20", "T20"])
    typen = [t for t, _ in liste]
    assert typen == ["dart", "triple", "dart", "triple", "dart", "triple", "visit", "one_eighty", "three_in_a_bed"]
    assert liste[-1][1] == {"player": "Anna", "score": 180, "darts": ["T20", "T20", "T20"], "remaining": 121}
    state = hass.states.get(EREIGNIS)
    assert state.attributes["event_type"] == "three_in_a_bed"
    # darts pulled, Ben: bull and bullseye, nothing special about the visit
    _board(hass, geladen, [])
    liste.clear()
    _board(hass, geladen, ["S25", "D25", "M"])
    assert [t for t, _ in liste] == ["dart", "bull", "dart", "bullseye", "dart", "visit"]
    _board(hass, geladen, [])
    # Anna checks out 121: T20 T11 D14 -> high finish, leg and match
    liste.clear()
    _board(hass, geladen, ["T20", "T11", "D14"])
    typen = [t for t, _ in liste]
    assert typen[-5:] == ["visit", "ton", "checkout", "high_finish", "match_won"]
    # undo does not fire again
    liste.clear()
    await _dienst(hass, "rueckgaengig")
    assert liste == []


async def test_bust_no_score_leg(hass: HomeAssistant, geladen) -> None:
    (anna,) = await _spieler(hass, "Anna")
    liste = _sammeln(geladen)
    await _dienst(hass, "spiel_starten", spieler=[anna], startwert=101, legs=2)
    _board(hass, geladen, [])
    _board(hass, geladen, ["M", "M", "M"])
    assert [t for t, _ in liste][-2:] == ["visit", "no_score"]
    _board(hass, geladen, [])
    _board(hass, geladen, ["T20", "T20"])
    assert [t for t, _ in liste][-2:] == ["visit", "bust"]
    _board(hass, geladen, [])
    liste.clear()
    _board(hass, geladen, ["T17", "D25"])
    assert [t for t, _ in liste][-5:] == ["visit", "ton", "checkout", "high_finish", "leg_won"]
    await _dienst(hass, "spiel_abbrechen")
    assert geladen.runtime_data.spiel._ev_spiel is None
