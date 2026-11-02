"""Auswahl wie im Board Manager (Kameras): Auflösung, Bildrate, Standby-Zeit."""

from __future__ import annotations

from homeassistant.components.select import SelectEntity
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .coordinator import DartsEntry
from .entity import DartsEntitaet


async def async_setup_entry(hass: HomeAssistant, entry: DartsEntry, async_add_entities: AddEntitiesCallback) -> None:
    d = entry.runtime_data
    async_add_entities([Standby(d), Bildrate(d), Aufloesung(d)])


class Auswahl(DartsEntitaet, SelectEntity):
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(self, d, schluessel, name, icon) -> None:
        super().__init__(d, d.system, schluessel, name, icon)

    @property
    def konfig(self) -> dict:
        return (self.coordinator.data or {}).get("konfig") or {}

    @property
    def available(self) -> bool:
        return super().available and self.online and bool(self.konfig)

    async def _setzen(self, daten: dict) -> None:
        await self.daten.board.befehl("/api/config", daten, "PATCH")
        await self.coordinator.async_request_refresh()


class Standby(Auswahl):
    _attr_options = ["10 Minuten", "15 Minuten", "30 Minuten"]

    def __init__(self, d) -> None:
        super().__init__(d, "standby", "Kamera-Standby", "mdi:sleep")

    @property
    def current_option(self) -> str | None:
        m = (self.konfig.get("motion") or {}).get("standbyMinutes")
        return f"{m} Minuten" if m is not None else None

    async def async_select_option(self, option: str) -> None:
        await self._setzen({"motion": {"standbyMinutes": int(option.split()[0])}})


def _mjpg(d) -> list[dict]:
    """Auflösungen/Bildraten der ersten Kamera (MJPG), wie der Board Manager sie anbietet."""
    for g in d.system.geraete or []:
        for f in g.get("formats") or []:
            if f.get("name") == "MJPG":
                return f.get("resolutions") or []
    return []


class Bildrate(Auswahl):
    def __init__(self, d) -> None:
        super().__init__(d, "bildrate_wahl", "Kamera-Bildrate einstellen", "mdi:speedometer")

    @property
    def options(self) -> list[str]:
        raten = sorted({r for a in _mjpg(self.daten) for r in a.get("framerates") or []}, reverse=True)
        jetzt = (self.konfig.get("cam") or {}).get("fps")
        if jetzt and jetzt not in raten:
            raten.insert(0, jetzt)
        return [str(r) for r in raten] or ["30"]

    @property
    def current_option(self) -> str | None:
        f = (self.konfig.get("cam") or {}).get("fps")
        return str(f) if f else None

    async def async_select_option(self, option: str) -> None:
        await self._setzen({"cam": {"fps": int(option)}})


class Aufloesung(Auswahl):
    def __init__(self, d) -> None:
        super().__init__(d, "aufloesung", "Kamera-Auflösung", "mdi:aspect-ratio")

    @property
    def options(self) -> list[str]:
        liste = [f"{a['width']}x{a['height']}" for a in _mjpg(self.daten) if a.get("width")]
        jetzt = self.current_option
        if jetzt and jetzt not in liste:
            liste.insert(0, jetzt)
        return liste or ["1280x720"]

    @property
    def current_option(self) -> str | None:
        c = self.konfig.get("cam") or {}
        return f"{c['width']}x{c['height']}" if c.get("width") else None

    async def async_select_option(self, option: str) -> None:
        b, h = (int(x) for x in option.split("x"))
        await self._setzen({"cam": {"width": b, "height": h}})
