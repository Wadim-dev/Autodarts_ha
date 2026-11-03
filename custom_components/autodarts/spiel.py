"""Lokale X01-Spiele in Home Assistant (ohne Autodarts-Konto, ohne Internet).

Der Spielleiter hört auf die Würfe des Boards (Zustand-Koordinator), legt sie als
Aufnahmen ab und lässt `x01.auswerten` alles Weitere ausrechnen. Spieler, Statistik,
Verlauf und ein laufendes Spiel liegen in .storage/autodarts.spiel (übersteht Neustarts).
"""

from __future__ import annotations

import asyncio
from collections.abc import Callable
import logging
import random
from typing import Any
import uuid

import aiohttp
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import HomeAssistantError, ServiceValidationError
from homeassistant.helpers.storage import Store
from homeassistant.util import dt as dt_util

from . import x01
from .api import Board
from .const import DOMAIN
from .coordinator import ZustandKoordinator

_LOGGER = logging.getLogger(__name__)

SPEICHER_VERSION = 1
MAX_SPIELER = 6
MAX_VERLAUF = 50
STANDARD = {"startwert": 501, "einwurf": "straight", "auswurf": "double", "legs": 1, "sets": 0, "bull_off": False}
MODI = ("straight", "double", "master")
STAT_FELDER = ("punkte", "darts", "f9p", "f9d", "versuche", "treffer", "n180", "n140", "n100", "legs", "sets")


def _fehler(schluessel: str, **platzhalter: str) -> ServiceValidationError:
    """Translated error for wrong input to an action."""
    return ServiceValidationError(translation_domain=DOMAIN, translation_key=schluessel, translation_placeholders=platzhalter or None)


class Spielleiter:
    def __init__(self, hass: HomeAssistant, board: Board, zustand: ZustandKoordinator) -> None:
        self.hass = hass
        self.board = board
        self.zustand = zustand
        self._store: Store[dict[str, Any]] = Store(hass, SPEICHER_VERSION, "autodarts.spiel")
        self.daten: dict[str, Any] = {"spieler": [], "statistik": {}, "verlauf": [], "letzte": dict(STANDARD), "spiel": None}
        self.stand: dict[str, Any] | None = None
        self._hoerer: list[Callable[[], None]] = []
        self._ereignis_hoerer: list[Callable[[str, dict[str, Any]], None]] = []
        self._ev_spiel: str | None = None
        self._ev_offen: tuple[int, int] = (-1, 0)
        self._ev_visit = -1
        self._gesehen = 0
        self._board_felder: list[str] = []
        self._bot_aufgabe: asyncio.Task[None] | None = None
        self._zufall = random.Random()
        self._sigma: dict[int, float] = {}

    # ---------- Grundlagen ----------

    async def laden(self) -> None:
        gespeichert = await self._store.async_load()
        if isinstance(gespeichert, dict):
            self.daten.update(gespeichert)
        self.daten["letzte"] = {**STANDARD, **(self.daten.get("letzte") or {})}
        self._gesehen = len((self.zustand.data or {}).get("wuerfe") or [])
        self._neu_rechnen(speichern=False)

    def hoerer(self, f: Callable[[], None]) -> Callable[[], None]:
        self._hoerer.append(f)
        return lambda: self._hoerer.remove(f)

    @property
    def spiel(self) -> dict[str, Any] | None:
        spiel: dict[str, Any] | None = self.daten.get("spiel")
        return spiel

    @property
    def _laufend(self) -> dict[str, Any]:
        """The current game where the caller already checked that one exists."""
        spiel = self.spiel
        assert spiel is not None
        return spiel

    @property
    def _stand(self) -> dict[str, Any]:
        """The evaluated state of the current game (exists whenever a game exists)."""
        assert self.stand is not None
        return self.stand

    def _speichern(self) -> None:
        self._store.async_delay_save(lambda: self.daten, 2)

    def _melden(self) -> None:
        self._ereignisse_pruefen()
        for f in list(self._hoerer):
            f()

    def ereignis_hoerer(self, f: Callable[[str, dict[str, Any]], None]) -> Callable[[], None]:
        """Listen to game events (dart, 180, bust, checkout, leg won …) for the event entity."""
        self._ereignis_hoerer.append(f)
        return lambda: self._ereignis_hoerer.remove(f)

    def _ereignis(self, typ: str, daten: dict[str, Any]) -> None:
        for f in list(self._ereignis_hoerer):
            f(typ, daten)

    def _ereignisse_pruefen(self) -> None:
        """Fire events for darts and visits that are new since the last check (never for undo or edits)."""
        sp, st = self.spiel, self.stand
        if not sp or not st or sp["phase"] not in ("laeuft", "beendet"):
            self._ev_spiel = None
            return
        verlauf = st.get("verlauf") or []
        aufnahme = st["aufnahme"]["darts"]
        offen = (verlauf[-1]["i"] if verlauf and aufnahme else len(sp["aufnahmen"]), len(aufnahme))
        visit = int(st["ansage_id"]) if st.get("ansage_id") not in (None, "") else -1
        if self._ev_spiel != sp["id"]:
            # game started or loaded: nothing happened yet
            self._ev_spiel, self._ev_offen, self._ev_visit = sp["id"], offen, visit
            return
        alt_i, alt_n = self._ev_offen
        neu = aufnahme[alt_n:] if offen[0] == alt_i else (aufnahme if offen[0] > alt_i else [])
        spieler = st["spieler"]
        for dart in neu:
            feld = dart["f"]
            punkte, faktor = x01.wert(feld)
            daten = {"player": spieler[st["am_zug"]]["name"], "field": feld, "points": punkte}
            self._ereignis("dart", daten)
            if feld == "D25":
                self._ereignis("bullseye", daten)
            elif feld == "S25":
                self._ereignis("bull", daten)
            elif faktor == 3:
                self._ereignis("triple", daten)
        self._ev_offen = offen
        if visit > self._ev_visit and visit < len(verlauf):
            self._visit_ereignisse(st, verlauf[visit])
        self._ev_visit = visit

    def _visit_ereignisse(self, st: dict[str, Any], z: dict[str, Any]) -> None:
        name = st["spieler"][z["s"]]["name"]
        daten = {"player": name, "score": z["p"], "darts": z["d"], "remaining": z["r"]}
        self._ereignis("visit", daten)
        if z["b"]:
            self._ereignis("bust", daten)
        elif z["p"] == 180:
            self._ereignis("one_eighty", daten)
        elif z["p"] >= 140:
            self._ereignis("ton_forty", daten)
        elif z["p"] >= 100:
            self._ereignis("ton", daten)
        elif z["p"] == 0:
            self._ereignis("no_score", daten)
        if len(z["d"]) == 3 and len(set(z["d"])) == 1 and z["d"][0] != "M":
            self._ereignis("three_in_a_bed", daten)
        if not z["c"]:
            return
        daten = {"player": name, "finish": z["p"], "darts": z["d"]}
        self._ereignis("checkout", daten)
        if z["p"] >= 100:
            self._ereignis("high_finish", daten)
        if st["spieler"][z["s"]]["leg_darts"] == 9:
            self._ereignis("nine_darter", daten)
        ansage = str(st.get("ansage") or "")
        if ansage.startswith("Spiel "):
            self._ereignis("match_won", {"player": name})
        elif ansage.startswith("Satz "):
            self._ereignis("set_won", {"player": name})
        else:
            self._ereignis("leg_won", {"player": name})

    def _neu_rechnen(self, speichern: bool = True) -> None:
        sp = self.spiel
        if sp and sp.get("phase") in ("laeuft", "beendet"):
            self.stand = x01.auswerten(sp)
            if sp["phase"] == "laeuft" and self.stand["gewinner"] is not None:
                self._spiel_abschliessen()
        else:
            self.stand = None
        if speichern:
            self._speichern()
        self._melden()
        self._bot_pruefen()

    async def beenden(self) -> None:
        self._bot_stoppen()
        await self._store.async_save(self.daten)

    # ---------- Würfe vom Board ----------

    @callback
    def board_aenderung(self) -> None:
        d = self.zustand.data or {}
        if d.get("verbindung") != "Online":
            return
        wuerfe = d.get("wuerfe") or []
        anzahl = len(wuerfe)
        felder = [x01.feld_aus(w["zahl"], w["faktor"]) for w in wuerfe]
        sp = self.spiel
        if anzahl < self._gesehen:
            # Darts gezogen: die Aufnahme ist vorbei
            self._gesehen = 0
            if sp and sp["phase"] == "laeuft" and not self._ist_bot_dran():
                self._aufnahme_schliessen(nur_wenn_darts=True)
        geaendert = False
        # Board hat einen schon gezählten Dart nachträglich korrigiert
        for i in range(min(self._gesehen, anzahl, len(self._board_felder))):
            if felder[i] != self._board_felder[i] and sp and sp["phase"] == "laeuft":
                for dart in self._offene_aufnahme().get("d", []):
                    if dart.get("b") == i and dart.get("q") == "board":
                        dart["f"] = felder[i]
                        dart["x"], dart["y"] = wuerfe[i].get("x"), wuerfe[i].get("y")
                        geaendert = True
        for i in range(self._gesehen, anzahl):
            w = wuerfe[i]
            dart = {"f": felder[i], "x": _rund(w.get("x")), "y": _rund(w.get("y")), "b": i, "q": "board"}
            if self._dart_annehmen(dart, vom_board=True):
                geaendert = True
        self._gesehen = anzahl
        self._board_felder = felder
        if geaendert:
            self._neu_rechnen()

    def _offene_aufnahme(self) -> dict[str, Any]:
        sp = self._laufend
        if not sp["aufnahmen"] or sp["aufnahmen"][-1].get("zu"):
            sp["aufnahmen"].append({"d": [], "zu": False})
        aufnahme: dict[str, Any] = sp["aufnahmen"][-1]
        return aufnahme

    @staticmethod
    def _bo_werfer(sp: dict[str, Any]) -> list[int]:
        """Wer in der aktuellen Bull-Off-Runde wirft (bei Gleichstand nur die Gleichen)."""
        return sp.get("bo_werfer") or list(range(len(sp["spieler"])))

    def _ist_bot_dran(self) -> bool:
        sp = self.spiel
        if not sp:
            return False
        if sp["phase"] == "bulloff":
            k, w = len(sp["bulloff"]), self._bo_werfer(sp)
            return k < len(w) and bool(sp["spieler"][w[k]].get("bot"))
        if sp["phase"] == "laeuft" and self.stand and self.stand["gewinner"] is None:
            return bool(sp["spieler"][self.stand["am_zug"]].get("bot"))
        return False

    def _dart_annehmen(self, dart: dict[str, Any], vom_board: bool) -> bool:
        sp = self.spiel
        if not sp or sp["phase"] not in ("bulloff", "laeuft"):
            return False
        if vom_board and self._ist_bot_dran():
            return False
        if sp["phase"] == "bulloff":
            sp["bulloff"].append(dart)
            if len(sp["bulloff"]) >= len(self._bo_werfer(sp)):
                self._bulloff_auswerten()
            return True
        if self.stand and (self.stand["gewinner"] is not None or self.stand["leg_gewinner"] is not None or self.stand["aufnahme"]["fertig"]):
            return False
        aufn = self._offene_aufnahme()
        if len(aufn["d"]) >= 3:
            return False
        aufn["d"].append(dart)
        return True

    def _aufnahme_schliessen(self, nur_wenn_darts: bool = False) -> bool:
        sp = self.spiel
        if not sp or sp["phase"] != "laeuft" or not self.stand or self.stand["gewinner"] is not None:
            return False
        if sp["aufnahmen"] and not sp["aufnahmen"][-1].get("zu"):
            aufn = sp["aufnahmen"][-1]
            if nur_wenn_darts and not aufn["d"]:
                return False
            aufn["zu"] = True
        elif nur_wenn_darts:
            return False
        else:
            sp["aufnahmen"].append({"d": [], "zu": True})
        self._neu_rechnen()
        return True

    def _bulloff_auswerten(self) -> None:
        sp = self._laufend
        w = self._bo_werfer(sp)
        abstaende = [x01.bull_abstand(d) for d in sp["bulloff"]]
        best = min(abstaende)
        gleich = [w[k] for k, a in enumerate(abstaende) if abs(a - best) < 1e-9]
        if len(gleich) > 1:
            # Gleichstand: nur diese werfen noch einmal
            sp.setdefault("bo_alt", []).append({"werfer": w, "darts": sp["bulloff"]})
            sp["bo_werfer"] = gleich
            sp["bulloff"] = []
            return
        sieger = gleich[0]
        n = len(sp["spieler"])
        sp["reihenfolge"] = [(sieger + k) % n for k in range(n)]
        sp["bulloff_sieger"] = sieger
        sp["phase"] = "laeuft"
        sp["aufnahmen"] = []

    # ---------- Bot ----------

    def _bot_stoppen(self) -> None:
        if self._bot_aufgabe and not self._bot_aufgabe.done():
            self._bot_aufgabe.cancel()
        self._bot_aufgabe = None

    def _bot_pruefen(self) -> None:
        if self._bot_aufgabe and not self._bot_aufgabe.done():
            return
        if self._ist_bot_dran():
            self._bot_aufgabe = self.hass.async_create_background_task(self._bot_werfen(), "autodarts_bot")

    async def _sigma_fuer(self, level: int) -> float:
        if level not in self._sigma:
            self._sigma[level] = await self.hass.async_add_executor_job(x01.streuung, float(level))
        return self._sigma[level]

    async def _bot_werfen(self) -> None:
        await _pause(2.0)
        sp = self.spiel
        if not sp or not self._ist_bot_dran():
            return
        if sp["phase"] == "bulloff":
            level = int(sp["spieler"][self._bo_werfer(sp)[len(sp["bulloff"])]]["bot"])
            dart = x01.bot_wurf("D25", await self._sigma_fuer(level), self._zufall)
            self._dart_annehmen(dart, vom_board=False)
            self._bot_aufgabe = None
            self._neu_rechnen()
            return
        p = self._stand["am_zug"]
        level = int(sp["spieler"][p]["bot"])
        sigma = await self._sigma_fuer(level)
        e = sp["einstellungen"]
        while True:
            st = self._stand
            if not self.spiel or self.spiel["phase"] != "laeuft" or st["am_zug"] != p or st["gewinner"] is not None:
                return
            if st["aufnahme"]["fertig"] or st["leg_gewinner"] is not None:
                break
            uebrig = 3 - len(st["aufnahme"]["darts"])
            ziel = x01.bot_ziel(st["spieler"][p]["rest"], uebrig, st["spieler"][p]["offen"], e["einwurf"], e["auswurf"])
            self._dart_annehmen(x01.bot_wurf(ziel, sigma, self._zufall), vom_board=False)
            self._neu_rechnen_ohne_bot()
            await _pause(1.2)
        await _pause(1.5)
        self._bot_aufgabe = None
        self._aufnahme_schliessen()

    def _neu_rechnen_ohne_bot(self) -> None:
        sp = self._laufend
        self.stand = x01.auswerten(sp)
        if self.stand["gewinner"] is not None:
            self._spiel_abschliessen()
        self._speichern()
        self._melden()

    # ---------- Spielende ----------

    def _spiel_abschliessen(self) -> None:
        sp = self._laufend
        sp["phase"] = "beendet"
        sp["ende"] = dt_util.now().isoformat()
        st = self._stand
        eintrag = {
            "zeit": sp["ende"],
            "modus": modus_text(sp["einstellungen"]),
            "gewinner": sp["spieler"][st["gewinner"]]["name"],
            "spieler": [
                {"name": s["name"], "avg": s["avg"], "legs": s["legs"], "sets": s["sets"], "sieger": k == st["gewinner"], "bot": s.get("bot")}
                for k, s in enumerate(st["spieler"])
            ],
        }
        self.daten["verlauf"] = [eintrag, *self.daten.get("verlauf", [])][:MAX_VERLAUF]
        for k, s in enumerate(sp["spieler"]):
            if not s.get("id"):
                continue
            ges = self.daten["statistik"].setdefault(s["id"], {})
            roh = st["statistik"][k]
            for f in STAT_FELDER:
                ges[f] = ges.get(f, 0) + roh[f]
            ges["spiele"] = ges.get("spiele", 0) + 1
            ges["siege"] = ges.get("siege", 0) + (1 if k == st["gewinner"] else 0)
            ges["hoechste"] = max(ges.get("hoechste", 0), roh["hoechste"])
            ges["finish"] = max(ges.get("finish", 0), roh["finish"])
            if roh["bestes_leg"]:
                ges["bestes_leg"] = min(ges.get("bestes_leg") or 999, roh["bestes_leg"])
            avg = round(roh["punkte"] / roh["darts"] * 3, 2) if roh["darts"] else 0
            ges["bester_avg"] = max(ges.get("bester_avg", 0), avg)

    # ---------- Dienste ----------

    async def starten(self, eintraege: list[str] | None, einstellungen: dict[str, Any]) -> None:
        e = {**self.daten["letzte"], **{k: v for k, v in einstellungen.items() if v is not None}}
        if int(e["startwert"]) not in (101, 170, 301, 501, 701, 901):
            raise _fehler("invalid_start_value")
        if e["einwurf"] not in MODI or e["auswurf"] not in MODI:
            raise _fehler("invalid_mode")
        e["legs"] = max(1, min(int(e["legs"]), 21))
        e["sets"] = max(0, min(int(e.get("sets") or 0), 13))
        e["bull_off"] = bool(e.get("bull_off"))
        eintraege = eintraege or e.get("spieler") or []
        spieler = []
        bekannt = {s["id"]: s for s in self.daten["spieler"]}
        for x in eintraege[:MAX_SPIELER]:
            x = str(x)
            if x.startswith("bot:"):
                level = max(10, min(int(x[4:] or 50), 120))
                spieler.append({"name": f"Bot {level}", "bot": level})
            elif x in bekannt:
                spieler.append({"id": x, "name": bekannt[x]["name"]})
        if not spieler:
            raise _fehler("no_player")
        e["spieler"] = [s["id"] if s.get("id") else f"bot:{s['bot']}" for s in spieler]
        self.daten["letzte"] = e
        self._bot_stoppen()
        einst = {k: e[k] for k in ("startwert", "einwurf", "auswurf", "legs", "sets", "bull_off")}
        bulloff = e["bull_off"] and len(spieler) > 1
        self.daten["spiel"] = {
            "id": uuid.uuid4().hex[:8],
            "beginn": dt_util.now().isoformat(),
            "einstellungen": einst,
            "spieler": spieler,
            "reihenfolge": list(range(len(spieler))),
            "phase": "bulloff" if bulloff else "laeuft",
            "bulloff": [],
            "aufnahmen": [],
        }
        await self._board_leeren()
        await self._erkennung_an()
        self._neu_rechnen()

    async def _erkennung_an(self) -> None:
        """Board an, aber Erkennung gestoppt (z. B. Stop gedrückt): zum Spielstart wieder starten."""
        if not self.zustand.online or (self.zustand.data or {}).get("laeuft"):
            return
        try:
            await self.board.befehl("/api/start")
        except (HomeAssistantError, aiohttp.ClientError, TimeoutError) as err:
            _LOGGER.debug("Board-Start: %s", err)

    async def _board_leeren(self) -> None:
        """Darts auf dem Board vergessen (Reset) und den neuen Stand sofort übernehmen."""
        self._gesehen = len((self.zustand.data or {}).get("wuerfe") or [])
        if not (self.zustand.online and self._gesehen):
            return
        try:
            await self.board.befehl("/api/reset")
            await _pause(0.3)
            jetzt = await self.board.holen("/api/state", 2)
            self._gesehen = len(jetzt.get("throws") or [])
            self._board_felder = self._board_felder[: self._gesehen]
        except (HomeAssistantError, aiohttp.ClientError, TimeoutError, ValueError) as err:
            _LOGGER.debug("Board-Reset: %s", err)

    async def abbrechen(self) -> None:
        self._bot_stoppen()
        self.daten["spiel"] = None
        self._neu_rechnen()

    async def weiter(self) -> None:
        sp = self.spiel
        if not sp:
            raise _fehler("no_game")
        if sp["phase"] == "bulloff":
            sp["bulloff"].append({"f": "M", "q": "hand"})
            if len(sp["bulloff"]) >= len(self._bo_werfer(sp)):
                self._bulloff_auswerten()
            self._neu_rechnen()
            return
        self._bot_stoppen()
        await self._board_leeren()
        self._aufnahme_schliessen()

    async def rueckgaengig(self) -> None:
        sp = self.spiel
        if not sp:
            raise _fehler("no_game")
        self._bot_stoppen()
        self._gesehen = len((self.zustand.data or {}).get("wuerfe") or [])
        if sp["phase"] == "bulloff":
            if sp["bulloff"]:
                sp["bulloff"].pop()
            elif sp.get("bo_alt"):
                alt = sp["bo_alt"].pop()
                sp["bo_werfer"] = alt["werfer"]
                sp["bulloff"] = alt["darts"][:-1]
            self._neu_rechnen()
            return
        if sp["phase"] == "beendet":
            sp["phase"] = "laeuft"
            sp.pop("ende", None)
            self.daten["verlauf"] = self.daten.get("verlauf", [])[1:]
            self._statistik_abziehen()
        auf = sp["aufnahmen"]
        while auf and not auf[-1]["d"]:
            auf.pop()
        if auf:
            auf[-1]["zu"] = False
            auf[-1]["d"].pop()
        elif sp.get("bulloff_sieger") is not None:
            sp["phase"] = "bulloff"
            sp["bulloff"].pop()
            sp["reihenfolge"] = list(range(len(sp["spieler"])))
            sp.pop("bulloff_sieger", None)
        self._neu_rechnen()

    def _statistik_abziehen(self) -> None:
        """Rückgängig nach Spielende: Gesamtstatistik wieder abziehen (Bestwerte bleiben)."""
        st = x01.auswerten(self._laufend)
        for k, s in enumerate(self._laufend["spieler"]):
            ges = self.daten["statistik"].get(s.get("id") or "")
            if not ges:
                continue
            roh = st["statistik"][k]
            for f in STAT_FELDER:
                ges[f] = max(0, ges.get(f, 0) - roh[f])
            ges["spiele"] = max(0, ges.get("spiele", 0) - 1)
            if k == st["gewinner"]:
                ges["siege"] = max(0, ges.get("siege", 0) - 1)

    async def wurf_aendern(self, aufnahme: int | None, dart: int, feld: str) -> None:
        sp = self.spiel
        if not sp or sp["phase"] not in ("laeuft", "bulloff"):
            raise _fehler("no_game")
        feld = (feld or "").upper().strip()
        feld = {"25": "S25", "50": "D25", "BULL": "D25", "MISS": "M", "0": "M"}.get(feld, feld)
        if feld and not x01.feld_ok(feld):
            raise _fehler("unknown_field", field=feld)
        if sp["phase"] == "bulloff":
            if 0 <= dart < len(sp["bulloff"]) and feld:
                sp["bulloff"][dart] = {"f": feld, "q": "hand"}
            elif dart == len(sp["bulloff"]) and feld and not self._ist_bot_dran():
                # ohne Board: Bull-Off-Dart von Hand eintragen
                self._dart_annehmen({"f": feld, "q": "hand"}, vom_board=False)
            self._neu_rechnen()
            return
        self._bot_stoppen()
        if aufnahme is None or aufnahme < 0:
            aufn = self._offene_aufnahme()
        else:
            if aufnahme >= len(sp["aufnahmen"]):
                raise _fehler("unknown_visit")
            aufn = sp["aufnahmen"][aufnahme]
        if not feld:
            if dart < len(aufn["d"]):
                aufn["d"].pop(dart)
        elif dart < len(aufn["d"]):
            aufn["d"][dart] = {"f": feld, "q": "hand"}
        elif len(aufn["d"]) < 3:
            aufn["d"].append({"f": feld, "q": "hand"})
        self._neu_rechnen()

    # Spieler

    async def spieler_anlegen(self, name: str) -> str:
        name = (name or "").strip()[:20]
        if not name:
            raise _fehler("name_missing")
        if any(s["name"].lower() == name.lower() for s in self.daten["spieler"]):
            raise _fehler("name_exists", name=name)
        sid = uuid.uuid4().hex[:8]
        self.daten["spieler"].append({"id": sid, "name": name, "seit": dt_util.now().date().isoformat()})
        self._speichern()
        self._melden()
        return sid

    async def spieler_aendern(self, sid: str, name: str | None, loeschen: bool) -> None:
        liste = self.daten["spieler"]
        s = next((s for s in liste if s["id"] == sid), None)
        if not s:
            raise _fehler("player_not_found")
        if loeschen:
            liste.remove(s)
            self.daten["statistik"].pop(sid, None)
        elif name and name.strip():
            s["name"] = name.strip()[:20]
        self._speichern()
        self._melden()

    async def statistik_loeschen(self, sid: str | None, verlauf: bool) -> None:
        if sid:
            self.daten["statistik"].pop(sid, None)
        else:
            self.daten["statistik"] = {}
        if verlauf:
            self.daten["verlauf"] = []
        self._speichern()
        self._melden()

    # ---------- Für die Sensoren ----------

    def phase(self) -> str:
        sp = self.spiel
        if not sp:
            return "idle"
        return {"bulloff": "bull_off", "laeuft": "running", "beendet": "finished"}[sp["phase"]]

    def spiel_attribute(self) -> dict[str, Any]:
        sp = self.spiel
        if not sp:
            return {"quelle": "HA"}
        a: dict[str, Any] = {
            "quelle": "HA",
            "id": sp["id"],
            "phase": sp["phase"],
            "modus": modus_text(sp["einstellungen"]),
            "einstellungen": sp["einstellungen"],
            "beginn": sp["beginn"],
        }
        if sp["phase"] == "bulloff":
            k, w = len(sp["bulloff"]), self._bo_werfer(sp)
            liste = []
            for i, s in enumerate(sp["spieler"]):
                j = w.index(i) if i in w else None
                d = sp["bulloff"][j] if j is not None and j < k else None
                liste.append({"name": s["name"], "bot": s.get("bot"), "dart": d, "raus": j is None,
                              "abstand": round(x01.bull_abstand(d) * 170) if d else None})
            a["bulloff"] = liste
            a["am_zug"] = w[min(k, len(w) - 1)]
            a["gleichstand"] = len(sp.get("bo_alt") or [])
            a["spieler"] = [{"name": s["name"], "bot": s.get("bot"), "rest": int(sp["einstellungen"]["startwert"]), "legs": 0, "sets": 0}
                            for s in sp["spieler"]]
            return a
        st = self.stand or {}
        a.update({k: st.get(k) for k in ("am_zug", "aufnahme", "weg", "spieler", "gewinner", "leg_gewinner", "leg", "set", "ansage", "ansage_id")})
        a["reihenfolge"] = sp["reihenfolge"]
        a["bot_wirft"] = bool(self._bot_aufgabe and not self._bot_aufgabe.done())
        a["aufnahmen"] = len(sp["aufnahmen"])
        a["verlauf"] = (st.get("verlauf") or [])[-30:]
        if sp.get("ende"):
            a["ende"] = sp["ende"]
        return a

    def spieler_attribute(self) -> dict[str, Any]:
        liste = []
        for s in self.daten["spieler"]:
            g = self.daten["statistik"].get(s["id"], {})
            liste.append({
                "id": s["id"],
                "name": s["name"],
                "spiele": g.get("spiele", 0),
                "siege": g.get("siege", 0),
                "avg": round(g["punkte"] / g["darts"] * 3, 2) if g.get("darts") else 0,
                "f9": round(g["f9p"] / g["f9d"] * 3, 2) if g.get("f9d") else 0,
                "quote": round(g["treffer"] / g["versuche"] * 100, 1) if g.get("versuche") else 0,
                "darts": g.get("darts", 0),
                "legs": g.get("legs", 0),
                "hoechste": g.get("hoechste", 0),
                "finish": g.get("finish", 0),
                "bestes_leg": g.get("bestes_leg", 0),
                "bester_avg": g.get("bester_avg", 0),
                "n180": g.get("n180", 0), "n140": g.get("n140", 0), "n100": g.get("n100", 0),
            })
        return {"spieler": liste, "verlauf": self.daten.get("verlauf", [])[:20], "letzte": self.daten.get("letzte")}


async def _pause(sekunden: float) -> None:
    """Wait (own function so tests can skip the bot's pauses)."""
    await asyncio.sleep(sekunden)


def _rund(v: Any) -> Any:
    return round(v, 3) if isinstance(v, (int, float)) else None


def modus_text(e: dict[str, Any]) -> str:
    teile = [str(e["startwert"])]
    if e["einwurf"] != "straight":
        teile.append({"double": "Double In", "master": "Master In"}[e["einwurf"]])
    teile.append({"straight": "Straight Out", "double": "Double Out", "master": "Master Out"}[e["auswurf"]])
    if e.get("sets"):
        teile.append(f"Erster bis {e['sets']} Sets à {e['legs']} Legs")
    else:
        teile.append(f"Erster bis {e['legs']} Leg" + ("s" if int(e["legs"]) > 1 else ""))
    return " · ".join(teile)
