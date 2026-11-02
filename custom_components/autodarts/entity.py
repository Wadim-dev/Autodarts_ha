"""Gemeinsame Basis für alle Autodarts-Entitäten."""

from __future__ import annotations

from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinator import DartsDaten
from .const import DOMAIN


class DartsEntitaet(CoordinatorEntity):
    """Entität am Gerät „Autodarts Board“; Name = Gerätename + eigener Name."""

    _attr_has_entity_name = True

    def __init__(self, daten: DartsDaten, koordinator, schluessel: str, name: str, icon: str | None = None) -> None:
        super().__init__(koordinator)
        self.daten = daten
        self.schluessel = schluessel
        self._attr_name = name
        self._attr_unique_id = f"{DOMAIN}_{schluessel}"
        self._attr_device_info = daten.geraet
        if icon:
            self._attr_icon = icon

    @property
    def online(self) -> bool:
        return self.daten.zustand.online
