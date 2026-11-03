"""Regeln der Spielarten neben X01 (ohne Home Assistant)."""

from __future__ import annotations

from typing import Any

from custom_components.autodarts import spielarten


def spiel(art: str, n: int = 2, aufnahmen: list[list[str]] | None = None, offen: list[str] | None = None, **e: Any) -> dict[str, Any]:
    auf = [{"d": [{"f": f} for f in a], "zu": True} for a in (aufnahmen or [])]
    if offen is not None:
        auf.append({"d": [{"f": f} for f in offen], "zu": False})
    return {"id": "test", "einstellungen": {"spiel": art, "legs": 1, **e},
            "spieler": [{"name": f"P{k}"} for k in range(n)], "aufnahmen": auf}


def test_x01_bleibt_x01() -> None:
    st = spielarten.auswerten({"id": "x", "einstellungen": {"startwert": 501, "einwurf": "straight", "auswurf": "double", "legs": 1},
                               "spieler": [{"name": "A"}], "aufnahmen": []})
    assert st["art"] == "x01"
    assert st["spieler"][0]["rest"] == 501


def test_cricket_marks_und_punkte() -> None:
    st = spielarten.auswerten(spiel("cricket", aufnahmen=[["T20", "T20", "S19"]]))
    a = st["spieler"][0]
    assert a["marks"][:2] == [3, 1]
    assert a["rest"] == 60
    assert st["verlauf"][0]["m"] == 7
    assert "zu:20" in st["verlauf"][0]["x"]
    assert "six_marks" in st["verlauf"][0]["x"]
    assert st["am_zug"] == 1
    assert st["zahlen"] == [20, 19, 18, 17, 16, 15, 25]


def test_cricket_geschlossen_bringt_keine_punkte() -> None:
    st = spielarten.auswerten(spiel("cricket", aufnahmen=[["T20", "M", "M"], ["T20", "M", "M"], ["T20", "M", "M"]]))
    assert st["spieler"][0]["rest"] == 0
    assert st["spieler"][1]["rest"] == 0


def test_cricket_sieg() -> None:
    alle = ["T20", "T19", "T18"], ["T17", "T16", "T15"], ["D25", "S25", "M"]
    auf: list[list[str]] = []
    for a in alle:
        auf += [a, ["M", "M", "M"]]
    st = spielarten.auswerten(spiel("cricket", aufnahmen=auf[:-1]))
    assert st["gewinner"] == 0
    assert st["ansage"] == "Spiel P0"
    assert st["verlauf"][0]["x"] == ["zu:20", "zu:19", "zu:18", "nine_marks"]


def test_cut_throat_punkte_an_gegner() -> None:
    st = spielarten.auswerten(spiel("cricket", aufnahmen=[["T20", "T20", "M"]], variante="cut_throat"))
    assert st["spieler"][0]["rest"] == 0
    assert st["spieler"][1]["rest"] == 60


def test_tactics_und_zufall() -> None:
    assert spielarten.auswerten(spiel("cricket", zahlen="tactics"))["zahlen"][0:2] == [20, 19]
    assert len(spielarten.auswerten(spiel("cricket", zahlen="tactics"))["zahlen"]) == 12
    z = spielarten.auswerten(spiel("cricket", zahlen="random"))["zahlen"]
    assert len(z) == 7 and z[-1] == 25
    assert z == spielarten.auswerten(spiel("cricket", zahlen="random"))["zahlen"]


def test_cricket_bot_ziel() -> None:
    st = spielarten.auswerten(spiel("cricket", n=1, offen=[]))
    assert st["bot_ziel"] == "T20"


def test_rund_um_die_uhr() -> None:
    st = spielarten.auswerten(spiel("atc", n=1, aufnahmen=[["S1", "T2", "S5"]]))
    assert st["spieler"][0]["rest"] == 3
    assert st["ziel"] == "S3"
    st = spielarten.auswerten(spiel("atc", n=1, aufnahmen=[["S1", "D2", "D3"]], variante="double"))
    assert st["spieler"][0]["rest"] == 1
    assert st["ziel"] == "D1"


def test_rund_um_die_uhr_ende() -> None:
    darts = [f"S{n}" for n in range(1, 21)] + ["S25"]
    auf = [darts[i:i + 3] for i in range(0, 21, 3)]
    st = spielarten.auswerten(spiel("atc", n=1, aufnahmen=auf))
    assert st["gewinner"] == 0
    assert "geschafft" in st["verlauf"][-1]["x"]


def test_bobs27() -> None:
    st = spielarten.auswerten(spiel("bobs27", n=1, aufnahmen=[["D1", "D1", "M"], ["M", "M", "M"]]))
    assert st["spieler"][0]["rest"] == 27 + 4 - 4
    assert st["ziel"] == "D3"
    st = spielarten.auswerten(spiel("bobs27", n=1, aufnahmen=[["M", "M", "M"]] * 5))
    assert st["spieler"][0]["raus"]
    assert st["gewinner"] == 0
    assert "raus" in st["verlauf"][-1]["x"]


def test_doppel_training() -> None:
    st = spielarten.auswerten(spiel("doppel", n=1, aufnahmen=[["D1", "S1", "D1"]]))
    assert st["spieler"][0]["rest"] == 2
    assert st["ziel"] == "D2"


def test_checkout121() -> None:
    st = spielarten.auswerten(spiel("checkout121", n=1, aufnahmen=[["T20", "T20", "S1"]], runden=2))
    assert st["spieler"][0]["rest"] == 121 and st["spieler"][0]["versuch"] == 2
    assert st["weg"] and st["weg"][-1].startswith("D")
    st = spielarten.auswerten(spiel("checkout121", n=1, aufnahmen=[["T20", "T19", "D2"]], runden=2))
    a = st["spieler"][0]
    assert a["zielwert"] == 122 and a["rest"] == 122 and a["geschafft"] == 1
    assert "check" in st["verlauf"][0]["x"]
    st = spielarten.auswerten(spiel("checkout121", n=1, aufnahmen=[["T20", "T20", "T20"]], runden=2))
    assert st["spieler"][0]["rest"] == 121
    assert "bust" in st["verlauf"][0]["x"]
    st = spielarten.auswerten(spiel("checkout121", n=1, aufnahmen=[["M", "M", "M"]] * 3, runden=1))
    assert st["gewinner"] == 0
    assert "verfehlt" in st["verlauf"][-1]["x"]


def test_highscore() -> None:
    st = spielarten.auswerten(spiel("highscore", n=2, aufnahmen=[["T20", "T20", "T20"], ["S1", "S1", "S1"]], runden=1))
    assert st["gewinner"] == 0
    assert st["spieler"][0]["rest"] == 180


def test_shanghai() -> None:
    st = spielarten.auswerten(spiel("shanghai", n=2, aufnahmen=[["S1", "D1", "S2"], ["M", "M", "M"]]))
    assert st["spieler"][0]["rest"] == 3
    assert st["ziel"] == "2"
    st = spielarten.auswerten(spiel("shanghai", n=2, offen=["S1", "D1", "T1"]))
    assert st["gewinner"] == 0
    assert "shanghai" in st["verlauf"][0]["x"]


def test_halve_it() -> None:
    st = spielarten.auswerten(spiel("halve_it", n=1, aufnahmen=[["S15", "T15", "M"], ["M", "M", "M"]]))
    assert st["spieler"][0]["rest"] == (40 + 60) // 2
    assert "halbiert" in st["verlauf"][1]["x"]
    assert st["ziel"] == "D"


def test_killer() -> None:
    s = spiel("killer", n=2, leben=1)
    st = spielarten.auswerten(s)
    a, b = st["spieler"]
    assert st["ziel"] == f"D{a['nummer']}"
    s["aufnahmen"] = [{"d": [{"f": f"D{a['nummer']}"}, {"f": f"D{b['nummer']}"}], "zu": False}]
    st = spielarten.auswerten(s)
    assert st["gewinner"] == 0
    assert "killer" in st["verlauf"][0]["x"]
    assert "raus:1" in st["verlauf"][0]["x"]


def test_golf() -> None:
    st = spielarten.auswerten(spiel("golf", n=1, aufnahmen=[["T1"], ["S2", "D2"]]))
    assert st["spieler"][0]["rest"] == 1 + 2
    assert "hole_in_one" in st["verlauf"][0]["x"]
    assert st["spieler"][0]["darts"] == 3


def test_baseball() -> None:
    st = spielarten.auswerten(spiel("baseball", n=1, aufnahmen=[["T1", "T1", "S1"]]))
    assert st["spieler"][0]["rest"] == 7
    assert "home_run" in st["verlauf"][0]["x"]


def test_legs_in_spielarten() -> None:
    s = spiel("shanghai", n=2, legs=2)
    s["aufnahmen"] = [{"d": [{"f": "S1"}, {"f": "D1"}, {"f": "T1"}], "zu": True}]
    st = spielarten.auswerten(s)
    assert st["gewinner"] is None
    assert st["spieler"][0]["legs"] == 1
    assert st["leg"] == 2
    assert st["am_zug"] == 1
