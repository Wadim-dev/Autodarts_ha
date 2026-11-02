"""Kameras: die drei Board-Kameras und das Erkennungsbild.

Standbild über /api/img/..., Live-Bild (nur beim Öffnen) über den MJPEG-Strom des Boards.
"""

from __future__ import annotations

from aiohttp import ClientTimeout, web

from homeassistant.components.camera import Camera
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_aiohttp_proxy_web, async_get_clientsession
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .coordinator import DartsEntry
from .entity import DartsEntitaet


async def async_setup_entry(hass: HomeAssistant, entry: DartsEntry, async_add_entities: AddEntitiesCallback) -> None:
    d = entry.runtime_data
    liste = [BoardKamera(d, f"kamera_{i + 1}", f"Kamera {i + 1}", f"/api/img/cams/{i}", f"/api/streams/cams/{i}", str(i)) for i in range(3)]
    liste.append(BoardKamera(d, "erkennung_bild", "Erkennungsbild", "/api/img/detection", "/api/streams/detection"))
    liste.append(BoardKamera(d, "live_bild", "Live-Bild", "/api/img/live", "/api/streams/live"))
    async_add_entities(liste)


class BoardKamera(DartsEntitaet, Camera):
    # Kalibrierpunkte nicht in den Verlauf schreiben (das Zugangs-Token ändert sich alle 5 min)
    _unrecorded_attributes = frozenset({"kalibrierung"})

    def __init__(self, d, schluessel, name, bild, strom, nr: str | None = None) -> None:
        DartsEntitaet.__init__(self, d, d.system, schluessel, name, "mdi:camera")
        Camera.__init__(self)
        self._bild = bild
        self._strom = strom
        self.content_type = "image/jpeg"
        self._nr = nr

    @property
    def extra_state_attributes(self) -> dict | None:
        if self._nr is None:
            return None
        netz = ((self.coordinator.data or {}).get("netz") or {}).get(self._nr)
        return {"kalibrierung": netz} if netz else None

    @property
    def available(self) -> bool:
        return super().available and self.online

    async def async_camera_image(self, width: int | None = None, height: int | None = None) -> bytes | None:
        return await self.daten.board.bild(self._bild)

    async def handle_async_mjpeg_stream(self, request: web.Request) -> web.StreamResponse | None:
        session = async_get_clientsession(self.hass)
        stream = session.get(self.daten.board.basis + self._strom, timeout=ClientTimeout(total=None, sock_connect=5))
        return await async_aiohttp_proxy_web(self.hass, request, stream)
