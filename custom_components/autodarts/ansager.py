"""Caller: announces scores, checkouts and walk-on songs on the speakers of Home Assistant.

Runs in Home Assistant (also when no dashboard is open). Settings are kept in the storage
autodarts.ansager and edited in the caller card. Sound packs are folders in the media
folder autodarts/caller/<pack> with files like 180.mp3, bust.mp3, leg.mp3; whatever a pack
does not have is spoken by the chosen voice (TTS). Walk-on songs are files in
autodarts/walkon.
"""

from __future__ import annotations

import asyncio
from collections.abc import Callable
import logging
from pathlib import Path
from typing import Any

from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.storage import Store
import voluptuous as vol

_LOGGER = logging.getLogger(__name__)

ORDNER = ("autodarts", "caller")
SONG_ORDNER = ("autodarts", "walkon")
ENDUNGEN = (".mp3", ".wav", ".ogg", ".m4a", ".flac")
MEDIA_ANNOUNCE = 1048576  # MediaPlayerEntityFeature.MEDIA_ANNOUNCE


def _player(wert: Any) -> str:
    text = str(wert)
    if not text.startswith("media_player."):
        raise vol.Invalid("only media players")  # noqa: TRY003
    return text


EINSTELLUNGEN = vol.Schema({
    vol.Optional("aktiv", default=False): bool,
    vol.Optional("lautsprecher", default=[]): [_player],
    vol.Optional("stimme", default=""): str,
    vol.Optional("pack", default=""): str,
    vol.Optional("punkte", default=True): bool,
    vol.Optional("rest", default=True): bool,
    vol.Optional("ende", default=True): bool,
    vol.Optional("besondere", default=True): bool,
    vol.Optional("game_on", default=True): bool,
    vol.Optional("walkon", default=True): bool,
    vol.Optional("walkon_sekunden", default=15): vol.All(vol.Coerce(int), vol.Range(5, 60)),
    vol.Optional("songs", default={}): {str: str},
}, extra=vol.REMOVE_EXTRA)

TEXTE = {
    "en": {
        "180": "One hundred and eighty!", "bust": "No score!", "rest": "{n}, you require {r}",
        "game_on": "Game on!", "leg": "Game shot, and the leg, {n}!", "set": "Game shot, and the set, {n}!",
        "match": "Game shot, and the match, {n}!", "nine": "A nine-darter! {n}!", "tournament": "{n} wins the tournament!",
        "shanghai": "Shanghai, {n}!", "killer": "{n} is a killer!", "eliminated": "{n} is out!", "walk": "Ladies and gentlemen: {n}!",
    },
    "de": {
        "180": "Einhundertachtzig!", "bust": "Überworfen!", "rest": "{n}, du brauchst {r}",
        "game_on": "Game on!", "leg": "Game shot! Leg für {n}!", "set": "Game shot! Satz für {n}!",
        "match": "Game shot! Spiel für {n}!", "nine": "Ein Neun-Darter! {n}!", "tournament": "{n} gewinnt das Turnier!",
        "shanghai": "Shanghai, {n}!", "killer": "{n} ist Killer!", "eliminated": "{n} ist raus!", "walk": "Meine Damen und Herren: {n}!",
    },
}


def _dateien(ordner: Path) -> dict[str, str]:
    """Sound files of a folder by their name without ending (180, bust …)."""
    if not ordner.is_dir():
        return {}
    return {d.stem.lower(): d.name for d in sorted(ordner.iterdir()) if d.is_file() and d.suffix.lower() in ENDUNGEN}


def _uebersicht(basis: Path) -> dict[str, Any]:
    """Packs and songs in the media folder; creates the folders so they show up in the media browser."""
    packs: dict[str, list[str]] = {}
    for teil in (ORDNER, SONG_ORDNER):
        try:
            basis.joinpath(*teil).mkdir(parents=True, exist_ok=True)
        except OSError:
            pass
    caller = basis.joinpath(*ORDNER)
    if caller.is_dir():
        for d in sorted(caller.iterdir()):
            if d.is_dir():
                packs[d.name] = sorted(_dateien(d))
    return {"packs": packs, "songs": sorted(_dateien(basis.joinpath(*SONG_ORDNER)).values())}


class Ansager:
    """Turns game events into announcements on the chosen speakers."""

    def __init__(self, hass: HomeAssistant, stand: Callable[[], dict[str, Any] | None]) -> None:
        self.hass = hass
        self._stand = stand
        self._store: Store[dict[str, Any]] = Store(hass, 1, "autodarts.ansager")
        self.einst: dict[str, Any] = EINSTELLUNGEN({})
        self._puffer: list[tuple[str, dict[str, Any]]] = []
        self._geplant = False
        self._pack: dict[str, str] = {}
        self._aufgaben: set[asyncio.Task[None]] = set()
        self._einlauf: asyncio.Task[None] | None = None

    @property
    def _basis(self) -> Path:
        return Path(self.hass.config.media_dirs.get("local") or self.hass.config.path("media"))

    async def laden(self) -> None:
        try:
            self.einst = EINSTELLUNGEN((await self._store.async_load()) or {})
        except vol.Invalid as err:
            _LOGGER.warning("Caller settings ignored: %s", err)
        await self._pack_lesen()

    async def setzen(self, einst: dict[str, Any]) -> None:
        self.einst = EINSTELLUNGEN(dict(einst))
        await self._store.async_save(self.einst)
        await self._pack_lesen()

    async def uebersicht(self) -> dict[str, Any]:
        daten = await self.hass.async_add_executor_job(_uebersicht, self._basis)
        stimmen = sorted(self.hass.states.async_entity_ids("tts"))
        return {"einstellungen": self.einst, "stimmen": stimmen, **daten}

    async def _pack_lesen(self) -> None:
        pack = self.einst["pack"]
        self._pack = await self.hass.async_add_executor_job(_dateien, self._basis.joinpath(*ORDNER, pack)) if pack else {}

    async def beenden(self) -> None:
        for t in [*self._aufgaben, self._einlauf]:
            if t:
                t.cancel()
        await asyncio.gather(*[t for t in [*self._aufgaben, self._einlauf] if t], return_exceptions=True)

    # -- events ---------------------------------------------------------------------

    @callback
    def ereignis(self, typ: str, daten: dict[str, Any]) -> None:
        """Game event from the game manager; events of one visit come together and give one announcement."""
        if not self.einst["aktiv"] or not self.einst["lautsprecher"]:
            return
        if typ == "game_started":
            if self._einlauf:
                self._einlauf.cancel()
            self._einlauf = self.hass.async_create_background_task(self._spielbeginn(daten), "autodarts walk-on")
            return
        if typ == "dart":
            return
        self._puffer.append((typ, daten))
        if not self._geplant:
            self._geplant = True
            self.hass.loop.call_soon(self._auswerten)

    @callback
    def _auswerten(self) -> None:
        self._geplant = False
        puffer, self._puffer = self._puffer, []
        if teil := self.ansage(puffer):
            self._los(self._sagen(*teil))

    def ansage(self, puffer: list[tuple[str, dict[str, Any]]]) -> tuple[str, str] | None:
        """(sound file key, text) for the events of one visit, or None."""
        e, tx = dict(puffer), self._t()
        st = self._stand() or {}
        name = next((d.get("player") for _, d in puffer if d.get("player")), "")
        if "tournament_won" in e and self.einst["ende"]:
            return "tournament", tx["tournament"].format(n=e["tournament_won"].get("player", name))
        if self.einst["besondere"] and "nine_darter" in e:
            return "nine", tx["nine"].format(n=name)
        for k, schluessel in (("match_won", "match"), ("set_won", "set"), ("leg_won", "leg")):
            if k in e and self.einst["ende"]:
                return schluessel, tx[schluessel].format(n=e[k].get("player", name))
        if self.einst["besondere"]:
            for k in ("shanghai", "killer", "eliminated"):
                if k in e:
                    return k, tx[k].format(n=e[k].get("player", name))
        if "visit" not in e or st.get("art", "x01") not in ("x01", "highscore"):
            return None
        teile: list[str] = []
        schluessel = ""
        if self.einst["punkte"]:
            if "bust" in e:
                schluessel, text = "bust", tx["bust"]
            else:
                p = int(e["visit"].get("score") or 0)
                schluessel, text = str(p), (tx["180"] if p == 180 else str(p))
            teile.append(text)
        if self.einst["rest"] and st.get("art", "x01") == "x01" and st.get("gewinner") is None:
            spieler = st.get("spieler") or []
            zug = st.get("am_zug")
            wer = spieler[zug] if isinstance(zug, int) and zug < len(spieler) else {}
            if wer and not wer.get("bot") and 1 < int(wer.get("rest") or 0) <= 170 and st.get("weg"):
                teile.append(tx["rest"].format(n=wer.get("name", ""), r=wer["rest"]))
                if len(teile) > 1:
                    schluessel = ""  # a file would leave out the rest
        return (schluessel, ". ".join(teile)) if teile else None

    async def _spielbeginn(self, daten: dict[str, Any]) -> None:
        """Walk-on songs of the players (each for some seconds), then "Game on"."""
        try:
            if self.einst["walkon"]:
                for sid, name in zip(daten.get("player_ids") or [], daten.get("players") or [], strict=False):
                    song = self.einst["songs"].get(str(sid)) if sid else None
                    if not song:
                        continue
                    await self._sagen("", self._t()["walk"].format(n=name))
                    await asyncio.sleep(3)
                    await self._spielen(self._url(SONG_ORDNER, song), ansage=False)
                    await asyncio.sleep(self.einst["walkon_sekunden"])
                    await self._dienst("media_player", "media_stop", {"entity_id": self.einst["lautsprecher"]})
            if self.einst["game_on"]:
                await self._sagen("game_on", self._t()["game_on"])
        except asyncio.CancelledError:
            pass
        except Exception:  # a speaker that does not answer must not break the game
            _LOGGER.warning("Walk-on failed", exc_info=True)

    # -- output -----------------------------------------------------------------------

    def _t(self) -> dict[str, str]:
        return TEXTE["de" if str(self.hass.config.language).startswith("de") else "en"]

    def _url(self, teil: tuple[str, ...], datei: str) -> str:
        return "media-source://media_source/local/" + "/".join((*teil, datei))

    def _los(self, coro: Any) -> None:
        t = self.hass.async_create_background_task(coro, "autodarts caller")
        self._aufgaben.add(t)
        t.add_done_callback(self._aufgaben.discard)

    async def testen(self, text: str | None = None) -> None:
        await self._sagen("180", text or self._t()["180"])

    async def _sagen(self, schluessel: str, text: str) -> None:
        """Play the pack file of the key, or speak the text."""
        try:
            if schluessel and schluessel.lower() in self._pack:
                await self._spielen(self._url((*ORDNER, self.einst["pack"]), self._pack[schluessel.lower()]))
                return
            stimme = self.einst["stimme"] if self.hass.states.get(self.einst["stimme"]) else next(
                iter(sorted(self.hass.states.async_entity_ids("tts"))), "")
            if not stimme:
                _LOGGER.warning("Caller: no voice (TTS) available")
                return
            await self._dienst("tts", "speak", {"entity_id": stimme, "media_player_entity_id": self.einst["lautsprecher"],
                                                "message": text, "cache": True})
        except asyncio.CancelledError:
            raise
        except Exception:
            _LOGGER.warning("Caller could not play %s", schluessel or text, exc_info=True)

    async def _spielen(self, url: str, ansage: bool = True) -> None:
        mit: list[str] = []
        ohne: list[str] = []
        for e in self.einst["lautsprecher"]:
            s = self.hass.states.get(e)
            (mit if ansage and s and int(s.attributes.get("supported_features") or 0) & MEDIA_ANNOUNCE else ohne).append(e)
        for liste, extra in ((mit, {"announce": True}), (ohne, {})):
            if liste:
                await self._dienst("media_player", "play_media", {"entity_id": liste, "media_content_id": url,
                                                                  "media_content_type": "music", **extra})

    async def _dienst(self, domain: str, name: str, daten: dict[str, Any]) -> None:
        await self.hass.services.async_call(domain, name, daten, blocking=True)
