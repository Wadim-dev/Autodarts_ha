"""Pixel clocks (AWTRIX 3 and PixelIt): the score of the player at the oche and short effects at 180, checkout, bust and the win.

Both are small LED matrices with a local HTTP API. DartNest finds the type itself from the address,
shows its own app while a game runs and gives the display back (other apps, clock) when the game is over.
"""

from __future__ import annotations

import asyncio
from collections.abc import Callable
import logging
import re
from typing import TYPE_CHECKING, Any

import aiohttp
from homeassistant.core import CALLBACK_TYPE, HomeAssistant, callback
from homeassistant.exceptions import ServiceValidationError
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.event import async_call_later
from homeassistant.util import dt as dt_util

from .const import DOMAIN

if TYPE_CHECKING:
    from .coordinator import DartsDaten

_LOGGER = logging.getLogger(__name__)

TYPEN = ("awtrix", "pixelit")
APP = "dartnest"
MAX_GERAETE = 6
HOST = re.compile(r"^[A-Za-z0-9][A-Za-z0-9.\-]{0,62}(:\d{1,5})?$")
ZEIT = 4  # seconds an answer may take
EFFEKT_DAUER = 5  # seconds an effect stays
LEBEN = 900  # AWTRIX removes the app by itself if DartNest stops sending (HA off)
SIEGER_ZEIT = 60  # seconds the winner stays on the display after the game, then the display is given back

WEISS, ORANGE, GRUEN, ROT, GELB, GRAU = "#FFFFFF", "#FF8A4C", "#4CD964", "#FF3B30", "#FFCC00", "#8E8E93"

# event -> (text, colour, rainbow); {n} = player, {w} = value
EFFEKTE: dict[str, tuple[dict[str, str], str, bool]] = {
    "one_eighty": ({"en": "180!", "de": "180!"}, ORANGE, True),
    "nine_darter": ({"en": "NINE DARTER {n}", "de": "NEUN-DARTER {n}"}, GELB, True),
    "high_finish": ({"en": "CHECKOUT {w}", "de": "CHECKOUT {w}"}, GRUEN, True),
    "checkout": ({"en": "CHECKOUT {w}", "de": "CHECKOUT {w}"}, GRUEN, False),
    "ton_forty": ({"en": "{w}!", "de": "{w}!"}, ORANGE, False),
    "bust": ({"en": "BUST", "de": "BUST"}, ROT, False),
    "leg_won": ({"en": "LEG {n}", "de": "LEG {n}"}, GRUEN, False),
    "set_won": ({"en": "SET {n}", "de": "SATZ {n}"}, GRUEN, False),
    "match_won": ({"en": "{n} WINS", "de": "{n} GEWINNT"}, GELB, True),
    "tournament_won": ({"en": "{n} WINS THE TOURNAMENT", "de": "{n} GEWINNT DAS TURNIER"}, GELB, True),
    "bullseye": ({"en": "BULLSEYE", "de": "BULLSEYE"}, ROT, False),
}
# a checkout of 100+ also fires "checkout", a 180 is never also a 140+: one effect per visit is enough
_VORRANG = ("tournament_won", "match_won", "nine_darter", "set_won", "leg_won", "high_finish", "checkout", "one_eighty",
            "ton_forty", "bust", "bullseye")


def _fehler(schluessel: str, **platz: str) -> ServiceValidationError:
    return ServiceValidationError(translation_domain=DOMAIN, translation_key=schluessel, translation_placeholders=platz or None)


def host_pruefen(roh: str) -> str:
    """Address as typed (with or without http://, with a port) -> host[:port]; error if it is not one."""
    host = re.sub(r"^https?://", "", (roh or "").strip(), flags=re.I).strip("/").split("/")[0]
    if not HOST.match(host):
        raise _fehler("pixel_bad_address")
    return host


def _rgb(farbe: str) -> dict[str, int]:
    h = farbe.lstrip("#")
    return {"r": int(h[0:2], 16), "g": int(h[2:4], 16), "b": int(h[4:6], 16)}


def _kurz(name: str, laenge: int = 8) -> str:
    return (name or "?").strip().upper()[:laenge]


def _feld(f: str) -> str:
    if not f:
        return ""
    if f in ("D25", "Bull"):
        return "BULL"
    if f == "S25":
        return "25"
    return f


def wert(a: dict[str, Any], p: dict[str, Any]) -> str:
    """The big number of a player, as on the TV: rest (X01), target (Around the Clock), number (Killer) …"""
    art = a.get("art") or "x01"
    if art in ("atc", "nine_lives"):
        return "BULL" if p.get("fertig") else _feld(str(p.get("ziel") or ""))
    if art == "killer":
        return str(p["nummer"]) if p.get("nummer") is not None else ""
    for k in ("rest", "punkte"):
        if p.get(k) is not None:
            return str(p[k])
    return ""


def anzeige(a: dict[str, Any], sprache: str) -> list[dict[str, str]] | None:
    """What the display shows now, as coloured pieces; None = no game (give the display back)."""
    phase = a.get("phase")
    sp = a.get("spieler") or []
    if phase == "bulloff":
        return [{"t": "BULL-OFF", "c": ORANGE}]
    if phase == "beendet" and a.get("gewinner") is not None and a["gewinner"] < len(sp):
        name = _kurz((a.get("turnier") or {}).get("sieger") or sp[a["gewinner"]].get("name"))
        return [{"t": name, "c": GELB}, {"t": " GEWINNT" if sprache == "de" else " WINS", "c": WEISS}]
    if phase != "laeuft" or not sp:
        return None
    am = a.get("am_zug") or 0
    p = sp[am] if am < len(sp) else sp[0]
    name = _kurz(p.get("werfer") or p.get("name"), 6)
    teile = [{"t": name + " ", "c": WEISS}, {"t": wert(a, p) or "-", "c": ORANGE}]
    au = a.get("aufnahme") or {}
    if au.get("bust"):
        teile[1] = {"t": "BUST", "c": ROT}
    return teile


class PixelAnzeigen:
    """Sends the game to AWTRIX 3 and PixelIt displays in the home network."""

    daten: DartsDaten  # set once the integration is ready

    def __init__(self, hass: HomeAssistant) -> None:
        self.hass = hass
        self._abmelden: list[Callable[[], None]] = []
        self._zuletzt: dict[str, Any] = {}  # host -> what it shows (to send only changes)
        self._status: dict[str, bool] = {}  # host -> answered the last time
        self._halt: dict[str, CALLBACK_TYPE] = {}  # PixelIt shows an effect: the score waits
        self._offen = False  # a change waits to be sent
        self._sieger_timer: CALLBACK_TYPE | None = None  # gives the display back a minute after the game
        self._arbeiter: asyncio.Task[None] | None = None
        self._wartend: tuple[str, dict[str, Any]] | None = None  # effect of this visit, shown a moment later

    # ---------- settings ----------

    @property
    def einst(self) -> dict[str, Any]:
        e: dict[str, Any] = self.daten.spiel.daten.setdefault("pixel", {})
        e.setdefault("an", True)
        e.setdefault("effekte", True)
        e["geraete"] = [g for g in e.get("geraete") or [] if isinstance(g, dict) and g.get("typ") in TYPEN and g.get("host")]
        return e

    def _sprache(self) -> str:
        return "de" if (self.hass.config.language or "").startswith("de") else "en"

    def vorschau(self) -> list[dict[str, str]] | None:
        sp = self.daten.spiel
        if not sp.spiel:
            return None
        a = sp.spiel_attribute()
        if a.get("phase") == "beendet":
            ende = dt_util.parse_datetime(str(a.get("ende") or ""))
            rest = SIEGER_ZEIT - (dt_util.now() - ende).total_seconds() if ende else 0
            if rest <= 0:
                return None
            if self._sieger_timer is None and self.einst["geraete"]:
                @callback
                def weiter(_now: Any = None) -> None:
                    self._sieger_timer = None
                    self._planen()
                    self._gespeichert()

                self._sieger_timer = async_call_later(self.hass, rest + 0.5, weiter)
        return anzeige(a, self._sprache())

    def attribute(self) -> dict[str, Any]:
        e = self.einst
        return {"an": e["an"], "effekte": e["effekte"],
                "geraete": [{"host": g["host"], "typ": g["typ"], "name": g.get("name") or g["host"],
                             "version": g.get("version") or "", "online": self._status.get(g["host"])}
                            for g in e["geraete"]],
                "vorschau": self.vorschau() if e["an"] else None}

    async def setzen(self, an: bool | None, effekte: bool | None) -> None:
        e = self.einst
        if an is not None:
            e["an"] = an
        if effekte is not None:
            e["effekte"] = effekte
        self._zuletzt.clear()
        if not e["an"]:
            await asyncio.gather(*(self._freigeben(g) for g in e["geraete"]))
        self._gespeichert()
        self._planen()

    async def hinzufuegen(self, roh: str) -> dict[str, Any]:
        host = host_pruefen(roh)
        e = self.einst
        if any(g["host"] == host for g in e["geraete"]):
            raise _fehler("pixel_exists", host=host)
        if len(e["geraete"]) >= MAX_GERAETE:
            raise _fehler("pixel_too_many")
        typ, name, version = await self._erkennen(host)
        if typ is None:
            raise _fehler("pixel_not_found", host=host)
        g = {"host": host, "typ": typ, "name": name, "version": version}
        e["geraete"].append(g)
        self._status[host] = True
        self._gespeichert()
        await self._effekt_an(g, [{"t": "DARTNEST", "c": ORANGE}], True)
        self._planen()
        return g

    async def entfernen(self, roh: str) -> None:
        host = host_pruefen(roh)
        e = self.einst
        weg = [g for g in e["geraete"] if g["host"] == host]
        e["geraete"] = [g for g in e["geraete"] if g["host"] != host]
        for g in weg:
            await self._freigeben(g)
            self._zuletzt.pop(host, None)
            self._status.pop(host, None)
        self._gespeichert()

    async def testen(self, roh: str | None) -> None:
        e = self.einst
        host = host_pruefen(roh) if roh else None
        ziele = [g for g in e["geraete"] if host is None or g["host"] == host]
        if not ziele:
            raise _fehler("pixel_none")
        text = "HALLO VON DARTNEST" if self._sprache() == "de" else "HELLO FROM DARTNEST"
        ok = await asyncio.gather(*(self._effekt_an(g, [{"t": text, "c": ORANGE}], True) for g in ziele))
        self._gespeichert()
        if not all(ok):
            raise _fehler("pixel_offline", host=", ".join(g["host"] for g, o in zip(ziele, ok, strict=True) if not o))

    def _gespeichert(self) -> None:
        self.daten.spiel.einstellung_gespeichert()

    # ---------- running ----------

    def starten(self) -> None:
        self._abmelden = [self.daten.spiel.hoerer(self._planen), self.daten.spiel.ereignis_hoerer(self.ereignis)]
        self._planen()

    async def beenden(self) -> None:
        for ab in self._abmelden:
            ab()
        self._abmelden = []
        for ab in self._halt.values():
            ab()
        self._halt.clear()
        if self._sieger_timer:
            self._sieger_timer()
            self._sieger_timer = None
        if self._arbeiter:
            self._arbeiter.cancel()
            try:
                await self._arbeiter
            except asyncio.CancelledError:
                pass
            self._arbeiter = None

    @callback
    def _planen(self) -> None:
        """Something changed: bring the displays up to date (one short task, only while there is something to send)."""
        e = self.einst
        if not (e["an"] and e["geraete"]):
            return
        self._offen = True
        if self._arbeiter is None or self._arbeiter.done():
            self._arbeiter = self.hass.async_create_background_task(self._arbeiten(), "dartnest pixel")

    async def _arbeiten(self) -> None:
        while self._offen:
            self._offen = False
            try:
                await self._abgleichen()
            except Exception:  # never stop because of one display
                _LOGGER.exception("Pixel display update failed")
            await asyncio.sleep(0.3)  # several changes of one dart in one message

    async def _abgleichen(self) -> None:
        e = self.einst
        if not e["an"] or not e["geraete"]:
            return
        jetzt = self.vorschau()
        await asyncio.gather(*(self._zeigen(g, jetzt) for g in e["geraete"] if g["host"] not in self._halt))

    async def _zeigen(self, g: dict[str, Any], teile: list[dict[str, str]] | None) -> None:
        host = g["host"]
        if host in self._zuletzt and self._zuletzt[host] == teile:
            return
        neu_im_spiel = teile is not None and self._zuletzt.get(host) is None
        if teile is None:
            ok = await self._freigeben(g)
        elif g["typ"] == "awtrix":
            ok = await self._senden(host, f"custom?name={APP}", {"text": teile, "lifetime": LEBEN, "center": True})
            if ok and neu_im_spiel:
                await self._senden(host, "switch", {"name": APP})
        else:
            ok = await self._senden(host, "screen", _pixelit_text(teile))
        if ok:
            self._zuletzt[host] = teile
        else:
            self._zuletzt.pop(host, None)

    async def _freigeben(self, g: dict[str, Any]) -> bool:
        """Remove DartNest from the display: AWTRIX goes on with its apps, PixelIt shows the clock."""
        if g["typ"] == "awtrix":
            return await self._senden(g["host"], f"custom?name={APP}", None)
        return await self._senden(g["host"], "screen", {"clock": {"show": True, "switchAktiv": False, "withSeconds": False,
                                                                 "color": _rgb(WEISS)}})

    @callback
    def ereignis(self, typ: str, daten: dict[str, Any]) -> None:
        e = self.einst
        if not (e["an"] and e["effekte"] and e["geraete"]) or typ not in EFFEKTE:
            return
        # one visit fires several events (checkout + leg + match): only the most important one is shown
        if self._wartend and _VORRANG.index(self._wartend[0]) <= _VORRANG.index(typ):
            return
        if self._wartend is None:
            async_call_later(self.hass, 0.2, self._effekt_jetzt)
        self._wartend = (typ, daten)

    @callback
    def _effekt_jetzt(self, _now: Any = None) -> None:
        if not self._wartend:
            return
        typ, daten = self._wartend
        self._wartend = None
        texte, farbe, regenbogen = EFFEKTE[typ]
        text = texte[self._sprache()].format(n=_kurz(str(daten.get("player") or ""), 10), w=daten.get("finish") or daten.get("score") or "")
        for g in self.einst["geraete"]:
            self.hass.async_create_task(self._effekt_an(g, [{"t": text, "c": farbe}], regenbogen))

    async def _effekt_an(self, g: dict[str, Any], teile: list[dict[str, str]], regenbogen: bool) -> bool:
        host = g["host"]
        if g["typ"] == "awtrix":
            return await self._senden(host, "notify", {"text": teile, "rainbow": regenbogen, "duration": EFFEKT_DAUER,
                                                       "stack": False, "wakeup": True, "center": True})
        # PixelIt has no notifications: show the effect, then the score again
        if ab := self._halt.pop(host, None):
            ab()
        ok = await self._senden(host, "screen", _pixelit_text(teile))

        @callback
        def weiter(_now: Any = None) -> None:
            self._halt.pop(host, None)
            self._zuletzt.pop(host, None)
            self._planen()

        self._halt[host] = async_call_later(self.hass, EFFEKT_DAUER, weiter)
        return ok

    # ---------- network ----------

    async def _senden(self, host: str, pfad: str, daten: dict[str, Any] | None) -> bool:
        session = async_get_clientsession(self.hass)
        try:
            async with asyncio.timeout(ZEIT):
                async with session.post(f"http://{host}/api/{pfad}", json=daten if daten is not None else None,
                                        data=b"" if daten is None else None) as antwort:
                    ok = antwort.status < 300
        except (aiohttp.ClientError, TimeoutError) as err:
            _LOGGER.debug("Pixel display %s does not answer: %s", host, err)
            ok = False
        if self._status.get(host) != ok:
            self._status[host] = ok
            self.hass.loop.call_soon(self.daten.spiel.einstellung_gespeichert)
        return ok

    async def _erkennen(self, host: str) -> tuple[str | None, str, str]:
        """Which display answers at this address: AWTRIX 3 (/api/stats) or PixelIt (/api/matrixinfo)."""
        session = async_get_clientsession(self.hass)
        for typ, pfad in (("awtrix", "stats"), ("pixelit", "matrixinfo")):
            try:
                async with asyncio.timeout(ZEIT):
                    async with session.get(f"http://{host}/api/{pfad}") as antwort:
                        if antwort.status != 200:
                            continue
                        info = await antwort.json(content_type=None)
            except (aiohttp.ClientError, TimeoutError, ValueError):
                continue
            if not isinstance(info, dict):
                continue
            if typ == "awtrix":
                return typ, "AWTRIX 3", str(info.get("version") or "")
            return typ, "PixelIt", str(info.get("pixelitVersion") or "")
        return None, "", ""


def _pixelit_text(teile: list[dict[str, str]]) -> dict[str, Any]:
    """PixelIt shows one colour per text: the colour of the last piece (the score)."""
    text = "".join(t["t"] for t in teile)
    return {"text": {"textString": text, "bigFont": False, "scrollText": "auto", "scrollTextDelay": 40, "centerText": True,
                     "position": {"x": 0, "y": 1}, "color": _rgb(teile[-1]["c"])}}
