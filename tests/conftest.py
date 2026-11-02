"""Shared fixtures."""

from __future__ import annotations

import pytest

from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.autodarts.const import CONF_HOST, CONF_PORT, DOMAIN

HOST = "192.0.2.10"
PORT = 3180
BASIS = f"http://{HOST}:{PORT}"

STATE = {
    "status": "Throw",
    "event": "Throw detected",
    "running": True,
    "throws": [{"segment": {"name": "T20", "number": 20, "multiplier": 3, "bed": "Triple"}, "coords": {"x": 0.01, "y": -0.6}}],
}


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    """Load custom_components in every test."""
    return


@pytest.fixture
def mock_entry() -> MockConfigEntry:
    return MockConfigEntry(domain=DOMAIN, unique_id=DOMAIN, title="Autodarts Board", data={CONF_HOST: HOST, CONF_PORT: PORT})


SYSTEM = {
    "status": {"calibrated": True, "version": "1.0.0", "updateAvailable": "1.1.0", "calibratingCams": 0},
    "stats": {"cpuPercent": 12.5, "memoryBytes": 104857600, "fps": 25},
    "calibration": {"cams": [{"errorPx": 0.5}, {"errorPx": 1.25}]},
    "camStats": [{"fps": 30}, {"fps": 29}],
    "camState": {"isRunning": True},
    "config": {"motion": {"standbyMinutes": 15}, "cam": {"fps": 30, "width": 1280, "height": 720}},
}
DEVICES = [{"formats": [{"name": "MJPG", "resolutions": [
    {"width": 1280, "height": 720, "framerates": [30, 15]},
    {"width": 640, "height": 480, "framerates": [30]},
]}]}]
RING = [[i, i + 0.5] for i in range(20)]
ELLIPSES = {"0": {"doubleOuterPoints": RING, "doubleInnerPoints": RING, "trebleOuterPoints": RING,
                  "trebleInnerPoints": [], "bull": [1, 2]}, "1": "kaputt"}


def board_mock(aioclient_mock, state=None) -> None:
    """Answer every board endpoint like a running board."""
    aioclient_mock.get(f"{BASIS}/api/state", json=STATE if state is None else state)
    aioclient_mock.get(f"{BASIS}/api/system", json=SYSTEM)
    aioclient_mock.get(f"{BASIS}/api/devices", json=DEVICES)
    aioclient_mock.get(f"{BASIS}/api/host", json={"clientVersion": "1.0.0", "hostname": "board"})
    aioclient_mock.get(f"{BASIS}/api/config/calibration/ellipses", json=ELLIPSES)
    for pfad in ("start", "stop", "reset", "restart", "update/apply", "config/calibration/auto"):
        aioclient_mock.post(f"{BASIS}/api/{pfad}", status=200)
    aioclient_mock.patch(f"{BASIS}/api/config", status=200)


@pytest.fixture
async def geladen(hass, aioclient_mock, mock_entry):
    """Integration loaded against a mocked board; unloaded after the test."""
    board_mock(aioclient_mock)
    mock_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(mock_entry.entry_id)
    await hass.async_block_till_done()
    yield mock_entry
    await hass.config_entries.async_unload(mock_entry.entry_id)
    await hass.async_block_till_done()
