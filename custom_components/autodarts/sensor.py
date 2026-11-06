"""Sensoren: Verbindung, Status, Würfe, Aufnahme und Systemwerte."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorStateClass
from homeassistant.const import PERCENTAGE, EntityCategory, UnitOfInformation
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .coordinator import DartsDaten, DartsEntry
from .entity import DartsEntitaet

PARALLEL_UPDATES = 0

Koordinator = DataUpdateCoordinator[dict[str, Any]]
Lesen = Callable[[dict[str, Any]], Any]


async def async_setup_entry(hass: HomeAssistant, entry: DartsEntry, async_add_entities: AddEntitiesCallback) -> None:
    d = entry.runtime_data
    z = d.zustand
    s = d.system
    liste: list[SensorEntity] = [
        Verbindung(d, z, "verbindung", "connection"),
        Wert(d, z, "status", "status", lambda x: x["status"]),
        Wert(d, z, "ereignis", "event", lambda x: x["ereignis"], aus=True),
        Wert(d, z, "aufnahme", "visit_score", lambda x: sum(w["punkte"] for w in x["wuerfe"])),
        Wert(d, z, "anzahl", "throw_count", lambda x: len(x["wuerfe"]), aus=True),
    ]
    liste += [Wurf(d, z, i) for i in range(3)]
    liste += [
        System(d, s, "cpu", "cpu_load", lambda x: x.get("cpu"), PERCENTAGE),
        System(d, s, "speicher", "memory", lambda x: x.get("speicher_mb"), UnitOfInformation.MEGABYTES),
        System(d, s, "fps", "fps", lambda x: x.get("fps"), "fps"),
        System(d, s, "kamera_fps", "camera_fps",
               lambda x: min([f for f in x.get("kamera_fps") or [] if f is not None], default=None), "fps",
               lambda x: {"kameras": x.get("kamera_fps")}),
        System(d, s, "kalibrierfehler", "calibration_error",
               lambda x: max(x.get("kalibrierfehler") or [0]) if x.get("kalibrierfehler") else None, "px",
               lambda x: {"kameras": x.get("kalibrierfehler")}),
        System(d, s, "version", "software_version", lambda x: x.get("version"), None,
               lambda x: {k: (x.get("host") or {}).get(k) for k in ("visionVersion", "openCVVersion", "platformVersion", "kernelVersion", "hostname")}),
    ]
    liste += [SpielSensor(d), SpielerSensor(d)]
    async_add_entities(liste)


class Verbindung(DartsEntitaet, SensorEntity):
    @property
    def native_value(self) -> str:
        return str(self.coordinator.data["verbindung"])

    @property
    def icon(self) -> str | None:
        # States are "Online"/"Offline" (no translation keys), so the off icon is set here.
        return None if self.online else "mdi:wifi-off"



class Wert(DartsEntitaet, SensorEntity):
    def __init__(self, d: DartsDaten, k: Koordinator, schluessel: str, uebersetzung: str, wert: Lesen, aus: bool = False) -> None:
        super().__init__(d, k, schluessel, uebersetzung)
        self._attr_entity_registry_enabled_default = not aus
        self._wert = wert
        # Status zeigt „Offline“, alle anderen Werte sind dann nicht verfügbar.
        self._nur_online = schluessel != "status"

    @property
    def native_value(self) -> Any:
        return self._wert(self.coordinator.data)


class Wurf(DartsEntitaet, SensorEntity):
    """Wurf 1–3: Feld (z. B. T20), Position und Details als Attribute."""

    _nur_online = True

    def __init__(self, d: DartsDaten, k: Koordinator, i: int) -> None:
        super().__init__(d, k, f"wurf_{i + 1}", f"throw_{i + 1}")
        self._i = i

    def _wurf(self) -> dict[str, Any] | None:
        w: list[dict[str, Any]] = self.coordinator.data["wuerfe"]
        return w[self._i] if self._i < len(w) else None

    @property
    def native_value(self) -> str:
        w = self._wurf()
        return w["feld"] if w else "-"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        w = self._wurf()
        if not w:
            return {}
        return {k: w[k] for k in ("punkte", "zahl", "faktor", "bereich", "x", "y", "abpraller", "fehlgeschlagen", "methode")}


class System(DartsEntitaet, SensorEntity):
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, d: DartsDaten, k: Koordinator, schluessel: str, uebersetzung: str, wert: Lesen,
                 einheit: str | None = None, attribute: Callable[[dict[str, Any]], dict[str, Any]] | None = None) -> None:
        super().__init__(d, k, schluessel, uebersetzung)
        self._wert = wert
        self._attr_native_unit_of_measurement = einheit
        self._attribute = attribute
        if einheit and schluessel != "version":
            self._attr_state_class = SensorStateClass.MEASUREMENT
        if schluessel == "speicher":
            self._attr_device_class = SensorDeviceClass.DATA_SIZE
            self._attr_suggested_display_precision = 0

    @property
    def available(self) -> bool:
        return super().available and bool(self.coordinator.data)

    @property
    def native_value(self) -> Any:
        return self._wert(self.coordinator.data)

    @property
    def extra_state_attributes(self) -> dict[str, Any] | None:
        return self._attribute(self.coordinator.data) if self._attribute and self.coordinator.data else None


class _SpielBasis(SensorEntity):
    """Sensoren des lokalen Spiels (Werte kommen vom Spielleiter, nicht vom Board)."""

    _attr_has_entity_name = True
    _attr_should_poll = False

    def __init__(self, d: DartsDaten, schluessel: str, uebersetzung: str) -> None:
        self.daten = d
        self._attr_translation_key = uebersetzung
        self._attr_unique_id = f"autodarts_{schluessel}"
        self._attr_device_info = d.geraet

    async def async_added_to_hass(self) -> None:
        self.async_on_remove(self.daten.spiel.hoerer(self.async_write_ha_state))


class SpielSensor(_SpielBasis):
    """Laufendes Spiel: Zustand = Phase, alles andere in Attributen (nicht im Verlauf gespeichert)."""

    _unrecorded_attributes = frozenset({"quelle", "id", "phase", "modus", "einstellungen", "beginn", "ende", "bulloff", "am_zug",
                                        "aufnahme", "weg", "spieler", "gewinner", "leg_gewinner", "leg", "set", "ansage",
                                        "ansage_id", "reihenfolge", "bot_wirft", "aufnahmen", "verlauf",
                                        "art", "zahlen", "runden", "ziel", "turnier"})

    _attr_device_class = SensorDeviceClass.ENUM
    _attr_options = ["idle", "bull_off", "running", "finished"]  # noqa: RUF012

    def __init__(self, d: DartsDaten) -> None:
        super().__init__(d, "spiel", "game")

    @property
    def native_value(self) -> str:
        return self.daten.spiel.phase()

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        return self.daten.spiel.spiel_attribute()


class SpielerSensor(_SpielBasis):
    """Angelegte Spieler mit Gesamtstatistik und den letzten Spielen."""

    _unrecorded_attributes = frozenset({"spieler", "verlauf", "letzte", "turnier", "strom", "tv", "clips", "pixel"})

    def __init__(self, d: DartsDaten) -> None:
        super().__init__(d, "spieler", "players")

    @property
    def native_value(self) -> int:
        return len(self.daten.spiel.daten["spieler"])

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        return self.daten.spiel.spieler_attribute()
