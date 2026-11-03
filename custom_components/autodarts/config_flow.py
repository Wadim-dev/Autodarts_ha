"""Config flow: find or enter the Autodarts Board Manager and test it."""

from __future__ import annotations

from ipaddress import IPv4Address
from typing import Any

from aioautodarts import AutodartsError
from homeassistant.config_entries import SOURCE_RECONFIGURE, ConfigFlow, ConfigFlowResult
from homeassistant.helpers.service_info.zeroconf import ZeroconfServiceInfo
import voluptuous as vol

from .api import board_erstellen
from .const import CONF_HOST, CONF_PORT, DOMAIN, GERAETENAME, STANDARD_PORT

SCHEMA = vol.Schema({
    vol.Required(CONF_HOST): str,
    vol.Required(CONF_PORT, default=STANDARD_PORT): vol.All(vol.Coerce(int), vol.Range(min=1, max=65535)),
})


async def board_testen(flow: ConfigFlow, host: str, port: int) -> None:
    """Raise AutodartsError if the Board Manager does not answer on /api/state."""
    await board_erstellen(flow.hass, host, port).state()


def _adresse(info: ZeroconfServiceInfo) -> str | None:
    """IPv4 address of the announcing board (only addresses the board itself sent from)."""
    nutzbar = [a for a in info.ip_addresses if not (a.is_loopback or a.is_link_local or a.is_unspecified)]
    nutzbar.sort(key=lambda a: not isinstance(a, IPv4Address))
    return str(nutzbar[0]) if nutzbar else None


def _port(info: ZeroconfServiceInfo) -> int:
    """Plain HTTP port; newer Board Managers also announce an HTTPS port."""
    for wert in (info.properties.get("insecurePort"), info.port):
        try:
            port = int(wert)  # type: ignore[arg-type]
        except (TypeError, ValueError):
            continue
        if 0 < port < 65536:
            return port
    return STANDARD_PORT


class DartsConfigFlow(ConfigFlow, domain=DOMAIN):
    """Set up one Autodarts board."""

    VERSION = 1

    def __init__(self) -> None:
        self._gefunden: dict[str, Any] = {}

    async def _formular(self, step_id: str, user_input: dict[str, Any] | None, vorschlag: dict[str, Any] | None) -> ConfigFlowResult | None:
        """Test the input; return the form again on errors, None when the board answered."""
        fehler: dict[str, str] = {}
        if user_input is not None:
            try:
                await board_testen(self, user_input[CONF_HOST], user_input[CONF_PORT])
            except AutodartsError:
                fehler["base"] = "cannot_connect"
            else:
                return None
        return self.async_show_form(
            step_id=step_id,
            data_schema=self.add_suggested_values_to_schema(SCHEMA, user_input or vorschlag),
            errors=fehler,
        )

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()
        if (form := await self._formular("user", user_input, None)) is not None:
            return form
        assert user_input is not None
        return self.async_create_entry(title=GERAETENAME, data=user_input)

    async def async_step_zeroconf(self, discovery_info: ZeroconfServiceInfo) -> ConfigFlowResult:
        """The Board Manager announces itself as _autodarts-board._tcp."""
        host = _adresse(discovery_info)
        if host is None:
            return self.async_abort(reason="cannot_connect")
        port = _port(discovery_info)
        await self.async_set_unique_id(DOMAIN)
        # Board got a new address: take it over, but only if the old one no longer answers.
        eintrag = self.hass.config_entries.async_entry_for_domain_unique_id(DOMAIN, DOMAIN)
        if eintrag is not None and (eintrag.data[CONF_HOST], eintrag.data.get(CONF_PORT, STANDARD_PORT)) != (host, port):
            try:
                await board_testen(self, eintrag.data[CONF_HOST], eintrag.data.get(CONF_PORT, STANDARD_PORT))
            except AutodartsError:
                try:
                    await board_testen(self, host, port)
                except AutodartsError:
                    return self.async_abort(reason="already_configured")
                self._abort_if_unique_id_configured(updates={CONF_HOST: host, CONF_PORT: port})
        self._abort_if_unique_id_configured()
        try:
            await board_testen(self, host, port)
        except AutodartsError:
            return self.async_abort(reason="cannot_connect")
        self._gefunden = {CONF_HOST: host, CONF_PORT: port}
        self.context["title_placeholders"] = {"host": host}
        return await self.async_step_zeroconf_confirm()

    async def async_step_zeroconf_confirm(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        if user_input is not None:
            return self.async_create_entry(title=GERAETENAME, data=self._gefunden)
        self._set_confirm_only()
        return self.async_show_form(step_id="zeroconf_confirm", description_placeholders={"host": self._gefunden[CONF_HOST]})

    async def async_step_reconfigure(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        """Change address or port of the board."""
        eintrag = self._get_reconfigure_entry()
        if (form := await self._formular("reconfigure", user_input, dict(eintrag.data))) is not None:
            return form
        assert user_input is not None and self.source == SOURCE_RECONFIGURE
        return self.async_update_reload_and_abort(eintrag, data_updates=user_input)
