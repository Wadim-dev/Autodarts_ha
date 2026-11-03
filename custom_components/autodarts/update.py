"""Update entity for the board software (reported by the board itself).

Updates of this integration itself come through HACS / the Marketplace.
"""

from __future__ import annotations

from typing import Any

from homeassistant.components.update import UpdateDeviceClass, UpdateEntity, UpdateEntityFeature
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .api import befehl
from .coordinator import DartsDaten, DartsEntry
from .entity import DartsEntitaet

PARALLEL_UPDATES = 1


async def async_setup_entry(hass: HomeAssistant, entry: DartsEntry, async_add_entities: AddEntitiesCallback) -> None:
    async_add_entities([BoardUpdate(entry.runtime_data)])


class BoardUpdate(DartsEntitaet, UpdateEntity):
    """Update der Board-Software (meldet das Board selbst)."""

    _attr_entity_category = EntityCategory.CONFIG
    _attr_supported_features = UpdateEntityFeature.INSTALL
    _attr_title = "Autodarts Board"
    _attr_device_class = UpdateDeviceClass.FIRMWARE

    def __init__(self, d: DartsDaten) -> None:
        super().__init__(d, d.system, "board_update", "board_software")

    @property
    def available(self) -> bool:
        return super().available and bool(self.coordinator.data)

    @property
    def installed_version(self) -> str | None:
        return (self.coordinator.data or {}).get("version")

    @property
    def latest_version(self) -> str | None:
        neu = (self.coordinator.data or {}).get("update")
        return neu or self.installed_version

    async def async_install(self, version: str | None, backup: bool, **kwargs: Any) -> None:
        await befehl(self.daten.board.apply_update())
        await self.coordinator.async_request_refresh()
