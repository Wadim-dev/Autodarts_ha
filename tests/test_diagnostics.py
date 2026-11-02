"""Diagnostics test."""

from __future__ import annotations

from homeassistant.core import HomeAssistant

from custom_components.autodarts.diagnostics import async_get_config_entry_diagnostics


async def test_diagnostics(hass: HomeAssistant, geladen) -> None:
    daten = await async_get_config_entry_diagnostics(hass, geladen)
    assert daten["entry"]["data"]["host"] == "**REDACTED**"
    assert daten["board"]["online"] is True
    assert daten["board"]["system"]["host"]["hostname"] == "**REDACTED**"
    assert "netz" not in daten["board"]["system"]
    assert daten["board"]["calibration_cameras"] == ["0"]
    assert daten["game"] == {"phase": "idle", "players": 0, "finished_games": 0, "running": False}
