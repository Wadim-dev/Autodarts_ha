"""Config flow tests."""

from __future__ import annotations

from unittest.mock import patch

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


def _zeroconf(adresse: str = HOST, eigenschaften: dict | None = None):
    from ipaddress import ip_address

    from homeassistant.helpers.service_info.zeroconf import ZeroconfServiceInfo

    return ZeroconfServiceInfo(
        ip_address=ip_address(adresse), ip_addresses=[ip_address("fe80::1"), ip_address(adresse)],
        hostname="board.local.", name="board._autodarts-board._tcp.local.", port=3181,
        properties=eigenschaften if eigenschaften is not None else {"insecurePort": str(PORT)}, type="_autodarts-board._tcp.local.",
    )


async def test_zeroconf_found_and_confirmed(hass: HomeAssistant, aioclient_mock) -> None:
    aioclient_mock.get(f"{BASIS}/api/state", json=STATE)
    result = await hass.config_entries.flow.async_init(DOMAIN, context={"source": config_entries.SOURCE_ZEROCONF}, data=_zeroconf())
    assert result["type"] is FlowResultType.FORM and result["step_id"] == "zeroconf_confirm"
    result = await hass.config_entries.flow.async_configure(result["flow_id"], {})
    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["data"] == EINGABE


async def test_zeroconf_board_not_answering(hass: HomeAssistant, aioclient_mock) -> None:
    aioclient_mock.get(f"http://{HOST}:3181/api/state", exc=TimeoutError)
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_ZEROCONF}, data=_zeroconf(eigenschaften={"insecurePort": "x"}))
    assert result["type"] is FlowResultType.ABORT and result["reason"] == "cannot_connect"


async def test_zeroconf_only_link_local(hass: HomeAssistant) -> None:
    from ipaddress import ip_address

    info = _zeroconf()
    info.ip_addresses = [ip_address("fe80::1")]
    result = await hass.config_entries.flow.async_init(DOMAIN, context={"source": config_entries.SOURCE_ZEROCONF}, data=info)
    assert result["reason"] == "cannot_connect"


async def test_zeroconf_already_configured(hass: HomeAssistant, mock_entry) -> None:
    mock_entry.add_to_hass(hass)
    result = await hass.config_entries.flow.async_init(DOMAIN, context={"source": config_entries.SOURCE_ZEROCONF}, data=_zeroconf())
    assert result["reason"] == "already_configured"


async def test_zeroconf_new_address(hass: HomeAssistant, mock_entry, aioclient_mock) -> None:
    """Old address dead, new one answers: the entry follows the board."""
    mock_entry.add_to_hass(hass)
    neu = "192.0.2.20"
    aioclient_mock.get(f"{BASIS}/api/state", exc=TimeoutError)
    aioclient_mock.get(f"http://{neu}:{PORT}/api/state", json=STATE)
    result = await hass.config_entries.flow.async_init(DOMAIN, context={"source": config_entries.SOURCE_ZEROCONF}, data=_zeroconf(neu))
    assert result["reason"] == "already_configured"
    assert mock_entry.data[CONF_HOST] == neu


async def test_zeroconf_other_device_ignored(hass: HomeAssistant, mock_entry, aioclient_mock) -> None:
    """Old address still answers: another announcement does not move the entry."""
    mock_entry.add_to_hass(hass)
    aioclient_mock.get(f"{BASIS}/api/state", json=STATE)
    result = await hass.config_entries.flow.async_init(DOMAIN, context={"source": config_entries.SOURCE_ZEROCONF}, data=_zeroconf("192.0.2.30"))
    assert result["reason"] == "already_configured"
    assert mock_entry.data[CONF_HOST] == HOST


async def test_zeroconf_new_address_dead_too(hass: HomeAssistant, mock_entry, aioclient_mock) -> None:
    mock_entry.add_to_hass(hass)
    aioclient_mock.get(f"{BASIS}/api/state", exc=TimeoutError)
    aioclient_mock.get(f"http://192.0.2.40:{PORT}/api/state", exc=TimeoutError)
    result = await hass.config_entries.flow.async_init(DOMAIN, context={"source": config_entries.SOURCE_ZEROCONF}, data=_zeroconf("192.0.2.40"))
    assert result["reason"] == "already_configured"
    assert mock_entry.data[CONF_HOST] == HOST


async def test_reconfigure(hass: HomeAssistant, mock_entry, aioclient_mock) -> None:
    mock_entry.add_to_hass(hass)
    neu = {CONF_HOST: "192.0.2.50", CONF_PORT: 3180}
    aioclient_mock.get("http://192.0.2.50:3180/api/state", exc=TimeoutError)
    result = await mock_entry.start_reconfigure_flow(hass)
    assert result["type"] is FlowResultType.FORM and result["step_id"] == "reconfigure"
    result = await hass.config_entries.flow.async_configure(result["flow_id"], neu)
    assert result["errors"] == {"base": "cannot_connect"}
    aioclient_mock.clear_requests()
    aioclient_mock.get("http://192.0.2.50:3180/api/state", json=STATE)
    with patch("custom_components.autodarts.async_setup_entry", return_value=True):
        result = await hass.config_entries.flow.async_configure(result["flow_id"], neu)
    assert result["type"] is FlowResultType.ABORT and result["reason"] == "reconfigure_successful"
    assert mock_entry.data == neu
