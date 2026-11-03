"""Async client for the local Board Manager REST API (built into the integration)."""

from __future__ import annotations

import asyncio
from typing import Any, Literal

import aiohttp


class AutodartsError(Exception):
    """Base error."""


class AutodartsConnectionError(AutodartsError):
    """The board did not answer (switched off, wrong address, timeout, bad data)."""


class AutodartsResponseError(AutodartsError):
    """The board answered with an error status."""

    def __init__(self, status: int, path: str) -> None:
        super().__init__(f"Board answered {status} for /api/{path.lstrip('/')}")
        self.status = status
        self.path = path


DEFAULT_PORT = 3180

Stream = Literal["cam0", "cam1", "cam2", "detection", "live"]
_BILDPFADE: dict[str, str] = {
    "cam0": "img/cams/0",
    "cam1": "img/cams/1",
    "cam2": "img/cams/2",
    "detection": "img/detection",
    "live": "img/live",
}


def _dict(daten: Any) -> dict[str, Any]:
    if daten is None:
        return {}
    if not isinstance(daten, dict):
        raise AutodartsConnectionError(f"Unexpected answer: {type(daten).__name__}")  # noqa: TRY003
    return daten


def _list(daten: Any) -> list[dict[str, Any]]:
    if daten is None:
        return []
    if not isinstance(daten, list):
        raise AutodartsConnectionError(f"Unexpected answer: {type(daten).__name__}")  # noqa: TRY003
    return daten


class AutodartsBoard:
    """One Autodarts Board Manager, reached at http://host:port.

    The caller owns the aiohttp session and closes it.
    """

    def __init__(
        self,
        host: str,
        port: int = DEFAULT_PORT,
        *,
        session: aiohttp.ClientSession,
        request_timeout: float = 10,
    ) -> None:
        self.host = host
        self.port = port
        self.url = f"http://{host}:{port}"
        self._session = session
        self._timeout = request_timeout

    # -- low level -----------------------------------------------------------------

    async def get_json(self, path: str, timeout: float | None = None) -> Any:
        """GET /api/<path> and return the decoded JSON."""
        try:
            async with asyncio.timeout(timeout or self._timeout):
                async with self._session.get(self._api(path)) as response:
                    if response.status >= 300:
                        raise AutodartsResponseError(response.status, path)
                    return await response.json(content_type=None)
        except (aiohttp.ClientError, TimeoutError, ValueError) as err:
            raise AutodartsConnectionError(str(err) or type(err).__name__) from err

    async def command(self, path: str, data: dict[str, Any] | None = None, method: str = "POST") -> None:
        """Send a command. Board Manager 2.x expects PUT for some POST endpoints."""
        try:
            async with asyncio.timeout(self._timeout):
                async with self._session.request(method, self._api(path), json=data) as response:
                    status = response.status
                if status in (404, 405) and method == "POST":
                    async with self._session.request("PUT", self._api(path), json=data) as response:
                        status = response.status
        except (aiohttp.ClientError, TimeoutError) as err:
            raise AutodartsConnectionError(str(err) or type(err).__name__) from err
        if status >= 300:
            raise AutodartsResponseError(status, path)

    def _api(self, path: str) -> str:
        return f"{self.url}/api/{path.lstrip('/')}"

    # -- reading -------------------------------------------------------------------

    async def state(self, timeout: float = 2) -> dict[str, Any]:
        """Detection state: status, throws, number of darts, event."""
        return _dict(await self.get_json("state", timeout))

    async def system(self) -> dict[str, Any]:
        """System info: calibration, cameras, statistics, version."""
        return _dict(await self.get_json("system", 5))

    async def devices(self) -> list[dict[str, Any]]:
        """Cameras connected to the board PC."""
        return _list(await self.get_json("devices", 5))

    async def host_info(self) -> dict[str, Any]:
        """Name and operating system of the board PC."""
        return _dict(await self.get_json("host", 5))

    async def config(self) -> dict[str, Any]:
        """The Board Manager configuration."""
        return _dict(await self.get_json("config", 5))

    async def calibration_ellipses(self) -> dict[str, Any]:
        """Calibration grid of each camera."""
        return _dict(await self.get_json("config/calibration/ellipses", 5))

    async def image(self, stream: Stream) -> bytes | None:
        """Current JPEG of a camera, the detection image or the live image; None if not available."""
        try:
            async with asyncio.timeout(6):
                async with self._session.get(self._api(_BILDPFADE[stream])) as response:
                    if response.status != 200:
                        return None
                    return await response.read()
        except (aiohttp.ClientError, TimeoutError):
            return None

    def stream_url(self, stream: Stream) -> str:
        """MJPEG stream address of a camera, the detection image or the live image."""
        return self._api(_BILDPFADE[stream].replace("img/", "streams/", 1))

    # -- commands ------------------------------------------------------------------

    async def start(self) -> None:
        await self.command("start")

    async def stop(self) -> None:
        await self.command("stop")

    async def reset(self) -> None:
        """Remove the darts of the current visit."""
        await self.command("reset")

    async def calibrate(self) -> None:
        """Start the automatic calibration."""
        await self.command("config/calibration/auto")

    async def restart(self) -> None:
        """Restart the Board Manager software."""
        await self.command("restart")

    async def apply_update(self) -> None:
        """Install a pending Board Manager update."""
        await self.command("update/apply")

    async def set_config(self, data: dict[str, Any]) -> None:
        """Change parts of the configuration, e.g. {"cam": {"fps": 15}}."""
        await self.command("config", data, "PATCH")
