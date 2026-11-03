"""Local client for the Autodarts Board Manager REST API (http://<host>:3180/api/...)."""

from __future__ import annotations

import asyncio
from typing import Any

import aiohttp
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN


class Board:
    """Verbindung zum Board Manager."""

    def __init__(self, hass: HomeAssistant, host: str, port: int) -> None:
        self.basis = f"http://{host}:{port}"
        self._session = async_get_clientsession(hass)

    async def holen(self, pfad: str, zeit: float = 3) -> Any:
        async with asyncio.timeout(zeit):
            async with self._session.get(self.basis + pfad) as antwort:
                antwort.raise_for_status()
                return await antwort.json(content_type=None)

    async def bild(self, pfad: str) -> bytes | None:
        try:
            async with asyncio.timeout(6):
                async with self._session.get(self.basis + pfad) as antwort:
                    if antwort.status != 200:
                        return None
                    return await antwort.read()
        except (aiohttp.ClientError, TimeoutError):
            return None

    async def befehl(self, pfad: str, daten: dict[str, Any] | None = None, methode: str = "POST") -> None:
        try:
            async with asyncio.timeout(10):
                async with self._session.request(methode, self.basis + pfad, json=daten) as antwort:
                    status = antwort.status
                if status in (404, 405) and methode == "POST":
                    # Board 2.x: Start/Stop erwarten PUT
                    async with self._session.request("PUT", self.basis + pfad, json=daten) as antwort:
                        status = antwort.status
                if status >= 300:
                    raise HomeAssistantError(
                        translation_domain=DOMAIN, translation_key="board_error",
                        translation_placeholders={"status": str(status), "path": pfad},
                    )
        except (aiohttp.ClientError, TimeoutError) as err:
            raise HomeAssistantError(
                translation_domain=DOMAIN, translation_key="board_unreachable",
                translation_placeholders={"error": str(err) or type(err).__name__},
            ) from err


