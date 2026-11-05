"""Tournaments (without Home Assistant): knockout, double knockout, groups + knockout and league.

Only the participants and the winner of each match are stored (with the legs).
Brackets with byes and later rounds, fixtures and tables are built from that every time.

Match keys: knockout "r-m", league "r-m", double knockout "w r-m" (winners bracket),
"l r-m" (losers bracket), "f0"/"f1" (grand final and its decider), groups "g gruppe-r-m"
and the knockout after the groups "k r-m" (without the spaces).
"""

from __future__ import annotations

from typing import Any

MIN_SPIELER = 3
MAX_SPIELER = 32
LIGA_MAX = 10  # a league of 10 already has 45 matches
DOPPEL_MAX = 16  # double knockout of 16: 30 matches
GRUPPEN_MIN = 6
MODI = ("ko", "doppel_ko", "gruppen", "liga")
GRENZEN = {"ko": (MIN_SPIELER, MAX_SPIELER), "doppel_ko": (MIN_SPIELER, DOPPEL_MAX),
           "gruppen": (GRUPPEN_MIN, MAX_SPIELER), "liga": (MIN_SPIELER, LIGA_MAX)}
FREI = -1  # Freilos


def _groesse(n: int) -> int:
    g = 2
    while g < n:
        g *= 2
    return g


def baum(t: dict[str, Any]) -> list[list[dict[str, Any]]]:
    """Runden mit Matches {a, b, sieger} (Indizes in t["teilnehmer"], None = Freilos/offen)."""
    return _ko(list(range(len(t["teilnehmer"]))), t.get("ergebnisse") or {}, "")


def _ko(setzliste: list[int | None], ergebnisse: dict[str, int], praefix: str) -> list[list[dict[str, Any]]]:
    """K.-o.-Baum für eine Setzliste (None = noch unbekannt, z. B. Gruppenplatz)."""
    g = _groesse(len(setzliste))
    plaetze: list[int | None] = [*setzliste, *([FREI] * (g - len(setzliste)))]
    runden: list[list[dict[str, Any]]] = []
    paare: list[tuple[int | None, int | None]] = [(plaetze[i], plaetze[g - 1 - i]) for i in range(g // 2)]
    # 1 gegen letzten, 2 gegen vorletzten … und die Hälften verzahnt, damit sich die Besten erst spät treffen
    reihenfolge = _verzahnt(g // 2)
    paare = [paare[i] for i in reihenfolge]
    r = 0
    while True:
        runde: list[dict[str, Any]] = []
        for m, (a, b) in enumerate(paare):
            k = f"{praefix}{r}-{m}"
            sieger, _verl = _ergebnis(k, a, b, ergebnisse)
            runde.append({"k": k, "a": a, "b": b, "sieger": sieger, "freilos": FREI in (a, b)})
        runden.append(runde)
        if len(runde) == 1:
            break
        paare = [(runde[2 * j]["sieger"], runde[2 * j + 1]["sieger"]) for j in range(len(runde) // 2)]
        r += 1
    return runden


def _ergebnis(k: str, a: int | None, b: int | None, ergebnisse: dict[str, int]) -> tuple[int | None, int | None]:
    """(Sieger, Verlierer) eines Matches; Freilose gehen von selbst weiter, None = noch offen."""
    if a is None or b is None:
        return None, None
    if a == FREI and b == FREI:
        return FREI, FREI
    if b == FREI:
        return a, FREI
    if a == FREI:
        return b, FREI
    s = ergebnisse.get(k)
    if s == a:
        return a, b
    if s == b:
        return b, a
    return None, None


def _verzahnt(n: int) -> list[int]:
    """Reihenfolge der ersten Runde (Standard-Setzliste): 0, n-1, … so dass Nr. 1 und 2 erst im Finale aufeinandertreffen."""
    reihe = [0]
    while len(reihe) < n:
        k = len(reihe) * 2
        reihe = [x for i in reihe for x in (i, k - 1 - i)]
    return reihe


def doppel(t: dict[str, Any]) -> dict[str, Any]:
    """Double knockout: winners bracket, losers bracket and grand final (with a decider if needed).

    Who loses in the winners bracket drops into the losers bracket; who loses twice is out.
    """
    erg: dict[str, int] = t.get("ergebnisse") or {}
    oben = _ko(list(range(len(t["teilnehmer"]))), erg, "w")
    k = len(oben)  # Runden oben
    unten: list[list[dict[str, Any]]] = []

    def runde(paare: list[tuple[int | None, int | None]], r: int) -> list[dict[str, Any]]:
        out = []
        for m, (a, b) in enumerate(paare):
            key = f"l{r}-{m}"
            sieger, _v = _ergebnis(key, a, b, erg)
            out.append({"k": key, "a": a, "b": b, "sieger": sieger, "freilos": FREI in (a, b)})
        return out

    verlierer = [[_ergebnis(x["k"], x["a"], x["b"], erg)[1] for x in r] for r in oben]
    if k > 1:
        erste = verlierer[0]
        unten.append(runde([(erste[2 * j], erste[2 * j + 1]) for j in range(len(erste) // 2)], 0))
        for i in range(1, k):
            sieger_unten = [x["sieger"] for x in unten[-1]]
            dazu = verlierer[i] if i % 2 else list(reversed(verlierer[i]))  # anders herum, damit Rückspiele spät kommen
            unten.append(runde(list(zip(sieger_unten, dazu, strict=True)), len(unten)))
            if i < k - 1:
                w = [x["sieger"] for x in unten[-1]]
                unten.append(runde([(w[2 * j], w[2 * j + 1]) for j in range(len(w) // 2)], len(unten)))
    oben_sieger = oben[-1][0]["sieger"]
    unten_sieger = unten[-1][0]["sieger"] if unten else FREI
    f0s, _ = _ergebnis("f0", oben_sieger, unten_sieger, erg)
    finale = [{"k": "f0", "a": oben_sieger, "b": unten_sieger, "sieger": f0s, "freilos": FREI in (oben_sieger, unten_sieger)}]
    if f0s is not None and f0s != oben_sieger and f0s != FREI:
        # der Sieger aus dem unteren Baum hat dem oberen die erste Niederlage beigebracht: Entscheidungsspiel
        f1s, _ = _ergebnis("f1", oben_sieger, unten_sieger, erg)
        finale.append({"k": "f1", "a": oben_sieger, "b": unten_sieger, "sieger": f1s, "freilos": False})
    return {"oben": oben, "unten": unten, "finale": finale}


def _doppel_reihe(d: dict[str, Any]) -> list[dict[str, Any]]:
    """Spielreihenfolge: oben 1, unten 1, dann je oben n, unten 2n-1 und 2n, zum Schluss das Finale."""
    oben, unten = d["oben"], d["unten"]
    reihe = list(oben[0]) + (list(unten[0]) if unten else [])
    for i in range(1, len(oben)):
        reihe += oben[i]
        for j in (2 * i - 1, 2 * i):
            if j < len(unten):
                reihe += unten[j]
    return reihe + list(d["finale"])


def gruppen_anzahl(n: int) -> int:
    """2 Gruppen bis 11 Spieler, 4 bis 23, sonst 8 – je 3 bis 6 Spieler, die Besten zwei kommen weiter."""
    return 2 if n < 12 else 4 if n < 24 else 8


def gruppen_einteilung(n: int) -> list[list[int]]:
    """Schlangenlinie nach Setzliste: 1 → A, 2 → B, … dann rückwärts, damit die Gruppen gleich stark sind."""
    g = gruppen_anzahl(n)
    gruppen: list[list[int]] = [[] for _ in range(g)]
    for i in range(n):
        durchgang, pos = divmod(i, g)
        gruppen[pos if durchgang % 2 == 0 else g - 1 - pos].append(i)
    return gruppen


def gruppen(t: dict[str, Any]) -> dict[str, Any]:
    """Gruppenphase (jeder gegen jeden in der Gruppe) und K.-o. der zwei Besten jeder Gruppe."""
    erg: dict[str, int] = t.get("ergebnisse") or {}
    legs: dict[str, list[int]] = t.get("legs") or {}
    teile: list[dict[str, Any]] = []
    fertig = True
    for gi, mitglieder in enumerate(gruppen_einteilung(len(t["teilnehmer"]))):
        spiele = []
        for r, runde in enumerate(liga_runden(len(mitglieder))):
            for m, (a, b) in enumerate(runde):
                key = f"g{gi}-{r}-{m}"
                pa, pb = mitglieder[a], mitglieder[b]
                spiele.append({"k": key, "a": pa, "b": pb, "sieger": erg.get(key), "freilos": False, "legs": legs.get(key)})
                if key not in erg:
                    fertig = False
        teile.append({"mitglieder": mitglieder, "spiele": spiele, "tabelle": _tabelle(mitglieder, spiele, erg, legs)})
    g = len(teile)
    if fertig:
        setz: list[int | None] = [x["tabelle"][0]["i"] for x in teile] + [x["tabelle"][1]["i"] for x in teile]
    else:
        setz = [None] * (2 * g)
    return {"gruppen": teile, "ko": _ko(setz, erg, "k"), "fertig": fertig}


def _tabelle(mitglieder: list[int], spiele: list[dict[str, Any]], erg: dict[str, int], legs: dict[str, list[int]]) -> list[dict[str, Any]]:
    """Tabelle: Siege (2 Punkte), dann Leg-Differenz, gewonnene Legs, Setzliste."""
    zeilen = {i: {"i": i, "spiele": 0, "siege": 0, "legs": 0, "gegen": 0} for i in mitglieder}
    for x in spiele:
        k, a, b = x["k"], x["a"], x["b"]
        if k not in erg:
            continue
        la, lb = legs.get(k) or ([1, 0] if erg[k] == a else [0, 1])
        for p, eigen, fremd in ((a, la, lb), (b, lb, la)):
            z = zeilen[p]
            z["spiele"] += 1
            z["legs"] += eigen
            z["gegen"] += fremd
        zeilen[erg[k]]["siege"] += 1
    return sorted(zeilen.values(), key=lambda z: (-z["siege"], z["gegen"] - z["legs"], -z["legs"], z["i"]))


def reihe(t: dict[str, Any]) -> list[dict[str, Any]]:
    """Alle Matches in Spielreihenfolge (mit Schlüssel k, a, b, sieger, freilos)."""
    modus = t.get("modus") or "ko"
    if modus == "doppel_ko":
        return _doppel_reihe(doppel(t))
    if modus == "gruppen":
        gr = gruppen(t)
        # Gruppen abwechselnd, damit niemand lange zweimal hintereinander spielt
        spiele = [x["spiele"] for x in gr["gruppen"]]
        gemischt = [s[i] for i in range(max(len(s) for s in spiele)) for s in spiele if i < len(s)]
        return gemischt + [x for r in gr["ko"] for x in r]
    if modus == "liga":
        erg = t.get("ergebnisse") or {}
        return [{"k": f"{r}-{m}", "a": a, "b": b, "sieger": erg.get(f"{r}-{m}"), "freilos": False}
                for r, runde in enumerate(liga_runden(len(t["teilnehmer"]))) for m, (a, b) in enumerate(runde)]
    return [x for r in baum(t) for x in r]


def naechstes_match(t: dict[str, Any]) -> tuple[str, int, int] | None:
    """(Schlüssel, a, b) des nächsten offenen Matches oder None."""
    for x in reihe(t):
        if x["sieger"] is None and x["a"] not in (None, FREI) and x["b"] not in (None, FREI):
            return x["k"], x["a"], x["b"]
    return None


def liga_runden(n: int) -> list[list[tuple[int, int]]]:
    """Fixtures of a league (circle method): every player meets every other once, one match after the other."""
    plaetze: list[int] = list(range(n)) + ([FREI] if n % 2 else [])
    k = len(plaetze)
    runden = []
    for _ in range(k - 1):
        runden.append([(plaetze[i], plaetze[k - 1 - i]) for i in range(k // 2) if FREI not in (plaetze[i], plaetze[k - 1 - i])])
        plaetze = [plaetze[0], plaetze[-1], *plaetze[1:-1]]
    return runden


def tabelle(t: dict[str, Any]) -> list[dict[str, Any]]:
    """League table: wins (2 points each), then leg difference, then legs won."""
    erg = t.get("ergebnisse") or {}
    spiele = [{"k": f"{r}-{m}", "a": a, "b": b} for r, runde in enumerate(liga_runden(len(t["teilnehmer"]))) for m, (a, b) in enumerate(runde)]
    return _tabelle(list(range(len(t["teilnehmer"]))), spiele, erg, t.get("legs") or {})


def naechstes(t: dict[str, Any]) -> tuple[int, int, int, int] | None:
    """(Runde, Match, a, b) des nächsten offenen Matches (K.-o. und Liga) oder None."""
    n = naechstes_match(t)
    if n is None:
        return None
    r, m = (int(x) for x in n[0].lstrip("wlfgk").split("-")[-2:]) if "-" in n[0] else (0, 0)
    return r, m, n[1], n[2]


def champion(t: dict[str, Any]) -> int | None:
    modus = t.get("modus") or "ko"
    if modus == "liga":
        return None if naechstes_match(t) else int(tabelle(t)[0]["i"])
    if modus == "doppel_ko":
        f = doppel(t)["finale"]
        s = f[-1]["sieger"]
        return None if s in (None, FREI) or (len(f) == 1 and s != f[0]["a"]) else int(s)
    b = gruppen(t)["ko"] if modus == "gruppen" else baum(t)
    sieger: int | None = b[-1][0]["sieger"]
    return sieger


def _schluessel(aktiv: Any) -> str | None:
    if aktiv is None:
        return None
    if isinstance(aktiv, (list, tuple)):
        return f"{aktiv[0]}-{aktiv[1]}"
    return str(aktiv)


def ansicht(t: dict[str, Any], aktiv: Any) -> dict[str, Any]:
    """Für die Karte: Namen statt Indizes, nächstes Match, Sieger, Banner für das laufende Match.

    aktiv: Schlüssel des laufenden Matches (oder (Runde, Match) bei K.-o./Liga).
    """
    namen = t["namen"]
    modus = t.get("modus") or "ko"
    k_aktiv = _schluessel(aktiv)
    legs = t.get("legs") or {}
    n = naechstes_match(t)
    ch = champion(t)

    def match(x: dict[str, Any], platz: tuple[str, str] | None = None) -> dict[str, Any]:
        s = x["sieger"]
        out = {"k": x["k"], "a": _name(namen, x["a"]), "b": _name(namen, x["b"]),
               "sieger": None if s in (None, FREI) or x["a"] is None or x["b"] is None else (0 if s == x["a"] else 1),
               "freilos": x["freilos"], "aktiv": x["k"] == k_aktiv, "legs": legs.get(x["k"])}
        if platz and x["a"] is None:
            out["pa"], out["pb"] = platz
        return out

    basis: dict[str, Any] = {
        "id": t["id"], "modus": modus,
        "naechstes": {"k": n[0], "a": namen[n[1]], "b": namen[n[2]]} if n else None,
        "sieger": namen[ch] if ch is not None else None,
        "aktiv": k_aktiv,
    }
    if modus == "liga":
        spiele = [match(x) for x in reihe(t)]
        nr = next((i for i, x in enumerate(spiele) if x["aktiv"]), 0)
        return {**basis, "spiele": spiele,
                "tabelle": _tabelle_namen(namen, tabelle(t)),
                "match_nr": [0, nr + 1, len(spiele), 0] if k_aktiv else None, "phase": "liga" if k_aktiv else None}
    if modus == "doppel_ko":
        d = doppel(t)
        out = {**basis, "runden": [[match(x) for x in r] for r in d["oben"]],
               "unten": [[match(x) for x in r] for r in d["unten"]],
               "finale": [match(x) for x in d["finale"]]}
        out.update(_banner_doppel(d, k_aktiv))
        return out
    if modus == "gruppen":
        gr = gruppen(t)
        gruppen_out = []
        for gi, x in enumerate(gr["gruppen"]):
            gruppen_out.append({"name": chr(65 + gi), "spiele": [match(m) for m in x["spiele"]],
                                "tabelle": _tabelle_namen(namen, x["tabelle"])})
        g = len(gr["gruppen"])
        platz = [f"1 {chr(65 + i)}" for i in range(g)] + [f"2 {chr(65 + i)}" for i in range(g)]
        runden = []
        for r, runde in enumerate(gr["ko"]):
            zeile = []
            for m, x in enumerate(runde):
                pl = None
                if r == 0:
                    a_i, b_i = _erste_runde_plaetze(len(platz))[m]
                    pl = (platz[a_i], platz[b_i])
                zeile.append(match(x, pl))
            runden.append(zeile)
        out = {**basis, "gruppen": gruppen_out, "runden": runden, "gruppen_fertig": gr["fertig"]}
        out.update(_banner_gruppen(gr, k_aktiv))
        return out
    b = baum(t)
    return {**basis, "runden": [[match(x) for x in r] for r in b],
            "match_nr": _match_nr(b, k_aktiv) if k_aktiv else None, "phase": "ko" if k_aktiv else None}


def _tabelle_namen(namen: list[str], zeilen: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [{"name": namen[z["i"]], "spiele": z["spiele"], "siege": z["siege"], "punkte": z["siege"] * 2,
             "legs": z["legs"], "gegen": z["gegen"]} for z in zeilen]


def _erste_runde_plaetze(n: int) -> list[tuple[int, int]]:
    """Setzplätze (a, b) je Match der ersten K.-o.-Runde, wie in _ko."""
    g = _groesse(n)
    return [(i, g - 1 - i) for i in _verzahnt(g // 2)]


def _banner_doppel(d: dict[str, Any], k: str | None) -> dict[str, Any]:
    if not k:
        return {"match_nr": None, "phase": None}
    for teil, phase in (("oben", "oben"), ("unten", "unten")):
        for r, runde in enumerate(d[teil]):
            for x in runde:
                if x["k"] == k:
                    echte = [y["k"] for y in runde if not y["freilos"]]
                    return {"match_nr": [r, (echte.index(k) + 1) if k in echte else 1, len(echte), len(d[teil])], "phase": phase}
    return {"match_nr": [0, 1, 1, 0], "phase": "entscheidung" if k == "f1" else "finale"}


def _banner_gruppen(gr: dict[str, Any], k: str | None) -> dict[str, Any]:
    if not k:
        return {"match_nr": None, "phase": None}
    if k.startswith("g"):
        gi = int(k[1:].split("-")[0])
        spiele = gr["gruppen"][gi]["spiele"]
        nr = next(i for i, x in enumerate(spiele) if x["k"] == k)
        return {"match_nr": [0, nr + 1, len(spiele), 0], "phase": "gruppe", "gruppe": chr(65 + gi)}
    return {"match_nr": _match_nr(gr["ko"], k), "phase": "ko"}


def _name(namen: list[str], i: int | None) -> str | None:
    """Name, "" für ein Freilos, None solange offen."""
    if i is None:
        return None
    return "" if i == FREI else namen[i]


def _match_nr(b: list[list[dict[str, Any]]], k: str) -> list[int]:
    """[Runde, Nummer des Matches in der Runde (ohne Freilose), Anzahl echter Matches, Runden gesamt]."""
    for r, runde in enumerate(b):
        keys = [x["k"] for x in runde]
        if k in keys:
            echte = [x["k"] for x in runde if not x["freilos"]]
            return [r, (echte.index(k) + 1) if k in echte else 1, len(echte), len(b)]
    return [0, 1, 1, len(b)]
