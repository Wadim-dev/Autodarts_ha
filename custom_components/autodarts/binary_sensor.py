"""Binärsensoren: Erkennung läuft, Board kalibriert."""

from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .coordinator import DartsEntry
from .entity import DartsEntitaet

PARALLEL_UPDATES = 0


async def async_setup_entry(hass: HomeAssistant, entry: DartsEntry, async_add_entities: AddEntitiesCallback) -> None:
    d = entry.runtime_data
    async_add_entities([
        Laeuft(d, d.zustand, "erkennung", "Erkennung läuft", "mdi:motion-sensor"),
        Kalibriert(d, d.system, "kalibriert", "Kalibriert", "mdi:crosshairs-gps"),
    ])


class Laeuft(DartsEntitaet, BinarySensorEntity):
    _nur_online = True

    @property
    def is_on(self) -> bool:
        return bool(self.coordinator.data.get("laeuft"))


class Kalibriert(DartsEntitaet, BinarySensorEntity):
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    @property
    def available(self) -> bool:
        return super().available and bool(self.coordinator.data)

    @property
    def is_on(self) -> bool:
        return bool(self.coordinator.data.get("kalibriert"))

    @property
    def extra_state_attributes(self):
        return {"kalibriert_gerade": self.coordinator.data.get("kalibriert_wird", False)}
