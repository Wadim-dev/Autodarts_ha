"""Gemeinsame Basis für alle Autodarts-Entitäten."""

from __future__ import annotations

from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinator import DartsDaten
from .const import DOMAIN


class DartsEntitaet(CoordinatorEntity):
    """Entität am Gerät „Autodarts Board“; Name = Gerätename + übersetzter Name (strings.json)."""

    _attr_has_entity_name = True
    # Wenn True: Entität ist nicht verfügbar, solange das Board nicht antwortet.
    _nur_online = False

    def __init__(self, daten: DartsDaten, koordinator, schluessel: str, uebersetzung: str, icon: str | None = None) -> None:
        super().__init__(koordinator)
        self.daten = daten
        self.schluessel = schluessel
        self._attr_translation_key = uebersetzung
        self._attr_unique_id = f"{DOMAIN}_{schluessel}"
        self._attr_device_info = daten.geraet
        if icon:
            self._attr_icon = icon

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()
        if self._nur_online and self.coordinator is not self.daten.zustand:
            # Board an/aus sofort zeigen, nicht erst beim nächsten Systemabruf (nur bei Wechsel schreiben)
            self._war_online = self.online

            def _wechsel() -> None:
                if self.online != self._war_online:
                    self._war_online = self.online
                    self.async_write_ha_state()

            self.async_on_remove(self.daten.zustand.async_add_listener(_wechsel))

    @property
    def available(self) -> bool:
        return super().available and (self.online or not self._nur_online)

    @property
    def online(self) -> bool:
        return self.daten.zustand.online
