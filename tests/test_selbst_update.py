"""The integration updates itself from custom_templates/autodarts_update."""

from __future__ import annotations

import json
from pathlib import Path
import shutil
from unittest.mock import patch

from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity_component import async_update_entity
import pytest
from pytest_homeassistant_custom_component.common import async_mock_service

from custom_components.autodarts import update as update_modul

UPD = "update.autodarts_board_integration"


@pytest.fixture(autouse=True)
def eingeschaltet():
    """The entity is off by default (updates come through the Marketplace); switch it on for these tests."""
    with patch.object(update_modul.IntegrationUpdate, "_attr_entity_registry_enabled_default", True):
        yield


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


def test_patch(tmp_path: Path) -> None:
    ziel = tmp_path / "ziel"
    ziel.mkdir()
    (ziel / "a.js").write_text("eins\nzwei\ndrei\nvier\nfünf\n")
    (ziel / "b.js").write_text("x\ny")
    ablage = tmp_path / "ablage"
    ablage.mkdir()
    (ablage / "a.js.patch").write_text("--- a/a.js\n+++ b/a.js\n@@ -1,3 +1,3 @@\n eins\n-zwei\n+ZWEI\n drei\n@@ -5 +5,2 @@\n fünf\n+sechs\n")
    (ablage / "b.js.patch").write_text("@@ -2 +2 @@\n-y\n\\ No newline at end of file\n+z\n\\ No newline at end of file\n")
    update_modul._einspielen(ablage, ziel)
    assert (ziel / "a.js").read_text() == "eins\nZWEI\ndrei\nvier\nfünf\nsechs\n"
    assert (ziel / "b.js").read_text() == "x\nz"
    # a patch that does not fit changes nothing
    ablage.mkdir()
    (ablage / "neu.txt").write_text("neu")
    (ablage / "a.js.patch").write_text("@@ -1 +1 @@\n-falsch\n+x\n")
    with pytest.raises(update_modul.PatchFehler):
        update_modul._einspielen(ablage, ziel)
    assert not (ziel / "neu.txt").exists() and ablage.exists()


async def test_patch_fehler_meldung(hass: HomeAssistant, geladen, tmp_path: Path) -> None:
    ablage = Path(hass.config.path("custom_templates", "autodarts_update"))
    ablage.mkdir(parents=True, exist_ok=True)
    (ablage / "x.py.patch").write_text("@@ -1 +1 @@\n-a\n+b\n")
    (ablage / "manifest.json").write_text(json.dumps({"domain": "autodarts", "version": "99.0.0"}))
    (tmp_path / "x.py").write_text("anders\n")
    await async_update_entity(hass, UPD)
    with patch.object(update_modul, "ZIEL", tmp_path), pytest.raises(HomeAssistantError):
        await hass.services.async_call("update", "install", {"entity_id": UPD}, blocking=True)
    assert (tmp_path / "x.py").read_text() == "anders\n"
    shutil.rmtree(ablage)
