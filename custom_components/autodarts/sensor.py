"""Sensoren: Verbindung, Status, Würfe, Aufnahme und Systemwerte."""

from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.const import PERCENTAGE, EntityCategory, UnitOfInformation
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .coordinator import DartsEntry
from .entity import DartsEntitaet

PARALLEL_UPDATES = 0


async def async_setup_entry(hass: HomeAssistant, entry: DartsEntry, async_add_entities: AddEntitiesCallback) -> None:
    d = entry.runtime_data
    z = d.zustand
    s = d.system
    liste: list[SensorEntity] = [
        Verbindung(d, z, "verbindung", "Verbindung", "mdi:wifi-check"),
        Wert(d, z, "status", "Status", "mdi:state-machine", lambda x: x["status"]),
        Wert(d, z, "ereignis", "Ereignis", "mdi:flash-outline", lambda x: x["ereignis"]),
        Wert(d, z, "aufnahme", "Aktuelle Aufnahme", "mdi:bullseye-arrow", lambda x: sum(w["punkte"] for w in x["wuerfe"])),
        Wert(d, z, "anzahl", "Anzahl Würfe", "mdi:counter", lambda x: len(x["wuerfe"])),
    ]
    liste += [Wurf(d, z, i) for i in range(3)]
    liste += [
        System(d, s, "cpu", "CPU-Last", "mdi:cpu-64-bit", lambda x: x.get("cpu"), PERCENTAGE),
        System(d, s, "speicher", "Speicher", "mdi:memory", lambda x: x.get("speicher_mb"), UnitOfInformation.MEGABYTES),
        System(d, s, "fps", "Bildrate", "mdi:speedometer", lambda x: x.get("fps"), "fps"),
        System(d, s, "kamera_fps", "Kamera-Bildrate", "mdi:camera-timer",
               lambda x: min([f for f in x.get("kamera_fps") or [] if f is not None], default=None), "fps",
               lambda x: {"kameras": x.get("kamera_fps")}),
        System(d, s, "kalibrierfehler", "Kalibrier-Abweichung", "mdi:crosshairs-question",
               lambda x: max(x.get("kalibrierfehler") or [0]) if x.get("kalibrierfehler") else None, "px",
               lambda x: {"kameras": x.get("kalibrierfehler")}),
        System(d, s, "version", "Board-Software", "mdi:information-outline", lambda x: x.get("version"), None,
               lambda x: {k: (x.get("host") or {}).get(k) for k in ("visionVersion", "openCVVersion", "platformVersion", "kernelVersion", "hostname")}),
    ]
    liste += [SpielSensor(d), SpielerSensor(d)]
    async_add_entities(liste)


class Verbindung(DartsEntitaet, SensorEntity):
    @property
    def native_value(self) -> str:
        return self.coordinator.data["verbindung"]

    @property
    def icon(self) -> str:
        return "mdi:wifi-check" if self.online else "mdi:wifi-off"


class Wert(DartsEntitaet, SensorEntity):
    def __init__(self, d, k, schluessel, name, icon, wert) -> None:
        super().__init__(d, k, schluessel, name, icon)
        self._wert = wert
        # Status zeigt „Offline“, alle anderen Werte sind dann nicht verfügbar.
        self._nur_online = schluessel != "status"

    @property
    def native_value(self) -> Any:
        return self._wert(self.coordinator.data)


class Wurf(DartsEntitaet, SensorEntity):
    """Wurf 1–3: Feld (z. B. T20), Position und Details als Attribute."""

    _nur_online = True

    def __init__(self, d, k, i: int) -> None:
        super().__init__(d, k, f"wurf_{i + 1}", f"Wurf {i + 1}", f"mdi:numeric-{i + 1}-circle-outline")
        self._i = i

    def _wurf(self) -> dict | None:
        w = self.coordinator.data["wuerfe"]
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

    def __init__(self, d, k, schluessel, name, icon, wert, einheit=None, attribute=None) -> None:
        super().__init__(d, k, schluessel, name, icon)
        self._wert = wert
        self._attr_native_unit_of_measurement = einheit
        self._attribute = attribute
        if einheit and schluessel != "version":
            self._attr_state_class = SensorStateClass.MEASUREMENT

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

    def __init__(self, d, schluessel: str, name: str, icon: str) -> None:
        self.daten = d
        self._attr_name = name
        self._attr_unique_id = f"autodarts_{schluessel}"
        self._attr_device_info = d.geraet
        self._attr_icon = icon

    async def async_added_to_hass(self) -> None:
        self.async_on_remove(self.daten.spiel.hoerer(self.async_write_ha_state))


class SpielSensor(_SpielBasis):
    """Laufendes Spiel: Zustand = Phase, alles andere in Attributen (nicht im Verlauf gespeichert)."""

    _unrecorded_attributes = frozenset({"quelle", "id", "phase", "modus", "einstellungen", "beginn", "ende", "bulloff", "am_zug",
                                        "aufnahme", "weg", "spieler", "gewinner", "leg_gewinner", "leg", "set", "ansage",
                                        "ansage_id", "reihenfolge", "bot_wirft", "aufnahmen", "verlauf"})

    def __init__(self, d) -> None:
        super().__init__(d, "spiel", "Spiel", "mdi:bullseye-arrow")

    @property
    def native_value(self) -> str:
        return self.daten.spiel.phase()

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        return self.daten.spiel.spiel_attribute()


class SpielerSensor(_SpielBasis):
    """Angelegte Spieler mit Gesamtstatistik und den letzten Spielen."""

    _unrecorded_attributes = frozenset({"spieler", "verlauf", "letzte"})

    def __init__(self, d) -> None:
        super().__init__(d, "spieler", "Spieler", "mdi:account-group")

    @property
    def native_value(self) -> int:
        return len(self.daten.spiel.daten["spieler"])

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        return self.daten.spiel.spieler_attribute()
