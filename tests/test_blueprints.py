"""The blueprints in blueprints/automation/autodarts load and do what they say."""

from __future__ import annotations

from pathlib import Path
import shutil
from unittest.mock import patch

from homeassistant.core import HomeAssistant
from homeassistant.setup import async_setup_component
import pytest
from pytest_homeassistant_custom_component.common import async_mock_service

QUELLE = Path(__file__).parent.parent / "blueprints" / "automation" / "autodarts"
EVENT = "event.autodarts_board_game_event"


@pytest.fixture
def blueprints(hass: HomeAssistant) -> None:
    ziel = Path(hass.config.path("blueprints", "automation", "autodarts"))
    ziel.mkdir(parents=True, exist_ok=True)
    for f in QUELLE.glob("*.yaml"):
        shutil.copy(f, ziel / f.name)


async def _automation(hass: HomeAssistant, datei: str, eingaben: dict) -> None:
    hass.states.async_set(EVENT, "unknown", {"event_types": []})
    assert await async_setup_component(hass, "automation", {"automation": [
        {"alias": datei, "use_blueprint": {"path": f"autodarts/{datei}", "input": eingaben}}]})
    await hass.async_block_till_done()
    assert hass.states.get("automation." + datei.replace(".", "_")).state == "on"


def _ereignis(hass: HomeAssistant, zeit: str, typ: str, **daten) -> None:
    hass.states.async_set(EVENT, zeit, {"event_type": typ, **daten})


async def test_awtrix(hass: HomeAssistant, blueprints) -> None:
    aufrufe = async_mock_service(hass, "mqtt", "publish")
    await _automation(hass, "awtrix.yaml", {"event_entity": EVENT, "prefix": "awtrix_1"})
    _ereignis(hass, "2026-11-03T10:00:00", "dart", player="Alex")
    _ereignis(hass, "2026-11-03T10:00:01", "one_eighty", player="Alex", score=180)
    _ereignis(hass, "2026-11-03T10:00:02", "checkout", player="Sam", finish=121)
    await hass.async_block_till_done()
    assert [a.data["topic"] for a in aufrufe] == ["awtrix_1/notify"] * 2
    assert '"text":"180! Alex"' in aufrufe[0].data["payload"] and '"rainbow":true' in aufrufe[0].data["payload"]
    assert '"text":"Checkout 121 Sam"' in aufrufe[1].data["payload"] and "#43A047" in aufrufe[1].data["payload"]


async def test_caller(hass: HomeAssistant, blueprints) -> None:
    aufrufe = async_mock_service(hass, "tts", "speak")
    await _automation(hass, "caller.yaml", {"event_entity": EVENT, "tts": "tts.x", "speaker": "media_player.y"})
    _ereignis(hass, "2026-11-03T10:00:01", "match_won", player="Mia")
    _ereignis(hass, "2026-11-03T10:00:02", "ton", player="Mia", score=100)
    await hass.async_block_till_done()
    assert len(aufrufe) == 1
    assert aufrufe[0].data["message"] == "Game shot, and the match, Mia!"
    assert aufrufe[0].data["media_player_entity_id"] == "media_player.y"


async def test_notify(hass: HomeAssistant, blueprints) -> None:
    with patch("homeassistant.components.device_automation.action.async_validate_action_config", side_effect=lambda h, c: c), \
         patch("homeassistant.helpers.script.device_action.async_call_action_from_config") as aufruf:
        await _automation(hass, "notify.yaml", {"event_entity": EVENT, "phone": "handy123"})
        _ereignis(hass, "2026-11-03T10:00:01", "tournament_won", player="Sam")
        _ereignis(hass, "2026-11-03T10:00:02", "bust", player="Sam")
        await hass.async_block_till_done()
    assert aufruf.call_count == 1
    variablen = aufruf.call_args.args[2]
    assert variablen["a"]["event_type"] == "tournament_won"
