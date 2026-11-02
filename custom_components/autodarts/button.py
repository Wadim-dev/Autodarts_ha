"""Knöpfe wie im Board Manager: Start, Stop, Reset, Kalibrieren, Neustart."""

from __future__ import annotations

import asyncio

from homeassistant.components.button import ButtonEntity
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .coordinator import DartsEntry
from .entity import DartsEntitaet

PARALLEL_UPDATES = 1

# Schlüssel, Name, Symbol, Pfad, Kategorie
KNOEPFE = [
    ("start", "Erkennung starten", "mdi:play", "/api/start", None),
    ("stop", "Erkennung stoppen", "mdi:stop", "/api/stop", None),
    ("reset", "Würfe zurücksetzen", "mdi:eject", "/api/reset", None),
    ("kalibrieren", "Kalibrieren", "mdi:crosshairs-gps", "/api/config/calibration/auto", EntityCategory.CONFIG),
    ("neustart", "Board-Software neu starten", "mdi:restart", "/api/restart", EntityCategory.CONFIG),
]


async def async_setup_entry(hass: HomeAssistant, entry: DartsEntry, async_add_entities: AddEntitiesCallback) -> None:
    d = entry.runtime_data
    async_add_entities([Knopf(d, *k) for k in KNOEPFE])


class Knopf(DartsEntitaet, ButtonEntity):
    _nur_online = True

    def __init__(self, d, schluessel, name, icon, pfad, kategorie) -> None:
        super().__init__(d, d.system, schluessel, name, icon)
        self._pfad = pfad
        self._attr_entity_category = kategorie

    async def async_press(self) -> None:
        if self.schluessel == "kalibrieren" and not (self.daten.zustand.data or {}).get("laeuft"):
            # Kalibrieren braucht laufende Kameras
            await self.daten.board.befehl("/api/start")
            await asyncio.sleep(4)
        await self.daten.board.befehl(self._pfad)
        await self.daten.zustand.async_request_refresh()
        if self.schluessel in ("kalibrieren", "neustart"):
            await self.daten.system.async_request_refresh()
