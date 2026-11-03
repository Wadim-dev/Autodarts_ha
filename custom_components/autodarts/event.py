"""Event entity: everything that happens in a local game, for automations (lights on a 180 …)."""

from __future__ import annotations

from typing import Any

from homeassistant.components.event import EventEntity
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import EREIGNISSE
from .coordinator import DartsDaten, DartsEntry

PARALLEL_UPDATES = 0



async def async_setup_entry(hass: HomeAssistant, entry: DartsEntry, async_add_entities: AddEntitiesCallback) -> None:
    async_add_entities([SpielEreignis(entry.runtime_data)])


class SpielEreignis(EventEntity):
    """Fires on every dart and visit of the local game (not for undo or corrections)."""

    _attr_has_entity_name = True
    _attr_should_poll = False
    _attr_translation_key = "game_event"
    _attr_event_types = EREIGNISSE

    def __init__(self, d: DartsDaten) -> None:
        self.daten = d
        self._attr_unique_id = "autodarts_spiel_ereignis"
        self._attr_device_info = d.geraet

    async def async_added_to_hass(self) -> None:
        self.async_on_remove(self.daten.spiel.ereignis_hoerer(self._ausloesen))

    @callback
    def _ausloesen(self, typ: str, daten: dict[str, Any]) -> None:
        self._trigger_event(typ, daten)
        self.async_write_ha_state()
