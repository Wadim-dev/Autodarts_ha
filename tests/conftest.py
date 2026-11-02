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
