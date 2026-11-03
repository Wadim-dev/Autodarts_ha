"""Data update coordinators for the Autodarts board.

- State every second (/api/state): status, event, throws with position.
- System every 15 s (/api/system): calibration, cameras, CPU, memory, version.
While the board PC is off, state is polled every 30 s and sensors show "Offline".
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
import logging
from typing import TYPE_CHECKING, Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .board import AutodartsBoard, AutodartsError
from .const import DOMAIN

if TYPE_CHECKING:
    from .lichter import Lichtshow
    from .spiel import Spielleiter

_LOGGER = logging.getLogger(__name__)

TAKT_ONLINE = timedelta(seconds=1)
TAKT_OFFLINE = timedelta(seconds=30)
TAKT_SYSTEM = timedelta(seconds=15)


def wurf_lesen(t: dict[str, Any]) -> dict[str, Any]:
    """Einen Wurf in eine feste Form bringen (altes und neues Board-Format)."""
    seg: dict[str, Any] = t["segment"] if isinstance(t.get("segment"), dict) else {}
    koord: dict[str, Any] = t["coords"] if isinstance(t.get("coords"), dict) else {}
    zahl = seg.get("number", t.get("segmentNumber")) or 0
    mult = seg.get("multiplier", t.get("multiplier")) or 0
    name = seg.get("name") or t.get("segmentName") or "?"
    return {
        "feld": name,
        "zahl": int(zahl),
        "faktor": int(mult),
        "punkte": int(zahl) * int(mult),
        "bereich": seg.get("bed") or t.get("bed") or "",
        "x": koord.get("x", t.get("coordsX")),
        "y": koord.get("y", t.get("coordsY")),
        "abpraller": bool(t.get("bouncer", False)),
        "fehlgeschlagen": bool(t.get("failed", False)),
        "methode": t.get("method") or "",
    }


OFFLINE = {
    "verbindung": "Offline",
    "status": "Offline",
    "ereignis": "-",
    "laeuft": False,
    "wuerfe": [],
}


class ZustandKoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Fragt jede Sekunde den Spielzustand ab (Board aus: alle 30 s)."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry, board: AutodartsBoard) -> None:
        super().__init__(hass, _LOGGER, name=f"{DOMAIN} Zustand", update_interval=TAKT_ONLINE, config_entry=entry)
        self.board = board
        self.online = False

    async def _async_update_data(self) -> dict[str, Any]:
        try:
            daten = await self.board.state()
        except AutodartsError:
            if self.online:
                _LOGGER.info("Autodarts Board nicht mehr erreichbar")
            self.online = False
            self.update_interval = TAKT_OFFLINE
            return dict(OFFLINE)
        if not self.online:
            _LOGGER.info("Autodarts Board verbunden")
        self.online = True
        self.update_interval = TAKT_ONLINE
        wuerfe = [wurf_lesen(t) for t in (daten.get("throws") or []) if isinstance(t, dict)]
        return {
            "verbindung": "Online",
            "status": daten.get("status") or "unbekannt",
            "ereignis": daten.get("event") or "-",
            "laeuft": bool(daten.get("running")),
            "wuerfe": wuerfe,
        }


def _netz(daten: Any) -> dict[str, Any]:
    """Kalibrierpunkte je Kamera: Ringe (außen nach innen, je 20 Punkte an den Feldgrenzen 20|1, 1|18 …) und Bull."""
    netz: dict[str, Any] = {}
    if not isinstance(daten, dict):
        return netz
    for nr, kam in daten.items():
        if not isinstance(kam, dict):
            continue
        ringe = []
        for name in ("doubleOuterPoints", "doubleInnerPoints", "trebleOuterPoints", "trebleInnerPoints"):
            punkte = kam.get(name) or []
            ringe.append([[round(float(p[0]), 1), round(float(p[1]), 1)] for p in punkte if isinstance(p, (list, tuple)) and len(p) >= 2] if len(punkte) == 20 else [])
        if ringe[0]:
            netz[str(nr)] = {"ringe": ringe, "bull": kam.get("bull")}
    return netz


class SystemKoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Holt alle 15 s Systemdaten (nur wenn das Board erreichbar ist)."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry, board: AutodartsBoard, zustand: ZustandKoordinator) -> None:
        super().__init__(hass, _LOGGER, name=f"{DOMAIN} System", update_interval=TAKT_SYSTEM, config_entry=entry)
        self.board = board
        self.zustand = zustand
        self.geraete: list[dict[str, Any]] = []

    async def _async_update_data(self) -> dict[str, Any]:
        if not self.zustand.online:
            return {}
        try:
            s = await self.board.system()
            if not self.geraete:
                self.geraete = await self.board.devices()
            if not (self.data or {}).get("host"):
                host = await self.board.host_info()
            else:
                host = self.data["host"]
        except AutodartsError:
            return {}
        kal = s.get("calibration") or {}
        kams = [k for k in (kal.get("cams") or []) if isinstance(k, dict)]
        fehler = [round(float(k.get("errorPx") or 0), 2) for k in kams]
        netz = (self.data or {}).get("netz")
        if not netz or fehler != (self.data or {}).get("kalibrierfehler"):
            # Kalibriernetz nur nach neuer Kalibrierung holen (für Entzerrung und Netz in den Karten)
            try:
                netz = _netz(await self.board.calibration_ellipses()) or netz
            except AutodartsError:
                pass
        status = s.get("status") or {}
        stats = s.get("stats") or {}
        return {
            "kalibriert": bool(status.get("calibrated", kal.get("calibrated"))),
            "kalibriert_wird": int(status.get("calibratingCams") or 0) > 0,
            "kalibrierfehler": fehler,
            "netz": netz or {},
            "kamera_fps": [c.get("fps") for c in (s.get("camStats") or [])],
            "kameras_laufen": bool((s.get("camState") or {}).get("isRunning")),
            "cpu": round(float(stats.get("cpuPercent") or 0), 1),
            "speicher_mb": round(float(stats.get("memoryBytes") or 0) / 1048576, 1),
            "fps": stats.get("fps"),
            "version": status.get("version") or host.get("clientVersion"),
            "update": status.get("updateAvailable") or "",
            "verbindung_cloud": status.get("link") or "",
            "konfig": s.get("config") or {},
            "host": host,
        }


@dataclass
class DartsDaten:
    board: AutodartsBoard
    zustand: ZustandKoordinator
    system: SystemKoordinator
    geraet: DeviceInfo
    spiel: Spielleiter
    lichter: Lichtshow


type DartsEntry = ConfigEntry[DartsDaten]


