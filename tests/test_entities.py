"""Tests for buttons, selects, cameras, update, board API and availability."""

from __future__ import annotations

from datetime import timedelta
from unittest.mock import patch

from homeassistant.const import STATE_UNAVAILABLE
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.util import dt as dt_util
import pytest
from pytest_homeassistant_custom_component.common import async_fire_time_changed

from custom_components.autodarts.api import befehl

from .conftest import BASIS, STATE


def _aufrufe(aioclient_mock, methode: str, pfad: str) -> list:
    return [c for c in aioclient_mock.mock_calls if c[0] == methode and str(c[1]).endswith(pfad)]


async def test_system_werte(hass: HomeAssistant, geladen) -> None:
    assert hass.states.get("sensor.autodarts_board_cpu_load").state == "12.5"
    assert hass.states.get("sensor.autodarts_board_memory").state == "100.0"
    assert hass.states.get("sensor.autodarts_board_camera_frame_rate").state == "29"
    assert hass.states.get("sensor.autodarts_board_calibration_deviation").state == "1.25"
    assert hass.states.get("sensor.autodarts_board_board_software").attributes["hostname"] == "board"
    assert hass.states.get("binary_sensor.autodarts_board_calibrated").state == "on"
    assert hass.states.get("binary_sensor.autodarts_board_detection_running").state == "on"
    assert hass.states.get("sensor.autodarts_board_current_visit").state == "60"
    assert hass.states.get("sensor.autodarts_board_throw_1").attributes["punkte"] == 60
    assert hass.states.get("sensor.autodarts_board_throw_2").state == "-"
    kamera = hass.states.get("camera.autodarts_board_camera_1")
    assert kamera.attributes["kalibrierung"]["bull"] == [1, 2]
    assert "kalibrierung" not in hass.states.get("camera.autodarts_board_camera_2").attributes
    upd = hass.states.get("update.autodarts_board_board_software")
    assert upd.state == "on" and upd.attributes["latest_version"] == "1.1.0"


async def test_knoepfe(hass: HomeAssistant, geladen, aioclient_mock) -> None:
    for name, pfad in (("stop_detection", "/api/stop"), ("reset_throws", "/api/reset"),
                       ("restart_board_software", "/api/restart")):
        await hass.services.async_call("button", "press", {"entity_id": f"button.autodarts_board_{name}"}, blocking=True)
        assert _aufrufe(aioclient_mock, "POST", pfad)
    # calibration needs running cameras: start first
    geladen.runtime_data.zustand.data["laeuft"] = False
    with patch("custom_components.autodarts.button.asyncio.sleep"):
        await hass.services.async_call("button", "press", {"entity_id": "button.autodarts_board_calibrate"}, blocking=True)
    assert _aufrufe(aioclient_mock, "POST", "/api/start")
    assert _aufrufe(aioclient_mock, "POST", "/api/config/calibration/auto")


async def test_auswahl(hass: HomeAssistant, geladen, aioclient_mock) -> None:
    standby = hass.states.get("select.autodarts_board_camera_standby")
    assert standby.state == "15"
    rate = hass.states.get("select.autodarts_board_camera_frame_rate_setting")
    assert rate.attributes["options"] == ["30", "15"] and rate.state == "30"
    aufl = hass.states.get("select.autodarts_board_camera_resolution")
    assert aufl.attributes["options"] == ["1280x720", "640x480"]
    for eid, option, erwartet in (
        ("camera_standby", "30", {"motion": {"standbyMinutes": 30}}),
        ("camera_frame_rate_setting", "15", {"cam": {"fps": 15}}),
        ("camera_resolution", "640x480", {"cam": {"width": 640, "height": 480}}),
    ):
        await hass.services.async_call("select", "select_option", {"entity_id": f"select.autodarts_board_{eid}", "option": option}, blocking=True)
        assert _aufrufe(aioclient_mock, "PATCH", "/api/config")[-1][2] == erwartet


async def test_auswahl_ohne_geraeteliste(hass: HomeAssistant, geladen) -> None:
    d = geladen.runtime_data
    d.system.geraete = []
    d.system.data["konfig"] = {"cam": {"fps": 25}}
    d.system.async_update_listeners()
    assert hass.states.get("select.autodarts_board_camera_frame_rate_setting").attributes["options"] == ["25"]
    aufl = hass.states.get("select.autodarts_board_camera_resolution")
    assert aufl.attributes["options"] == ["1280x720"] and aufl.state == "unknown"
    assert hass.states.get("select.autodarts_board_camera_standby").state == "unknown"
    d.system.data["konfig"] = {"cam": {"fps": 60, "width": 800, "height": 600}}
    d.system.geraete = [{"formats": [{"name": "MJPG", "resolutions": [{"width": 640, "height": 480, "framerates": [30]}]}]}]
    d.system.async_update_listeners()
    assert hass.states.get("select.autodarts_board_camera_frame_rate_setting").attributes["options"] == ["60", "30"]
    assert hass.states.get("select.autodarts_board_camera_resolution").attributes["options"] == ["800x600", "640x480"]


async def test_kamera(hass: HomeAssistant, geladen, aioclient_mock, hass_client) -> None:
    aioclient_mock.get(f"{BASIS}/api/img/cams/0", content=b"jpeg")
    aioclient_mock.get(f"{BASIS}/api/img/live", status=404)
    aioclient_mock.get(f"{BASIS}/api/streams/cams/0", content=b"--frame")
    from homeassistant.components.camera import async_get_image

    bild = await async_get_image(hass, "camera.autodarts_board_camera_1")
    assert bild.content == b"jpeg"
    with pytest.raises(HomeAssistantError):
        await async_get_image(hass, "camera.autodarts_board_live_image")
    client = await hass_client()
    token = hass.states.get("camera.autodarts_board_camera_1").attributes["access_token"]
    antwort = await client.get(f"/api/camera_proxy_stream/camera.autodarts_board_camera_1?token={token}")
    assert antwort.status == 200


async def test_board_update(hass: HomeAssistant, geladen, aioclient_mock) -> None:
    await hass.services.async_call("update", "install", {"entity_id": "update.autodarts_board_board_software"}, blocking=True)
    assert _aufrufe(aioclient_mock, "POST", "/api/update/apply")


async def test_befehl_put_und_fehler(hass: HomeAssistant, geladen, aioclient_mock) -> None:
    board = geladen.runtime_data.board
    aioclient_mock.clear_requests()
    aioclient_mock.post(f"{BASIS}/api/neu", status=405)
    aioclient_mock.put(f"{BASIS}/api/neu", status=200)
    await befehl(board.command("neu"))
    assert _aufrufe(aioclient_mock, "PUT", "/api/neu")

    aioclient_mock.post(f"{BASIS}/api/kaputt", status=500)
    with pytest.raises(HomeAssistantError) as err:
        await befehl(board.command("kaputt"))
    assert err.value.translation_key == "board_error"
    assert err.value.translation_placeholders == {"status": "500", "path": "/api/kaputt"}

    aioclient_mock.post(f"{BASIS}/api/weg", exc=TimeoutError)
    with pytest.raises(HomeAssistantError) as err:
        await befehl(board.command("weg"))
    assert err.value.translation_key == "board_unreachable"


async def test_offline_und_wieder_online(hass: HomeAssistant, geladen, aioclient_mock) -> None:
    aioclient_mock.clear_requests()
    aioclient_mock.get(f"{BASIS}/api/state", exc=TimeoutError)
    # a busy board that misses one or two answers stays online (game start at full CPU)
    for i in (2, 4):
        async_fire_time_changed(hass, dt_util.utcnow() + timedelta(seconds=i))
        await hass.async_block_till_done()
        assert hass.states.get("sensor.autodarts_board_connection").state == "Online"
        assert hass.states.get("camera.autodarts_board_camera_1").state != STATE_UNAVAILABLE
    async_fire_time_changed(hass, dt_util.utcnow() + timedelta(seconds=6))
    await hass.async_block_till_done()
    # connection and status keep showing "Offline", everything else is unavailable
    assert hass.states.get("sensor.autodarts_board_connection").state == "Offline"
    assert hass.states.get("sensor.autodarts_board_status").state == "Offline"
    for eid in ("sensor.autodarts_board_throw_1", "sensor.autodarts_board_current_visit",
                "binary_sensor.autodarts_board_detection_running", "button.autodarts_board_start_detection",
                "camera.autodarts_board_camera_1", "select.autodarts_board_camera_standby"):
        assert hass.states.get(eid).state == STATE_UNAVAILABLE, eid
    # system data are dropped while offline
    async_fire_time_changed(hass, dt_util.utcnow() + timedelta(seconds=20))
    await hass.async_block_till_done()
    assert hass.states.get("sensor.autodarts_board_cpu_load").state == STATE_UNAVAILABLE

    aioclient_mock.clear_requests()
    aioclient_mock.get(f"{BASIS}/api/state", json=STATE)
    async_fire_time_changed(hass, dt_util.utcnow() + timedelta(seconds=60))
    await hass.async_block_till_done()
    assert hass.states.get("sensor.autodarts_board_connection").state == "Online"
    assert hass.states.get("sensor.autodarts_board_throw_1").state == "T20"


async def test_systemdaten_fehler(hass: HomeAssistant, geladen, aioclient_mock) -> None:
    aioclient_mock.clear_requests()
    aioclient_mock.get(f"{BASIS}/api/state", json=STATE)
    aioclient_mock.get(f"{BASIS}/api/system", exc=TimeoutError)
    async_fire_time_changed(hass, dt_util.utcnow() + timedelta(seconds=20))
    await hass.async_block_till_done()
    assert hass.states.get("sensor.autodarts_board_cpu_load").state == STATE_UNAVAILABLE
