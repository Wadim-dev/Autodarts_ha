"""One shared image source per board camera.

The board PC is small: every live view used to open its own stream, and each stream made the
board encode 30 JPEG images per second. Now the board is asked for single images only while
somebody watches (a card, the TV page or the highlight recorder), at most 10 per second, and
every viewer gets the same image. A slow answer means the board is busy, so the source waits
longer instead of asking faster.
"""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator
import logging
import time
from typing import Any

from aiohttp import web
from homeassistant.core import HomeAssistant

from .board import AutodartsBoard, Stream

_LOGGER = logging.getLogger(__name__)

LIVE_TAKT = 1 / 10  # live views: 10 images per second
GRENZE = "dartnestbild"


class _Quelle:
    """Images of one camera, fetched only while someone is subscribed."""

    def __init__(self, hass: HomeAssistant, board: AutodartsBoard, strom: Stream) -> None:
        self.hass, self.board, self.strom = hass, board, strom
        self.abos: dict[object, float] = {}
        self.bild: bytes | None = None
        self.zeit = 0.0
        self.nr = 0
        self._neu = asyncio.Event()
        self._task: asyncio.Task[None] | None = None

    def anmelden(self, takt: float) -> object:
        schluessel = object()
        self.abos[schluessel] = takt
        if self._task is None or self._task.done():
            self._task = self.hass.async_create_background_task(self._laufen(), f"dartnest bilder {self.strom}")
        return schluessel

    def abmelden(self, schluessel: object) -> None:
        self.abos.pop(schluessel, None)

    async def warten(self, nr: int, zeit: float) -> bool:
        """Wait up to `zeit` seconds for an image newer than `nr`."""
        if self.nr != nr:
            return True
        try:
            async with asyncio.timeout(zeit):
                await self._neu.wait()
        except TimeoutError:
            return False
        return True

    async def _laufen(self) -> None:
        while self.abos:
            takt = min(self.abos.values())
            start = time.monotonic()
            try:
                bild = await self.board.image(self.strom)
            except Exception:
                _LOGGER.debug("Image of %s failed", self.strom, exc_info=True)
                bild = None
            dauer = time.monotonic() - start
            if bild:
                self.bild, self.zeit, self.nr = bild, time.monotonic(), self.nr + 1
                self._neu.set()
                self._neu = asyncio.Event()
            await asyncio.sleep(max(takt - dauer, dauer, 0.0) if bild else 1.0)

    async def beenden(self) -> None:
        self.abos.clear()
        if self._task and not self._task.done():
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass


class Bildverteiler:
    """Hands the newest image of each camera to all viewers; asks the board only while needed."""

    def __init__(self, hass: HomeAssistant, board: AutodartsBoard) -> None:
        self.hass, self.board = hass, board
        self._quellen: dict[str, _Quelle] = {}

    def _quelle(self, strom: Stream) -> _Quelle:
        if strom not in self._quellen:
            self._quellen[strom] = _Quelle(self.hass, self.board, strom)
        return self._quellen[strom]

    def aktiv(self, strom: Stream) -> bool:
        q = self._quellen.get(strom)
        return bool(q and q.abos)

    async def standbild(self, strom: Stream) -> bytes | None:
        """A still image: the shared one if it is fresh, otherwise one from the board."""
        q = self._quellen.get(strom)
        if q and q.bild and time.monotonic() - q.zeit < 1.0:
            return q.bild
        return await self.board.image(strom)

    async def bilder(self, strom: Stream, takt: float) -> AsyncIterator[bytes]:
        """Every new image of the camera, at most one per `takt` seconds."""
        q = self._quelle(strom)
        schluessel = q.anmelden(takt)
        nr = q.nr
        try:
            while True:
                if not await q.warten(nr, 5):
                    continue
                nr = q.nr
                if q.bild:
                    yield q.bild
        finally:
            q.abmelden(schluessel)

    async def mjpeg(self, request: web.Request, strom: Stream) -> web.StreamResponse:
        """Live view as MJPEG for cards and the TV page, from the shared images."""
        antwort = web.StreamResponse(headers={
            "Content-Type": f"multipart/x-mixed-replace;boundary={GRENZE}",
            "Cache-Control": "no-cache, no-store",
        })
        await antwort.prepare(request)
        q = self._quelle(strom)
        schluessel = q.anmelden(LIVE_TAKT)
        nr = -1
        try:
            while not _zu(request):
                if not await q.warten(nr, 5):
                    continue
                nr = q.nr
                if q.bild:
                    kopf = f"--{GRENZE}\r\nContent-Type: image/jpeg\r\nContent-Length: {len(q.bild)}\r\n\r\n".encode()
                    await antwort.write(kopf + q.bild + b"\r\n")
        except (ConnectionResetError, ConnectionError):
            pass
        finally:
            q.abmelden(schluessel)
        return antwort

    async def beenden(self) -> None:
        for q in self._quellen.values():
            await q.beenden()


def _zu(request: Any) -> bool:
    transport = request.transport
    return transport is None or transport.is_closing()
