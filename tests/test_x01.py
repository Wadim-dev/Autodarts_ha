"""Tests for the X01 rules (no Home Assistant needed)."""

from __future__ import annotations

import random

import pytest

from custom_components.autodarts import x01


def _spiel(aufnahmen, start=501, ein="straight", aus="double", legs=1, sets=0, n=2):
    return {
        "einstellungen": {"startwert": start, "einwurf": ein, "auswurf": aus, "legs": legs, "sets": sets},
        "spieler": [{"name": f"P{i}"} for i in range(n)],
        "aufnahmen": [{"d": [{"f": f} for f in a], "zu": True} for a in aufnahmen],
    }


def test_felder() -> None:
    assert x01.feld_ok("T20") and x01.feld_ok("M") and not x01.feld_ok("T25")
    assert x01.wert("T20") == (60, 3)
    assert x01.wert("M") == (0, 0)
    assert x01.wert("") == (0, 0)
    assert x01.feld_aus(20, 3) == "T20"
    assert x01.feld_aus(25, 2) == "D25"
    assert x01.feld_aus(25, 1) == "S25"
    assert x01.feld_aus(0, 0) == "M"
    assert x01.feld_text("D25") == "Bull"
    assert x01.feld_text("T19") == "T19"


@pytest.mark.parametrize(
    ("rest", "darts", "aus", "erwartet"),
    [
        (40, 1, "double", ["D20"]),
        (170, 3, "double", ["T20", "T20", "D25"]),
        (171, 3, "double", None),
        (169, 3, "double", None),
        (60, 1, "straight", ["T20"]),
        (60, 1, "master", ["T20"]),
        (0, 3, "double", None),
        (100, 2, "double", ["T20", "D20"]),
    ],
)
def test_weg(rest, darts, aus, erwartet) -> None:
    assert x01.weg(rest, darts, aus) == erwartet
    # cached result is the same
    assert x01.weg(rest, darts, aus) == erwartet


def test_ein_dart_finish() -> None:
    assert x01.ein_dart_finish(50, "double")
    assert not x01.ein_dart_finish(41, "double")


def test_auswerten_leg_und_statistik() -> None:
    # P0: 180, 180, 141 (T20 T19 D12) = 9-darter
    sp = _spiel([["T20"] * 3, ["S1", "S1", "S1"], ["T20"] * 3, ["S1"] * 3, ["T20", "T19", "D12"]])
    st = x01.auswerten(sp)
    assert st["gewinner"] == 0
    assert st["ansage"] == "Spiel P0"
    p0 = st["spieler"][0]
    assert p0["rest"] == 0 and p0["legs"] == 1
    assert p0["n180"] == 2 and p0["n140"] == 1
    assert p0["bestes_leg"] == 9 and p0["finish"] == 141
    assert p0["avg"] == 167.0
    assert st["spieler"][1]["rest"] == 495


def test_auswerten_bust_und_offene_aufnahme() -> None:
    sp = _spiel([["T20", "T20", "T20"], ["M", "M", "M"]], start=101)
    sp["aufnahmen"].append({"d": [{"f": "T20"}], "zu": False})
    st = x01.auswerten(sp)
    # 101 - 180 -> bust, rest stays
    assert st["aufnahme"]["rest_vor"] == 101
    assert st["spieler"][0]["rest"] == 41
    assert st["verlauf"][0]["b"] is True
    assert st["ansage"] in ("0", "Bust")
    assert st["am_zug"] == 0
    assert st["aufnahme"]["summe"] == 60
    assert st["weg"] == x01.weg(41, 2, "double")


def test_auswerten_rest_eins_und_ohne_doppel() -> None:
    st = x01.auswerten(_spiel([["S20"]], start=21))
    assert st["spieler"][0]["rest"] == 21  # rest 1 is a bust with double out
    st = x01.auswerten(_spiel([["S20"]], start=20))
    assert st["spieler"][0]["rest"] == 20  # no double to finish


def test_auswerten_double_in_und_master() -> None:
    sp = _spiel([["S20", "D10", "S5"]], start=301, ein="double")
    st = x01.auswerten(sp)
    assert st["spieler"][0]["rest"] == 276
    sp = _spiel([["T20", "S5"]], start=301, ein="master")
    assert x01.auswerten(sp)["spieler"][0]["rest"] == 236
    sp = _spiel([["S20"]], start=301, ein="master")
    assert x01.auswerten(sp)["spieler"][0]["offen"] is False
    # master out allows a treble finish
    assert x01.auswerten(_spiel([["T20"]], start=60, aus="master"))["gewinner"] == 0
    assert x01.auswerten(_spiel([["S20"]], start=20, aus="straight"))["gewinner"] == 0


def test_auswerten_legs_und_sets() -> None:
    # first to 2 legs: P0 wins leg 1, P1 starts leg 2
    sp = _spiel([["D20"], ["D20"]], start=40, legs=2)
    st = x01.auswerten(sp)
    assert st["spieler"][0]["legs"] == 1 and st["leg"] == 3
    assert st["spieler"][1]["legs"] == 1
    sp["aufnahmen"].append({"d": [{"f": "D20"}], "zu": True})
    assert x01.auswerten(sp)["gewinner"] == 0
    # sets: first to 1 set of 1 leg
    st = x01.auswerten(_spiel([["D20"]], start=40, legs=1, sets=1))
    assert st["gewinner"] == 0 and st["spieler"][0]["sets"] == 1 and st["set"] == 1
    st = x01.auswerten(_spiel([["D20"]], start=40, legs=1, sets=2))
    assert st["gewinner"] is None and st["ansage"] == "Satz P0"


def test_leg_gewinner_bei_offener_aufnahme() -> None:
    sp = _spiel([], start=40, legs=2)
    sp["aufnahmen"] = [{"d": [{"f": "D20"}], "zu": False}]
    st = x01.auswerten(sp)
    assert st["leg_gewinner"] == 0 and st["gewinner"] is None
    assert st["ansage"] == "Leg P0"


def test_geometrie() -> None:
    assert x01.feld_an(0, 0) == "D25"
    assert x01.feld_an(0, 10) == "S25"
    assert x01.feld_an(0, 200) == "M"
    assert x01.feld_an(0, 103) == "T20"
    assert x01.feld_an(0, 166) == "D20"
    assert x01.feld_an(0, 50) == "S20"
    for f in ("T20", "D16", "S5"):
        x, y = x01.zielpunkt(f)
        assert x01.feld_an(x, y) == f
    assert x01.zielpunkt("D25") == (0.0, 0.0)


def test_streuung() -> None:
    gut = x01.streuung(90)
    schlecht = x01.streuung(30)
    assert 0 < gut < schlecht
    assert x01.streuung(500) == x01._TABELLE[0][0]
    assert x01.streuung(-1) == x01._TABELLE[-1][0]


def test_bot() -> None:
    assert x01.bot_ziel(501, 3, False, "double", "double") == "D20"
    assert x01.bot_ziel(501, 3, False, "master", "double") == "T20"
    assert x01.bot_ziel(40, 3, True, "straight", "double") == "D20"
    assert x01.bot_ziel(301, 3, True, "straight", "double") == "T20"
    assert x01.bot_ziel(160, 3, True, "straight", "double") == "T20"
    assert x01.bot_ziel(119, 1, True, "straight", "double") == "T20"
    assert x01.bot_ziel(3, 1, True, "straight", "double") == "S1"
    ziel = x01.bot_ziel(59, 1, True, "straight", "double")
    assert x01.feld_ok(ziel)
    wurf = x01.bot_wurf("T20", 0.001, random.Random(1))
    assert wurf["f"] == "T20" and wurf["q"] == "bot"


def test_bull_abstand() -> None:
    assert x01.bull_abstand({"x": 0.3, "y": 0.4}) == pytest.approx(0.5)
    assert x01.bull_abstand({"f": "D25"}) == 0.02
    assert x01.bull_abstand({"f": "T20"}) == 9.0
