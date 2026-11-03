"""Kameras: die drei Board-Kameras und das Erkennungsbild.

Standbild über aioautodarts, Live-Bild (nur beim Öffnen) über den MJPEG-Strom des Boards.
"""

from __future__ import annotations

from typing import Any

from aioautodarts import Stream
from aiohttp import ClientTimeout, web
from homeassistant.components.camera import Camera
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_aiohttp_proxy_web, async_get_clientsession
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .coordinator import DartsDaten, DartsEntry
from .entity import DartsEntitaet

PARALLEL_UPDATES = 0


async def async_setup_entry(hass: HomeAssistant, entry: DartsEntry, async_add_entities: AddEntitiesCallback) -> None:
    d = entry.runtime_data
    kameras: tuple[Stream, ...] = ("cam0", "cam1", "cam2")
    liste = [BoardKamera(d, f"kamera_{i + 1}", f"camera_{i + 1}", k, str(i)) for i, k in enumerate(kameras)]
    liste.append(BoardKamera(d, "erkennung_bild", "detection_image", "detection"))
    liste.append(BoardKamera(d, "live_bild", "live_image", "live"))
    async_add_entities(liste)


class BoardKamera(DartsEntitaet, Camera):
    # Kalibrierpunkte nicht in den Verlauf schreiben (das Zugangs-Token ändert sich alle 5 min)
    _unrecorded_attributes = frozenset({"kalibrierung"})
    _nur_online = True

    def __init__(self, d: DartsDaten, schluessel: str, uebersetzung: str, strom: Stream, nr: str | None = None) -> None:
        DartsEntitaet.__init__(self, d, d.system, schluessel, uebersetzung)
        Camera.__init__(self)
        self._strom = strom
        self.content_type = "image/jpeg"
        self._nr = nr

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        if self._nr is None:
            return None
        netz = ((self.coordinator.data or {}).get("netz") or {}).get(self._nr)
        return {"kalibrierung": netz} if netz else None

    async def async_camera_image(self, width: int | None = None, height: int | None = None) -> bytes | None:
        return await self.daten.board.image(self._strom)

    async def handle_async_mjpeg_stream(self, request: web.Request) -> web.StreamResponse | None:
        session = async_get_clientsession(self.hass)
        stream = session.get(self.daten.board.stream_url(self._strom), timeout=ClientTimeout(total=None, sock_connect=5))
        return await async_aiohttp_proxy_web(self.hass, request, stream)
