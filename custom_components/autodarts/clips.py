"""Highlight clips: the last seconds of a board camera as a short video at 180, high finish, match dart.

While a game runs (and the board detects), DartNest keeps the last seconds of the chosen
camera as still images in memory. At a highlight it turns them into an MP4 with ffmpeg,
straightened with the calibration like the board in the cards, and stores it under
media/dartnest/clips (also visible in the media browser).
"""

from __future__ import annotations

import asyncio
from collections import deque
from collections.abc import Callable
import logging
from pathlib import Path
import re
import secrets
import shutil
import subprocess
import tempfile
import time
from typing import TYPE_CHECKING, Any

from aiohttp import web
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ServiceValidationError
from homeassistant.helpers.http import HomeAssistantView
from homeassistant.util import dt as dt_util

from .board import Stream
from .const import DOMAIN

if TYPE_CHECKING:
    from .coordinator import DartsDaten

_LOGGER = logging.getLogger(__name__)

# events that can make a clip, best first (one visit can fire several: the best one names the clip)
ANLAESSE = ("match_won", "nine_darter", "high_finish", "one_eighty", "leg_won", "ton_forty", "checkout", "bullseye", "three_in_a_bed")
STANDARD_ANLAESSE = ["one_eighty", "high_finish", "match_won"]
KAMERAS = ("camera_1", "camera_2", "camera_3")
_STROEME: tuple[Stream, ...] = ("cam0", "cam1", "cam2")
VORHER = 8.0  # seconds before the event
NACHHER = 1.5  # seconds after it (the dart sits, the caller speaks)
FREI_MIN = 1_000_000_000  # no new clip when less than 1 GB is free on the disk
TAKT = 1 / 5  # time between images while recording (5 per second, light on the board PC)
GROESSE = 720  # straightened clip: square, px
RAND_MM = 225.0  # straightened clip shows ±225 mm around the bull (like the TV page)
DATEI = re.compile(r"^[0-9a-f]{12}\.(mp4|jpg)$")
CLIP_URL = f"/api/{DOMAIN}/clip"
RADIEN = (170.0, 162.0, 107.0, 99.0)


def _rang(art: str) -> int:
    return ANLAESSE.index(art) if art in ANLAESSE else len(ANLAESSE)


def _fehler(schluessel: str) -> ServiceValidationError:
    return ServiceValidationError(translation_domain=DOMAIN, translation_key=schluessel)


# ---------- calibration: camera image (px) -> board (mm), like entzerrung() in the cards ----------

def _mul(a: list[list[float]], b: list[list[float]]) -> list[list[float]]:
    return [[sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]


def _inv(m: list[list[float]]) -> list[list[float]] | None:
    (a, b, c), (d, e, f), (g, h, i) = m
    A, B, C = e * i - f * h, f * g - d * i, d * h - e * g
    det = a * A + b * B + c * C
    if abs(det) < 1e-12:
        return None
    return [[A / det, (c * h - b * i) / det, (b * f - c * e) / det],
            [B / det, (a * i - c * g) / det, (c * d - a * f) / det],
            [C / det, (b * g - a * h) / det, (a * e - b * d) / det]]


def homographie(kal: dict[str, Any] | None) -> list[list[float]] | None:
    """Least squares homography camera px -> board mm from the calibration points (4 rings × 20 + bull)."""
    import math

    if not kal or not kal.get("ringe"):
        return None
    src: list[tuple[float, float]] = []
    dst: list[tuple[float, float]] = []
    for j, ring in enumerate(kal["ringe"][:4]):
        for k, p in enumerate(ring or []):
            w = math.radians(9 + 18 * k)
            src.append((float(p[0]), float(p[1])))
            dst.append((RADIEN[j] * math.sin(w), -RADIEN[j] * math.cos(w)))
    bull = kal.get("bull")
    if isinstance(bull, (list, tuple)) and len(bull) >= 2:
        src.append((float(bull[0]), float(bull[1])))
        dst.append((0.0, 0.0))
    if len(src) < 8:
        return None
    mx = sum(p[0] for p in src) / len(src)
    my = sum(p[1] for p in src) / len(src)
    sd = sum(math.hypot(p[0] - mx, p[1] - my) for p in src)
    if not sd:
        return None
    sc = math.sqrt(2) * len(src) / sd
    M = [[0.0] * 9 for _ in range(8)]
    for (px, py), (u0, v0) in zip(src, dst, strict=True):
        x, y, u, v = (px - mx) * sc, (py - my) * sc, u0 / 170, v0 / 170
        for zeile in ([x, y, 1, 0, 0, 0, -u * x, -u * y, u], [0, 0, 0, x, y, 1, -v * x, -v * y, v]):
            for i in range(8):
                for k in range(9):
                    M[i][k] += zeile[i] * zeile[k]
    for i in range(8):
        m = max(range(i, 8), key=lambda r: abs(M[r][i]))
        M[i], M[m] = M[m], M[i]
        if abs(M[i][i]) < 1e-12:
            return None
        for r in range(8):
            if r != i:
                f = M[r][i] / M[i][i]
                for k in range(i, 9):
                    M[r][k] -= f * M[i][k]
    hv = [M[i][8] / M[i][i] for i in range(8)]
    H = [[hv[0], hv[1], hv[2]], [hv[3], hv[4], hv[5]], [hv[6], hv[7], 1.0]]
    return _mul(_mul([[170, 0, 0], [0, 170, 0], [0, 0, 1]], H), [[sc, 0, -sc * mx], [0, sc, -sc * my], [0, 0, 1]])


def ecken(kal: dict[str, Any] | None) -> list[tuple[float, float]] | None:
    """Camera pixels of the square ±225 mm around the bull: top left, top right, bottom left, bottom right."""
    H = homographie(kal)
    inv = _inv(H) if H else None
    if inv is None:
        return None
    punkte = []
    for x, y in ((-RAND_MM, -RAND_MM), (RAND_MM, -RAND_MM), (-RAND_MM, RAND_MM), (RAND_MM, RAND_MM)):
        w = inv[2][0] * x + inv[2][1] * y + inv[2][2]
        if abs(w) < 1e-9:
            return None
        punkte.append(((inv[0][0] * x + inv[0][1] * y + inv[0][2]) / w, (inv[1][0] * x + inv[1][1] * y + inv[1][2]) / w))
    return punkte


def _filter(eck: list[tuple[float, float]] | None) -> str:
    if not eck:
        return "scale=960:-2,format=yuv420p"
    p = ":".join(f"x{i}={x:.1f}:y{i}={y:.1f}" for i, (x, y) in enumerate(eck))
    return f"perspective={p}:sense=source:interpolation=linear,scale={GROESSE}:{GROESSE},setsar=1,format=yuv420p"


def _kodieren(ffmpeg: str, bilder: list[bytes], fps: float, eck: list[tuple[float, float]] | None, video: Path, vorschau: Path, mitte: int) -> bool:
    """Write the images as MP4 and a still image (runs in the executor)."""
    with tempfile.TemporaryDirectory() as tmp:
        for i, b in enumerate(bilder):
            (Path(tmp) / f"{i:04d}.jpg").write_bytes(b)
        vf = _filter(eck)
        try:
            r = subprocess.run([ffmpeg, "-y", "-v", "error", "-framerate", f"{fps:.3f}", "-i", str(Path(tmp) / "%04d.jpg"),
                                "-vf", vf, "-c:v", "libx264", "-preset", "veryfast", "-crf", "25", "-r", "25",
                                "-movflags", "+faststart", str(video)], capture_output=True, timeout=120, check=False)
            if r.returncode != 0:
                _LOGGER.warning("Clip could not be made: %s", r.stderr.decode(errors="replace")[-300:])
                return False
            subprocess.run([ffmpeg, "-y", "-v", "error", "-i", str(Path(tmp) / f"{mitte:04d}.jpg"), "-vf", vf.replace(",format=yuv420p", ""),
                            "-frames:v", "1", "-q:v", "4", str(vorschau)], capture_output=True, timeout=60, check=False)
        except (OSError, subprocess.SubprocessError) as err:
            _LOGGER.warning("Clip could not be made: %s", err)
            return False
    return video.exists()


class Clips:
    """Records the last seconds of a board camera and saves highlights as videos."""

    daten: DartsDaten  # set once the integration is ready

    def __init__(self, hass: HomeAssistant) -> None:
        self.hass = hass
        self._puffer: deque[tuple[float, bytes]] = deque(maxlen=int((VORHER + NACHHER + 1) / TAKT) + 10)
        self._aufnahme: asyncio.Task[None] | None = None
        self._offen: dict[str, Any] | None = None  # highlight waiting for the seconds after it
        self._abmelden: list[Callable[[], None]] = []
        self.arbeitet = False

    # ---------- settings ----------

    @property
    def einst(self) -> dict[str, Any]:
        e: dict[str, Any] = self.daten.spiel.daten.setdefault("clips", {})
        e.setdefault("an", False)
        if e.get("kamera") not in KAMERAS:
            e["kamera"] = "camera_1"
        e["anlaesse"] = [a for a in e.get("anlaesse", STANDARD_ANLAESSE) if a in ANLAESSE]
        e.setdefault("anzahl", 30)
        e.setdefault("wiederholung", True)
        e.setdefault("liste", [])
        return e

    def attribute(self) -> dict[str, Any]:
        e = self.einst
        return {k: e[k] for k in ("an", "kamera", "anlaesse", "anzahl", "wiederholung")} | {"liste": e["liste"][:60]}

    async def setzen(self, werte: dict[str, Any]) -> None:
        e = self.einst
        for k in ("an", "kamera", "anlaesse", "anzahl", "wiederholung"):
            if werte.get(k) is not None:
                e[k] = werte[k]
        if werte.get("kamera") is not None:
            self._puffer.clear()
        await self._aufraeumen()
        self.daten.spiel.einstellung_gespeichert()
        self.pruefen()

    @property
    def ordner(self) -> Path:
        return Path(self.hass.config.media_dirs.get("local") or self.hass.config.path("media")) / "dartnest" / "clips"

    # ---------- recording ----------

    def starten(self) -> None:
        self._abmelden = [self.daten.spiel.hoerer(self.pruefen), self.daten.zustand.async_add_listener(self.pruefen),
                          self.daten.spiel.ereignis_hoerer(self.ereignis)]
        self.pruefen()
        self.hass.async_create_background_task(self._waisen_weg(), "dartnest clips cleanup")

    async def _waisen_weg(self) -> None:
        """Remove files that are not in the list (left over after a crash or a manual change)."""
        behalten = {c["id"] for c in self.einst["liste"]}
        ordner = self.ordner

        def weg() -> None:
            if not ordner.is_dir():
                return
            for datei in ordner.iterdir():
                if datei.is_file() and DATEI.match(datei.name) and datei.stem not in behalten:
                    datei.unlink(missing_ok=True)

        await self.hass.async_add_executor_job(weg)

    async def beenden(self) -> None:
        for ab in self._abmelden:
            ab()
        self._abmelden = []
        await self._stopp()

    def _soll(self) -> bool:
        sp = self.daten.spiel.spiel
        z = self.daten.zustand
        return bool(self.einst["an"] and sp and sp.get("phase") == "laeuft" and z.online and (z.data or {}).get("laeuft"))

    def _laeuft(self) -> bool:
        return self._aufnahme is not None and not self._aufnahme.done()

    def pruefen(self) -> None:
        """Start or stop keeping the last seconds, following game and board."""
        if self._soll() and not self._laeuft():
            self._aufnahme = self.hass.async_create_background_task(self._aufnehmen(), "dartnest clips")
        elif not self._soll() and self._laeuft() and self._offen is None:
            self.hass.async_create_task(self._stopp())

    async def _stopp(self) -> None:
        if self._aufnahme and not self._aufnahme.done():
            self._aufnahme.cancel()
            try:
                await self._aufnahme
            except asyncio.CancelledError:
                pass
        self._aufnahme = None
        self._puffer.clear()

    async def _aufnehmen(self) -> None:
        strom = _STROEME[KAMERAS.index(self.einst["kamera"])]
        while True:
            start = time.monotonic()
            bild = await self.daten.board.image(strom)
            jetzt = time.monotonic()
            if bild:
                self._puffer.append((jetzt, bild))
            while self._puffer and self._puffer[0][0] < jetzt - VORHER - NACHHER - 1:
                self._puffer.popleft()
            if self._offen is not None and jetzt >= self._offen["bis"]:
                offen, self._offen = self._offen, None
                self.hass.async_create_task(self._speichern(offen, list(self._puffer)))
                if not self._soll():
                    self._aufnahme = None
                    self._puffer.clear()
                    return
            # a slow or missing answer means the board is busy: give it room instead of asking faster
            dauer = jetzt - start
            await asyncio.sleep(max(TAKT - dauer, dauer, 0.0) if bild else 1.0)

    def ereignis(self, typ: str, daten: dict[str, Any]) -> None:
        if typ not in self.einst["anlaesse"]:
            return
        self.merken(typ, daten)

    def merken(self, typ: str, daten: dict[str, Any]) -> bool:
        """Highlight now: save once the seconds after it are recorded too. One visit = one clip (the best event names it)."""
        if not self._laeuft():
            return False
        jetzt = time.monotonic()
        wert = daten.get("finish") or daten.get("score") or daten.get("points")
        neu = {"art": typ, "spieler": str(daten.get("player") or ""), "wert": wert, "um": jetzt, "bis": jetzt + NACHHER, "zeit": dt_util.now().isoformat(timespec="seconds")}
        alt = self._offen
        if alt is not None:
            if _rang(typ) < _rang(alt["art"]):
                alt.update({k: neu[k] for k in ("art", "spieler", "wert")})
            return True
        self._offen = neu
        return True

    async def jetzt_speichern(self) -> None:
        """Button "save clip": the last seconds, without a highlight."""
        if not self.einst["an"]:
            raise _fehler("clips_off")
        if not self._laeuft() or not self._puffer:
            raise _fehler("clips_no_image")
        self.merken("manual", {})

    async def _speichern(self, offen: dict[str, Any], bilder: list[tuple[float, bytes]]) -> None:
        bilder = [b for b in bilder if b[0] >= offen["um"] - VORHER]
        if len(bilder) < 6:
            return
        dauer = max(0.5, bilder[-1][0] - bilder[0][0])
        fps = max(1.0, (len(bilder) - 1) / dauer)
        mitte = min(range(len(bilder)), key=lambda i: abs(bilder[i][0] - offen["um"]))
        nr = KAMERAS.index(self.einst["kamera"])
        kal = ((self.daten.system.data or {}).get("netz") or {}).get(str(nr))
        cid = secrets.token_hex(6)
        ordner = self.ordner
        def platz() -> int:
            ordner.mkdir(parents=True, exist_ok=True)
            return shutil.disk_usage(ordner).free

        if await self.hass.async_add_executor_job(platz) < FREI_MIN:
            _LOGGER.warning("Clip not saved: less than 1 GB free on the disk")
            return
        self.arbeitet = True
        try:
            ok = await self.hass.async_add_executor_job(_kodieren, self._ffmpeg(), [b for _, b in bilder], fps, ecken(kal),
                                                        ordner / f"{cid}.mp4", ordner / f"{cid}.jpg", mitte)
        finally:
            self.arbeitet = False
        if not ok:
            return
        e = self.einst
        e["liste"].insert(0, {"id": cid, "zeit": offen["zeit"], "art": offen["art"], "spieler": offen["spieler"], "wert": offen["wert"],
                              "dauer": round(dauer, 1), "gerade": kal is not None and ecken(kal) is not None})
        await self._aufraeumen()
        self.daten.spiel.einstellung_gespeichert()

    def _ffmpeg(self) -> str:
        try:
            from homeassistant.components.ffmpeg import get_ffmpeg_manager

            return get_ffmpeg_manager(self.hass).binary
        except (ImportError, ValueError, KeyError):
            return shutil.which("ffmpeg") or "ffmpeg"

    # ---------- list ----------

    def neuester(self) -> dict[str, Any] | None:
        """Latest clip for the replay on the TV page and the overlay (only the first minute)."""
        e = self.einst
        if not e["wiederholung"] or not e["liste"]:
            return None
        c = e["liste"][0]
        zeit = dt_util.parse_datetime(str(c.get("zeit")))
        if zeit is None or (dt_util.now() - zeit).total_seconds() > 60:
            return None
        return {k: c.get(k) for k in ("id", "art", "spieler", "wert", "dauer")}

    async def loeschen(self, cid: str | None) -> None:
        e = self.einst
        weg = [c for c in e["liste"] if cid is None or c["id"] == cid]
        e["liste"] = [c for c in e["liste"] if c not in weg]
        await self._dateien_weg([c["id"] for c in weg])
        self.daten.spiel.einstellung_gespeichert()

    async def _aufraeumen(self) -> None:
        e = self.einst
        zuviel = e["liste"][int(e["anzahl"]):]
        if zuviel:
            e["liste"] = e["liste"][: int(e["anzahl"])]
            await self._dateien_weg([c["id"] for c in zuviel])

    async def _dateien_weg(self, ids: list[str]) -> None:
        ordner = self.ordner

        def weg() -> None:
            for cid in ids:
                for endung in ("mp4", "jpg"):
                    (ordner / f"{cid}.{endung}").unlink(missing_ok=True)

        await self.hass.async_add_executor_job(weg)

    def datei(self, name: str) -> Path | None:
        if not DATEI.match(name) or not any(c["id"] == name[:12] for c in self.einst["liste"]):
            return None
        return self.ordner / name


def clips_fuer(hass: HomeAssistant) -> list[Clips]:
    return [e.runtime_data.clips for e in hass.config_entries.async_loaded_entries(DOMAIN)]


async def clip_antwort(clips: list[Clips], name: str) -> web.StreamResponse:
    for c in clips:
        pfad = c.datei(name)
        if pfad is not None and await c.hass.async_add_executor_job(pfad.exists):
            return web.FileResponse(pfad, headers={"Cache-Control": "max-age=86400"})
    return web.Response(status=404)


class ClipDatei(HomeAssistantView):
    """A clip or its still image for the cards (logged in, or a signed link)."""

    url = CLIP_URL + "/{name}"
    name = "autodarts:clip"

    async def get(self, request: web.Request, name: str) -> web.StreamResponse:
        return await clip_antwort(clips_fuer(request.app["hass"]), name)


async def async_setup_clips(hass: HomeAssistant) -> None:
    if hass.http is not None:
        hass.http.register_view(ClipDatei())
