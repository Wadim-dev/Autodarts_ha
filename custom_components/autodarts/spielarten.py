"""Spielarten neben X01: Cricket, Training und Partyspiele (ohne Home Assistant).

Wie bei X01 wird ein Spiel nur als Liste von Aufnahmen gespeichert. `auswerten`
spielt alle Aufnahmen jedes Mal neu durch; jede Spielart beschreibt dabei nur, was
ein Dart und das Ende einer Aufnahme bewirken. Ergebnis hat dieselbe Form wie
`x01.auswerten`, dazu Felder für die Karte (Ziel, Marks, Leben …).
"""

from __future__ import annotations

import random
from typing import Any, ClassVar

from . import x01

GRUPPEN = {
    "x01": "x01",
    "cricket": "cricket", "wild_mouse": "cricket", "mickey": "cricket",
    "atc": "training", "bobs27": "training", "doppel": "training", "checkout121": "training", "checkout": "training",
    "catch40": "training", "jdc": "training", "singles": "training",
    "shanghai": "party", "killer": "party", "halve_it": "party", "golf": "party", "baseball": "party", "highscore": "party",
    "bermuda": "party", "rtw": "party", "gotcha": "party", "nine_lives": "party", "football": "party", "scram": "party",
}
CRICKET_VARIANTEN = ("standard", "cut_throat", "no_score")
CRICKET_ZAHLEN = ("classic", "tactics", "random", "hidden")
ATC_VARIANTEN = ("single", "double", "triple")
HALVE_IT = ["15", "16", "D", "17", "18", "T", "19", "20", "B"]
MAX_STECHEN = 5  # danach gewinnt bei Gleichstand, wer zuerst geworfen hat


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
    stechen = False  # Gleichstand nach der letzten Runde: die Gleichen spielen Extra-Runden

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
        self.wer_wirft = -1  # wer gerade wirft und wie viele Darts er noch hat (für Checkout-Wege)
        self.noch_darts = 3

    def darts_frei(self, p: int) -> int:
        """Darts, die Spieler p in dieser Aufnahme noch hat (3, wenn er nicht dran ist)."""
        return self.noch_darts if p == self.wer_wirft else 3

    # Ablauf
    def leg_start(self) -> None:
        self.score = [self.startwert()] * self.n
        self.runde = [0] * self.n
        self.raus = [False] * self.n
        self.fertig = [False] * self.n
        self.limit = [self.runden] * self.n

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
        if self.runden and self.runde[p] >= self.limit[p]:
            self.fertig[p] = True

    def sieger(self) -> int | None:
        """Gewinner des Legs, sobald er feststeht."""
        if self.runden and all(self.fertig[p] or self.raus[p] for p in range(self.n)):
            if self.stechen and self.n > 1:
                b = self.bester()
                gleich = [q for q in range(self.n) if not self.raus[q] and self.score[q] == self.score[b]]
                if len(gleich) > 1 and self.runde[b] < self.runden + MAX_STECHEN:
                    for q in gleich:
                        self.fertig[q] = False
                        self.limit[q] = self.runde[q] + 1
                    self.tags.append("stechen")
                    return None
            return self.bester()
        return None

    def im_stechen(self, p: int) -> bool:
        return bool(self.runden) and self.runde[p] >= self.runden

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
        return self.runde[p] % 20 + 1


# ---------- Cricket ----------

class Cricket(Art):
    def __init__(self, e: dict[str, Any], n: int, seed: str) -> None:
        super().__init__(e, n, seed)
        self.variante = e.get("variante") if e.get("variante") in CRICKET_VARIANTEN else "standard"
        self.art = e.get("zahlen") if e.get("zahlen") in CRICKET_ZAHLEN else "classic"
        self.seed = seed
        self.leg_nr = 0
        if self.art == "tactics":
            self.zahlen: list[Any] = [*range(20, 9, -1), 25]
        elif self.art in ("random", "hidden"):
            self.zahlen = self._ziehen()
        else:
            self.zahlen = [*range(20, 14, -1), 25]
        self.mehr_ist_besser = self.variante != "cut_throat"
        self.marks: list[dict[Any, int]] = []
        self.verdeckt: set[Any] = set()

    def _ziehen(self) -> list[Any]:
        """Sechs Zufallszahlen und Bull; jedes Leg neu (das erste wie bisher aus der Spiel-ID)."""
        quelle = random.Random(self.seed if not self.leg_nr else f"{self.seed}:{self.leg_nr}")
        return [*sorted(quelle.sample(range(1, 21), 6), reverse=True), 25]

    def leg_start(self) -> None:
        super().leg_start()
        if self.art in ("random", "hidden") and self.marks:
            self.leg_nr += 1
            self.zahlen = self._ziehen()
        self.marks = [dict.fromkeys(self.zahlen, 0) for _ in range(self.n)]
        self.verdeckt = {z for z in self.zahlen if z != 25} if self.art == "hidden" else set()

    def visit_start(self, p: int) -> None:
        super().visit_start(p)
        self.visit_marks = 0

    def offen_fuer(self, zahl: Any, ausser: int) -> list[int]:
        return [q for q in range(self.n) if q != ausser and self.marks[q][zahl] < 3]

    def dart(self, p: int, f: str, k: int) -> bool:
        zahl, fak = zahl_faktor(f)
        if zahl not in self.marks[p]:
            return False
        if zahl in self.verdeckt:
            self.verdeckt.discard(zahl)
            self.tags.append(f"auf:{zahl}")
        return self._marken(p, zahl, fak)

    def _marken(self, p: int, zahl: Any, fak: int, wert: int | None = None) -> bool:
        """fak Marks auf ein Ziel; Überzählige bringen Punkte (wert je Mark, sonst die Zahl)."""
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
            punkte = ueber * (zahl if wert is None else wert)
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
        if self.verdeckt:
            sichtbar = [z for z in self.zahlen if z not in self.verdeckt and self.marks[p][z] < 3]
            if sichtbar:
                return _ziel_feld(sichtbar[0])
            gesehen = set(self.zahlen) - self.verdeckt
            raten = [z for z in range(20, 0, -1) if z not in gesehen]
            return _ziel_feld(raten[(sum(self.runde) * 7) % len(raten)])
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


class WildMouse(Cricket):
    """Wild Mouse: Cricket auf 20–15 und Bull plus Doubles, Triples und 3 in a Bed (je drei Marks).

    Ein Dart markiert zuerst seine eigene Zahl, solange sie für dich offen ist, sonst Doubles
    bzw. Triples, solange offen. Sonst punktet er auf einem geschlossenen Ziel, das ein Gegner
    noch offen hat. Drei Darts im selben Feld einer Aufnahme schließen 3 in a Bed sofort.
    """

    ZAHLEN: ClassVar[list[Any]] = [20, 19, 18, 17, 16, 15, "D", "T", "3B", 25]

    def __init__(self, e: dict[str, Any], n: int, seed: str) -> None:
        super().__init__({**e, "zahlen": "classic", "variante": self.variante_von(e)}, n, seed)
        self.dreier = e.get("variante") != "ohne_3b"
        self.zahlen = [z for z in self.ZAHLEN if self.dreier or z != "3B"]

    @staticmethod
    def variante_von(e: dict[str, Any]) -> str:
        return "standard"

    def visit_start(self, p: int) -> None:
        super().visit_start(p)
        self.felder: list[str] = []

    def dart(self, p: int, f: str, k: int) -> bool:
        self.felder.append(f)
        zahl, fak = zahl_faktor(f)
        m = self.marks[p]
        if fak:
            if zahl in m and m[zahl] < 3:
                self._marken(p, zahl, fak)
            elif fak == 2 and "D" in m and m["D"] < 3:
                self._marken(p, "D", 1)
            elif fak == 3 and "T" in m and m["T"] < 3:
                self._marken(p, "T", 1)
            elif zahl in m and self.offen_fuer(zahl, p):
                self._marken(p, zahl, fak)
            elif fak == 2 and "D" in m and self.offen_fuer("D", p):
                self._marken(p, "D", 1, wert=zahl * 2)
            elif fak == 3 and "T" in m and self.offen_fuer("T", p):
                self._marken(p, "T", 1, wert=zahl * 3)
        if self.dreier and k == 2 and fak and len(set(self.felder)) == 1:
            summe = sum(x01.wert(x)[0] for x in self.felder)
            if m["3B"] < 3:
                self._marken(p, "3B", 3)
            elif self.offen_fuer("3B", p):
                self._marken(p, "3B", 1, wert=summe)
        return self.sieger() is not None

    def bot_ziel(self, p: int, uebrig: int) -> str:
        m = self.marks[p]
        offen = [z for z in self.zahlen if m[z] < 3]
        if not offen and self.variante != "no_score":
            offen = [z for z in self.zahlen if self.offen_fuer(z, p)]
        z = offen[0] if offen else 20
        if z == "D":
            return "D20"
        if z in ("T", "3B"):
            return "T20"
        return _ziel_feld(int(z))


class MickeyMouse(WildMouse):
    """Mickey Mouse: wer zuerst 20–12, drei Doubles, drei Triples und Bull geschlossen hat, gewinnt. Ohne Punkte."""

    ZAHLEN: ClassVar[list[Any]] = [20, 19, 18, 17, 16, 15, 14, 13, 12, "D", "T", 25]

    @staticmethod
    def variante_von(e: dict[str, Any]) -> str:
        return "no_score"

    def __init__(self, e: dict[str, Any], n: int, seed: str) -> None:
        super().__init__({**e, "variante": "ohne_3b"}, n, seed)


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
                "weg": x01.weg(self.rest[p], self.darts_frei(p), "double")}

    def bot_ziel(self, p: int, uebrig: int) -> str:
        return x01.bot_ziel(self.rest[p], uebrig, True, "straight", "double")


class Highscore(Art):
    """Count-Up (früher Highscore): in N Aufnahmen so viele Punkte wie möglich."""

    stechen = True

    def __init__(self, e: dict[str, Any], n: int, seed: str) -> None:
        super().__init__(e, n, seed)
        self.runden = max(1, min(int(e.get("runden") or 8), 20))

    def dart(self, p: int, f: str, k: int) -> bool:
        pkt = x01.wert(f)[0]
        self.score[p] += pkt
        self.visit_punkte += pkt
        return False


BOGEY = {159, 162, 163, 165, 166, 168, 169}


class Catch40(Art):
    """Catch 40: 61 bis 100 auschecken (Double Out), je höchstens zwei Aufnahmen.

    Mit 2 Darts 3 Punkte, mit 3 Darts 2 (bei 99 auch 3), in der zweiten Aufnahme 1 Punkt.
    """

    runden = 40

    def leg_start(self) -> None:
        super().leg_start()
        self.nr = [0] * self.n
        self.rest = [61] * self.n
        self.aufn = [0] * self.n
        self.treffer_n = [0] * self.n

    def zielwert(self, p: int) -> int:
        return 61 + self.nr[p]

    def visit_start(self, p: int) -> None:
        super().visit_start(p)
        self.rest_vor = self.rest[p]
        self.geschafft = False
        self.bust = False
        self.darts = 0

    def dart(self, p: int, f: str, k: int) -> bool:
        if self.fertig[p]:
            return True
        self.darts += 1
        pkt, fak = x01.wert(f)
        neu = self.rest[p] - pkt
        if neu < 0 or neu == 1 or (neu == 0 and fak != 2):
            self.bust = True
            self.rest[p] = self.rest_vor
            return True
        self.rest[p] = neu
        if neu == 0:
            self.geschafft = True
            return True
        return False

    def punkte(self, p: int) -> int:
        if self.aufn[p] > 0:
            return 1
        if self.darts <= 2 or self.zielwert(p) == 99:
            return 3
        return 2

    def visit_ende(self, p: int, felder: list[str]) -> None:
        if self.bust:
            self.tags.append("bust")
        if self.geschafft:
            self.visit_punkte = self.punkte(p)
            self.score[p] += self.visit_punkte
            self.treffer_n[p] += 1
            self.tags.append("check")
            self._weiter(p)
        elif self.aufn[p] >= 1:
            self.tags.append("verfehlt")
            self._weiter(p)
        else:
            self.aufn[p] += 1

    def _weiter(self, p: int) -> None:
        self.nr[p] += 1
        self.runde[p] = self.nr[p]
        self.aufn[p] = 0
        if self.nr[p] >= self.runden:
            self.fertig[p] = True
        else:
            self.rest[p] = self.zielwert(p)

    def extra(self, p: int) -> dict[str, Any]:
        return {"zielwert": self.zielwert(p) if not self.fertig[p] else None, "restwert": self.rest[p], "versuch": self.aufn[p] + 1,
                "versuche_max": 2, "geschafft": self.treffer_n[p], "weg": None if self.fertig[p] else x01.weg(self.rest[p], self.darts_frei(p), "double")}

    def bot_ziel(self, p: int, uebrig: int) -> str:
        return x01.bot_ziel(self.rest[p], uebrig, True, "straight", "double")


class CheckoutTraining(Checkout121):
    """Checkout-Training: zufällige Finishes von 2 bis 170, je drei Aufnahmen (Double Out). Die meisten Checkouts gewinnen.

    Alle bekommen dieselben Finishes in derselben Reihenfolge, damit es fair bleibt.
    """

    def __init__(self, e: dict[str, Any], n: int, seed: str) -> None:
        super().__init__(e, n, seed)
        self.runden = max(1, min(int(e.get("runden") or 10), 30))

    def leg_start(self) -> None:
        super().leg_start()
        moeglich = [z for z in range(2, 171) if z not in BOGEY]
        self.ziele = [self.zufall.choice(moeglich) for _ in range(self.runden)]
        self.zielwert = [self.ziele[0]] * self.n
        self.rest = [self.ziele[0]] * self.n
        self.score = list(self.rest)

    def visit_ende(self, p: int, felder: list[str]) -> None:
        vorher = self.runde[p]
        geschafft = self.geschafft
        ziel = self.zielwert[p]
        super().visit_ende(p, felder)
        if self.runde[p] != vorher:
            if geschafft:
                self.bestes[p] = max(self.bestes[p], ziel)
            neu = self.ziele[min(self.runde[p], len(self.ziele) - 1)]
            self.zielwert[p] = self.rest[p] = self.score[p] = neu


class JDC(Art):
    """JDC Challenge: Shanghai 10–15, je ein Dart auf D1–D20 und Bull, Shanghai 15–20 (57 Darts)."""

    runden = 19

    def leg_start(self) -> None:
        super().leg_start()
        self.nr = [0] * self.n

    def teil(self, p: int) -> int:
        r = self.runde[p]
        return 1 if r < 6 else 2 if r < 13 else 3

    def ziel(self, p: int) -> str | None:
        if self.fertig[p]:
            return None
        r = self.runde[p]
        if r < 6:
            return str(10 + r)
        if r >= 13:
            return str(15 + r - 13)
        i = (r - 6) * 3 + min(self.nr[p], 2)
        return "D25" if i >= 20 else f"D{i + 1}"

    def visit_start(self, p: int) -> None:
        super().visit_start(p)
        self.nr[p] = 0
        self.arten: set[int] = set()

    def dart(self, p: int, f: str, k: int) -> bool:
        z = self.ziel(p) or ""
        zahl, fak = zahl_faktor(f)
        if self.teil(p) == 2:
            if f == z:
                pkt = 100 if z == "D25" else 50
                self.score[p] += pkt
                self.visit_punkte += pkt
        elif fak and str(zahl) == z:
            self.score[p] += zahl * fak
            self.visit_punkte += zahl * fak
            self.arten.add(fak)
            if self.arten == {1, 2, 3}:
                self.arten.add(0)
                self.score[p] += 100
                self.visit_punkte += 100
                self.tags.append("shanghai")
        self.nr[p] += 1
        return False

    def visit_ende(self, p: int, felder: list[str]) -> None:
        super().visit_ende(p, felder)
        self.nr[p] = 0

    def extra(self, p: int) -> dict[str, Any]:
        return {"teil": self.teil(p)}

    def bot_ziel(self, p: int, uebrig: int) -> str:
        z = self.ziel(p) or "T20"
        if z[0] == "D":
            return z
        fehlt = {1, 2, 3} - self.arten
        fak = 3 if 3 in fehlt or not fehlt else (2 if 2 in fehlt else 1)
        return {1: "S", 2: "D", 3: "T"}[fak] + z


class Singles(Art):
    """Singles-Training: eine Aufnahme auf jede Zahl 1–20 und Bull. Single 1, Double 2, Triple 3 Punkte."""

    runden = 21

    def zielzahl(self, p: int) -> int:
        return 25 if self.runde[p] >= 20 else self.runde[p] + 1

    def ziel(self, p: int) -> str | None:
        if self.fertig[p]:
            return None
        return "B" if self.zielzahl(p) == 25 else str(self.zielzahl(p))

    def dart(self, p: int, f: str, k: int) -> bool:
        zahl, fak = zahl_faktor(f)
        if fak and zahl == self.zielzahl(p):
            self.score[p] += fak
            self.visit_punkte += fak
        return False

    def bot_ziel(self, p: int, uebrig: int) -> str:
        z = self.zielzahl(p)
        return "D25" if z == 25 else f"T{z}"


# ---------- Partyspiele ----------

class Shanghai(Art):
    """Shanghai: Runde n zählt nur die Zahl n. Single, Double und Triple in einer Aufnahme gewinnt sofort."""

    stechen = True

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

    ziele: ClassVar[list[str]] = HALVE_IT
    runden = len(HALVE_IT)
    stechen = True
    halbieren = True

    def startwert(self) -> int:
        return 40

    def ziel(self, p: int) -> str | None:
        if self.fertig[p]:
            return None
        return self.ziele[self.runde[p]] if self.runde[p] < len(self.ziele) else "B"

    def visit_start(self, p: int) -> None:
        super().visit_start(p)
        self.getroffen = False

    def dart(self, p: int, f: str, k: int) -> bool:
        z = self.ziel(p)
        zahl, fak = zahl_faktor(f)
        if not fak:
            return False
        ok = ((z == "D" and fak == 2) or (z == "T" and fak == 3) or (z == "B" and zahl == 25) or (z == "DB" and f == "D25")
              or (z not in ("D", "T", "B", "DB") and str(zahl) == z))
        if ok:
            self.getroffen = True
            self.visit_punkte += zahl * fak
        return False

    def visit_ende(self, p: int, felder: list[str]) -> None:
        if self.getroffen:
            self.score[p] += self.visit_punkte
        elif not self.halbieren:
            self.visit_punkte = 0
        else:
            alt = self.score[p]
            self.score[p] = alt // 2
            self.visit_punkte = self.score[p] - alt
            if alt > 0:
                self.tags.append("halbiert")
        super().visit_ende(p, felder)

    def bot_ziel(self, p: int, uebrig: int) -> str:
        z = self.ziel(p) or "20"
        return {"D": "D20", "T": "T20", "B": "D25", "DB": "D25"}.get(z, "T" + z)


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
    stechen = True

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
    stechen = True

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


class Bermuda(HalveIt):
    """Bermuda: 12, 13, 14, ein Double, 15, 16, 17, ein Triple, 18, 19, 20, Bull, Bullseye. Start bei 0."""

    ziele: ClassVar[list[str]] = ["12", "13", "14", "D", "15", "16", "17", "T", "18", "19", "20", "B", "DB"]
    runden = 13

    def __init__(self, e: dict[str, Any], n: int, seed: str) -> None:
        super().__init__(e, n, seed)
        self.halbieren = e.get("variante") != "ohne_halbieren"

    def startwert(self) -> int:
        return 0


class RundUmDieWelt(Art):
    """Round the World: 1–20 (auf-, absteigend oder zufällig), dann Bull. Jeder Treffer zählt seine Punkte, wer zuerst Bull trifft, gewinnt."""

    def __init__(self, e: dict[str, Any], n: int, seed: str) -> None:
        super().__init__(e, n, seed)
        self.reihenfolge = e.get("variante") if e.get("variante") in ("ab", "zufall") else "auf"

    def leg_start(self) -> None:
        super().leg_start()
        zahlen = list(range(1, 21))
        if self.reihenfolge == "ab":
            zahlen.reverse()
        elif self.reihenfolge == "zufall":
            self.zufall.shuffle(zahlen)
        self.folge = [*zahlen, 25]
        self.pos = [0] * self.n

    def ziel(self, p: int) -> str | None:
        if self.fertig[p]:
            return None
        z = self.folge[self.pos[p]]
        return "B" if z == 25 else str(z)

    def dart(self, p: int, f: str, k: int) -> bool:
        zahl, fak = zahl_faktor(f)
        if not fak or zahl != self.folge[self.pos[p]]:
            return False
        pkt = x01.wert(f)[0]
        self.score[p] += pkt
        self.visit_punkte += pkt
        self.pos[p] += 1
        self.runde[p] = self.pos[p]
        if self.pos[p] >= len(self.folge):
            self.fertig[p] = True
            self.tags.append("geschafft")
            return True
        return False

    def visit_ende(self, p: int, felder: list[str]) -> None:
        pass

    def sieger(self) -> int | None:
        return next((p for p in range(self.n) if self.fertig[p]), None)

    def extra(self, p: int) -> dict[str, Any]:
        return {"treffer": self.pos[p], "folge": self.folge}

    def bot_ziel(self, p: int, uebrig: int) -> str:
        z = self.folge[self.pos[p]] if not self.fertig[p] else 20
        return "D25" if z == 25 else f"T{z}"


class Gotcha(Art):
    """Gotcha: alle zählen von 0 hoch bis zum Ziel (z. B. 301). Wer genau den Stand eines anderen trifft, schickt ihn auf 0."""

    def __init__(self, e: dict[str, Any], n: int, seed: str) -> None:
        super().__init__(e, n, seed)
        ziel = int(e.get("zielwert") or 301)
        self.ziel_wert = ziel if 101 <= ziel <= 1001 else 301
        self.aus: str = str(e["variante"]) if e.get("variante") in ("double", "master") else "straight"

    def visit_start(self, p: int) -> None:
        super().visit_start(p)
        self.vor = list(self.score)
        self.bust = False

    def dart(self, p: int, f: str, k: int) -> bool:
        pkt, fak = x01.wert(f)
        neu = self.score[p] + pkt
        rest = self.ziel_wert - neu
        erlaubt = self.aus == "straight" or fak == 2 or (self.aus == "master" and fak == 3)
        if rest < 0 or (rest == 1 and self.aus != "straight") or (rest == 0 and not erlaubt):
            self.bust = True
            self.score = list(self.vor)
            self.visit_punkte = 0
            self.tags = ["bust"]
            return True
        self.score[p] = neu
        self.visit_punkte += pkt
        if rest == 0:
            self.fertig[p] = True
            self.tags.append("geschafft")
            return True
        if pkt:
            for q in range(self.n):
                if q != p and self.score[q] == neu:
                    self.score[q] = 0
                    self.tags.append(f"gotcha:{q}")
        return False

    def visit_ende(self, p: int, felder: list[str]) -> None:
        self.runde[p] += 1

    def sieger(self) -> int | None:
        return next((p for p in range(self.n) if self.fertig[p]), None)

    def extra(self, p: int) -> dict[str, Any]:
        rest = self.ziel_wert - self.score[p]
        return {"zielwert": self.ziel_wert, "restwert": rest, "weg": x01.weg(rest, self.darts_frei(p), self.aus) if 0 < rest <= 180 else None}

    def bot_ziel(self, p: int, uebrig: int) -> str:
        rest = self.ziel_wert - self.score[p]
        if rest > 60:
            # wenn möglich einen Gegner zurückschicken
            for q in sorted(range(self.n), key=lambda q: -self.score[q]):
                diff = self.score[q] - self.score[p]
                if q != p and 0 < diff <= 60 and self.score[q] < self.ziel_wert:
                    for f in [f"T{z}" for z in range(20, 0, -1)] + [f"S{z}" for z in range(20, 0, -1)] + ["S25", "D25"]:
                        if x01.wert(f)[0] == diff:
                            return f
        return x01.bot_ziel(rest, uebrig, True, "straight", self.aus)


class NineLives(Art):
    """Nine Lives: 1 bis 20 der Reihe nach. Eine Aufnahme ohne Treffer aufs Ziel kostet ein Leben."""

    def __init__(self, e: dict[str, Any], n: int, seed: str) -> None:
        super().__init__(e, n, seed)
        self.leben_start = max(1, min(int(e.get("leben") or 3), 9))

    def leg_start(self) -> None:
        super().leg_start()
        self.pos = [0] * self.n
        self.leben = [self.leben_start] * self.n

    def ziel(self, p: int) -> str | None:
        return None if self.fertig[p] or self.raus[p] else str(self.pos[p] + 1)

    def visit_start(self, p: int) -> None:
        super().visit_start(p)
        self.getroffen = False

    def dart(self, p: int, f: str, k: int) -> bool:
        zahl, fak = zahl_faktor(f)
        if fak and zahl == self.pos[p] + 1:
            self.getroffen = True
            self.pos[p] += 1
            self.score[p] = self.pos[p]
            self.visit_punkte += 1
            if self.pos[p] >= 20:
                self.fertig[p] = True
                self.tags.append("geschafft")
                return True
        return False

    def visit_ende(self, p: int, felder: list[str]) -> None:
        self.runde[p] += 1
        if not self.getroffen and not self.fertig[p]:
            self.leben[p] -= 1
            self.tags.append(f"leben:{p}")
            if self.leben[p] <= 0:
                self.raus[p] = True
                self.tags.append(f"raus:{p}")

    def sieger(self) -> int | None:
        fertig = next((p for p in range(self.n) if self.fertig[p]), None)
        if fertig is not None:
            return fertig
        drin = [p for p in range(self.n) if not self.raus[p]]
        if self.n > 1 and len(drin) == 1:
            return drin[0]
        if not drin:
            return max(range(self.n), key=lambda p: (self.pos[p], -p))
        return None

    def extra(self, p: int) -> dict[str, Any]:
        return {"leben": self.leben[p]}

    def bot_ziel(self, p: int, uebrig: int) -> str:
        return f"S{min(self.pos[p] + 1, 20)}"


class Fussball(Art):
    """Fußball: Bull holt den Ball, danach ist jedes Double ein Tor. Wer zuerst die Tore hat, gewinnt."""

    def __init__(self, e: dict[str, Any], n: int, seed: str) -> None:
        super().__init__(e, n, seed)
        tore = int(e.get("zielwert") or 10)
        self.tore = tore if 1 <= tore <= 20 else 10

    def leg_start(self) -> None:
        super().leg_start()
        self.ball = [False] * self.n

    def ziel(self, p: int) -> str | None:
        if self.fertig[p]:
            return None
        return "D" if self.ball[p] else "B"

    def dart(self, p: int, f: str, k: int) -> bool:
        zahl, fak = zahl_faktor(f)
        if not self.ball[p]:
            if zahl == 25:
                self.ball[p] = True
                self.tags.append("ball")
            return False
        if fak == 2:
            self.score[p] += 1
            self.visit_punkte += 1
            self.tags.append("tor")
            if self.score[p] >= self.tore:
                self.fertig[p] = True
                return True
        return False

    def visit_ende(self, p: int, felder: list[str]) -> None:
        self.runde[p] += 1

    def sieger(self) -> int | None:
        return next((p for p in range(self.n) if self.fertig[p]), None)

    def extra(self, p: int) -> dict[str, Any]:
        return {"ball": self.ball[p], "zielwert": self.tore}

    def bot_ziel(self, p: int, uebrig: int) -> str:
        return "D20" if self.ball[p] else "D25"


SCRAM = [20, 19, 18, 17, 16, 15, 25]


class Scram(Art):
    """Scram (2 Spieler): der Stopper schließt 15–20 und Bull, der Scorer punktet auf allem, was noch offen ist. Dann Rollentausch."""

    zahlen: ClassVar[list[Any]] = SCRAM

    def leg_start(self) -> None:
        super().leg_start()
        self.erster: int | None = None
        self.halbzeit = 0
        self.zu = dict.fromkeys(SCRAM, 0)
        self.stopper_aufn = [0] * self.n

    def stopper(self) -> int:
        erster = self.erster if self.erster is not None else 0
        return erster if self.halbzeit == 0 else (erster + 1) % max(self.n, 1)

    def visit_start(self, p: int) -> None:
        super().visit_start(p)
        if self.erster is None:
            self.erster = p

    def alle_zu(self) -> bool:
        return all(m >= 3 for m in self.zu.values())

    def dart(self, p: int, f: str, k: int) -> bool:
        zahl, fak = zahl_faktor(f)
        if zahl not in self.zu or not fak:
            return False
        if p == self.stopper():
            if self.zu[zahl] < 3:
                self.zu[zahl] = min(3, self.zu[zahl] + fak)
                self.visit_punkte += fak
                if self.zu[zahl] >= 3:
                    self.tags.append(f"zu:{zahl}")
            return self.alle_zu()
        if self.zu[zahl] < 3:
            self.score[p] += zahl * fak
            self.visit_punkte += zahl * fak
        return False

    def visit_ende(self, p: int, felder: list[str]) -> None:
        self.runde[p] += 1
        if p == self.stopper():
            self.stopper_aufn[p] += 1
        if self.alle_zu():
            if self.halbzeit == 0 and self.n > 1:
                self.halbzeit = 1
                self.zu = dict.fromkeys(SCRAM, 0)
                self.tags.append("wechsel")
            else:
                self.fertig = [True] * self.n

    def sieger(self) -> int | None:
        if all(self.fertig):
            return self.bester()
        return None

    def bester(self) -> int:
        return min(range(self.n), key=lambda p: (-self.score[p], self.stopper_aufn[p], p))

    def ziel(self, p: int) -> str | None:
        return None

    def extra(self, p: int) -> dict[str, Any]:
        return {"rolle": "stopper" if p == self.stopper() else "scorer", "marks": [self.zu[z] for z in SCRAM]}

    def bot_ziel(self, p: int, uebrig: int) -> str:
        offen = [z for z in SCRAM if self.zu[z] < 3]
        if not offen:
            return "T20"
        return _ziel_feld(offen[0])


ARTEN: dict[str, type[Art]] = {
    "cricket": Cricket, "wild_mouse": WildMouse, "mickey": MickeyMouse,
    "atc": RundT, "bobs27": Bobs27, "doppel": Doppel, "checkout121": Checkout121, "checkout": CheckoutTraining,
    "catch40": Catch40, "jdc": JDC, "singles": Singles,
    "highscore": Highscore, "shanghai": Shanghai, "killer": Killer, "halve_it": HalveIt, "golf": Golf, "baseball": Baseball,
    "bermuda": Bermuda, "rtw": RundUmDieWelt, "gotcha": Gotcha, "nine_lives": NineLives, "football": Fussball, "scram": Scram,
}
SPIELER_GRENZEN = {"scram": (2, 2), "killer": (2, 8)}  # (min, max); sonst 1–8


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
    art.wer_wirft, art.noch_darts = am_zug, uebrig
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
    verdeckt = getattr(art, "verdeckt", None) or set()
    art_zahlen = getattr(art, "zahlen", None)
    return {
        "art": art_id,
        # verdeckte Zahlen (Hidden Cricket) verlassen die Auswertung nicht
        "zahlen": [None if z in verdeckt else z for z in art_zahlen] if isinstance(art_zahlen, list) else None,
        "verdeckt": [z in verdeckt for z in art_zahlen] if verdeckt and isinstance(art_zahlen, list) else None,
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
