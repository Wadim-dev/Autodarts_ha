"""X01-Regeln ohne Home Assistant: Felder, Checkout-Wege, Auswertung eines Spiels, Bot.

Ein Spiel wird nur als Liste von Aufnahmen gespeichert (je bis zu 3 Darts). Alles
andere (Rest, Bust, Legs, Sets, Statistik, wer dran ist) rechnet `auswerten` jedes
Mal neu aus. Dadurch sind Korrekturen und Rückgängig einfach und immer stimmig.
"""

from __future__ import annotations

import math
import random
from typing import Any

ORDER = [20, 1, 18, 4, 13, 6, 10, 15, 2, 17, 3, 19, 7, 16, 8, 11, 14, 9, 12, 5]
FAKTOR = {"S": 1, "D": 2, "T": 3}
# Radien in mm (Doppelring außen = 170)
R_BULL, R_25, R_T1, R_T2, R_D1, R_D2 = 6.35, 15.9, 99.0, 107.0, 162.0, 170.0

ALLE = [f"{m}{n}" for m in "SDT" for n in range(1, 21)] + ["S25", "D25"]


def feld_ok(f: str) -> bool:
    return f == "M" or f in ALLE


def wert(f: str) -> tuple[int, int]:
    """(Punkte, Faktor) eines Felds wie T20, D25, M."""
    if not f or f == "M":
        return 0, 0
    fak = FAKTOR[f[0]]
    return int(f[1:]) * fak, fak


def feld_aus(zahl: int, faktor: int) -> str:
    if not zahl or not faktor:
        return "M"
    if zahl == 25:
        return "D25" if faktor >= 2 else "S25"
    return {1: "S", 2: "D", 3: "T"}.get(faktor, "S") + str(zahl)


def feld_text(f: str) -> str:
    return {"S25": "25", "D25": "Bull", "M": "Miss"}.get(f, f)


# ---------- Checkout ----------

def _endet(f: str, aus: str) -> bool:
    _, fak = wert(f)
    if aus == "double":
        return fak == 2
    if aus == "master":
        return fak in (2, 3)
    return fak > 0


DOPPEL_VORZUG = [20, 16, 8, 10, 12, 18, 4, 6, 14, 2, 9, 19, 13, 15, 17, 3, 5, 7, 11, 1]
# Vorbereitungs-Darts nach Beliebtheit (Rang = Position)
VORBEREITUNG = (
    [f"T{n}" for n in range(20, 9, -1)] + [f"S{n}" for n in range(20, 0, -1)] + ["S25"]
    + [f"T{n}" for n in range(9, 0, -1)] + ["D25"] + [f"D{n}" for n in DOPPEL_VORZUG]
)
_RANG = {f: i for i, f in enumerate(VORBEREITUNG)}
_BESTER: dict[int, str] = {}
for _f in VORBEREITUNG:
    _BESTER.setdefault(wert(_f)[0], _f)


def _abschluesse(aus: str) -> list[str]:
    d = [f"D{n}" for n in DOPPEL_VORZUG] + ["D25"]
    if aus == "double":
        return d
    if aus == "master":
        return d + [f"T{n}" for n in range(20, 0, -1)]
    return [f"S{n}" for n in range(20, 0, -1)] + ["S25"] + d + [f"T{n}" for n in range(20, 0, -1)]


_WEG_CACHE: dict[tuple[int, int, str], list[str] | None] = {}


def weg(rest: int, darts: int, aus: str = "double") -> list[str] | None:
    """Bester Checkout-Weg für `rest` mit höchstens `darts` Darts (oder None).

    Weniger Darts gehen vor; sonst zählt der Rang der Felder (Abschluss dreifach).
    """
    schluessel = (rest, darts, aus)
    if schluessel in _WEG_CACHE:
        return _WEG_CACHE[schluessel]
    ergebnis = None
    if 0 < rest <= 180 and darts > 0:
        enden = _abschluesse(aus)
        for anzahl in range(1, min(darts, 3) + 1):
            beste = None
            for ri, e in enumerate(enden):
                vor = rest - wert(e)[0]
                if anzahl == 1:
                    kandidaten = [[e]] if vor == 0 else []
                elif anzahl == 2:
                    kandidaten = [[_BESTER[vor], e]] if vor in _BESTER else []
                else:
                    kandidaten = [[a, _BESTER[vor - wert(a)[0]], e] for a in VORBEREITUNG if vor - wert(a)[0] in _BESTER]
                for k in kandidaten:
                    punkte = ri * 3 + sum(_RANG[x] for x in k[:-1])
                    if beste is None or punkte < beste[0]:
                        beste = (punkte, k)
            if beste:
                ergebnis = beste[1]
                break
    _WEG_CACHE[schluessel] = ergebnis
    return ergebnis


def ein_dart_finish(rest: int, aus: str) -> bool:
    return weg(rest, 1, aus) is not None


# ---------- Auswertung ----------

def _leer_stat() -> dict[str, Any]:
    return {"punkte": 0, "darts": 0, "f9p": 0, "f9d": 0, "versuche": 0, "treffer": 0, "hoechste": 0,
            "finish": 0, "n180": 0, "n140": 0, "n100": 0, "legs": 0, "sets": 0, "bestes_leg": 0, "aufnahmen": 0}


def auswerten(spiel: dict[str, Any]) -> dict[str, Any]:
    """Rechnet aus den Aufnahmen den kompletten Spielstand aus.

    Aufnahmen: [{"d": [{"f": "T20", ...}, ...], "zu": bool}]; nur die letzte darf offen sein.
    """
    e = spiel["einstellungen"]
    start, ein, aus = int(e["startwert"]), e["einwurf"], e["auswurf"]
    legs_ziel, sets_ziel = int(e["legs"]), int(e.get("sets") or 0)
    spieler = spiel["spieler"]
    n = len(spieler)
    reihe = spiel.get("reihenfolge") or list(range(n))
    st = [_leer_stat() for _ in range(n)]
    sets = [0] * n
    legs = [0] * n

    def neues_leg():
        return [start] * n, [ein == "straight"] * n, [0] * n, [0] * n, [None] * n

    rest, offen, leg_darts, leg_aufn, letzte = neues_leg()
    leg_nr = 0
    pos = 0
    gewinner = leg_gewinner = None
    verlauf: list[dict[str, Any]] = []
    aktuell = None
    ansage = ""
    ansage_id = ""
    aufnahmen = spiel.get("aufnahmen") or []

    for i, aufn in enumerate(aufnahmen):
        letzt = i == len(aufnahmen) - 1
        p = reihe[pos % n]
        rest_vor = r = rest[p]
        summe = genutzt = 0
        bust = checkout = False
        f9 = leg_aufn[p] < 3
        for dart in aufn["d"][:3]:
            if bust or checkout:
                break
            pkt, fak = wert(dart["f"])
            genutzt += 1
            if offen[p] and ein_dart_finish(r, aus):
                st[p]["versuche"] += 1
            if not offen[p]:
                if (ein == "double" and fak == 2) or (ein == "master" and fak in (2, 3)):
                    offen[p] = True
                else:
                    continue
            neu = r - pkt
            if neu < 0 or (aus != "straight" and neu == 1) or (neu == 0 and not _endet(dart["f"], aus)):
                bust = True
                break
            r = neu
            summe += pkt
            checkout = r == 0
        zu = bool(aufn.get("zu"))
        fertig = zu or bust or checkout or genutzt >= 3
        punkte = 0 if bust else summe
        gezaehlt = genutzt if checkout else (3 if (zu or bust) else genutzt)
        rest[p] = rest_vor if bust else r
        s = st[p]
        s["punkte"] += punkte
        s["darts"] += gezaehlt
        leg_darts[p] += gezaehlt
        if f9:
            s["f9p"] += punkte
            s["f9d"] += gezaehlt
        if fertig:
            s["aufnahmen"] += 1
            s["hoechste"] = max(s["hoechste"], punkte)
            if punkte == 180:
                s["n180"] += 1
            elif punkte >= 140:
                s["n140"] += 1
            elif punkte >= 100:
                s["n100"] += 1
            letzte[p] = "Bust" if bust else punkte
            leg_aufn[p] += 1
            ansage = "Bust" if bust else str(punkte)
            ansage_id = str(i)
        verlauf.append({"i": i, "s": p, "d": [d["f"] for d in aufn["d"][:3]], "p": punkte, "r": rest[p], "b": bust, "c": checkout})
        if letzt:
            aktuell = {"darts": aufn["d"][:3], "summe": punkte, "bust": bust, "checkout": checkout, "rest_vor": rest_vor, "fertig": fertig}
        if checkout:
            s["treffer"] += 1
            s["finish"] = max(s["finish"], summe)
            s["legs"] += 1
            s["bestes_leg"] = min(s["bestes_leg"] or 999, leg_darts[p])
            legs[p] += 1
            ansage = f"Leg {spieler[p]['name']}"
            ende = False
            if sets_ziel and legs[p] >= legs_ziel:
                sets[p] += 1
                s["sets"] += 1
                ansage = f"Satz {spieler[p]['name']}"
                legs = [0] * n
                ende = sets[p] >= sets_ziel
            elif not sets_ziel:
                ende = legs[p] >= legs_ziel
            if ende:
                gewinner = p
                ansage = f"Spiel {spieler[p]['name']}"
                break
            if not zu:
                leg_gewinner = p
                break
            leg_nr += 1
            pos = leg_nr
            rest, offen, leg_darts, leg_aufn, letzte = neues_leg()
            aktuell = None
            continue
        if zu:
            pos += 1
            aktuell = None

    am_zug = gewinner if gewinner is not None else (leg_gewinner if leg_gewinner is not None else reihe[pos % n])
    if aktuell is None:
        aktuell = {"darts": [], "summe": 0, "bust": False, "checkout": False, "rest_vor": rest[am_zug], "fertig": False}
    uebrig = 3 - len(aktuell["darts"])
    w = None
    if gewinner is None and leg_gewinner is None and not aktuell["fertig"] and offen[am_zug]:
        w = weg(rest[am_zug], uebrig, aus)
    sp = []
    for k in range(n):
        s = st[k]
        sp.append({
            "name": spieler[k]["name"],
            "bot": spieler[k].get("bot"),
            "rest": rest[k],
            "legs": legs[k],
            "sets": sets[k],
            "offen": offen[k],
            "avg": round(s["punkte"] / s["darts"] * 3, 2) if s["darts"] else 0,
            "f9": round(s["f9p"] / s["f9d"] * 3, 2) if s["f9d"] else 0,
            "darts": s["darts"],
            "leg_darts": leg_darts[k],
            "letzte": letzte[k],
            "quote": round(s["treffer"] / s["versuche"] * 100, 1) if s["versuche"] else 0,
            "versuche": s["versuche"],
            "treffer": s["treffer"],
            "hoechste": s["hoechste"],
            "finish": s["finish"],
            "n180": s["n180"], "n140": s["n140"], "n100": s["n100"],
            "bestes_leg": s["bestes_leg"],
            "weg": weg(rest[k], 3, aus) if offen[k] else None,
        })
    return {
        "am_zug": am_zug,
        "aufnahme": {**aktuell, "darts": [{"f": d["f"], "x": d.get("x"), "y": d.get("y")} for d in aktuell["darts"]]},
        "weg": w,
        "spieler": sp,
        "statistik": st,
        "gewinner": gewinner,
        "leg_gewinner": leg_gewinner,
        "leg": leg_nr + 1,
        "set": sum(sets) + 1 if gewinner is None else sum(sets),
        "verlauf": verlauf,
        "ansage": ansage,
        "ansage_id": ansage_id,
    }


# ---------- Board-Geometrie und Bot ----------

def feld_an(x_mm: float, y_mm: float) -> str:
    r = math.hypot(x_mm, y_mm)
    if r <= R_BULL:
        return "D25"
    if r <= R_25:
        return "S25"
    if r > R_D2:
        return "M"
    winkel = (math.degrees(math.atan2(x_mm, y_mm)) + 9) % 360
    zahl = ORDER[int(winkel // 18) % 20]
    if R_T1 <= r <= R_T2:
        return f"T{zahl}"
    if R_D1 <= r <= R_D2:
        return f"D{zahl}"
    return f"S{zahl}"


def zielpunkt(f: str) -> tuple[float, float]:
    if f in ("D25", "S25", "M"):
        return 0.0, 0.0
    zahl = int(f[1:])
    radius = {"T": (R_T1 + R_T2) / 2, "D": (R_D1 + R_D2) / 2, "S": (R_T2 + R_D1) / 2}[f[0]]
    w = math.radians(ORDER.index(zahl) * 18)
    return radius * math.sin(w), radius * math.cos(w)


def _streuung_tabelle() -> list[tuple[float, float]]:
    """3-Dart-Average je Streuung (mm), Ziel T20. Einmal berechnet."""
    zufall = random.Random(1)
    ax, ay = zielpunkt("T20")
    tabelle = []
    for sigma in [2 + i * 2.5 for i in range(50)]:
        summe = 0
        for _ in range(2500):
            summe += wert(feld_an(ax + zufall.gauss(0, sigma), ay + zufall.gauss(0, sigma)))[0]
        tabelle.append((sigma, summe / 2500 * 3))
    return tabelle


_TABELLE: list[tuple[float, float]] = []


def streuung(average: float) -> float:
    global _TABELLE
    if not _TABELLE:
        _TABELLE = _streuung_tabelle()
    for (s1, a1), (s2, a2) in zip(_TABELLE, _TABELLE[1:]):
        if a1 >= average >= a2:
            return s1 + (s2 - s1) * ((a1 - average) / (a1 - a2) if a1 != a2 else 0)
    return _TABELLE[0][0] if average > _TABELLE[0][1] else _TABELLE[-1][0]


LEAVES = [40, 32, 36, 24, 16, 20, 8, 12, 28, 18, 10, 4, 38, 34, 30, 26, 22, 14, 6, 2]


def bot_ziel(rest: int, darts_uebrig: int, offen: bool, ein: str, aus: str) -> str:
    if not offen:
        return "D20" if ein == "double" else "T20"
    w = weg(rest, darts_uebrig, aus)
    if w:
        return w[0]
    if rest > 180 or rest >= 100:
        return "T20" if rest - 60 not in (1,) else "T19"
    for leave in LEAVES:
        vor = rest - leave
        if vor <= 0:
            continue
        for f in [f"S{n}" for n in range(20, 0, -1)] + ["S25"] + [f"T{n}" for n in range(20, 0, -1)]:
            if wert(f)[0] == vor:
                return f
    return "T20" if rest > 60 else "S1"


def bot_wurf(ziel: str, sigma: float, zufall: random.Random) -> dict[str, Any]:
    ax, ay = zielpunkt(ziel)
    x, y = ax + zufall.gauss(0, sigma), ay + zufall.gauss(0, sigma)
    return {"f": feld_an(x, y), "x": round(x / R_D2, 3), "y": round(y / R_D2, 3), "q": "bot"}


def bull_abstand(dart: dict[str, Any]) -> float:
    x, y = dart.get("x"), dart.get("y")
    if isinstance(x, (int, float)) and isinstance(y, (int, float)):
        return math.hypot(x, y)
    return {"D25": 0.02, "S25": 0.06}.get(dart.get("f"), 9.0)
