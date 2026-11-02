"""Setup and unload tests."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntryState
from homeassistant.core import HomeAssistant

from custom_components.autodarts.const import DOMAIN

from .conftest import BASIS, STATE


def _board(aioclient_mock) -> None:
    aioclient_mock.get(f"{BASIS}/api/state", json=STATE)
    aioclient_mock.get(f"{BASIS}/api/system", json={"status": {"calibrated": True, "version": "1.0.0"}, "stats": {"cpuPercent": 12.5}})
    aioclient_mock.get(f"{BASIS}/api/devices", json=[])
    aioclient_mock.get(f"{BASIS}/api/host", json={"clientVersion": "1.0.0"})
    aioclient_mock.get(f"{BASIS}/api/config/calibration/ellipses", json={})


async def test_setup_and_unload(hass: HomeAssistant, aioclient_mock, mock_entry) -> None:
    _board(aioclient_mock)
    mock_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(mock_entry.entry_id)
    await hass.async_block_till_done()
    assert mock_entry.state is ConfigEntryState.LOADED
    assert hass.states.get("sensor.autodarts_board_throw_1").state == "T20"
    assert hass.states.get("sensor.autodarts_board_connection").state == "Online"
    assert hass.services.has_service(DOMAIN, "spiel_starten")

    assert await hass.config_entries.async_unload(mock_entry.entry_id)
    await hass.async_block_till_done()
    assert mock_entry.state is ConfigEntryState.NOT_LOADED


async def test_setup_board_offline(hass: HomeAssistant, aioclient_mock, mock_entry) -> None:
    aioclient_mock.get(f"{BASIS}/api/state", exc=TimeoutError)
    mock_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(mock_entry.entry_id)
    await hass.async_block_till_done()
    assert mock_entry.state is ConfigEntryState.LOADED
    assert hass.states.get("sensor.autodarts_board_connection").state == "Offline"


async def test_karten_werden_geladen(hass: HomeAssistant) -> None:
    """With the frontend running, the card file is served and added to every dashboard."""
    from unittest.mock import AsyncMock, MagicMock, patch

    from custom_components.autodarts import KARTEN_URL, _karten_anmelden

    hass.http = MagicMock(async_register_static_paths=AsyncMock())
    hass.config.components.add("frontend")
    with patch("custom_components.autodarts.add_extra_js_url") as extra:
        await _karten_anmelden(hass)
    pfad = hass.http.async_register_static_paths.call_args[0][0][0]
    assert pfad.url_path == KARTEN_URL and pfad.path.endswith("autodarts-cards.js")
    assert extra.call_args[0][1].startswith(KARTEN_URL + "?v=")
