"""Connection to the Board Manager through the aioautodarts library."""

from __future__ import annotations

from collections.abc import Awaitable

from aioautodarts import AutodartsBoard, AutodartsConnectionError, AutodartsResponseError
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN


def board_erstellen(hass: HomeAssistant, host: str, port: int) -> AutodartsBoard:
    """Board client on Home Assistant's shared web session."""
    return AutodartsBoard(host, port, session=async_get_clientsession(hass))


async def befehl(aufruf: Awaitable[None]) -> None:
    """Run a board command and turn its errors into translated Home Assistant errors."""
    try:
        await aufruf
    except AutodartsResponseError as err:
        raise HomeAssistantError(
            translation_domain=DOMAIN, translation_key="board_error",
            translation_placeholders={"status": str(err.status), "path": f"/api/{err.path}"},
        ) from err
    except AutodartsConnectionError as err:
        raise HomeAssistantError(
            translation_domain=DOMAIN, translation_key="board_unreachable",
            translation_placeholders={"error": str(err)},
        ) from err
