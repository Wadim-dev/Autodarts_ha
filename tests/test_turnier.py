"""Knockout tournament: bracket, byes, next match, champion, undo."""

from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ServiceValidationError
import pytest

from custom_components.autodarts import turnier

from .test_ereignisse import _sammeln
from .test_spiel import SPIEL, _attr, _dienst, _spieler


def _t(namen: list[str], ergebnisse: dict[str, int] | None = None) -> dict:
    return {"id": "x", "teilnehmer": namen, "namen": namen, "ergebnisse": ergebnisse or {}}


def test_baum_mit_freilosen() -> None:
    t = _t(["A", "B", "C", "D", "E"])
    runden = turnier.baum(t)
    assert [len(r) for r in runden] == [4, 2, 1]
    freilose = [m for m in runden[0] if turnier.FREI in (m["a"], m["b"])]
    assert len(freilose) == 3
    # the top seeds get the byes and only meet in the final
    assert runden[0][0]["a"] == 0 and runden[0][0]["sieger"] is not None
    r, _m, a, b = turnier.naechstes(t)
    assert (r, {a, b}) == (0, {3, 4})
    assert turnier.champion(t) is None


def test_ansicht_und_champion() -> None:
    t = _t(["A", "B", "C"])
    r, m, a, b = turnier.naechstes(t)
    t["ergebnisse"][f"{r}-{m}"] = a
    r, m, a, b = turnier.naechstes(t)
    assert r == 1
    v = turnier.ansicht(t, (r, m))
    assert v["match_nr"][0] == 1 and v["match_nr"][3] == 2
    t["ergebnisse"][f"{r}-{m}"] = b
    assert turnier.naechstes(t) is None
    assert turnier.champion(t) == b
    assert turnier.ansicht(t, None)["sieger"] == t["namen"][b]


async def _highscore_match(hass: HomeAssistant, gewinner: int) -> None:
    """Both players throw one visit; the given one scores more."""
    for p in range(2):
        feld = "T20" if p == gewinner else "S1"
        for d in range(3):
            await _dienst(hass, "wurf_aendern", dart=d, feld=feld)
        if p == 0:
            await _dienst(hass, "weiter")


async def test_turnier_im_spiel(hass: HomeAssistant, geladen) -> None:
    anna, ben, cem = await _spieler(hass, "Anna", "Ben", "Cem")
    liste = _sammeln(geladen)
    with pytest.raises(ServiceValidationError):
        await _dienst(hass, "turnier_starten", spieler=[anna, ben], spiel="highscore", runden=1)
    with pytest.raises(ServiceValidationError):
        await _dienst(hass, "turnier_weiter")
    await _dienst(hass, "turnier_starten", spieler=[anna, ben, cem], spiel="highscore", runden=1)
    tur = _attr(hass, "turnier")
    assert tur["match_nr"][:2] == [0, 1]
    namen = [s["name"] for s in _attr(hass, "spieler")]
    assert set(namen) == {"Ben", "Cem"}  # Anna has a bye
    await _highscore_match(hass, 1)
    assert hass.states.get(SPIEL).state == "finished"
    tur = _attr(hass, "turnier")
    assert tur["sieger"] is None and tur["naechstes"]
    # undo takes the result back, finishing again records it
    await _dienst(hass, "rueckgaengig")
    assert geladen.runtime_data.spiel.daten["turnier"]["ergebnisse"] == {}
    await _dienst(hass, "wurf_aendern", dart=2, feld="T20")
    assert geladen.runtime_data.spiel.daten["turnier"]["ergebnisse"]
    # final: Anna against the winner, the tournament settings are kept
    await _dienst(hass, "turnier_weiter")
    assert "Anna" in [s["name"] for s in _attr(hass, "spieler")]
    assert _attr(hass, "art") == "highscore"
    await _highscore_match(hass, 0)
    tur = _attr(hass, "turnier")
    assert tur["sieger"] == _attr(hass, "spieler")[0]["name"]
    assert ("tournament_won", {"player": tur["sieger"]}) in liste
    with pytest.raises(ServiceValidationError):
        await _dienst(hass, "turnier_weiter")
    # the last single-game settings are untouched by tournament matches
    assert len(geladen.runtime_data.spiel.daten["letzte"]["spieler"]) == 3
    await _dienst(hass, "turnier_abbrechen")
    assert "turnier" not in hass.states.get(SPIEL).attributes


def test_32_spieler_ko() -> None:
    t = _t([f"S{i}" for i in range(32)])
    b = turnier.baum(t)
    assert len(b) == 5 and len(b[0]) == 16 and not any(x["freilos"] for x in b[0])
    assert turnier.naechstes(t)[:2] == (0, 0)


def test_liga_spielplan_und_tabelle() -> None:
    for n in range(3, turnier.LIGA_MAX + 1):
        paare = [tuple(sorted(p)) for runde in turnier.liga_runden(n) for p in runde]
        assert len(paare) == n * (n - 1) // 2 == len(set(paare))
    t = {**_t(["A", "B", "C"]), "modus": "liga"}
    spiele = [p for runde in turnier.liga_runden(3) for p in runde]
    assert turnier.champion(t) is None
    for r, runde in enumerate(turnier.liga_runden(3)):
        for m, (a, b) in enumerate(runde):
            sieger = min(a, b) if 2 not in (a, b) else 2  # C wins everything, then A beats B
            t["ergebnisse"][f"{r}-{m}"] = sieger
            t.setdefault("legs", {})[f"{r}-{m}"] = [2, 1] if sieger == a else [0, 2]
    assert turnier.naechstes(t) is None and turnier.champion(t) == 2
    v = turnier.ansicht(t, None)
    assert v["modus"] == "liga" and v["sieger"] == "C" and len(v["spiele"]) == len(spiele) == 3
    assert [z["name"] for z in v["tabelle"]] == ["C", "A", "B"] and v["tabelle"][0]["punkte"] == 4


async def test_liga_im_spiel(hass: HomeAssistant, geladen) -> None:
    anna, ben, cem = await _spieler(hass, "Anna", "Ben", "Cem")
    await _dienst(hass, "turnier_starten", spieler=[anna, ben, cem], spiel="highscore", runden=1, turnier_modus="liga")
    tur = _attr(hass, "turnier")
    assert tur["modus"] == "liga" and tur["match_nr"][1:3] == [1, 3]
    await _highscore_match(hass, 0)
    assert geladen.runtime_data.spiel.daten["turnier"]["legs"]["0-0"] == [1, 0]
    tur = _attr(hass, "turnier")
    assert tur["tabelle"][0]["siege"] == 1 and tur["naechstes"]
    await _dienst(hass, "turnier_abbrechen")
    zehn = [x for x in await _spieler(hass, *[f"P{i}" for i in range(8)])] + [anna, ben, cem]
    with pytest.raises(ServiceValidationError):
        await _dienst(hass, "turnier_starten", spieler=zehn, spiel="highscore", runden=1, turnier_modus="liga")


def _durchspielen(t: dict, wahl) -> list[tuple[str, int, int, int]]:
    """Plays every match (wahl picks the winner) and returns (key, a, b, winner)."""
    gespielt = []
    for _ in range(500):
        n = turnier.naechstes_match(t)
        if n is None:
            break
        k, a, b = n
        assert a != b
        s = wahl(k, a, b)
        t["ergebnisse"][k] = s
        gespielt.append((k, a, b, s))
    return gespielt


@pytest.mark.parametrize("n", range(3, 17))
@pytest.mark.parametrize("glueck", [0, 1, 2])
def test_doppel_ko_vollstaendig(n: int, glueck: int) -> None:
    import random

    zufall = random.Random(n * 10 + glueck)
    namen = [f"P{i}" for i in range(n)]
    t = {**_t(namen), "modus": "doppel_ko"}
    # glueck 0: better seed always wins, 1: worse seed wins, 2: random
    gespielt = _durchspielen(t, lambda k, a, b: min(a, b) if glueck == 0 else max(a, b) if glueck == 1 else zufall.choice([a, b]))
    ch = turnier.champion(t)
    assert ch is not None
    niederlagen = {i: 0 for i in range(n)}
    for _k, a, b, s in gespielt:
        niederlagen[b if s == a else a] += 1
    # everyone but the champion is out after exactly two defeats, the champion has at most one
    assert niederlagen[ch] <= 1
    assert all(v == 2 for i, v in niederlagen.items() if i != ch)
    assert len(gespielt) in (2 * n - 2, 2 * n - 1)
    if glueck == 0:
        assert ch == 0
    v = turnier.ansicht(t, None)
    assert v["sieger"] == namen[ch] and v["naechstes"] is None
    assert v["unten"] and v["finale"]


def test_doppel_ko_entscheidungsspiel() -> None:
    t = {**_t(["A", "B", "C", "D"]), "modus": "doppel_ko"}
    # A wins the winners bracket, B comes through the losers bracket and beats A in the final
    gespielt = _durchspielen(t, lambda k, a, b: min(a, b) if k.startswith("w") or 1 not in (a, b) else 1)
    keys = [g[0] for g in gespielt]
    assert keys[-2:] == ["f0", "f1"]
    assert turnier.champion(t) == 1
    v = turnier.ansicht(t, "f1")
    assert v["phase"] == "entscheidung" and len(v["finale"]) == 2


@pytest.mark.parametrize("n", [6, 7, 9, 11, 12, 16, 23, 24, 32])
def test_gruppen_vollstaendig(n: int) -> None:
    namen = [f"P{i}" for i in range(n)]
    t = {**_t(namen), "modus": "gruppen"}
    einteilung = turnier.gruppen_einteilung(n)
    assert sorted(i for g in einteilung for i in g) == list(range(n))
    assert all(3 <= len(g) <= 6 for g in einteilung)
    assert max(len(g) for g in einteilung) - min(len(g) for g in einteilung) <= 1
    v = turnier.ansicht(t, None)
    assert v["runden"][0][0]["pa"].startswith("1 ")  # places before the groups are done
    gespielt = _durchspielen(t, lambda k, a, b: min(a, b))
    g = len(einteilung)
    gruppenspiele = sum(len(x) * (len(x) - 1) // 2 for x in einteilung)
    assert len(gespielt) == gruppenspiele + 2 * g - 1
    # group winners never meet their own runner-up in the first knockout round
    erste = [x for x in gespielt if x[0].startswith("k0-")]
    gruppe_von = {i: gi for gi, x in enumerate(einteilung) for i in x}
    assert all(gruppe_von[a] != gruppe_von[b] for _k, a, b, _s in erste)
    assert turnier.champion(t) == 0
    v = turnier.ansicht(t, None)
    assert len(v["gruppen"]) == g and v["sieger"] == "P0"


def test_gruppen_banner() -> None:
    t = {**_t([f"P{i}" for i in range(6)]), "modus": "gruppen"}
    k, _a, _b = turnier.naechstes_match(t)
    v = turnier.ansicht(t, k)
    assert v["phase"] == "gruppe" and v["gruppe"] == "A" and v["match_nr"][1:3] == [1, 3]
