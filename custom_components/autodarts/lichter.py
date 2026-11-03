"""Light effects on game events: chosen lights blink, flash, pulse, show a colour, a rainbow,
the light's own effect (WLED, Hue) or a WLED preset.

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
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.storage import Store
import voluptuous as vol

from .const import EREIGNISSE

_LOGGER = logging.getLogger(__name__)

EFFEKTE = ["farbe", "blinken", "blitz", "regenbogen", "pulsieren", "lampe", "preset"]
# "lampe" = an effect of the light itself (WLED, Hue …), "preset" = a WLED preset
WLED_ZAHLEN = {"speed": "tempo", "segment_speed": "tempo", "intensity": "staerke", "segment_intensity": "staerke"}
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
    vol.Optional("lampen_effekt", default=""): str,
    vol.Optional("preset", default=""): str,
    vol.Optional("tempo"): vol.Any(None, vol.All(vol.Coerce(int), vol.Range(0, 255))),
    vol.Optional("staerke"): vol.Any(None, vol.All(vol.Coerce(int), vol.Range(0, 255))),
})


def wled_teile(hass: HomeAssistant, licht: str) -> dict[str, list[str]]:
    """Preset select and speed/intensity numbers of the WLED device a light belongs to."""
    reg = er.async_get(hass)
    eintrag = reg.async_get(licht)
    if not eintrag or eintrag.platform != "wled" or not eintrag.device_id:
        return {}
    teile: dict[str, list[str]] = {"preset": [], "tempo": [], "staerke": []}
    for e in er.async_entries_for_device(reg, eintrag.device_id):
        if e.platform != "wled" or e.disabled_by:
            continue
        if e.domain == "select" and e.translation_key == "preset":
            teile["preset"].append(e.entity_id)
        elif e.domain == "number" and e.translation_key in WLED_ZAHLEN:
            teile[WLED_ZAHLEN[e.translation_key]].append(e.entity_id)
    return teile


def wled_uebersicht(hass: HomeAssistant) -> dict[str, dict[str, Any]]:
    """For the lights card: WLED lights with their presets and whether speed/intensity exist."""
    aus: dict[str, dict[str, Any]] = {}
    for e in er.async_get(hass).entities.values():
        if e.domain != "light" or e.platform != "wled" or e.disabled_by:
            continue
        teile = wled_teile(hass, e.entity_id)
        presets: list[str] = []
        for sel in teile.get("preset", []):
            if (s := hass.states.get(sel)) and isinstance(s.attributes.get("options"), list):
                presets += [o for o in s.attributes["options"] if o not in presets]
        aus[e.entity_id] = {"presets": presets, "tempo": bool(teile.get("tempo") or teile.get("staerke"))}
    return aus


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
        zahlen: list[str] = []  # WLED speed/intensity, restored afterwards like the lights
        if regel["effekt"] == "lampe":
            for e in lichter:
                t = wled_teile(self.hass, e)
                zahlen += [z for k in ("tempo", "staerke") if regel.get(k) is not None for z in t.get(k, [])
                           if z not in zahlen and self.hass.states.get(z)]
        for e in lichter + zahlen:
            if e not in self._besitz:
                self._vorher[e] = self.hass.states.get(e)  # type: ignore[assignment]
            alt = self._besitz.get(e)
            self._besitz[e] = lauf
            if alt and alt in self._laeufe:
                self._laeufe[alt].cancel()
        self._laeufe[lauf] = self.hass.async_create_background_task(self._lauf(lauf, regel, lichter, zahlen), "autodarts light effect")

    async def beenden(self) -> None:
        for task in list(self._laeufe.values()):
            task.cancel()
        await asyncio.gather(*self._laeufe.values(), return_exceptions=True)

    async def _lauf(self, lauf: str, r: dict[str, Any], lichter: list[str], zahlen: list[str]) -> None:
        try:
            await self._effekt(r, lichter)
        except asyncio.CancelledError:
            pass
        except Exception:  # a light that does not answer must not break the game
            _LOGGER.warning("Light effect failed", exc_info=True)
        finally:
            eigene = [e for e in lichter + zahlen if self._besitz.get(e) == lauf]
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
        elif art == "lampe":
            await self._lampen_effekt(r, lichter, rgb, hell)
            await asyncio.sleep(dauer)
        elif art == "preset":
            await self._preset(r, lichter, rgb, hell)
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

    async def _lampen_effekt(self, r: dict[str, Any], lichter: list[str], rgb: tuple[int, ...], hell: int) -> None:
        """The light's own effect (e.g. WLED "Fireworks"); lights without it show the colour."""
        name = r["lampen_effekt"]
        for e in lichter:
            for k in ("tempo", "staerke"):
                if r.get(k) is not None:
                    for z in wled_teile(self.hass, e).get(k, []):
                        await self.hass.services.async_call("number", "set_value", {"entity_id": z, "value": r[k]}, blocking=True)
        mit = [e for e in lichter if name and name in (((s := self.hass.states.get(e)) and s.attributes.get("effect_list")) or [])]
        if mit:
            await self._an(mit, rgb, hell, 0, {"effect": name})
        if rest := [e for e in lichter if e not in mit]:
            await self._an(rest, rgb, hell, 0.3)

    async def _preset(self, r: dict[str, Any], lichter: list[str], rgb: tuple[int, ...], hell: int) -> None:
        """A WLED preset; other lights show the colour."""
        rest = []
        for e in lichter:
            auswahl = [z for z in wled_teile(self.hass, e).get("preset", [])
                       if r["preset"] in (((s := self.hass.states.get(z)) and s.attributes.get("options")) or [])]
            if not auswahl:
                rest.append(e)
            for z in auswahl:
                await self.hass.services.async_call("select", "select_option", {"entity_id": z, "option": r["preset"]}, blocking=True)
        if rest:
            await self._an(rest, rgb, hell, 0.3)

    def _farbig(self, e: str) -> bool:
        s = self.hass.states.get(e)
        modi = set((s.attributes.get("supported_color_modes") or []) if s else [])
        return bool(modi & FARBMODI)

    async def _an(self, lichter: list[str], rgb: tuple[int, ...], hell: int, uebergang: float, extra: dict[str, Any] | None = None) -> None:
        farbig = [e for e in lichter if self._farbig(e)]
        rest = [e for e in lichter if e not in farbig]
        daten: dict[str, Any] = {"brightness_pct": hell, "transition": uebergang, **(extra or {})}
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
                if s.domain == "number":
                    await self.hass.services.async_call("number", "set_value", {"entity_id": e, "value": float(s.state)}, blocking=True)
                    continue
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
                jetzt = self.hass.states.get(e)
                if jetzt and jetzt.attributes.get("effect") != a.get("effect"):
                    liste = a.get("effect_list") or []
                    zurueck = next((x for x in (a.get("effect"), "Solid", "off", "None") if x in liste), None)
                    if zurueck:
                        daten["effect"] = zurueck
                await self._dienst("turn_on", [e], daten)
            except Exception:
                _LOGGER.warning("Could not restore %s", e, exc_info=True)
