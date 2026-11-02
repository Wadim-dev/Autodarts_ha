"""Autodarts integration: local Autodarts board plus local X01 games in Home Assistant.

Everything runs locally against the Board Manager (http://<host>:3180/api/...).
Local X01 games with players, bot and statistics live in spiel.py and x01.py.
"""

from __future__ import annotations

from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.typing import ConfigType

from .api import Board
from .const import CONF_HOST, CONF_PORT, DOMAIN, GERAETENAME, STANDARD_PORT
from .coordinator import DartsDaten, DartsEntry, SystemKoordinator, ZustandKoordinator
from .services import async_setup_services
from .spiel import Spielleiter

PLATFORMS = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.BUTTON,
    Platform.CAMERA,
    Platform.SELECT,
    Platform.UPDATE,
]

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the actions once for the whole integration."""
    async_setup_services(hass)
    return True


async def async_setup_entry(hass: HomeAssistant, entry: DartsEntry) -> bool:
    """Set up the board from a config entry.

    The board PC is often switched off by a smart plug. The integration still loads and
    reports "Offline" until the board answers again (see quality_scale.yaml).
    """
    board = Board(hass, entry.data[CONF_HOST], entry.data.get(CONF_PORT, STANDARD_PORT))
    zustand = ZustandKoordinator(hass, entry, board)
    system = SystemKoordinator(hass, entry, board, zustand)
    await zustand.async_config_entry_first_refresh()
    await system.async_config_entry_first_refresh()
    geraet = DeviceInfo(
        identifiers={(DOMAIN, entry.entry_id)},
        name=GERAETENAME,
        manufacturer="Autodarts",
        model="Board Manager (local)",
        configuration_url=board.basis,
    )
    spiel = Spielleiter(hass, board, zustand)
    await spiel.laden()
    entry.runtime_data = DartsDaten(board, zustand, system, geraet, spiel)
    entry.async_on_unload(zustand.async_add_listener(spiel.board_aenderung))
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: DartsEntry) -> bool:
    """Unload a config entry."""
    ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if ok and entry.runtime_data.spiel:
        await entry.runtime_data.spiel.beenden()
    return ok
