"""Board client (board.py): answers, errors, commands and images."""

from __future__ import annotations

import asyncio

from aiohttp import ClientError
import pytest
from pytest_homeassistant_custom_component.test_util.aiohttp import AiohttpClientMocker

from custom_components.autodarts.board import AutodartsBoard, AutodartsConnectionError, AutodartsResponseError

URL = "http://pc:3180/api/"


@pytest.fixture
async def board(aioclient_mock: AiohttpClientMocker) -> AutodartsBoard:
    return AutodartsBoard("pc", session=aioclient_mock.create_session(asyncio.get_running_loop()), request_timeout=1)


async def test_lesen(aioclient_mock: AiohttpClientMocker, board: AutodartsBoard) -> None:
    assert board.url == "http://pc:3180"
    for pfad, daten in [("state", {"status": "Throw"}), ("system", {"a": 1}), ("devices", [{"id": 0}]),
                        ("host", {"hostname": "pc"}), ("config", {"cam": {}}), ("config/calibration/ellipses", {"0": []})]:
        aioclient_mock.get(URL + pfad, json=daten)
    assert await board.state() == {"status": "Throw"}
    assert await board.system() == {"a": 1}
    assert await board.devices() == [{"id": 0}]
    assert await board.host_info() == {"hostname": "pc"}
    assert await board.config() == {"cam": {}}
    assert await board.calibration_ellipses() == {"0": []}


@pytest.mark.parametrize(("text", "fehler"), [("null", None), ('["x"]', "list"), ("kein json", "")])
async def test_falsche_antworten(aioclient_mock: AiohttpClientMocker, board: AutodartsBoard, text: str, fehler: str | None) -> None:
    aioclient_mock.get(URL + "state", text=text)
    aioclient_mock.get(URL + "devices", text=text.replace('["x"]', '{"a": 1}'))
    if fehler is None:
        assert await board.state() == {} and await board.devices() == []
        return
    with pytest.raises(AutodartsConnectionError, match=fehler):
        await board.state()
    with pytest.raises(AutodartsConnectionError):
        await board.devices()


async def test_fehler(aioclient_mock: AiohttpClientMocker, board: AutodartsBoard) -> None:
    aioclient_mock.get(URL + "state", status=500)
    aioclient_mock.get(URL + "system", exc=ClientError())
    aioclient_mock.post(URL + "reset", exc=TimeoutError())
    aioclient_mock.get(URL + "img/live", exc=ClientError())
    with pytest.raises(AutodartsResponseError) as err:
        await board.state()
    assert err.value.status == 500 and str(err.value) == "Board answered 500 for /api/state"
    with pytest.raises(AutodartsConnectionError, match="ClientError"):
        await board.system()
    with pytest.raises(AutodartsConnectionError, match="TimeoutError"):
        await board.reset()
    assert await board.image("live") is None


@pytest.mark.parametrize(("methode", "pfad"), [("start", "start"), ("stop", "stop"), ("reset", "reset"),
                                               ("calibrate", "config/calibration/auto"), ("restart", "restart"),
                                               ("apply_update", "update/apply")])
async def test_befehle(aioclient_mock: AiohttpClientMocker, board: AutodartsBoard, methode: str, pfad: str) -> None:
    aioclient_mock.post(URL + pfad)
    await getattr(board, methode)()
    assert [(m.lower(), str(u)) for m, u, *_ in aioclient_mock.mock_calls] == [("post", URL + pfad)]


async def test_put_und_config(aioclient_mock: AiohttpClientMocker, board: AutodartsBoard) -> None:
    aioclient_mock.post(URL + "start", status=405)
    aioclient_mock.put(URL + "start")
    await board.start()
    assert [c[0].lower() for c in aioclient_mock.mock_calls] == ["post", "put"]
    aioclient_mock.patch(URL + "config")
    await board.set_config({"cam": {"fps": 15}})
    assert aioclient_mock.mock_calls[-1][2] == {"cam": {"fps": 15}}
    aioclient_mock.post(URL + "stop", status=500)
    with pytest.raises(AutodartsResponseError):
        await board.stop()


async def test_bilder(aioclient_mock: AiohttpClientMocker, board: AutodartsBoard) -> None:
    aioclient_mock.get(URL + "img/cams/1", content=b"jpg")
    aioclient_mock.get(URL + "img/detection", status=404)
    assert await board.image("cam1") == b"jpg"
    assert await board.image("detection") is None
    assert board.stream_url("cam2") == URL + "streams/cams/2"
    assert board.stream_url("live") == URL + "streams/live"
