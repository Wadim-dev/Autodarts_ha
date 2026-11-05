"""TV scoreboard: a page without login for Fire TV, Google TV, Chromecast or any browser.

The page (frontend/tv.html) gets the game live over server-sent events. It shows the
scoreboard while a game runs and a rest screen (clock, ranking, last games) otherwise.
"""

from __future__ import annotations

import asyncio
from collections.abc import Callable
import hmac
import json
import logging
from pathlib import Path
import secrets
from typing import Any

from aiohttp import web
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError, ServiceValidationError
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.http import HomeAssistantView
from homeassistant.helpers.network import NoURLAvailableError, get_url

from . import auswertung
from .const import DOMAIN
from .spiel import Spielleiter

_LOGGER = logging.getLogger(__name__)

TV_URL = f"/{DOMAIN}/tv"
# TV platforms DartNest can start the page on
PLATTFORMEN = ("androidtv", "androidtv_remote", "cast")
SILK = "com.amazon.cloud9"
PING = 20.0
SILK_AUS = "DARTNEST_SILK_OFF"  # printed by the ADB command when Silk is switched off


def _adb_befehl(url: str) -> str:
    """Fire TV: Silk browser; marks a switched-off Silk; other Android TVs: their default browser."""
    oeffnen = f"am start -a android.intent.action.VIEW -d '{url}'"
    return (f"if pm list packages -e {SILK} | grep -q {SILK}; then {oeffnen} {SILK}; "
            f"elif pm path {SILK} >/dev/null 2>&1; then echo {SILK_AUS}; else {oeffnen}; fi")


def _fehler(schluessel: str, **platzhalter: str) -> ServiceValidationError:
    return ServiceValidationError(translation_domain=DOMAIN, translation_key=schluessel, translation_placeholders=platzhalter or None)


class Fernseher:
    """Settings of the TV page and starting it on the TVs."""

    def __init__(self, hass: HomeAssistant, spiel: Spielleiter) -> None:
        self.hass = hass
        self.spiel = spiel

    @property
    def einst(self) -> dict[str, Any]:
        e: dict[str, Any] = self.spiel.daten.setdefault("tv", {})
        if not e.get("token"):
            e["token"] = secrets.token_hex(16)
        e.setdefault("geraete", [])
        e.setdefault("auto", False)
        return e

    def token_passt(self, token: str) -> bool:
        return hmac.compare_digest(token.encode(), str(self.einst["token"]).encode())

    def url(self) -> str:
        """Address of the page in the home network (the TV reaches Home Assistant directly)."""
        try:
            basis = get_url(self.hass, allow_external=False, allow_cloud=False, prefer_external=False)
        except NoURLAvailableError:
            try:
                basis = get_url(self.hass)
            except NoURLAvailableError:
                return ""  # no network address set in Home Assistant yet
        return f"{basis}{TV_URL}/{self.einst['token']}"

    def attribute(self) -> dict[str, Any]:
        e = self.einst
        return {"geraete": list(e["geraete"]), "auto": bool(e["auto"]), "url": self.url()}

    async def setzen(self, geraete: list[str] | None, auto: bool | None, neuer_link: bool) -> None:
        e = self.einst
        if geraete is not None:
            e["geraete"] = [g for g in dict.fromkeys(geraete) if g]
        if auto is not None:
            e["auto"] = bool(auto)
        if neuer_link:
            e["token"] = secrets.token_hex(16)
        self.spiel.einstellung_gespeichert()

    # ---------- page on the TV ----------

    def _plattform(self, eid: str) -> str:
        eintrag = er.async_get(self.hass).async_get(eid)
        return eintrag.platform if eintrag else ""

    def _ziele(self, geraete: list[str] | None) -> list[str]:
        ziele = [g for g in (geraete or self.einst["geraete"]) if g]
        if not ziele:
            raise _fehler("no_tv")
        for g in ziele:
            if self._plattform(g) not in PLATTFORMEN:
                raise _fehler("tv_unsupported", entity=g)
        return ziele

    async def zeigen(self, geraete: list[str] | None = None) -> None:
        url = self.url()
        ziele = self._ziele(geraete)
        if not url:
            raise _fehler("tv_no_url")
        for eid in ziele:
            p = self._plattform(eid)
            try:
                if p == "androidtv":
                    # Fire TV: Silk browser; other Android TVs: their default browser
                    await self._dienst("media_player", "turn_on", eid)
                    await self._dienst("androidtv", "adb_command", eid, {"command": _adb_befehl(url)})
                    zustand = self.hass.states.get(eid)
                    antwort = str(zustand.attributes.get("adb_response") or "") if zustand else ""
                    if SILK_AUS in antwort:
                        raise _fehler("tv_silk_off", entity=eid)
                    if "Error" in antwort:
                        raise _fehler("tv_failed", entity=eid, error=antwort.strip().splitlines()[-1])
                elif p == "androidtv_remote":
                    await self._dienst("media_player", "turn_on", eid)
                    await self._dienst("media_player", "play_media", eid, {"media_content_type": "url", "media_content_id": url})
                else:
                    await self._cast(eid, url)
            except ServiceValidationError:
                raise
            except HomeAssistantError as err:
                raise _fehler("tv_failed", entity=eid, error=str(err)) from err

    async def beenden(self, geraete: list[str] | None = None) -> None:
        for eid in self._ziele(geraete):
            p = self._plattform(eid)
            try:
                if p == "androidtv":
                    await self._dienst("androidtv", "adb_command", eid, {"command": "HOME"})
                elif p == "androidtv_remote":
                    fernbedienung = self._fernbedienung(eid)
                    if fernbedienung:
                        await self.hass.services.async_call("remote", "send_command", {"entity_id": fernbedienung, "command": "HOME"}, blocking=True)
                else:
                    await self._dienst("media_player", "turn_off", eid)  # Chromecast: quits the page
            except HomeAssistantError as err:
                raise _fehler("tv_failed", entity=eid, error=str(err)) from err

    def _fernbedienung(self, eid: str) -> str | None:
        reg = er.async_get(self.hass)
        eintrag = reg.async_get(eid)
        if not eintrag or not eintrag.device_id:
            return None
        for e in er.async_entries_for_device(reg, eintrag.device_id):
            if e.domain == "remote":
                return e.entity_id
        return None

    async def _dienst(self, domain: str, dienst: str, eid: str, daten: dict[str, Any] | None = None) -> None:
        await self.hass.services.async_call(domain, dienst, {"entity_id": eid, **(daten or {})}, blocking=True)

    async def _cast(self, eid: str, url: str) -> None:
        """Chromecast and Google TV with Chromecast built-in: the page via DashCast."""
        komponente = self.hass.data.get("media_player")
        entitaet = komponente.get_entity(eid) if komponente is not None else None
        cc = getattr(entitaet, "_chromecast", None)
        if cc is None:
            raise _fehler("tv_failed", entity=eid, error="not connected")

        def laden() -> None:
            from pychromecast.controllers.dashcast import DashCastController  # type: ignore[import-not-found,unused-ignore]

            dash = DashCastController()
            cc.register_handler(dash)
            dash.load_url(url, force=True)

        await self.hass.async_add_executor_job(laden)

    def ereignis(self, typ: str, daten: dict[str, Any]) -> None:
        """Show the page by itself when a game starts (if switched on)."""
        if typ == "game_started" and self.einst["auto"] and self.einst["geraete"]:
            self.hass.async_create_task(self._auto())

    async def _auto(self) -> None:
        try:
            await self.zeigen()
        except HomeAssistantError as err:
            _LOGGER.warning("TV page could not be started: %s", err)

    # ---------- data for the page ----------

    def live(self) -> dict[str, Any]:
        sp = self.spiel
        rang = []
        for s in sp.daten["spieler"]:
            g = sp.daten["statistik"].get(s["id"], {})
            pr = sp.daten.get("profil", {}).get(s["id"], {})
            rang.append({
                "name": s["name"],
                "elo": round(pr.get("elo", auswertung.ELO_START)),
                "avg": round(g["punkte"] / g["darts"] * 3, 1) if g.get("darts") else 0,
                "spiele": g.get("spiele", 0),
                "siege": g.get("siege", 0),
                "n180": g.get("n180", 0),
            })
        rang.sort(key=lambda r: (-r["elo"], -r["avg"]))
        return {
            "spiel": sp.spiel_attribute(),
            "rang": rang[:8],
            "verlauf": [
                {"zeit": v.get("zeit"), "modus": v.get("modus"), "gewinner": v.get("gewinner"),
                 "spieler": [{"name": x.get("name"), "sieger": x.get("sieger"), "legs": x.get("legs")} for x in v.get("spieler") or []]}
                for v in (sp.daten.get("verlauf") or [])[:5]
            ],
            "sprache": self.hass.config.language,
        }


def _fernseher_fuer(hass: HomeAssistant, token: str) -> Fernseher | None:
    for eintrag in hass.config_entries.async_loaded_entries(DOMAIN):
        f: Fernseher = eintrag.runtime_data.fernseher
        if f.token_passt(token):
            return f
    return None


class TvSeite(HomeAssistantView):
    """The page itself, without login (the address contains a secret key)."""

    url = TV_URL + "/{token}"
    name = "autodarts:tv"
    requires_auth = False

    def __init__(self, html: str) -> None:
        self._html = html

    async def get(self, request: web.Request, token: str) -> web.Response:
        if _fernseher_fuer(request.app["hass"], token) is None:
            return web.Response(status=404)
        return web.Response(text=self._html, content_type="text/html", headers={"Cache-Control": "no-store"})


class TvLive(HomeAssistantView):
    """Live data of the page as server-sent events: one message per change."""

    url = TV_URL + "/{token}/live"
    name = "autodarts:tv:live"
    requires_auth = False

    async def get(self, request: web.Request, token: str) -> web.StreamResponse:
        hass: HomeAssistant = request.app["hass"]
        f = _fernseher_fuer(hass, token)
        if f is None:
            return web.Response(status=404)
        antwort = web.StreamResponse(headers={"Content-Type": "text/event-stream", "Cache-Control": "no-store", "X-Accel-Buffering": "no"})
        await antwort.prepare(request)
        neu = asyncio.Event()
        abmelden: Callable[[], None] = f.spiel.hoerer(neu.set)
        alt = ""
        try:
            while True:
                text = json.dumps(f.live(), ensure_ascii=False, default=str)
                if text != alt:
                    alt = text
                    await antwort.write(f"data: {text}\n\n".encode())
                else:
                    await antwort.write(b": ping\n\n")
                neu.clear()
                try:
                    await asyncio.wait_for(neu.wait(), PING)
                except TimeoutError:
                    pass
                await asyncio.sleep(0.12)  # several changes of one dart in one message
        except (ConnectionResetError, ConnectionError):
            pass
        finally:
            abmelden()
        return antwort


async def async_setup_tv(hass: HomeAssistant) -> None:
    """Register the page once for the whole integration."""
    if hass.http is None:
        return
    datei = Path(__file__).parent / "frontend" / "tv.html"
    html = await hass.async_add_executor_job(datei.read_text, "utf-8")
    hass.http.register_view(TvSeite(html))
    hass.http.register_view(TvLive())
