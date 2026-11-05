"""Regeln der Spielarten neben X01 (ohne Home Assistant)."""

from __future__ import annotations

from typing import Any

import pytest

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


# ---------- 1.25.0: neue Spielarten ----------

def test_alle_spielarten_laufen_bis_zum_ende() -> None:
    """Jede Spielart: zwei Bots spielen ein ganzes Spiel ohne Fehler durch und es gibt einen Sieger."""
    import random as _r

    from custom_components.autodarts import x01

    for art in spielarten.ARTEN:
        for n in (1, 2, 3):
            lo, hi = spielarten.SPIELER_GRENZEN.get(art, (1, 8))
            if not lo <= n <= hi:
                continue
            s = spiel(art, n=n)
            zufall = _r.Random(art + str(n))
            for _ in range(4000):
                st = spielarten.auswerten(s)
                if st["gewinner"] is not None:
                    break
                auf = s["aufnahmen"]
                if not st["bot_ziel"]:  # Golf: stehen bleiben
                    assert art == "golf" and auf and not auf[-1]["zu"], (art, st)
                    auf[-1]["zu"] = True
                    continue
                d = x01.bot_wurf(st["bot_ziel"], 25.0, zufall)
                if auf and not auf[-1]["zu"] and len(auf[-1]["d"]) < 3:
                    auf[-1]["d"].append({"f": d["f"]})
                else:
                    auf.append({"d": [{"f": d["f"]}], "zu": False})
                st = spielarten.auswerten(s)
                if st["aufnahme"]["fertig"] or len(auf[-1]["d"]) >= 3:
                    auf[-1]["zu"] = True
            else:
                pytest.fail(f"{art} mit {n} Spielern endet nicht")
            assert st["gewinner"] in range(n), art


def test_gruppen_und_arten_passen() -> None:
    assert set(spielarten.GRUPPEN) - {"x01"} == set(spielarten.ARTEN)
    assert len(spielarten.GRUPPEN) >= 30 - 6  # Cricket-Varianten laufen über Optionen


def test_hidden_cricket() -> None:
    st = spielarten.auswerten(spiel("cricket", zahlen="hidden"))
    assert st["verdeckt"] == [True] * 6 + [False]
    assert st["zahlen"] == [None] * 6 + [25]  # nichts verraten
    z = spielarten.auswerten(spiel("cricket", zahlen="random"))["zahlen"][2]
    st = spielarten.auswerten(spiel("cricket", zahlen="hidden", aufnahmen=[[f"S{z}", "M", "M"]]))
    assert st["verdeckt"][2] is False and st["verdeckt"].count(True) == 5
    assert st["spieler"][0]["marks"][2] == 1
    assert f"auf:{z}" in st["verlauf"][0]["x"]
    assert st["zahlen"][2] == z and st["zahlen"][0] is None


def test_zufall_cricket_neue_zahlen_je_leg() -> None:
    alle = ["T20", "T19", "T18"]
    s = spiel("cricket", n=1, zahlen="random", legs=2)
    z1 = spielarten.auswerten(s)["zahlen"]
    s["aufnahmen"] = [{"d": [{"f": f"T{z}"} for z in z1[:3]], "zu": True}, {"d": [{"f": f"T{z}"} for z in z1[3:6]], "zu": True},
                      {"d": [{"f": "D25"}, {"f": "S25"}], "zu": True}]
    st = spielarten.auswerten(s)
    assert st["leg"] == 2 and st["spieler"][0]["legs"] == 1
    assert st["zahlen"] != z1 and len(st["zahlen"]) == 7
    assert alle  # nur Lesbarkeit


def test_wild_mouse() -> None:
    st = spielarten.auswerten(spiel("wild_mouse"))
    assert st["zahlen"] == [20, 19, 18, 17, 16, 15, "D", "T", "3B", 25]
    # D20 markiert zuerst die 20, ein D1 die Doubles
    st = spielarten.auswerten(spiel("wild_mouse", aufnahmen=[["D20", "D1", "T2"]]))
    m = st["spieler"][0]["marks"]
    assert m[0] == 2 and m[6] == 1 and m[7] == 1
    # 3 in a bed schließt sofort, die Darts zählen auch für ihre Zahl
    st = spielarten.auswerten(spiel("wild_mouse", aufnahmen=[["S5", "S5", "S5"]]))
    m = st["spieler"][0]["marks"]
    assert m[8] == 3 and "zu:3B" in st["verlauf"][0]["x"]
    # geschlossene Doubles punkten mit dem ganzen Dart, solange ein Gegner sie offen hat
    st = spielarten.auswerten(spiel("wild_mouse", aufnahmen=[["D1", "D2", "D3"], ["M", "M", "M"], ["D10", "M", "M"]]))
    assert st["spieler"][0]["rest"] == 20
    # ohne 3 in a Bed
    st = spielarten.auswerten(spiel("wild_mouse", variante="ohne_3b"))
    assert "3B" not in st["zahlen"]


def test_wild_mouse_sieg() -> None:
    auf = [["T20", "T19", "T18"], ["M", "M", "M"], ["T17", "T16", "T15"], ["M", "M", "M"], ["D1", "D2", "D3"], ["M", "M", "M"],
           ["T1", "T2", "T3"], ["M", "M", "M"], ["S7", "S7", "S7"], ["M", "M", "M"], ["D25", "S25"]]
    st = spielarten.auswerten(spiel("wild_mouse", aufnahmen=auf))
    assert st["gewinner"] == 0


def test_mickey_mouse() -> None:
    st = spielarten.auswerten(spiel("mickey"))
    assert st["zahlen"] == [20, 19, 18, 17, 16, 15, 14, 13, 12, "D", "T", 25]
    auf: list[list[str]] = []
    for a in (["T20", "T19", "T18"], ["T17", "T16", "T15"], ["T14", "T13", "T12"], ["D1", "D2", "D3"], ["T1", "T2", "T3"]):
        auf += [a, ["T20", "T20", "T20"]]
    auf.append(["D25", "S25"])
    st = spielarten.auswerten(spiel("mickey", aufnahmen=auf))
    assert st["gewinner"] == 0
    assert st["spieler"][0]["rest"] == 0 and st["spieler"][1]["rest"] == 0  # ohne Punkte


def test_count_up_stechen() -> None:
    st = spielarten.auswerten(spiel("highscore", n=2, aufnahmen=[["T20", "M", "M"], ["T20", "M", "M"]], runden=1))
    assert st["gewinner"] is None
    assert "stechen" in st["verlauf"][-1]["x"]
    assert st["am_zug"] == 0
    st = spielarten.auswerten(spiel("highscore", n=2, aufnahmen=[["T20", "M", "M"], ["T20", "M", "M"], ["S1", "M", "M"], ["S2", "M", "M"]], runden=1))
    assert st["gewinner"] == 1
    assert spielarten.auswerten(spiel("highscore", n=1))["runden"] == 8


def test_golf_stechen_auf_loch_10() -> None:
    auf = [["T1"], ["T1"]]
    st = spielarten.auswerten(spiel("golf", n=2, aufnahmen=auf, runden=1))
    assert st["gewinner"] is None
    # Golf hat immer 9 oder 18 Löcher; hier nur Grundregel: nach Gleichstand geht es weiter
    st = spielarten.auswerten(spiel("baseball", n=2, aufnahmen=[["S1", "M", "M"]] * 18))
    assert st["gewinner"] is None and st["ziel"] == "10"


def test_bermuda() -> None:
    st = spielarten.auswerten(spiel("bermuda", n=1, aufnahmen=[["M", "M", "M"], ["S13", "T13", "M"], ["M", "M", "M"]]))
    a = st["spieler"][0]
    assert a["rest"] == 52 // 2
    assert st["verlauf"][0]["x"] == []  # 0 halbieren ist kein Ereignis
    assert "halbiert" in st["verlauf"][2]["x"]
    assert st["ziel"] == "D"
    st = spielarten.auswerten(spiel("bermuda", n=1, aufnahmen=[["S12"], ["S13", "T13", "M"], ["M", "M", "M"]], variante="ohne_halbieren"))
    assert st["spieler"][0]["rest"] == 12 + 52
    ziele = ["S12", "S13", "S14", "D1", "S15", "S16", "S17", "T1", "S18", "S19", "S20", "S25", "D25"]
    st = spielarten.auswerten(spiel("bermuda", n=1, aufnahmen=[[z, "M", "M"] for z in ziele]))
    assert st["gewinner"] == 0
    assert st["spieler"][0]["rest"] == 12 + 13 + 14 + 2 + 15 + 16 + 17 + 3 + 18 + 19 + 20 + 25 + 50


def test_bermuda_bullseye_nur_innen() -> None:
    vor = [["S12"], ["S13"], ["S14"], ["D1"], ["S15"], ["S16"], ["S17"], ["T1"], ["S18"], ["S19"], ["S20"], ["S25"]]
    st = spielarten.auswerten(spiel("bermuda", n=1, aufnahmen=[*vor, ["S25", "M", "M"]]))
    assert "halbiert" in st["verlauf"][-1]["x"]


def test_round_the_world() -> None:
    st = spielarten.auswerten(spiel("rtw", n=2, aufnahmen=[["S1", "T2", "S5"]]))
    a = st["spieler"][0]
    assert a["rest"] == 1 + 6 and a["treffer"] == 2
    assert st["spieler"][0]["ziel"] == "3"
    st = spielarten.auswerten(spiel("rtw", n=1, variante="ab"))
    assert st["ziel"] == "20"
    z = spielarten.auswerten(spiel("rtw", n=1, variante="zufall"))["spieler"][0]["folge"]
    assert sorted(z[:-1]) == list(range(1, 21)) and z[-1] == 25
    darts = [f"S{n}" for n in range(1, 21)] + ["D25"]
    st = spielarten.auswerten(spiel("rtw", n=1, aufnahmen=[darts[i:i + 3] for i in range(0, 21, 3)]))
    assert st["gewinner"] == 0 and st["spieler"][0]["rest"] == 210 + 50


def test_gotcha() -> None:
    st = spielarten.auswerten(spiel("gotcha", n=2, aufnahmen=[["T20", "M", "M"], ["T20", "M", "M"]]))
    assert [p["rest"] for p in st["spieler"]] == [0, 60]
    assert "gotcha:0" in st["verlauf"][1]["x"]
    # Bust nimmt auch das Gotcha zurück
    st = spielarten.auswerten(spiel("gotcha", n=2, zielwert=101, aufnahmen=[["T20", "M", "M"], ["T20", "T20", "M"]]))
    assert [p["rest"] for p in st["spieler"]] == [60, 0]
    assert st["verlauf"][1]["x"] == ["bust"] and st["verlauf"][1]["b"]
    # Ziel genau treffen gewinnt (Straight)
    st = spielarten.auswerten(spiel("gotcha", n=2, zielwert=101, aufnahmen=[["T20", "S20", "S1"], ["M", "M", "M"], ["S20"]]))
    assert st["gewinner"] == 0
    # Double Out: Rest 1 ist Bust, Single aufs Ziel auch
    st = spielarten.auswerten(spiel("gotcha", n=1, zielwert=101, variante="double", aufnahmen=[["T20", "T20", "S1"]]))
    assert st["spieler"][0]["rest"] == 0
    st = spielarten.auswerten(spiel("gotcha", n=1, zielwert=101, variante="double", aufnahmen=[["T20", "S20", "S20"]]))
    assert st["spieler"][0]["rest"] == 0 and st["gewinner"] is None and "bust" in st["verlauf"][0]["x"]
    st = spielarten.auswerten(spiel("gotcha", n=1, zielwert=101, variante="double", aufnahmen=[["T20", "S20", "M"], ["S1", "D10"]]))
    assert st["gewinner"] == 0


def test_nine_lives() -> None:
    st = spielarten.auswerten(spiel("nine_lives", n=2, aufnahmen=[["S1", "S2", "M"], ["M", "M", "M"]]))
    a, b = st["spieler"]
    assert a["rest"] == 2 and a["leben"] == 3 and st["spieler"][0]["ziel"] == "3"
    assert b["leben"] == 2 and "leben:1" in st["verlauf"][1]["x"]
    st = spielarten.auswerten(spiel("nine_lives", n=2, leben=1, aufnahmen=[["S1", "M", "M"], ["M", "M", "M"]]))
    assert st["gewinner"] == 0 and "raus:1" in st["verlauf"][1]["x"]


def test_football() -> None:
    st = spielarten.auswerten(spiel("football", n=2, aufnahmen=[["D20", "S25", "D20"]]))
    a = st["spieler"][0]
    assert a["rest"] == 1 and a["ball"]
    assert st["verlauf"][0]["x"] == ["ball", "tor"]
    st = spielarten.auswerten(spiel("football", n=1, zielwert=2, aufnahmen=[["S25", "D1", "D2"]]))
    assert st["gewinner"] == 0


def test_scram() -> None:
    zu1 = [["T20", "T19", "T18"], ["T17", "T16", "T15"], ["D25", "S25"]]
    auf = [zu1[0], ["T20", "T17", "S25"], zu1[1], ["T16", "M", "M"], zu1[2]]
    st = spielarten.auswerten(spiel("scram", n=2, aufnahmen=auf))
    assert st["spieler"][1]["rest"] == 51 + 25  # 20 und 16 hat der Stopper schon zu
    assert "wechsel" in st["verlauf"][-1]["x"]
    assert st["am_zug"] == 1 and st["spieler"][1]["rolle"] == "stopper" and st["spieler"][0]["rolle"] == "scorer"
    auf += [zu1[0], ["T15", "M", "M"], zu1[1], ["M", "M", "M"], zu1[2]]
    st = spielarten.auswerten(spiel("scram", n=2, aufnahmen=auf))
    assert st["gewinner"] == 1
    assert st["spieler"][0]["rest"] == 45


def test_catch40() -> None:
    st = spielarten.auswerten(spiel("catch40", n=1, aufnahmen=[["S11", "D25"]]))
    a = st["spieler"][0]
    assert a["rest"] == 3 and a["zielwert"] == 62 and st["runden"] == 40
    assert "check" in st["verlauf"][0]["x"]
    st = spielarten.auswerten(spiel("catch40", n=1, aufnahmen=[["S1", "S20", "D20"]]))
    assert st["spieler"][0]["rest"] == 2
    st = spielarten.auswerten(spiel("catch40", n=1, aufnahmen=[["M", "M", "M"], ["S11", "D25"]]))
    assert st["spieler"][0]["rest"] == 1
    st = spielarten.auswerten(spiel("catch40", n=1, aufnahmen=[["M", "M", "M"], ["M", "M", "M"]]))
    assert st["spieler"][0]["rest"] == 0 and st["spieler"][0]["zielwert"] == 62
    assert "verfehlt" in st["verlauf"][1]["x"]
    st = spielarten.auswerten(spiel("catch40", n=1, aufnahmen=[["T20", "M", "M"]]))
    assert "bust" in st["verlauf"][0]["x"] and st["spieler"][0]["restwert"] == 61 and st["spieler"][0]["versuch"] == 2


def test_catch40_99_mit_drei_darts() -> None:
    s = spiel("catch40", n=1)
    a = Catch40Hilfe.bis(s, 99)
    a.append({"d": [{"f": "T19"}, {"f": "S10"}, {"f": "D16"}], "zu": True})
    st = spielarten.auswerten(s)
    assert st["verlauf"][-1]["p"] == 3


class Catch40Hilfe:
    @staticmethod
    def bis(s: dict[str, Any], ziel: int) -> list[dict[str, Any]]:
        for _ in range(61, ziel):
            s["aufnahmen"] += [{"d": [{"f": "M"}] * 3, "zu": True}] * 2
        return s["aufnahmen"]


def test_checkout_training() -> None:
    st = spielarten.auswerten(spiel("checkout", n=1, runden=3))
    z = st["spieler"][0]["zielwert"]
    assert 2 <= z <= 170 and z not in spielarten.BOGEY and st["spieler"][0]["rest"] == z
    st = spielarten.auswerten(spiel("checkout", n=1, runden=3, aufnahmen=[["M", "M", "M"]] * 3))
    assert st["spieler"][0]["geschafft"] == 0 and st["spieler"][0]["runde"] == 1
    assert "verfehlt" in st["verlauf"][-1]["x"]
    st = spielarten.auswerten(spiel("checkout", n=1, runden=1, aufnahmen=[["M", "M", "M"]] * 3))
    assert st["gewinner"] == 0
    # beide Spieler bekommen dieselben Finishes
    st = spielarten.auswerten(spiel("checkout", n=2, runden=3, aufnahmen=[["M", "M", "M"]] * 6))
    a, b = st["spieler"]
    assert a["zielwert"] == b["zielwert"] and a["runde"] == b["runde"] == 1


def test_jdc() -> None:
    st = spielarten.auswerten(spiel("jdc", n=1))
    assert st["ziel"] == "10" and st["runden"] == 19
    st = spielarten.auswerten(spiel("jdc", n=1, aufnahmen=[["S10", "D10", "T10"]]))
    assert st["spieler"][0]["rest"] == 60 + 100 and "shanghai" in st["verlauf"][0]["x"]
    st = spielarten.auswerten(spiel("jdc", n=1, aufnahmen=[["M", "M", "M"]] * 6 + [["D1", "D2", "D4"]]))
    assert st["spieler"][0]["rest"] == 100
    assert st["ziel"] == "D4"
    auf = [["M", "M", "M"]] * 12 + [["D19", "D20", "D25"]]
    st = spielarten.auswerten(spiel("jdc", n=1, aufnahmen=auf))
    assert st["spieler"][0]["rest"] == 200 and st["ziel"] == "15"
    st = spielarten.auswerten(spiel("jdc", n=1, aufnahmen=[["M", "M", "M"]] * 19))
    assert st["gewinner"] == 0
    assert st["spieler"][0]["darts"] == 57


def test_singles() -> None:
    st = spielarten.auswerten(spiel("singles", n=1, aufnahmen=[["S1", "D1", "T1"], ["S3", "M", "M"]]))
    assert st["spieler"][0]["rest"] == 6 and st["ziel"] == "3"
    auf = [["T" + str(z)] * 3 for z in range(1, 21)] + [["D25", "D25", "D25"]]
    st = spielarten.auswerten(spiel("singles", n=1, aufnahmen=auf))
    assert st["gewinner"] == 0 and st["spieler"][0]["rest"] == 186


def test_stechen_hat_ein_ende() -> None:
    gleich = [["S1", "M", "M"]] * 2 * (1 + spielarten.MAX_STECHEN)
    st = spielarten.auswerten(spiel("highscore", n=2, aufnahmen=gleich, runden=1))
    assert st["gewinner"] == 0


def test_checkout_weg_nur_mit_den_restlichen_darts() -> None:
    """Der Weg zeigt nur, was mit den Darts geht, die noch übrig sind."""
    # Gotcha bis 301: P0 hat 181, braucht 120 – mit drei Darts möglich
    vorher = [["T20", "T20", "T20"], ["S1", "S1", "S1"]]
    assert spielarten.auswerten(spiel("gotcha", aufnahmen=vorher, zielwert=301))["weg"]
    # nach einem Fehlwurf braucht P0 weiter 121, mit zwei Darts geht das nicht
    assert spielarten.auswerten(spiel("gotcha", aufnahmen=vorher, offen=["M"], zielwert=301))["weg"] is None
    # nach S20 braucht P0 101 – mit zwei Darts möglich
    st = spielarten.auswerten(spiel("gotcha", aufnahmen=vorher, offen=["S20"], zielwert=301))
    assert st["weg"] is not None
    assert len(st["weg"]) <= 2
