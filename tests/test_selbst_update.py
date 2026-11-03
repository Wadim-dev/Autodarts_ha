"""The integration updates itself from custom_templates/autodarts_update."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity_component import async_update_entity
import pytest
from pytest_homeassistant_custom_component.common import async_mock_service

from custom_components.autodarts import update as update_modul

UPD = "update.autodarts_board_integration"


async def test_selbst_update(hass: HomeAssistant, geladen, tmp_path: Path, hass_ws_client) -> None:
    neustart = async_mock_service(hass, "homeassistant", "restart")
    ziel = tmp_path / "autodarts"
    (ziel / "frontend").mkdir(parents=True)
    (ziel / "alt.py").write_text("x")
    (ziel / "bleibt.py").write_text("alt")
    state = hass.states.get(UPD)
    alt = state.attributes["installed_version"]
    assert state.state == "off" and state.attributes["latest_version"] == alt
    with pytest.raises(HomeAssistantError):
        await hass.services.async_call("update", "install", {"entity_id": UPD}, blocking=True)

    ablage = Path(hass.config.path("custom_templates", "autodarts_update"))
    (ablage / "frontend").mkdir(parents=True)
    (ablage / "frontend" / "karte.js").write_text("neu")
    (ablage / "__pycache__").mkdir()
    (ablage / "__pycache__" / "x.pyc").write_text("weg")
    (ablage / "_entfernen.txt").write_text("alt.py\n../../ausserhalb.txt\n\n")
    (ablage / "CHANGELOG.md").write_text("# Changelog\n\n## 99.0.0\n\n- Neu\n\n## 1.0.0\n\n- alt\n")
    (ablage / "manifest.json").write_text(json.dumps({"domain": "autodarts", "version": "99.0.0"}))
    await async_update_entity(hass, UPD)
    state = hass.states.get(UPD)
    assert state.state == "on" and state.attributes["latest_version"] == "99.0.0"
    ws = await hass_ws_client(hass)
    await ws.send_json({"id": 1, "type": "update/release_notes", "entity_id": UPD})
    assert (await ws.receive_json())["result"] == "- Neu"

    with patch.object(update_modul, "ZIEL", ziel):
        await hass.services.async_call("update", "install", {"entity_id": UPD}, blocking=True)
    assert (ziel / "frontend" / "karte.js").read_text() == "neu"
    assert (ziel / "manifest.json").exists() and not (ziel / "alt.py").exists() and (ziel / "bleibt.py").exists()
    assert not (ziel / "CHANGELOG.md").exists() and not (ziel / "__pycache__").exists()
    assert not ablage.exists() and len(neustart) == 1
    assert hass.states.get(UPD).attributes["installed_version"] == "99.0.0"


def test_ablage_kaputt(tmp_path: Path) -> None:
    assert update_modul._neue_version(tmp_path) is None
    (tmp_path / "manifest.json").write_text('{"domain": "anders", "version": "9"}')
    assert update_modul._neue_version(tmp_path) is None
    (tmp_path / "manifest.json").write_text("kaputt")
    assert update_modul._neue_version(tmp_path) is None
    assert update_modul._hinweise(tmp_path, "1.0.0") is None
    (tmp_path / "CHANGELOG.md").write_text("## 2.0.0\n- x")
    assert update_modul._hinweise(tmp_path, "1.0.0") is None
