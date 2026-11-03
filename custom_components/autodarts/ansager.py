"""Caller: announces scores, checkouts and walk-on songs on the speakers of Home Assistant.

Runs in Home Assistant (also when no dashboard is open). Settings are kept in the storage
autodarts.ansager and edited in the caller card. Sound packs are folders in the media
folder autodarts/caller/<pack> with files like 180.mp3, bust.mp3, leg.mp3; whatever a pack
does not have is spoken by the chosen voice (TTS). Walk-on songs are files in
autodarts/walkon.

Phones and tablets get the same announcements: the game card subscribes with its speaker
button (websocket autodarts/ansager/hoeren) and plays the URLs it is sent.

A pack can also be made here (ansager_pack_erzeugen): every score, "you require", player names and
game shot spoken once by the chosen voice – with Google AI in the style of a championship stage
announcer – and saved as files. A visit like "140 · Ben, you require 100" is joined from these files.
"""

from __future__ import annotations

import asyncio
from collections.abc import Callable
import hashlib
import logging
from pathlib import Path
import re
import shutil
from typing import Any
import wave

from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.storage import Store
import voluptuous as vol

_LOGGER = logging.getLogger(__name__)

ORDNER = ("autodarts", "caller")
SONG_ORDNER = ("autodarts", "walkon")
ENDUNGEN = (".mp3", ".wav", ".ogg", ".m4a", ".flac")
MEDIA_ANNOUNCE = 1048576  # MediaPlayerEntityFeature.MEDIA_ANNOUNCE
MIX = "_mix"  # joined announcements of a pack (cache)
MIX_MAX = 300
PAUSE = 6.5  # seconds between two sounds: Google AI allows 10 a minute
UNMOEGLICH = {163, 166, 169, 172, 173, 175, 176, 178, 179}  # scores three darts cannot make
GOOGLE_AI = "google_generative_ai_conversation"  # voices that follow a spoken style instruction
# short "Say …:" direction as in the Gemini speech docs; a longer one is read out loud
STIL = {
    "en": "Say loudly like an excited darts stage announcer: ",
    "de": "Sag laut und begeistert wie ein Darts-Ansager: ",
}


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
    vol.Optional("stil", default=True): bool,
}, extra=vol.REMOVE_EXTRA)

TEXTE = {
    "en": {
        "180": "One hundred and eighty!", "bust": "No score!", "rest": "{n}, you require {r}",
        "game_on": "Game on!", "leg": "Game shot, and the leg, {n}!", "set": "Game shot, and the set, {n}!",
        "match": "Game shot, and the match, {n}!", "nine": "A nine-darter! {n}!", "tournament": "{n} wins the tournament!",
        "shanghai": "Shanghai, {n}!", "killer": "{n} is a killer!", "eliminated": "{n} is out!", "walk": "Ladies and gentlemen: {n}!",
        "require": "you require", "0": "No score!",
        "p_require": "You require", "p_leg": "Game shot, and the leg!", "p_set": "Game shot, and the set!",
        "p_match": "Game shot, and the match!", "p_nine": "A nine-darter!", "p_tournament": "wins the tournament!",
        "p_walk": "Ladies and gentlemen!",
    },
    "de": {
        "180": "Einhundertachtzig!", "bust": "Überworfen!", "rest": "{n}, du brauchst {r}",
        "game_on": "Game on!", "leg": "Game shot! Leg für {n}!", "set": "Game shot! Satz für {n}!",
        "match": "Game shot! Spiel für {n}!", "nine": "Ein Neun-Darter! {n}!", "tournament": "{n} gewinnt das Turnier!",
        "shanghai": "Shanghai, {n}!", "killer": "{n} ist Killer!", "eliminated": "{n} ist raus!", "walk": "Meine Damen und Herren: {n}!",
        "require": "du brauchst", "0": "No score!",
        "p_require": "Du brauchst", "p_leg": "Game shot! Und das Leg!", "p_set": "Game shot! Und der Satz!",
        "p_match": "Game shot! Und das Spiel!", "p_nine": "Ein Neun-Darter!", "p_tournament": "gewinnt das Turnier!",
        "p_walk": "Meine Damen und Herren!",
    },
}


def _slug(name: Any) -> str:
    return "name_" + (re.sub(r"\W+", "_", str(name).lower()).strip("_") or "x")


def _mischen(ordner: Path, dateien: list[str]) -> str | None:
    """Join the WAV files of one announcement (with a short pause) into ordner/_mix; None if not possible."""
    name = hashlib.sha1("+".join(dateien).encode()).hexdigest()[:16] + ".wav"
    ziel = ordner / MIX / name
    if ziel.is_file():
        return name
    teile: list[bytes] = []
    art = None
    for d in dateien:
        try:
            with wave.open(str(ordner / d), "rb") as w:
                a = (w.getnchannels(), w.getsampwidth(), w.getframerate())
                if art not in (None, a):
                    return None
                art = a
                teile.append(w.readframes(w.getnframes()))
        except (OSError, wave.Error, EOFError):
            return None
    if not art:
        return None
    pause = b"\0" * int(art[2] * 0.12) * art[0] * art[1]
    ziel.parent.mkdir(exist_ok=True)
    alte = sorted(ziel.parent.glob("*.wav"), key=lambda f: f.stat().st_mtime)
    for f in alte[: max(0, len(alte) - MIX_MAX + 1)]:
        f.unlink(missing_ok=True)
    with wave.open(str(ziel), "wb") as w:
        w.setnchannels(art[0])
        w.setsampwidth(art[1])
        w.setframerate(art[2])
        w.writeframes(pause.join(teile))
    return name


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
        self._hoerer: set[Callable[[dict[str, Any]], None]] = set()
        self.erzeugung: dict[str, Any] = {}
        self._erzeuger: asyncio.Task[None] | None = None

    @callback
    def hoeren(self, senden: Callable[[dict[str, Any]], None]) -> Callable[[], None]:
        """A phone or tablet that plays the announcements itself; returns the function to stop."""
        self._hoerer.add(senden)
        return lambda: self._hoerer.discard(senden)

    @property
    def _boxen(self) -> bool:
        return bool(self.einst["aktiv"] and self.einst["lautsprecher"])

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
        return {"einstellungen": self.einst, "stimmen": stimmen, "erzeugung": self.erzeugung, **daten}

    async def _pack_lesen(self) -> None:
        pack = self.einst["pack"]
        self._pack = await self.hass.async_add_executor_job(_dateien, self._basis.joinpath(*ORDNER, pack)) if pack else {}

    async def beenden(self) -> None:
        alle = [t for t in [*self._aufgaben, self._einlauf, self._erzeuger] if t]
        for t in alle:
            t.cancel()
        await asyncio.gather(*alle, return_exceptions=True)

    # -- events ---------------------------------------------------------------------

    @callback
    def ereignis(self, typ: str, daten: dict[str, Any]) -> None:
        """Game event from the game manager; events of one visit come together and give one announcement."""
        if not self._boxen and not self._hoerer:
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

    def ansage(self, puffer: list[tuple[str, dict[str, Any]]]) -> tuple[str, str, list[str]] | None:
        """(sound file key, text, keys of the pack files to join) for the events of one visit, or None."""
        e, tx = dict(puffer), self._t()
        st = self._stand() or {}
        name = next((d.get("player") for _, d in puffer if d.get("player")), "")
        if "tournament_won" in e and self.einst["ende"]:
            n = e["tournament_won"].get("player", name)
            return "tournament", tx["tournament"].format(n=n), [_slug(n), "tournament"]
        if self.einst["besondere"] and "nine_darter" in e:
            return "nine", tx["nine"].format(n=name), ["nine", _slug(name)]
        for k, schluessel in (("match_won", "match"), ("set_won", "set"), ("leg_won", "leg")):
            if k in e and self.einst["ende"]:
                n = e[k].get("player", name)
                return schluessel, tx[schluessel].format(n=n), [schluessel, _slug(n)]
        if self.einst["besondere"]:
            for k in ("shanghai", "killer", "eliminated"):
                if k in e:
                    return k, tx[k].format(n=e[k].get("player", name)), []
        if "visit" not in e or st.get("art", "x01") not in ("x01", "highscore"):
            return None
        teile: list[str] = []
        keys: list[str] = []
        schluessel = ""
        if self.einst["punkte"]:
            if "bust" in e:
                schluessel, text = "bust", tx["bust"]
            else:
                p = int(e["visit"].get("score") or 0)
                schluessel, text = str(p), (tx["180"] if p == 180 else str(p))
            teile.append(text)
            keys.append(schluessel)
        if self.einst["rest"] and st.get("art", "x01") == "x01" and st.get("gewinner") is None:
            spieler = st.get("spieler") or []
            zug = st.get("am_zug")
            wer = spieler[zug] if isinstance(zug, int) and zug < len(spieler) else {}
            if wer and not wer.get("bot") and 1 < int(wer.get("rest") or 0) <= 170 and st.get("weg"):
                teile.append(tx["rest"].format(n=wer.get("name", ""), r=wer["rest"]))
                keys += [_slug(wer.get("name", "")), "require", str(wer["rest"])]
                if len(teile) > 1:
                    schluessel = ""  # a single file would leave out the rest
        return (schluessel, ". ".join(teile), keys) if teile else None

    async def _spielbeginn(self, daten: dict[str, Any]) -> None:
        """Walk-on songs of the players (each for some seconds), then "Game on"."""
        try:
            if self.einst["walkon"]:
                for sid, name in zip(daten.get("player_ids") or [], daten.get("players") or [], strict=False):
                    song = self.einst["songs"].get(str(sid)) if sid else None
                    if not song:
                        continue
                    await self._sagen("", self._t()["walk"].format(n=name), ["walk", _slug(name)])
                    await asyncio.sleep(3)
                    await self._spielen(self._url(SONG_ORDNER, song), ansage=False)
                    await asyncio.sleep(self.einst["walkon_sekunden"])
                    if self._boxen:
                        await self._dienst("media_player", "media_stop", {"entity_id": self.einst["lautsprecher"]})
                    self._melden({"stop": True})
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

    def _stimme(self) -> str:
        if self.hass.states.get(self.einst["stimme"]):
            return str(self.einst["stimme"])
        return next(iter(sorted(self.hass.states.async_entity_ids("tts"))), "")

    def _google(self, stimme: str) -> bool:
        e = er.async_get(self.hass).async_get(stimme)
        return bool(e and e.platform == GOOGLE_AI)

    def _stil(self, stimme: str, text: str) -> str:
        """Text with the style instruction for voices that follow one (Google AI)."""
        if not self._google(stimme):
            return text
        return STIL["de" if str(self.hass.config.language).startswith("de") else "en"] + text

    async def _sagen(self, schluessel: str, text: str, keys: list[str] | None = None) -> None:
        """Play the pack files (joined), the pack file of the key, or speak the text."""
        try:
            if keys and len(keys) > 1 and all(k.lower() in self._pack for k in keys):
                ordner = self._basis.joinpath(*ORDNER, self.einst["pack"])
                datei = await self.hass.async_add_executor_job(_mischen, ordner, [self._pack[k.lower()] for k in keys])
                if datei:
                    await self._spielen(self._url((*ORDNER, self.einst["pack"], MIX), datei))
                    return
            if keys and len(keys) == 1:
                schluessel = keys[0]
            if schluessel and schluessel.lower() in self._pack:
                await self._spielen(self._url((*ORDNER, self.einst["pack"]), self._pack[schluessel.lower()]))
                return
            stimme = self._stimme()
            if not stimme:
                _LOGGER.warning("Caller: no voice (TTS) available")
                return
            if self.einst["stil"]:
                text = self._stil(stimme, text)
            if self._boxen:
                await self._dienst("tts", "speak", {"entity_id": stimme, "media_player_entity_id": self.einst["lautsprecher"],
                                                    "message": text, "cache": True})
            if self._hoerer:
                from homeassistant.components.tts import generate_media_source_id

                await self._handy(generate_media_source_id(self.hass, text, engine=stimme, cache=True))
        except asyncio.CancelledError:
            raise
        except Exception:
            _LOGGER.warning("Caller could not play %s", schluessel or text, exc_info=True)

    async def _spielen(self, url: str, ansage: bool = True) -> None:
        if self._hoerer:
            await self._handy(url)
        if not self._boxen:
            return
        mit: list[str] = []
        ohne: list[str] = []
        for e in self.einst["lautsprecher"]:
            s = self.hass.states.get(e)
            (mit if ansage and s and int(s.attributes.get("supported_features") or 0) & MEDIA_ANNOUNCE else ohne).append(e)
        for liste, extra in ((mit, {"announce": True}), (ohne, {})):
            if liste:
                await self._dienst("media_player", "play_media", {"entity_id": liste, "media_content_id": url,
                                                                  "media_content_type": "music", **extra})

    async def _handy(self, media_id: str) -> None:
        """Send a playable address (TTS or media file) to the phones and tablets that listen."""
        from homeassistant.components import media_source
        from homeassistant.components.media_player.browse_media import async_process_play_media_url

        item = await media_source.async_resolve_media(self.hass, media_id, None)
        self._melden({"url": async_process_play_media_url(self.hass, item.url, allow_relative_url=True)})

    @callback
    def _melden(self, daten: dict[str, Any]) -> None:
        for senden in list(self._hoerer):
            senden(daten)

    # -- making a pack ------------------------------------------------------------------

    def pack_texte(self, namen: list[str]) -> dict[str, str]:
        """File key → text of a full pack: scores 0–180, you require, game shot …, player names."""
        tx = self._t()
        texte = {str(p): (tx["180"] if p == 180 else tx["0"] if p == 0 else f"{p}!") for p in range(181) if p not in UNMOEGLICH}
        texte.update({"bust": tx["bust"], "game_on": tx["game_on"]})
        texte.update({k: tx["p_" + k] for k in ("require", "leg", "set", "match", "nine", "tournament", "walk")})
        texte.update({_slug(n): f"{n}!" for n in namen if n})
        return texte

    def pack_erzeugen(self, name: str, namen: list[str], sprecher: str | None, nur: list[str] | None, neu: bool = False) -> None:
        """Start making a pack in the background (keeps files that already exist, so it can be resumed)."""
        if self._erzeuger and not self._erzeuger.done():
            return
        texte = self.pack_texte(namen)
        if nur:
            texte = {k: v for k, v in texte.items() if k in nur}
        self.erzeugung = {"pack": name, "fertig": 0, "gesamt": len(texte), "laeuft": True, "fehler": None}
        self._erzeuger = self.hass.async_create_background_task(self._erzeugen(name, texte, sprecher, neu), "autodarts caller pack")

    async def _erzeugen(self, name: str, texte: dict[str, str], sprecher: str | None, neu: bool = False) -> None:
        from homeassistant.components.tts import async_get_media_source_audio, generate_media_source_id

        stimme = self._stimme()
        ordner = self._basis.joinpath(*ORDNER, name)
        st = self.erzeugung
        try:
            if not stimme:
                st["fehler"] = "no voice"
                return
            google = self._google(stimme)
            await self.hass.async_add_executor_job(lambda: ordner.mkdir(parents=True, exist_ok=True))
            da = set() if neu else set(await self.hass.async_add_executor_job(_dateien, ordner))
            for f in await self.hass.async_add_executor_job(lambda: list((ordner / MIX).glob("*.wav"))):
                await self.hass.async_add_executor_job(f.unlink)  # joined sounds would keep the old voice
            fehler = 0
            for key, text in texte.items():
                if key in da:
                    st["fertig"] += 1
                    continue
                while True:
                    try:
                        mid = generate_media_source_id(
                            self.hass, STIL["de" if str(self.hass.config.language).startswith("de") else "en"] + text if google else text,
                            engine=stimme, options={"voice": sprecher} if sprecher else None, cache=False)
                        endung, daten = await async_get_media_source_audio(self.hass, mid)
                        break
                    except asyncio.CancelledError:
                        raise
                    except Exception as err:  # rate limit of the voice service: wait and try again
                        fehler += 1
                        if "per_day" in str(err) or "PerDay" in str(err):
                            st["fehler"] = "daily limit"  # the voice allows only so many a day: continue tomorrow
                            return
                        if fehler > 6:
                            st["fehler"] = str(err)[:200]
                            return
                        await asyncio.sleep(20 * fehler)
                fehler = 0
                await self.hass.async_add_executor_job((ordner / f"{key}.{endung}").write_bytes, daten)
                st["fertig"] += 1
                if google:
                    await asyncio.sleep(PAUSE)
            if name != self.einst["pack"]:
                await self.setzen({**self.einst, "pack": name})  # the pack just made is used right away
            else:
                await self._pack_lesen()
        except asyncio.CancelledError:
            raise
        except Exception as err:
            _LOGGER.warning("Making the caller pack failed", exc_info=True)
            st["fehler"] = str(err)[:200]
        finally:
            st["laeuft"] = False

    async def pack_loeschen(self, name: str) -> None:
        """Delete a pack folder (only below autodarts/caller)."""
        if self._erzeuger and not self._erzeuger.done() and self.erzeugung.get("pack") == name:
            self._erzeuger.cancel()
        ordner = self._basis.joinpath(*ORDNER, name)
        if ordner.parent == self._basis.joinpath(*ORDNER):
            await self.hass.async_add_executor_job(lambda: shutil.rmtree(ordner, ignore_errors=True))
        if self.einst["pack"] == name:
            await self.setzen({**self.einst, "pack": ""})

    async def _dienst(self, domain: str, name: str, daten: dict[str, Any]) -> None:
        await self.hass.services.async_call(domain, name, daten, blocking=True)
