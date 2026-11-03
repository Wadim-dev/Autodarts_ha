"""Player profiles: field counts, trend, Elo, streak, head to head, badges (also undo)."""

from __future__ import annotations

from datetime import date

from homeassistant.core import HomeAssistant

from custom_components.autodarts import auswertung

from .test_spiel import SPIELER, _dienst, _spieler


def test_serie() -> None:
    h = date(2026, 11, 3)
    assert auswertung.serie([], h) == (0, 0)
    assert auswertung.serie(["2026-11-01", "2026-11-02", "2026-11-03", "2026-10-20"], h) == (3, 3)
    assert auswertung.serie(["2026-11-01", "2026-11-02"], h) == (2, 2)
    assert auswertung.serie(["2026-10-01", "2026-10-02", "2026-10-03", "2026-10-04"], h) == (0, 4)


def test_abzeichen() -> None:
    liste = auswertung.abzeichen({"n180": 12, "bestes_leg": 14, "spiele": 3, "arten": {"cricket": {"spiele": 2, "siege": 1}}}, {"x": {"shanghai": 1}}, 8)
    d = {a["key"]: a for a in liste}
    assert d["n180"]["stufe"] == 2 and d["n180"]["ziel"] == 50
    assert d["kurzes_leg"]["stufe"] == 2
    assert d["serie"]["stufe"] == 2
    assert d["shanghai"]["stufe"] == 1
    assert d["allrounder"]["wert"] == 2
    assert d["darts"]["stufe"] == 0


async def test_profil_und_ruecknahme(hass: HomeAssistant, geladen) -> None:
    anna, ben = await _spieler(hass, "Anna", "Ben")
    await _dienst(hass, "spiel_starten", spieler=[anna, ben], startwert=101, auswurf="straight", spiel="x01")
    for f in ("T20", "T7", "S20"):
        await _dienst(hass, "wurf_aendern", dart=["T20", "T7", "S20"].index(f), feld=f)
    assert hass.states.get("sensor.autodarts_board_game").state == "finished"
    sp = {p["name"]: p for p in hass.states.get(SPIELER).attributes["spieler"]}
    assert sp["Anna"]["felder"] == {"T20": 1, "T7": 1, "S20": 1}
    assert sp["Anna"]["elo"] == 1016 and sp["Ben"]["elo"] == 984
    assert sp["Anna"]["gegen"] == {ben: [1, 0]} and sp["Ben"]["gegen"] == {anna: [0, 1]}
    assert sp["Anna"]["serie"] == 1
    assert sp["Anna"]["trend"][0][0] == "x01" and sp["Anna"]["trend"][0][2] is True
    assert any(a["key"] == "siege" and a["stufe"] == 1 for a in sp["Anna"]["abzeichen"])
    await _dienst(hass, "rueckgaengig")
    sp = {p["name"]: p for p in hass.states.get(SPIELER).attributes["spieler"]}
    assert sp["Anna"]["felder"] == {}
    assert sp["Anna"]["elo"] == 1000 and sp["Ben"]["elo"] == 1000
    assert sp["Anna"]["gegen"][ben] == [0, 0]
    assert sp["Anna"]["trend"] == []
    await _dienst(hass, "wurf_aendern", dart=2, feld="S20")
    await _dienst(hass, "statistik_loeschen")
    sp = {p["name"]: p for p in hass.states.get(SPIELER).attributes["spieler"]}
    assert sp["Anna"]["felder"] == {} and sp["Anna"]["elo"] == 1000


async def test_elo_gegen_bot(hass: HomeAssistant, geladen) -> None:
    (anna,) = await _spieler(hass, "Anna")
    await _dienst(hass, "spiel_starten", spieler=[anna, "bot:60"], spiel="shanghai", runden=7)
    for i, f in enumerate(("S1", "D1", "T1")):
        await _dienst(hass, "wurf_aendern", dart=i, feld=f)
    sp = hass.states.get(SPIELER).attributes["spieler"][0]
    assert sp["elo"] == 1016
    assert sp["felder"]["T1"] == 1
