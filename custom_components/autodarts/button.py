"""Knöpfe wie im Board Manager: Start, Stop, Reset, Kalibrieren, Neustart."""

from __future__ import annotations

import asyncio

from homeassistant.components.button import ButtonDeviceClass, ButtonEntity
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .api import befehl
from .coordinator import DartsDaten, DartsEntry
from .entity import DartsEntitaet

PARALLEL_UPDATES = 1

# Schlüssel, Übersetzungsschlüssel, Methode von aioautodarts, Kategorie (Symbole in icons.json)
KNOEPFE = [
    ("start", "start_detection", "start", None),
    ("stop", "stop_detection", "stop", None),
    ("reset", "reset_throws", "reset", None),
    ("kalibrieren", "calibrate", "calibrate", EntityCategory.CONFIG),
    ("neustart", "restart_software", "restart", EntityCategory.CONFIG),
]


async def async_setup_entry(hass: HomeAssistant, entry: DartsEntry, async_add_entities: AddEntitiesCallback) -> None:
    d = entry.runtime_data
    async_add_entities([Knopf(d, *k) for k in KNOEPFE])


class Knopf(DartsEntitaet, ButtonEntity):
    _nur_online = True

    def __init__(self, d: DartsDaten, schluessel: str, uebersetzung: str, pfad: str, kategorie: EntityCategory | None) -> None:
        super().__init__(d, d.system, schluessel, uebersetzung)
        self._pfad = pfad
        self._attr_entity_category = kategorie
        if schluessel == "neustart":
            self._attr_device_class = ButtonDeviceClass.RESTART

    async def async_press(self) -> None:
        if self.schluessel == "kalibrieren" and not (self.daten.zustand.data or {}).get("laeuft"):
            # Kalibrieren braucht laufende Kameras
            await befehl(self.daten.board.start())
            await asyncio.sleep(4)
        await befehl(getattr(self.daten.board, self._pfad)())
        await self.daten.zustand.async_request_refresh()
        if self.schluessel in ("kalibrieren", "neustart"):
            await self.daten.system.async_request_refresh()
