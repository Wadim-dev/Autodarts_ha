"""Config flow: enter the address of the Autodarts Board Manager and test it."""

from __future__ import annotations

import asyncio
from typing import Any

import aiohttp
import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import CONF_HOST, CONF_PORT, DOMAIN, GERAETENAME, STANDARD_PORT

SCHEMA = vol.Schema({
    vol.Required(CONF_HOST): str,
    vol.Required(CONF_PORT, default=STANDARD_PORT): vol.All(vol.Coerce(int), vol.Range(min=1, max=65535)),
})


async def board_testen(flow: ConfigFlow, host: str, port: int) -> None:
    """Raise if the Board Manager does not answer on /api/state."""
    session = async_get_clientsession(flow.hass)
    async with asyncio.timeout(5):
        async with session.get(f"http://{host}:{port}/api/state") as antwort:
            antwort.raise_for_status()
            daten = await antwort.json(content_type=None)
    if not isinstance(daten, dict):
        raise ValueError("unexpected answer")


class DartsConfigFlow(ConfigFlow, domain=DOMAIN):
    """Set up one Autodarts board."""

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()
        fehler: dict[str, str] = {}
        if user_input is not None:
            try:
                await board_testen(self, user_input[CONF_HOST], user_input[CONF_PORT])
            except (aiohttp.ClientError, TimeoutError, ValueError):
                fehler["base"] = "cannot_connect"
            else:
                return self.async_create_entry(title=GERAETENAME, data=user_input)
        return self.async_show_form(
            step_id="user",
            data_schema=self.add_suggested_values_to_schema(SCHEMA, user_input),
            errors=fehler,
        )
