"""Update entities: the board software (reported by the board) and this integration.

The integration is kept private. A new version is put into the folder
custom_templates/autodarts_update (manifest.json last). The integration update entity
offers it; installing copies the files over the integration and restarts Home Assistant.
"""

from __future__ import annotations

from datetime import timedelta
import json
from pathlib import Path
import shutil
from typing import Any

from awesomeversion import AwesomeVersion
from homeassistant.components.update import UpdateDeviceClass, UpdateEntity, UpdateEntityFeature
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.loader import async_get_integration

from .api import befehl
from .const import DOMAIN
from .coordinator import DartsDaten, DartsEntry
from .entity import DartsEntitaet

PARALLEL_UPDATES = 1
SCAN_INTERVAL = timedelta(minutes=1)  # only the integration update polls (one small file)
ABLAGE = ("custom_templates", "autodarts_update")
ENTFERNEN = "_entfernen.txt"  # files of the old version to delete, one path per line
NICHT_KOPIEREN = {ENTFERNEN, "CHANGELOG.md"}
ZIEL = Path(__file__).parent


async def async_setup_entry(hass: HomeAssistant, entry: DartsEntry, async_add_entities: AddEntitiesCallback) -> None:
    installiert = (await async_get_integration(hass, DOMAIN)).version
    async_add_entities([BoardUpdate(entry.runtime_data), IntegrationUpdate(entry.runtime_data, str(installiert or "0"))], True)


def _neue_version(ablage: Path) -> str | None:
    try:
        m = json.loads((ablage / "manifest.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return str(m["version"]) if isinstance(m, dict) and m.get("domain") == DOMAIN and m.get("version") else None


def _hinweise(ablage: Path, version: str) -> str | None:
    try:
        text = (ablage / "CHANGELOG.md").read_text(encoding="utf-8")
    except OSError:
        return None
    teil = text.split(f"## {version}\n", 1)
    return teil[1].split("\n## ", 1)[0].strip() if len(teil) == 2 else None


def _einspielen(ablage: Path, ziel: Path) -> None:
    for datei in sorted(ablage.rglob("*")):
        rel = datei.relative_to(ablage)
        if datei.is_dir() or rel.parts[0] in NICHT_KOPIEREN or "__pycache__" in rel.parts:
            continue
        (ziel / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(datei, ziel / rel)
    if (liste := ablage / ENTFERNEN).is_file():
        for zeile in liste.read_text(encoding="utf-8").splitlines():
            alt = (ziel / zeile.strip()).resolve()
            if zeile.strip() and alt.is_file() and alt.is_relative_to(ziel.resolve()):
                alt.unlink()
    shutil.rmtree(ablage)


class BoardUpdate(DartsEntitaet, UpdateEntity):
    """Update der Board-Software (meldet das Board selbst)."""

    _attr_entity_category = EntityCategory.CONFIG
    _attr_supported_features = UpdateEntityFeature.INSTALL
    _attr_title = "Autodarts Board"
    _attr_device_class = UpdateDeviceClass.FIRMWARE

    def __init__(self, d: DartsDaten) -> None:
        super().__init__(d, d.system, "board_update", "board_software")

    @property
    def available(self) -> bool:
        return super().available and bool(self.coordinator.data)

    @property
    def installed_version(self) -> str | None:
        return (self.coordinator.data or {}).get("version")

    @property
    def latest_version(self) -> str | None:
        neu = (self.coordinator.data or {}).get("update")
        return neu or self.installed_version

    async def async_install(self, version: str | None, backup: bool, **kwargs: Any) -> None:
        await befehl(self.daten.board.apply_update())
        await self.coordinator.async_request_refresh()


class IntegrationUpdate(UpdateEntity):
    """Update of this integration from the private folder custom_templates/autodarts_update."""

    _attr_has_entity_name = True
    _attr_translation_key = "integration"
    _attr_entity_category = EntityCategory.CONFIG
    _attr_supported_features = UpdateEntityFeature.INSTALL | UpdateEntityFeature.RELEASE_NOTES
    _attr_title = "Autodarts (unofficial)"

    def __init__(self, d: DartsDaten, installiert: str) -> None:
        self._attr_unique_id = f"{DOMAIN}_integration_update"
        self._attr_device_info = d.geraet
        self._attr_installed_version = installiert
        self._attr_latest_version = installiert

    @property
    def _ablage(self) -> Path:
        return Path(self.hass.config.path(*ABLAGE))

    async def async_update(self) -> None:
        neu = await self.hass.async_add_executor_job(_neue_version, self._ablage)
        alt = self._attr_installed_version or "0"
        self._attr_latest_version = neu if neu and AwesomeVersion(neu) > AwesomeVersion(alt) else alt

    async def async_release_notes(self) -> str | None:
        return await self.hass.async_add_executor_job(_hinweise, self._ablage, self._attr_latest_version or "")

    async def async_install(self, version: str | None, backup: bool, **kwargs: Any) -> None:
        await self.async_update()
        if self._attr_latest_version == self._attr_installed_version:
            raise HomeAssistantError(translation_domain=DOMAIN, translation_key="no_update")
        await self.hass.async_add_executor_job(_einspielen, self._ablage, ZIEL)
        self._attr_installed_version = self._attr_latest_version
        self.async_write_ha_state()
        await self.hass.services.async_call("homeassistant", "restart")
