"""Light on the board PC: shared camera images, CPU of the whole PC, camera standby."""

from __future__ import annotations

import asyncio
import time
from unittest.mock import AsyncMock, patch

from homeassistant.core import HomeAssistant

from custom_components.autodarts.coordinator import ZustandKoordinator, _kerne
from custom_components.autodarts.verteiler import Bildverteiler

from .test_spiel import _dienst, _spieler


class _Board:
    def __init__(self) -> None:
        self.anfragen = 0

    async def image(self, strom: str) -> bytes | None:
        self.anfragen += 1
        await asyncio.sleep(0)
        return f"{strom}-{self.anfragen}".encode()


async def _bis(bedingung, zeit: float = 3.0) -> None:
    ende = time.monotonic() + zeit
    while not bedingung():
        assert time.monotonic() < ende
        await asyncio.sleep(0.01)


async def test_ein_strom_fuer_alle(hass: HomeAssistant) -> None:
    board = _Board()
    v = Bildverteiler(hass, board)  # type: ignore[arg-type]
    gesehen: dict[str, list[bytes]] = {"a": [], "b": []}

    async def zuschauer(name: str, takt: float) -> None:
        async for bild in v.bilder("cam0", takt):
            gesehen[name].append(bild)

    a = hass.async_create_task(zuschauer("a", 0.05))
    b = hass.async_create_task(zuschauer("b", 0.2))
    await _bis(lambda: len(gesehen["a"]) >= 6 and len(gesehen["b"]) >= 6)
    assert v.aktiv("cam0") and not v.aktiv("cam1")
    # both get the same images; the board is asked once per image, not once per viewer
    assert set(gesehen["b"]) <= set(gesehen["a"])
    assert board.anfragen <= len(gesehen["a"]) + 2
    # a fresh shared image serves still images without asking the board
    vorher = board.anfragen
    assert await v.standbild("cam0") in gesehen["a"] + [f"cam0-{n}".encode() for n in range(vorher, vorher + 3)]
    a.cancel()
    b.cancel()
    await asyncio.gather(a, b, return_exceptions=True)
    await asyncio.sleep(0.3)
    # nobody watches: the board is not asked any more
    assert not v.aktiv("cam0")
    stand = board.anfragen
    await asyncio.sleep(0.3)
    assert board.anfragen == stand
    await v.beenden()


async def test_langsames_board_wird_geschont(hass: HomeAssistant) -> None:
    class Langsam(_Board):
        async def image(self, strom: str) -> bytes | None:
            self.anfragen += 1
            await asyncio.sleep(0.15)
            return b"x"

    board = Langsam()
    v = Bildverteiler(hass, board)  # type: ignore[arg-type]

    async def zuschauer() -> None:
        async for _ in v.bilder("cam1", 0.01):
            pass

    t = hass.async_create_task(zuschauer())
    await asyncio.sleep(1.0)
    t.cancel()
    await asyncio.gather(t, return_exceptions=True)
    # 0.15 s per answer: waits as long again, so about 3 instead of 6+ requests per second
    assert board.anfragen <= 5
    await v.beenden()


def test_kerne() -> None:
    assert _kerne({"cpu": {"cores": 4}}) == 4
    assert _kerne({}) == 1
    assert _kerne({"cpu": {"cores": "x"}}) == 1


async def test_cpu_vom_ganzen_pc(hass: HomeAssistant, geladen) -> None:
    system = geladen.runtime_data.system
    with patch.object(system.board, "host_info", AsyncMock(return_value={"cpu": {"cores": 4}})):
        system.data["host"] = {}
        await system.async_refresh()
    assert hass.states.get("sensor.autodarts_board_cpu_load").state == "3.1"  # 12.5 % of one core of four


async def test_standby_und_wecken(hass: HomeAssistant, geladen) -> None:
    d = geladen.runtime_data
    z, spiel = d.zustand, d.spiel
    assert isinstance(z, ZustandKoordinator)
    start = AsyncMock()
    stopped = {"status": "stopped", "running": False, "throws": []}
    with patch.object(d.board, "start", start), patch.object(d.board, "state", AsyncMock(return_value=stopped)):
        # no game: the board sleeps, nobody wakes it
        await z.async_refresh()
        assert hass.states.get("sensor.autodarts_board_status").state == "standby"
        await hass.async_block_till_done()
        assert start.await_count == 0

        # a game is played: standby in a pause wakes the detection again
        (anna,) = await _spieler(hass, "Anna")
        await _dienst(hass, "spiel_starten", spieler=[anna], startwert=501)
        start.reset_mock()
        spiel._geweckt = 0.0
        await z.async_refresh()
        await hass.async_block_till_done()
        assert start.await_count == 1
        # not again right away
        await z.async_refresh()
        await hass.async_block_till_done()
        assert start.await_count == 1

        # nobody played for a long time: the board may sleep
        spiel._geweckt = 0.0
        spiel._aktiv = time.monotonic() - 46 * 60
        await z.async_refresh()
        await hass.async_block_till_done()
        assert start.await_count == 1

        # stopped with the Stop button: stays stopped, shown as stopped
        spiel._aktiv = time.monotonic()
        await hass.services.async_call("button", "press", {"entity_id": "button.autodarts_board_stop_detection"}, blocking=True)
        assert z.manuell_gestoppt
        await z.async_refresh()
        await hass.async_block_till_done()
        assert hass.states.get("sensor.autodarts_board_status").state == "stopped"
        assert start.await_count == 1
