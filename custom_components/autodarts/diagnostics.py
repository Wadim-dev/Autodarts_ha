"""Diagnostics: what the integration currently knows about the board and the local game."""

from __future__ import annotations

from typing import Any

from homeassistant.components.diagnostics import async_redact_data
from homeassistant.core import HomeAssistant

from .const import CONF_HOST
from .coordinator import DartsEntry

# Address and host details identify the home network.
VERDECKT = {"hostname", "ip", "macAddress", "mac"}


async def async_get_config_entry_diagnostics(hass: HomeAssistant, entry: DartsEntry) -> dict[str, Any]:
    d = entry.runtime_data
    system = dict(d.system.data or {})
    netz = system.pop("netz", {})
    spiel = d.spiel
    return async_redact_data(
        {
            "entry": {"data": async_redact_data(dict(entry.data), {CONF_HOST}), "version": entry.version},
            "board": {
                "online": d.zustand.online,
                "state": d.zustand.data,
                "system": system,
                "calibration_cameras": sorted(netz),
                "devices": d.system.geraete,
            },
            "game": {
                "phase": spiel.phase() if spiel else None,
                "players": len(spiel.daten["spieler"]) if spiel else 0,
                "finished_games": len(spiel.daten.get("verlauf") or []) if spiel else 0,
                "running": bool(spiel and spiel.spiel),
            },
        },
        VERDECKT,
    )
