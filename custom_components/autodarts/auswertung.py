"""Spielerprofile über alle Spiele: Trefferbild, Trend, Elo-Wertung, Serie, direkter Vergleich, Abzeichen.

Liegt in .storage/autodarts.spiel unter "profil" (je Spieler-ID). Jedes beendete Spiel
wird mit `nachtragen(+1)` eingerechnet und bei Rückgängig nach Spielende mit `-1`
wieder herausgenommen.
"""

from __future__ import annotations

from datetime import date, timedelta
from itertools import pairwise
from typing import Any

MAX_XY = 150
MAX_TREND = 60
MAX_TAGE = 400
ELO_START = 1000
ZAEHL_TAGS = ("nine_marks", "shanghai", "hole_in_one", "killer", "home_run", "check", "geschafft")

# Abzeichen: Schlüssel, Schwellen Bronze/Silber/Gold, kleiner ist besser
ABZEICHEN: list[tuple[str, tuple[int, int, int], bool]] = [
    ("n180", (1, 10, 50), False),
    ("ton", (10, 100, 500), False),
    ("high_finish", (100, 130, 170), False),
    ("kurzes_leg", (18, 15, 12), True),
    ("average", (40, 60, 80), False),
    ("siege", (1, 25, 100), False),
    ("spiele", (10, 100, 500), False),
    ("darts", (1000, 10000, 50000), False),
    ("serie", (3, 7, 30), False),
    ("nine_marks", (1, 5, 20), False),
    ("shanghai", (1, 3, 10), False),
    ("hole_in_one", (1, 10, 50), False),
    ("allrounder", (3, 6, 11), False),
]


def bot_elo(level: int) -> float:
    """Feste Wertung eines Bots (Average 60 ≈ 1000)."""
    return 400 + 10 * level


def _profil(daten: dict[str, Any], sid: str) -> dict[str, Any]:
    p: dict[str, Any] = daten.setdefault("profil", {}).setdefault(sid, {})
    return p


def nachtragen(daten: dict[str, Any], spiel: dict[str, Any], stand: dict[str, Any], vorzeichen: int, heute: date) -> None:
    """Ein beendetes Spiel in die Profile einrechnen (+1) oder wieder herausnehmen (-1)."""
    spieler = spiel["spieler"]
    gewinner = stand["gewinner"]
    art = stand.get("art", "x01")
    verlauf = stand.get("verlauf") or []
    for k, s in enumerate(spieler):
        sid = s.get("id")
        if not sid:
            continue
        p = _profil(daten, sid)
        felder: dict[str, int] = p.setdefault("felder", {})
        tags: dict[str, int] = p.setdefault("x", {})
        for z in verlauf:
            if z["s"] != k:
                continue
            for f in z["d"]:
                felder[f] = max(0, felder.get(f, 0) + vorzeichen)
                if not felder[f]:
                    del felder[f]
            for t in z.get("x") or []:
                if t in ZAEHL_TAGS:
                    tags[t] = max(0, tags.get(t, 0) + vorzeichen)
        trend: list[dict[str, Any]] = p.setdefault("trend", [])
        if vorzeichen > 0:
            sk = stand["spieler"][k]
            trend.append({"id": spiel["id"], "t": heute.isoformat(), "art": art, "w": sk["avg"] if art in ("x01", "cricket") else sk["rest"], "s": k == gewinner})
            del trend[:-MAX_TREND]
            xy: list[list[float]] = p.setdefault("xy", [])
            xy.extend(_positionen(spiel, stand, k))
            del xy[:-MAX_XY]
            tage: list[str] = p.setdefault("tage", [])
            if heute.isoformat() not in tage:
                tage.append(heute.isoformat())
                del tage[:-MAX_TAGE]
        else:
            p["trend"] = [e for e in trend if e.get("id") != spiel["id"]]
        # direkter Vergleich: Sieger gegen jeden anderen angelegten Spieler
        if gewinner is not None and k != gewinner:
            g_id = spieler[gewinner].get("id")
            if g_id:
                gegen = _profil(daten, g_id).setdefault("gegen", {}).setdefault(sid, [0, 0])
                gegen[0] = max(0, gegen[0] + vorzeichen)
                mein = p.setdefault("gegen", {}).setdefault(g_id, [0, 0])
                mein[1] = max(0, mein[1] + vorzeichen)
    _elo(daten, spiel, gewinner, vorzeichen)


def _positionen(spiel: dict[str, Any], stand: dict[str, Any], k: int) -> list[list[float]]:
    """x/y der Board-Darts eines Spielers (relativ zum Doppelring)."""
    aufnahmen = spiel.get("aufnahmen") or []
    out: list[list[float]] = []
    for z in stand.get("verlauf") or []:
        if z["s"] != k or z["i"] >= len(aufnahmen):
            continue
        for d in aufnahmen[z["i"]]["d"][:3]:
            x, y = d.get("x"), d.get("y")
            if isinstance(x, (int, float)) and isinstance(y, (int, float)) and d.get("q") != "bot":
                out.append([round(x, 3), round(y, 3)])
    return out


def _elo(daten: dict[str, Any], spiel: dict[str, Any], gewinner: int | None, vorzeichen: int) -> None:
    """Elo: Sieger gegen jeden anderen; Bots haben eine feste Wertung. Rücknahme über gespeicherte Änderung."""
    if gewinner is None or len(spiel["spieler"]) < 2:
        return
    if vorzeichen < 0:
        for sid, delta in (spiel.pop("elo", None) or {}).items():
            p = _profil(daten, sid)
            p["elo"] = round(p.get("elo", ELO_START) - delta, 1)
        return
    def wertung(s: dict[str, Any]) -> float:
        if s.get("bot"):
            return bot_elo(int(s["bot"]))
        return float(_profil(daten, s["id"]).get("elo", ELO_START)) if s.get("id") else float(ELO_START)
    sp = spiel["spieler"]
    n = len(sp)
    faktor = 32 / (n - 1)
    delta = [0.0] * n
    for k in range(n):
        if k == gewinner:
            continue
        rg, rk = wertung(sp[gewinner]), wertung(sp[k])
        erwartet = 1 / (1 + 10 ** ((rk - rg) / 400))
        delta[gewinner] += faktor * (1 - erwartet)
        delta[k] -= faktor * (1 - erwartet)
    gespeichert = {}
    for k, s in enumerate(sp):
        if s.get("id"):
            p = _profil(daten, s["id"])
            p["elo"] = round(p.get("elo", ELO_START) + delta[k], 1)
            gespeichert[s["id"]] = round(delta[k], 1)
    spiel["elo"] = gespeichert


def serie(tage: list[str], heute: date) -> tuple[int, int]:
    """(aktuelle Serie, beste Serie) in Tagen hintereinander gespielt."""
    if not tage:
        return 0, 0
    menge = sorted({date.fromisoformat(t) for t in tage})
    beste = lauf = 1
    for a, b in pairwise(menge):
        lauf = lauf + 1 if b - a == timedelta(days=1) else 1
        beste = max(beste, lauf)
    aktuell = 0
    tag = heute if heute in menge else heute - timedelta(days=1)
    while tag in menge:
        aktuell += 1
        tag -= timedelta(days=1)
    return aktuell, beste


def abzeichen(ges: dict[str, Any], profil: dict[str, Any], beste_serie: int) -> list[dict[str, Any]]:
    """Abzeichen mit Stufe 0 (noch nicht) bis 3 (Gold) und dem Wert dazu."""
    arten = ges.get("arten") or {}
    werte = {
        "n180": ges.get("n180", 0),
        "ton": ges.get("n100", 0) + ges.get("n140", 0) + ges.get("n180", 0),
        "high_finish": ges.get("finish", 0),
        "kurzes_leg": ges.get("bestes_leg", 0),
        "average": ges.get("bester_avg", 0),
        "siege": ges.get("siege", 0) + sum(a.get("siege", 0) for a in arten.values()),
        "spiele": ges.get("spiele", 0) + sum(a.get("spiele", 0) for a in arten.values()),
        "darts": ges.get("darts", 0) + sum(a.get("darts", 0) for a in arten.values()),
        "serie": beste_serie,
        "nine_marks": (profil.get("x") or {}).get("nine_marks", 0),
        "shanghai": (profil.get("x") or {}).get("shanghai", 0),
        "hole_in_one": (profil.get("x") or {}).get("hole_in_one", 0),
        "allrounder": (1 if ges.get("spiele") else 0) + sum(1 for a in arten.values() if a.get("spiele")),
    }
    liste = []
    for key, stufen, kleiner in ABZEICHEN:
        w = werte[key]
        if kleiner:
            stufe = sum(1 for s in stufen if w and w <= s)
        else:
            stufe = sum(1 for s in stufen if w >= s)
        liste.append({"key": key, "wert": round(w, 1) if isinstance(w, float) else w, "stufe": stufe,
                      "ziel": stufen[stufe] if stufe < 3 else None})
    return liste
