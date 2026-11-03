"""Light effects on game events: chosen lights blink, flash, pulse, show a colour or a rainbow.

The rules are kept by the integration (storage autodarts.lichter) and edited in the
lights card or with the action autodarts.lichteffekte_setzen. After an effect every
light goes back to the state it had before.
"""

from __future__ import annotations

import asyncio
from collections.abc import Iterable
import colorsys
import logging
from typing import Any
import uuid

from homeassistant.components.light.const import ColorMode
from homeassistant.const import STATE_ON
from homeassistant.core import HomeAssistant, State, callback
from homeassistant.helpers.storage import Store
import voluptuous as vol

from .const import EREIGNISSE

_LOGGER = logging.getLogger(__name__)

EFFEKTE = ["farbe", "blinken", "blitz", "regenbogen", "pulsieren"]
FARBMODI = {ColorMode.HS, ColorMode.XY, ColorMode.RGB, ColorMode.RGBW, ColorMode.RGBWW}
# Zigbee and Wi-Fi lights cope with about two commands per second
TAKT = 0.5


def _licht(wert: Any) -> str:
    text = str(wert)
    if not text.startswith("light."):
        raise vol.Invalid("only lights")  # noqa: TRY003
    return text


REGEL = vol.Schema({
    vol.Optional("id"): str,
    vol.Required("ereignis"): vol.In(EREIGNISSE),
    vol.Required("lichter"): vol.All([_licht], vol.Length(min=1)),
    vol.Optional("effekt", default="farbe"): vol.In(EFFEKTE),
    vol.Optional("farbe", default=[255, 0, 0]): vol.All(
        vol.ExactSequence([vol.All(vol.Coerce(int), vol.Range(0, 255))] * 3), list
    ),
    vol.Optional("helligkeit", default=100): vol.All(vol.Coerce(int), vol.Range(1, 100)),
    vol.Optional("dauer", default=3): vol.All(vol.Coerce(float), vol.Range(1, 60)),
    vol.Optional("aktiv", default=True): bool,
})


def regel_pruefen(daten: dict[str, Any]) -> dict[str, Any]:
    """Validate one rule and give it an id."""
    r: dict[str, Any] = REGEL(daten)
    r.setdefault("id", uuid.uuid4().hex[:8])
    return r


class Lichtshow:
    """Plays the effects of the stored rules."""

    def __init__(self, hass: HomeAssistant) -> None:
        self.hass = hass
        self._store: Store[dict[str, Any]] = Store(hass, 1, "autodarts.lichter")
        self.regeln: list[dict[str, Any]] = []
        self._vorher: dict[str, State] = {}  # state of each light before its effect
        self._besitz: dict[str, str] = {}  # light -> run that currently drives it
        self._laeufe: dict[str, asyncio.Task[None]] = {}

    async def laden(self) -> None:
        daten = await self._store.async_load() or {}
        self.regeln = []
        for r in daten.get("regeln") or []:
            try:
                self.regeln.append(regel_pruefen(r))
            except vol.Invalid as err:
                _LOGGER.warning("Light rule ignored: %s", err)

    async def setzen(self, regeln: Iterable[dict[str, Any]]) -> None:
        self.regeln = [regel_pruefen(dict(r)) for r in regeln]
        await self._store.async_save({"regeln": self.regeln})

    @callback
    def ereignis(self, typ: str, daten: dict[str, Any]) -> None:
        """Game event from the game manager."""
        for r in self.regeln:
            if r["aktiv"] and r["ereignis"] == typ:
                self.abspielen(r)

    @callback
    def abspielen(self, regel: dict[str, Any]) -> None:
        lichter = [e for e in regel["lichter"] if (s := self.hass.states.get(e)) and s.state in ("on", "off")]
        if not lichter:
            return
        lauf = uuid.uuid4().hex
        for e in lichter:
            if e not in self._besitz:
                self._vorher[e] = self.hass.states.get(e)  # type: ignore[assignment]
            alt = self._besitz.get(e)
            self._besitz[e] = lauf
            if alt and alt in self._laeufe:
                self._laeufe[alt].cancel()
        self._laeufe[lauf] = self.hass.async_create_background_task(self._lauf(lauf, regel, lichter), "autodarts light effect")

    async def beenden(self) -> None:
        for task in list(self._laeufe.values()):
            task.cancel()
        await asyncio.gather(*self._laeufe.values(), return_exceptions=True)

    async def _lauf(self, lauf: str, r: dict[str, Any], lichter: list[str]) -> None:
        try:
            await self._effekt(r, lichter)
        except asyncio.CancelledError:
            pass
        except Exception:  # a light that does not answer must not break the game
            _LOGGER.warning("Light effect failed", exc_info=True)
        finally:
            eigene = [e for e in lichter if self._besitz.get(e) == lauf]
            for e in eigene:
                del self._besitz[e]
            self._laeufe.pop(lauf, None)
            await self._zurueck(eigene)

    async def _effekt(self, r: dict[str, Any], lichter: list[str]) -> None:
        rgb, hell, dauer, art = tuple(r["farbe"]), r["helligkeit"], r["dauer"], r["effekt"]
        ende = asyncio.get_running_loop().time() + dauer

        def noch() -> bool:
            return bool(asyncio.get_running_loop().time() < ende)

        if art == "farbe":
            await self._an(lichter, rgb, hell, 0.3)
            await asyncio.sleep(dauer)
        elif art == "blinken":
            while noch():
                await self._an(lichter, rgb, hell, 0)
                await asyncio.sleep(TAKT)
                await self._aus(lichter)
                await asyncio.sleep(TAKT)
        elif art == "blitz":
            while noch():
                await self._an(lichter, rgb, 100, 0)
                await asyncio.sleep(TAKT / 2)
                await self._an(lichter, rgb, max(1, hell // 10), 0)
                await asyncio.sleep(TAKT * 1.5)
        elif art == "regenbogen":
            ton = 0.0
            while noch():
                farbe = tuple(round(x * 255) for x in colorsys.hsv_to_rgb(ton, 1, 1))
                await self._an(lichter, farbe, hell, TAKT * 1.2)
                await asyncio.sleep(TAKT * 1.2)
                ton = (ton + 1 / 8) % 1
        else:  # pulsieren
            while noch():
                await self._an(lichter, rgb, hell, 1)
                await asyncio.sleep(1)
                await self._an(lichter, rgb, max(1, hell // 8), 1)
                await asyncio.sleep(1)

    def _farbig(self, e: str) -> bool:
        s = self.hass.states.get(e)
        modi = set((s.attributes.get("supported_color_modes") or []) if s else [])
        return bool(modi & FARBMODI)

    async def _an(self, lichter: list[str], rgb: tuple[int, ...], hell: int, uebergang: float) -> None:
        farbig = [e for e in lichter if self._farbig(e)]
        rest = [e for e in lichter if e not in farbig]
        daten: dict[str, Any] = {"brightness_pct": hell, "transition": uebergang}
        if farbig:
            await self._dienst("turn_on", farbig, {**daten, "rgb_color": list(rgb)})
        if rest:
            await self._dienst("turn_on", rest, daten)

    async def _aus(self, lichter: list[str]) -> None:
        await self._dienst("turn_off", lichter, {"transition": 0})

    async def _dienst(self, name: str, lichter: list[str], daten: dict[str, Any]) -> None:
        await self.hass.services.async_call("light", name, {"entity_id": lichter, **daten}, blocking=True)

    async def _zurueck(self, lichter: list[str]) -> None:
        """Put every light back the way it was before the effect."""
        for e in lichter:
            s = self._vorher.pop(e, None)
            if s is None:
                continue
            try:
                if s.state != STATE_ON:
                    await self._dienst("turn_off", [e], {})
                    continue
                a = s.attributes
                daten: dict[str, Any] = {}
                if a.get("brightness") is not None:
                    daten["brightness"] = a["brightness"]
                modus = a.get("color_mode")
                if modus in FARBMODI and a.get("hs_color"):
                    daten["hs_color"] = a["hs_color"]
                elif modus == ColorMode.COLOR_TEMP and a.get("color_temp_kelvin"):
                    daten["color_temp_kelvin"] = a["color_temp_kelvin"]
                await self._dienst("turn_on", [e], daten)
            except Exception:
                _LOGGER.warning("Could not restore %s", e, exc_info=True)
