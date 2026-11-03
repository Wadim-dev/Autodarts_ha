"""Spielarten neben X01: Cricket, Training und Partyspiele (ohne Home Assistant).

Wie bei X01 wird ein Spiel nur als Liste von Aufnahmen gespeichert. `auswerten`
spielt alle Aufnahmen jedes Mal neu durch; jede Spielart beschreibt dabei nur, was
ein Dart und das Ende einer Aufnahme bewirken. Ergebnis hat dieselbe Form wie
`x01.auswerten`, dazu Felder für die Karte (Ziel, Marks, Leben …).
"""

from __future__ import annotations

import random
from typing import Any

from . import x01

GRUPPEN = {
    "x01": "x01",
    "cricket": "cricket",
    "atc": "training", "bobs27": "training", "doppel": "training", "checkout121": "training", "highscore": "training",
    "shanghai": "party", "killer": "party", "halve_it": "party", "golf": "party", "baseball": "party",
}
CRICKET_VARIANTEN = ("standard", "cut_throat", "no_score")
CRICKET_ZAHLEN = ("classic", "tactics", "random")
ATC_VARIANTEN = ("single", "double", "triple")
HALVE_IT = ["15", "16", "D", "17", "18", "T", "19", "20", "B"]


def zahl_faktor(f: str) -> tuple[int, int]:
    """(Zahl, Faktor) eines Felds: T20 → (20, 3), D25 → (25, 2), M → (0, 0)."""
    if not f or f == "M":
        return 0, 0
    return int(f[1:]), x01.FAKTOR[f[0]]


class Art:
    """Grundgerüst einer Spielart; Unterklassen überschreiben nur, was sie brauchen."""

    runden: int = 0  # 0 = ohne Rundenende
    rest_als_miss = True  # Weiter mit weniger als 3 Darts: fehlende zählen als Fehlwurf
    mehr_ist_besser = True

    def __init__(self, e: dict[str, Any], n: int, seed: str) -> None:
        self.e = e
        self.n = n
        self.zufall = random.Random(seed)
        self.tags: list[str] = []
        self.visit_punkte = 0
        self.score = [0] * n
        self.runde = [0] * n
        self.raus = [False] * n
        self.fertig = [False] * n

    # Ablauf
    def leg_start(self) -> None:
        self.score = [self.startwert()] * self.n
        self.runde = [0] * self.n
        self.raus = [False] * self.n
        self.fertig = [False] * self.n

    def startwert(self) -> int:
        return 0

    def aktiv(self, p: int) -> bool:
        return not self.raus[p] and not self.fertig[p]

    def visit_start(self, p: int) -> None:
        self.tags = []
        self.visit_punkte = 0

    def dart(self, p: int, f: str, k: int) -> bool:
        """Dart k (0–2) auf Feld f. True = Aufnahme ist sofort vorbei (Sieg, raus …)."""
        return False

    def visit_ende(self, p: int, felder: list[str]) -> None:
        self.runde[p] += 1
        if self.runden and self.runde[p] >= self.runden:
            self.fertig[p] = True

    def sieger(self) -> int | None:
        """Gewinner des Legs, sobald er feststeht."""
        if self.runden and all(self.fertig[p] or self.raus[p] for p in range(self.n)):
            return self.bester()
        return None

    def bester(self) -> int:
        reihe = sorted(range(self.n), key=lambda p: (self.raus[p], -self.score[p] if self.mehr_ist_besser else self.score[p], p))
        return reihe[0]

    # Anzeige
    def ziel(self, p: int) -> str | None:
        return None

    def extra(self, p: int) -> dict[str, Any]:
        return {}

    def bot_ziel(self, p: int, uebrig: int) -> str:
        z = self.ziel(p)
        return z if z and z[0] in "SDT" else "T20"

    def zielzahl(self, p: int) -> int:
        return self.runde[p] + 1


# ---------- Cricket ----------

class Cricket(Art):
    def __init__(self, e: dict[str, Any], n: int, seed: str) -> None:
        super().__init__(e, n, seed)
        self.variante = e.get("variante") if e.get("variante") in CRICKET_VARIANTEN else "standard"
        art = e.get("zahlen") if e.get("zahlen") in CRICKET_ZAHLEN else "classic"
        if art == "tactics":
            self.zahlen = [*range(20, 9, -1), 25]
        elif art == "random":
            self.zahlen = [*sorted(random.Random(seed).sample(range(1, 21), 6), reverse=True), 25]
        else:
            self.zahlen = [*range(20, 14, -1), 25]
        self.mehr_ist_besser = self.variante != "cut_throat"
        self.marks: list[dict[int, int]] = []

    def leg_start(self) -> None:
        super().leg_start()
        self.marks = [dict.fromkeys(self.zahlen, 0) for _ in range(self.n)]

    def visit_start(self, p: int) -> None:
        super().visit_start(p)
        self.visit_marks = 0

    def offen_fuer(self, zahl: int, ausser: int) -> list[int]:
        return [q for q in range(self.n) if q != ausser and self.marks[q][zahl] < 3]

    def dart(self, p: int, f: str, k: int) -> bool:
        zahl, fak = zahl_faktor(f)
        if zahl not in self.marks[p]:
            return False
        vorher = self.marks[p][zahl]
        self.marks[p][zahl] = min(3, vorher + fak)
        ueber = vorher + fak - 3 if vorher + fak > 3 else 0
        if vorher + fak <= 3 or (self.variante != "no_score" and self.offen_fuer(zahl, p)):
            self.visit_marks += fak
        else:
            self.visit_marks += 3 - vorher
        if vorher < 3 <= vorher + fak:
            self.tags.append(f"zu:{zahl}")
        if ueber and self.variante != "no_score":
            punkte = ueber * zahl
            if self.variante == "cut_throat":
                for q in self.offen_fuer(zahl, p):
                    self.score[q] += punkte
                    self.visit_punkte += punkte
            elif self.offen_fuer(zahl, p):
                self.score[p] += punkte
                self.visit_punkte += punkte
        return self.sieger() is not None

    def visit_ende(self, p: int, felder: list[str]) -> None:
        self.runde[p] += 1
        if self.visit_marks >= 9:
            self.tags.append("nine_marks")
        elif self.visit_marks >= 6:
            self.tags.append("six_marks")

    def alle_zu(self, p: int) -> bool:
        return all(m >= 3 for m in self.marks[p].values())

    def sieger(self) -> int | None:
        for p in range(self.n):
            if not self.alle_zu(p):
                continue
            andere = [self.score[q] for q in range(self.n) if q != p]
            if self.variante == "no_score" or not andere:
                return p
            if self.variante == "cut_throat" and self.score[p] <= min(andere):
                return p
            if self.variante == "standard" and self.score[p] >= max(andere):
                return p
        return None

    def extra(self, p: int) -> dict[str, Any]:
        return {"marks": [self.marks[p][z] for z in self.zahlen]}

    def bot_ziel(self, p: int, uebrig: int) -> str:
        eigene = [z for z in self.zahlen if self.marks[p][z] < 3]
        andere = [self.score[q] for q in range(self.n) if q != p]
        hinten = bool(andere) and (self.score[p] < max(andere) if self.variante == "standard" else self.score[p] > min(andere))
        if hinten and self.variante != "no_score":
            punkten = [z for z in self.zahlen if self.marks[p][z] >= 3 and self.offen_fuer(z, p)]
            if punkten:
                return _ziel_feld(punkten[0])
        if eigene:
            return _ziel_feld(eigene[0])
        return _ziel_feld(self.zahlen[0])


def _ziel_feld(zahl: int) -> str:
    return "D25" if zahl == 25 else f"T{zahl}"


# ---------- Training ----------

class RundT(Art):
    """Rund um die Uhr: 1–20, dann Bull. Erster am Ziel gewinnt."""

    def __init__(self, e: dict[str, Any], n: int, seed: str) -> None:
        super().__init__(e, n, seed)
        self.bereich = str(e.get("variante")) if e.get("variante") in ATC_VARIANTEN else "single"
        self.folge = [*range(1, 21), 25]

    def startwert(self) -> int:
        return 1

    def ziel(self, p: int) -> str | None:
        if self.fertig[p]:
            return None
        zahl = self.score[p]
        if zahl == 25:
            return "S25" if self.bereich == "single" else "D25"
        return {"single": "S", "double": "D", "triple": "T"}[self.bereich] + str(zahl)

    def dart(self, p: int, f: str, k: int) -> bool:
        zahl, fak = zahl_faktor(f)
        if zahl != self.score[p] or not fak:
            return False
        if zahl != 25 and ((self.bereich == "double" and fak != 2) or (self.bereich == "triple" and fak != 3)):
            return False
        if zahl == 25 and self.bereich != "single" and fak != 2:
            return False
        self.visit_punkte += 1
        i = self.folge.index(zahl)
        if i == len(self.folge) - 1:
            self.fertig[p] = True
            self.tags.append("geschafft")
            return True
        self.score[p] = self.folge[i + 1]
        return False

    def visit_ende(self, p: int, felder: list[str]) -> None:
        self.runde[p] += 1

    def sieger(self) -> int | None:
        return next((p for p in range(self.n) if self.fertig[p]), None)

    def bot_ziel(self, p: int, uebrig: int) -> str:
        z = self.ziel(p) or "S20"
        return "D25" if z == "S25" else z


class Bobs27(Art):
    """Bob's 27: je drei Darts auf D1 … D20 und Bull; Treffer bringen das Doppelte, null Treffer kosten es."""

    runden = 21

    def startwert(self) -> int:
        return 27

    def zielzahl(self, p: int) -> int:
        return 25 if self.runde[p] >= 20 else self.runde[p] + 1

    def ziel(self, p: int) -> str | None:
        return None if self.fertig[p] or self.raus[p] else f"D{self.zielzahl(p)}"

    def visit_start(self, p: int) -> None:
        super().visit_start(p)
        self.treffer = 0

    def dart(self, p: int, f: str, k: int) -> bool:
        if f == self.ziel(p):
            self.treffer += 1
            self.visit_punkte += 2 * self.zielzahl(p)
        return False

    def visit_ende(self, p: int, felder: list[str]) -> None:
        wert = 2 * self.zielzahl(p)
        if self.treffer:
            self.score[p] += self.visit_punkte
        else:
            self.score[p] -= wert
            self.visit_punkte = -wert
        if self.score[p] < 0:
            self.raus[p] = True
            self.tags.append("raus")
        super().visit_ende(p, felder)

    def sieger(self) -> int | None:
        if all(self.fertig[p] or self.raus[p] for p in range(self.n)):
            # alle raus: wer am weitesten kam
            if all(self.raus):
                return max(range(self.n), key=lambda p: (self.runde[p], self.score[p]))
            return self.bester()
        return None


class Doppel(Bobs27):
    """Doppel-Training: je drei Darts auf D1 … D20 und Bull, jeder Treffer zählt einen Punkt."""

    def startwert(self) -> int:
        return 0

    def dart(self, p: int, f: str, k: int) -> bool:
        if f == self.ziel(p):
            self.treffer += 1
            self.visit_punkte += 1
        return False

    def visit_ende(self, p: int, felder: list[str]) -> None:
        self.score[p] += self.visit_punkte
        Art.visit_ende(self, p, felder)


class Checkout121(Art):
    """121: drei Aufnahmen für einen Checkout (Double Out). Geschafft → Ziel +1, sonst −1 (nicht unter 121)."""

    def __init__(self, e: dict[str, Any], n: int, seed: str) -> None:
        super().__init__(e, n, seed)
        self.runden = int(e.get("runden") or 10)
        self.start = 121

    def leg_start(self) -> None:
        super().leg_start()
        self.zielwert = [self.start] * self.n
        self.rest = [self.start] * self.n
        self.versuch_aufn = [0] * self.n
        self.bestes = [0] * self.n
        self.treffer_n = [0] * self.n
        self.score = list(self.rest)

    def startwert(self) -> int:
        return 0

    def visit_start(self, p: int) -> None:
        super().visit_start(p)
        self.rest_vor = self.rest[p]
        self.geschafft = False
        self.bust = False

    def dart(self, p: int, f: str, k: int) -> bool:
        if self.geschafft or self.bust:
            return True
        pkt, fak = x01.wert(f)
        neu = self.rest[p] - pkt
        if neu < 0 or neu == 1 or (neu == 0 and fak != 2):
            self.bust = True
            self.rest[p] = self.score[p] = self.rest_vor
            self.visit_punkte = 0
            return True
        self.rest[p] = neu
        self.score[p] = neu
        self.visit_punkte += pkt
        if neu == 0:
            self.geschafft = True
            return True
        return False

    def visit_ende(self, p: int, felder: list[str]) -> None:
        self.versuch_aufn[p] += 1
        if self.bust:
            self.tags.append("bust")
        if self.geschafft or self.versuch_aufn[p] >= 3:
            if self.geschafft:
                self.tags.append("check")
                self.treffer_n[p] += 1
                self.bestes[p] = max(self.bestes[p], self.zielwert[p])
                self.zielwert[p] += 1
            else:
                self.tags.append("verfehlt")
                self.zielwert[p] = max(self.start, self.zielwert[p] - 1)
            self.rest[p] = self.zielwert[p]
            self.versuch_aufn[p] = 0
            self.runde[p] += 1
            if self.runde[p] >= self.runden:
                self.fertig[p] = True
        self.score[p] = self.rest[p]

    def bester(self) -> int:
        return max(range(self.n), key=lambda p: (self.treffer_n[p], self.bestes[p], -p))

    def extra(self, p: int) -> dict[str, Any]:
        return {"zielwert": self.zielwert[p], "versuch": self.versuch_aufn[p] + 1, "bestes": self.bestes[p], "geschafft": self.treffer_n[p],
                "weg": x01.weg(self.rest[p], 3, "double")}

    def bot_ziel(self, p: int, uebrig: int) -> str:
        return x01.bot_ziel(self.rest[p], uebrig, True, "straight", "double")


class Highscore(Art):
    """Highscore: in N Aufnahmen so viele Punkte wie möglich."""

    def __init__(self, e: dict[str, Any], n: int, seed: str) -> None:
        super().__init__(e, n, seed)
        self.runden = int(e.get("runden") or 10)

    def dart(self, p: int, f: str, k: int) -> bool:
        pkt = x01.wert(f)[0]
        self.score[p] += pkt
        self.visit_punkte += pkt
        return False


# ---------- Partyspiele ----------

class Shanghai(Art):
    """Shanghai: Runde n zählt nur die Zahl n. Single, Double und Triple in einer Aufnahme gewinnt sofort."""

    def __init__(self, e: dict[str, Any], n: int, seed: str) -> None:
        super().__init__(e, n, seed)
        self.runden = 20 if int(e.get("runden") or 7) >= 20 else 7

    def ziel(self, p: int) -> str | None:
        return None if self.fertig[p] else str(self.zielzahl(p))

    def visit_start(self, p: int) -> None:
        super().visit_start(p)
        self.arten: set[int] = set()
        self.shanghai: int | None = None

    def dart(self, p: int, f: str, k: int) -> bool:
        zahl, fak = zahl_faktor(f)
        if zahl != self.zielzahl(p):
            return False
        self.score[p] += zahl * fak
        self.visit_punkte += zahl * fak
        self.arten.add(fak)
        if self.arten == {1, 2, 3}:
            self.shanghai = p
            self.tags.append("shanghai")
            return True
        return False

    def sieger(self) -> int | None:
        if self.shanghai is not None:
            return self.shanghai
        return super().sieger()

    def leg_start(self) -> None:
        super().leg_start()
        self.shanghai = None

    def bot_ziel(self, p: int, uebrig: int) -> str:
        z = self.zielzahl(p)
        fehlt = {1, 2, 3} - self.arten
        fak = 3 if 3 in fehlt else (2 if 2 in fehlt else 1)
        return {1: "S", 2: "D", 3: "T"}[fak] + str(z)


class HalveIt(Art):
    """Halve-It: 15, 16, ein Double, 17, 18, ein Triple, 19, 20, Bull. Kein Treffer halbiert den Stand."""

    runden = len(HALVE_IT)

    def startwert(self) -> int:
        return 40

    def ziel(self, p: int) -> str | None:
        return None if self.fertig[p] else HALVE_IT[self.runde[p]]

    def visit_start(self, p: int) -> None:
        super().visit_start(p)
        self.getroffen = False

    def dart(self, p: int, f: str, k: int) -> bool:
        z = self.ziel(p)
        zahl, fak = zahl_faktor(f)
        if not fak:
            return False
        ok = (z == "D" and fak == 2) or (z == "T" and fak == 3) or (z == "B" and zahl == 25) or (z not in ("D", "T", "B") and str(zahl) == z)
        if ok:
            self.getroffen = True
            self.visit_punkte += zahl * fak
        return False

    def visit_ende(self, p: int, felder: list[str]) -> None:
        if self.getroffen:
            self.score[p] += self.visit_punkte
        else:
            alt = self.score[p]
            self.score[p] = alt // 2
            self.visit_punkte = self.score[p] - alt
            self.tags.append("halbiert")
        super().visit_ende(p, felder)

    def bot_ziel(self, p: int, uebrig: int) -> str:
        z = self.ziel(p) or "20"
        return {"D": "D20", "T": "T20", "B": "D25"}.get(z, "T" + z)


class Killer(Art):
    """Killer: Triff dein Double, um Killer zu werden; dann kostet dein Treffer auf ein fremdes Double ein Leben."""

    def __init__(self, e: dict[str, Any], n: int, seed: str) -> None:
        super().__init__(e, n, seed)
        self.leben_start = max(1, min(int(e.get("leben") or 3), 9))
        self.nummer = random.Random(seed).sample(range(1, 21), n)

    def leg_start(self) -> None:
        super().leg_start()
        self.leben = [self.leben_start] * self.n
        self.killer = [False] * self.n
        self.score = list(self.leben)

    def ziel(self, p: int) -> str | None:
        return None if self.killer[p] else f"D{self.nummer[p]}"

    def dart(self, p: int, f: str, k: int) -> bool:
        zahl, fak = zahl_faktor(f)
        if fak != 2 or zahl == 25:
            return False
        if zahl == self.nummer[p]:
            if not self.killer[p]:
                self.killer[p] = True
                self.tags.append("killer")
            else:
                self._treffer(p)
        else:
            q = next((q for q in range(self.n) if self.nummer[q] == zahl and not self.raus[q]), None)
            if q is not None and self.killer[p]:
                self._treffer(q)
                self.visit_punkte += 1
        if self.raus[p]:
            return True
        return self.sieger() is not None

    def _treffer(self, q: int) -> None:
        self.leben[q] -= 1
        self.score[q] = self.leben[q]
        self.tags.append(f"leben:{q}")
        if self.leben[q] <= 0:
            self.raus[q] = True
            self.tags.append(f"raus:{q}")

    def sieger(self) -> int | None:
        drin = [p for p in range(self.n) if not self.raus[p]]
        if len(drin) == 1 and self.n > 1:
            return drin[0]
        if self.n == 1 and self.raus[0]:
            return 0
        return None

    def extra(self, p: int) -> dict[str, Any]:
        return {"nummer": self.nummer[p], "leben": self.leben[p], "killer": self.killer[p]}

    def bot_ziel(self, p: int, uebrig: int) -> str:
        if not self.killer[p]:
            return f"D{self.nummer[p]}"
        opfer = [q for q in range(self.n) if q != p and not self.raus[q]]
        if not opfer:
            return "S20"
        q = min(opfer, key=lambda q: (self.leben[q], q))
        return f"D{self.nummer[q]}"


class Golf(Art):
    """Darts-Golf: Loch n = Zahl n. Der letzte Dart zählt: Triple 1, Double 2, Single 3, daneben 5. Wenigste Schläge gewinnen."""

    rest_als_miss = False
    mehr_ist_besser = False

    def __init__(self, e: dict[str, Any], n: int, seed: str) -> None:
        super().__init__(e, n, seed)
        self.runden = 18 if int(e.get("runden") or 9) >= 18 else 9

    def ziel(self, p: int) -> str | None:
        return None if self.fertig[p] else str(self.zielzahl(p))

    def schlaege(self, p: int, f: str) -> int:
        zahl, fak = zahl_faktor(f)
        return {3: 1, 2: 2, 1: 3}[fak] if zahl == self.zielzahl(p) else 5

    def dart(self, p: int, f: str, k: int) -> bool:
        self.visit_punkte = self.schlaege(p, f)
        if k == 0 and self.visit_punkte == 1:
            self.tags.append("hole_in_one")
        return False

    def visit_ende(self, p: int, felder: list[str]) -> None:
        if not felder:
            self.visit_punkte = 5
        self.score[p] += self.visit_punkte
        super().visit_ende(p, felder)

    def bot_ziel(self, p: int, uebrig: int) -> str:
        if uebrig < 3 and self.visit_punkte <= 2:
            return ""  # stehen bleiben
        return f"T{self.zielzahl(p)}"


class Baseball(Art):
    """Baseball: Inning n = Zahl n. Single 1, Double 2, Triple 3 Runs."""

    runden = 9

    def ziel(self, p: int) -> str | None:
        return None if self.fertig[p] else str(self.zielzahl(p))

    def dart(self, p: int, f: str, k: int) -> bool:
        zahl, fak = zahl_faktor(f)
        if zahl == self.zielzahl(p):
            self.score[p] += fak
            self.visit_punkte += fak
        return False

    def visit_ende(self, p: int, felder: list[str]) -> None:
        if self.visit_punkte >= 6:
            self.tags.append("home_run")
        super().visit_ende(p, felder)

    def bot_ziel(self, p: int, uebrig: int) -> str:
        return f"T{self.zielzahl(p)}"


ARTEN: dict[str, type[Art]] = {
    "cricket": Cricket, "atc": RundT, "bobs27": Bobs27, "doppel": Doppel, "checkout121": Checkout121,
    "highscore": Highscore, "shanghai": Shanghai, "killer": Killer, "halve_it": HalveIt, "golf": Golf, "baseball": Baseball,
}


def _leer_stat() -> dict[str, Any]:
    return {"darts": 0, "aufnahmen": 0, "punkte": 0, "marks": 0, "hoechste": 0, "legs": 0}


def auswerten(spiel: dict[str, Any]) -> dict[str, Any]:
    """Spielstand jeder Spielart (X01 rechnet x01.auswerten)."""
    e = spiel["einstellungen"]
    art_id = e.get("spiel") or "x01"
    if art_id not in ARTEN:
        stand = x01.auswerten(spiel)
        stand["art"] = "x01"
        return stand
    spieler = spiel["spieler"]
    n = len(spieler)
    reihe = spiel.get("reihenfolge") or list(range(n))
    legs_ziel = max(1, int(e.get("legs") or 1))
    art = ARTEN[art_id](e, n, str(spiel.get("id") or ""))
    art.leg_start()
    st = [_leer_stat() for _ in range(n)]
    legs = [0] * n
    leg_darts = [0] * n
    letzte: list[Any] = [None] * n
    leg_nr = 0
    gewinner = leg_gewinner = None
    verlauf: list[dict[str, Any]] = []
    aktuell: dict[str, Any] | None = None
    ansage = ansage_id = ""
    aufnahmen = spiel.get("aufnahmen") or []

    def naechster(z: int) -> int:
        for k in range(n):
            if art.aktiv(reihe[(z + k) % n]):
                return z + k
        return z

    zug = naechster(0)
    for i, aufn in enumerate(aufnahmen):
        p = reihe[zug % n]
        art.visit_start(p)
        felder: list[str] = []
        stopp = False
        for k, dart in enumerate(aufn["d"][:3]):
            felder.append(dart["f"])
            if art.dart(p, dart["f"], k):
                stopp = True
                break
        zu = bool(aufn.get("zu"))
        fertig = zu or stopp or len(felder) >= 3
        gezaehlt = len(felder) if (stopp or not art.rest_als_miss) else (3 if zu else len(felder))
        if fertig:
            art.visit_ende(p, felder)
        s = st[p]
        s["darts"] += gezaehlt
        leg_darts[p] += gezaehlt
        if isinstance(art, Cricket):
            vm = art.visit_marks
        else:
            vm = 0
        sieg = art.sieger() if fertig else None
        if fertig:
            s["aufnahmen"] += 1
            s["marks"] += vm
            s["hoechste"] = max(s["hoechste"], art.visit_punkte)
            letzte[p] = art.visit_punkte
            ansage = f"{vm} Marks" if isinstance(art, Cricket) and vm else str(art.visit_punkte)
            ansage_id = str(i)
        z = {"i": i, "s": p, "d": [d["f"] for d in aufn["d"][:3]], "p": art.visit_punkte, "r": art.score[p],
             "b": any(t.startswith("raus") or t in ("halbiert", "bust") for t in art.tags), "c": sieg is not None, "x": list(art.tags)}
        if isinstance(art, Cricket):
            z["m"] = vm
        verlauf.append(z)
        if i == len(aufnahmen) - 1:
            aktuell = {"darts": aufn["d"][:3], "summe": art.visit_punkte, "bust": False, "checkout": sieg is not None, "rest_vor": art.score[p], "fertig": fertig}
        if sieg is not None:
            legs[sieg] += 1
            st[sieg]["legs"] += 1
            ansage = f"Leg {spieler[sieg]['name']}"
            if legs[sieg] >= legs_ziel:
                gewinner = sieg
                ansage = f"Spiel {spieler[sieg]['name']}"
                break
            if not zu:
                leg_gewinner = sieg
                break
            leg_nr += 1
            art.leg_start()
            leg_darts = [0] * n
            letzte = [None] * n
            zug = naechster(leg_nr)
            aktuell = None
            continue
        if zu:
            zug = naechster(zug + 1)
            aktuell = None

    am_zug = gewinner if gewinner is not None else (leg_gewinner if leg_gewinner is not None else reihe[zug % n])
    if aktuell is None:
        art.visit_start(am_zug)
        aktuell = {"darts": [], "summe": 0, "bust": False, "checkout": False, "rest_vor": art.score[am_zug], "fertig": False}
    uebrig = 3 - len(aktuell["darts"])
    laeuft = gewinner is None and leg_gewinner is None and not aktuell["fertig"]
    sp = []
    for k in range(n):
        s = st[k]
        if isinstance(art, Cricket):
            avg = round(s["marks"] / s["darts"] * 3, 2) if s["darts"] else 0
        else:
            avg = round(sum(v["p"] for v in verlauf if v["s"] == k and v["p"] > 0) / max(1, s["aufnahmen"]), 1)
        sp.append({
            "name": spieler[k]["name"], "bot": spieler[k].get("bot"), "rest": art.score[k], "legs": legs[k], "sets": 0,
            "offen": True, "avg": avg, "darts": s["darts"], "leg_darts": leg_darts[k], "letzte": letzte[k],
            "runde": art.runde[k], "raus": art.raus[k], "fertig": art.fertig[k], "ziel": art.ziel(k),
            "versuche": 0, "treffer": 0, "quote": 0, "hoechste": s["hoechste"], "finish": 0, "n180": 0, "n140": 0, "n100": 0, "bestes_leg": 0,
            "weg": None, **art.extra(k),
        })
    weg = sp[am_zug].get("weg") if laeuft else None
    return {
        "art": art_id,
        "zahlen": getattr(art, "zahlen", None),
        "runden": art.runden,
        "am_zug": am_zug,
        "aufnahme": {**aktuell, "darts": [{"f": d["f"], "x": d.get("x"), "y": d.get("y")} for d in aktuell["darts"]]},
        "weg": weg,
        "ziel": art.ziel(am_zug) if laeuft else None,
        "spieler": sp,
        "statistik": st,
        "gewinner": gewinner,
        "leg_gewinner": leg_gewinner,
        "leg": leg_nr + 1,
        "set": 1,
        "verlauf": verlauf,
        "ansage": ansage,
        "ansage_id": ansage_id,
        "bot_ziel": art.bot_ziel(am_zug, uebrig) if laeuft else None,
    }
