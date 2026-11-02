"""Config flow tests."""

from __future__ import annotations

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType

from custom_components.autodarts.const import CONF_HOST, CONF_PORT, DOMAIN

from .conftest import BASIS, HOST, PORT, STATE

EINGABE = {CONF_HOST: HOST, CONF_PORT: PORT}


async def test_user_flow_success(hass: HomeAssistant, aioclient_mock) -> None:
    aioclient_mock.get(f"{BASIS}/api/state", json=STATE)
    result = await hass.config_entries.flow.async_init(DOMAIN, context={"source": config_entries.SOURCE_USER})
    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {}
    result = await hass.config_entries.flow.async_configure(result["flow_id"], EINGABE)
    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["title"] == "Autodarts Board"
    assert result["data"] == EINGABE
    assert result["result"].unique_id == DOMAIN


async def test_user_flow_cannot_connect_then_recover(hass: HomeAssistant, aioclient_mock) -> None:
    aioclient_mock.get(f"{BASIS}/api/state", exc=TimeoutError)
    result = await hass.config_entries.flow.async_init(DOMAIN, context={"source": config_entries.SOURCE_USER})
    result = await hass.config_entries.flow.async_configure(result["flow_id"], EINGABE)
    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {"base": "cannot_connect"}

    aioclient_mock.clear_requests()
    aioclient_mock.get(f"{BASIS}/api/state", json=STATE)
    result = await hass.config_entries.flow.async_configure(result["flow_id"], EINGABE)
    assert result["type"] is FlowResultType.CREATE_ENTRY


async def test_user_flow_unexpected_answer(hass: HomeAssistant, aioclient_mock) -> None:
    aioclient_mock.get(f"{BASIS}/api/state", json=["not", "a", "board"])
    result = await hass.config_entries.flow.async_init(DOMAIN, context={"source": config_entries.SOURCE_USER})
    result = await hass.config_entries.flow.async_configure(result["flow_id"], EINGABE)
    assert result["errors"] == {"base": "cannot_connect"}


async def test_user_flow_http_error(hass: HomeAssistant, aioclient_mock) -> None:
    aioclient_mock.get(f"{BASIS}/api/state", status=500)
    result = await hass.config_entries.flow.async_init(DOMAIN, context={"source": config_entries.SOURCE_USER})
    result = await hass.config_entries.flow.async_configure(result["flow_id"], EINGABE)
    assert result["errors"] == {"base": "cannot_connect"}


async def test_already_configured(hass: HomeAssistant, mock_entry) -> None:
    mock_entry.add_to_hass(hass)
    result = await hass.config_entries.flow.async_init(DOMAIN, context={"source": config_entries.SOURCE_USER})
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "already_configured"
