"""K.-o.-Turnier (ohne Home Assistant): Baum aus Teilnehmern und Ergebnissen.

Gespeichert werden nur die Teilnehmer und je Match der Sieger. Der Baum mit
Freilosen und den späteren Runden wird daraus jedes Mal neu gebaut.
"""

from __future__ import annotations

from typing import Any

MIN_SPIELER = 3
MAX_SPIELER = 16
FREI = -1  # Freilos


def _groesse(n: int) -> int:
    g = 2
    while g < n:
        g *= 2
    return g


def baum(t: dict[str, Any]) -> list[list[dict[str, Any]]]:
    """Runden mit Matches {a, b, sieger} (Indizes in t["teilnehmer"], None = Freilos/offen)."""
    n = len(t["teilnehmer"])
    g = _groesse(n)
    plaetze: list[int | None] = [*range(n), *([FREI] * (g - n))]
    ergebnisse: dict[str, int] = t.get("ergebnisse") or {}
    runden: list[list[dict[str, Any]]] = []
    paare = [(plaetze[i], plaetze[g - 1 - i]) for i in range(g // 2)]
    # 1 gegen letzten, 2 gegen vorletzten … und die Hälften verzahnt, damit sich die Besten erst spät treffen
    reihenfolge = _verzahnt(g // 2)
    paare = [paare[i] for i in reihenfolge]
    r = 0
    while True:
        runde = []
        for m, (a, b) in enumerate(paare):
            sieger: int | None
            if a is None or b is None:
                sieger = None  # wartet auf ein früheres Match
            elif b == FREI:
                sieger = a
            elif a == FREI:
                sieger = b
            else:
                sieger = ergebnisse.get(f"{r}-{m}")
            runde.append({"a": a, "b": b, "sieger": sieger, "freilos": FREI in (a, b)})
        runden.append(runde)
        if len(runde) == 1:
            break
        paare = [(runde[2 * j]["sieger"], runde[2 * j + 1]["sieger"]) for j in range(len(runde) // 2)]
        r += 1
    return runden


def _verzahnt(n: int) -> list[int]:
    """Reihenfolge der ersten Runde (Standard-Setzliste): 0, n-1, … so dass Nr. 1 und 2 erst im Finale aufeinandertreffen."""
    reihe = [0]
    while len(reihe) < n:
        k = len(reihe) * 2
        reihe = [x for i in reihe for x in (i, k - 1 - i)]
    return reihe


def naechstes(t: dict[str, Any]) -> tuple[int, int, int, int] | None:
    """(Runde, Match, a, b) des nächsten offenen Matches oder None."""
    for r, runde in enumerate(baum(t)):
        for m, x in enumerate(runde):
            if x["sieger"] is None and x["a"] is not None and x["b"] is not None and not x["freilos"]:
                return r, m, x["a"], x["b"]
    return None


def champion(t: dict[str, Any]) -> int | None:
    sieger: int | None = baum(t)[-1][0]["sieger"]
    return sieger


def ansicht(t: dict[str, Any], aktiv: tuple[int, int] | None) -> dict[str, Any]:
    """Für die Karte: Namen statt Indizes, nächstes Match, Sieger."""
    namen = t["namen"]
    b = baum(t)
    n = naechstes(t)
    ch = champion(t)
    return {
        "id": t["id"],
        "runden": [[{"a": _name(namen, x["a"]), "b": _name(namen, x["b"]),
                     "sieger": None if x["sieger"] is None else (0 if x["sieger"] == x["a"] else 1), "freilos": x["freilos"],
                     "aktiv": aktiv == (r, m)} for m, x in enumerate(runde)] for r, runde in enumerate(b)],
        "naechstes": {"runde": n[0], "match": n[1], "a": namen[n[2]], "b": namen[n[3]]} if n else None,
        "sieger": namen[ch] if ch is not None else None,
        "aktiv": list(aktiv) if aktiv else None,
        "match_nr": _match_nr(b, aktiv) if aktiv else None,
    }


def _name(namen: list[str], i: int | None) -> str | None:
    """Name, "" für ein Freilos, None solange offen."""
    if i is None:
        return None
    return "" if i == FREI else namen[i]


def _match_nr(b: list[list[dict[str, Any]]], aktiv: tuple[int, int]) -> list[int]:
    """[Runde, Nummer des Matches in der Runde (ohne Freilose), Anzahl echter Matches, Runden gesamt]."""
    r, m = aktiv
    echte = [k for k, x in enumerate(b[r]) if not x["freilos"]]
    return [r, (echte.index(m) + 1) if m in echte else 1, len(echte), len(b)]
