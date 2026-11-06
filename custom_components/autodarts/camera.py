"""Kameras: die drei Board-Kameras und das Erkennungsbild.

Standbild und Live-Bild kommen aus dem gemeinsamen Bildverteiler: das Board wird nur gefragt,
solange jemand zusieht, und jedes Bild geht an alle Zuschauer (schont den Board-PC).
"""

from __future__ import annotations

from typing import Any

from aiohttp import web
from homeassistant.components.camera import Camera
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .board import Stream
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
        return await self.daten.bilder.standbild(self._strom)

    async def handle_async_mjpeg_stream(self, request: web.Request) -> web.StreamResponse | None:
        return await self.daten.bilder.mjpeg(request, self._strom)
