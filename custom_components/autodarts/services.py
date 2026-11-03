"""Actions (services) for local X01 games. Registered once in async_setup."""

from __future__ import annotations

from typing import Any

from homeassistant.components.websocket_api import async_register_command
from homeassistant.components.websocket_api.connection import ActiveConnection
from homeassistant.components.websocket_api.decorators import websocket_command
from homeassistant.core import HomeAssistant, ServiceCall, ServiceResponse, SupportsResponse, callback
from homeassistant.exceptions import ServiceValidationError
from homeassistant.helpers import config_validation as cv
import voluptuous as vol

from .const import DOMAIN, EREIGNISSE
from .coordinator import DartsEntry
from .lichter import EFFEKTE, REGEL, wled_uebersicht
from .spiel import EINSTELLUNGEN, Spielleiter
from .spielarten import GRUPPEN

MODUS = vol.In(["straight", "double", "master"])
START = {
    vol.Optional("spiel"): vol.In(list(GRUPPEN)),
    vol.Optional("variante"): cv.string,
    vol.Optional("zahlen"): vol.In(["classic", "tactics", "random"]),
    vol.Optional("runden"): vol.Coerce(int),
    vol.Optional("leben"): vol.Coerce(int),
    vol.Optional("spieler"): vol.All(cv.ensure_list, [cv.string]),
    vol.Optional("startwert"): vol.Coerce(int),
    vol.Optional("einwurf"): MODUS,
    vol.Optional("auswurf"): MODUS,
    vol.Optional("legs"): vol.Coerce(int),
    vol.Optional("sets"): vol.Coerce(int),
    vol.Optional("bull_off"): cv.boolean,
}

DIENSTE = {
    "spiel_starten": vol.Schema(START),
    "turnier_starten": vol.Schema(START),
    "spiel_abbrechen": vol.Schema({}),
    "turnier_weiter": vol.Schema({}),
    "turnier_abbrechen": vol.Schema({}),
    "weiter": vol.Schema({}),
    "rueckgaengig": vol.Schema({}),
    "wurf_aendern": vol.Schema({
        vol.Optional("aufnahme"): vol.Coerce(int),
        vol.Required("dart"): vol.Coerce(int),
        vol.Optional("feld", default=""): cv.string,
    }),
    "spieler_anlegen": vol.Schema({vol.Required("name"): cv.string}),
    "spieler_aendern": vol.Schema({
        vol.Required("id"): cv.string,
        vol.Optional("name"): cv.string,
        vol.Optional("loeschen", default=False): cv.boolean,
    }),
    "lichteffekte_setzen": vol.Schema({vol.Required("regeln"): [dict]}),
    "lichteffekt_testen": vol.Schema({vol.Required("regel"): dict}),
    "statistik_loeschen": vol.Schema({
        vol.Optional("id"): cv.string,
        vol.Optional("verlauf", default=False): cv.boolean,
    }),
}


def _leiter(hass: HomeAssistant) -> Spielleiter:
    eintrag: DartsEntry
    for eintrag in hass.config_entries.async_loaded_entries(DOMAIN):
        return eintrag.runtime_data.spiel
    raise ServiceValidationError(translation_domain=DOMAIN, translation_key="not_set_up")


def _eintrag(hass: HomeAssistant) -> DartsEntry:
    for eintrag in hass.config_entries.async_loaded_entries(DOMAIN):
        return eintrag
    raise ServiceValidationError(translation_domain=DOMAIN, translation_key="not_set_up")


async def _lichter(hass: HomeAssistant, name: str, d: dict[str, Any]) -> None:
    show = _eintrag(hass).runtime_data.lichter
    try:
        if name == "lichteffekte_setzen":
            await show.setzen(d["regeln"])
        else:
            show.abspielen(REGEL(d["regel"]))
    except vol.Invalid as err:
        raise ServiceValidationError(
            translation_domain=DOMAIN, translation_key="light_rule", translation_placeholders={"error": str(err)}
        ) from err


@websocket_command({vol.Required("type"): "autodarts/lichteffekte"})
@callback
def ws_lichteffekte(hass: HomeAssistant, connection: ActiveConnection, msg: dict[str, Any]) -> None:
    """Rules of the light effects for the lights card."""
    eintraege = hass.config_entries.async_loaded_entries(DOMAIN)
    regeln = eintraege[0].runtime_data.lichter.regeln if eintraege else []
    connection.send_result(msg["id"], {"regeln": regeln, "ereignisse": EREIGNISSE, "effekte": EFFEKTE, "wled": wled_uebersicht(hass)})


def async_setup_services(hass: HomeAssistant) -> None:
    """Register all actions of the integration."""
    async_register_command(hass, ws_lichteffekte)

    async def ausfuehren(call: ServiceCall) -> ServiceResponse:
        s = _leiter(hass)
        d = call.data
        name = call.service
        if name == "spiel_starten":
            await s.starten(d.get("spieler"), {k: d.get(k) for k in EINSTELLUNGEN})
        elif name == "turnier_starten":
            await s.turnier_starten(d.get("spieler"), {k: d.get(k) for k in EINSTELLUNGEN})
        elif name == "turnier_weiter":
            await s.turnier_weiter()
        elif name == "turnier_abbrechen":
            await s.turnier_abbrechen()
        elif name == "spiel_abbrechen":
            await s.abbrechen()
        elif name == "weiter":
            await s.weiter()
        elif name == "rueckgaengig":
            await s.rueckgaengig()
        elif name == "wurf_aendern":
            await s.wurf_aendern(d.get("aufnahme"), d["dart"], d.get("feld", ""))
        elif name == "spieler_anlegen":
            sid = await s.spieler_anlegen(d["name"])
            return {"id": sid} if call.return_response else None
        elif name == "spieler_aendern":
            await s.spieler_aendern(d["id"], d.get("name"), d["loeschen"])
        elif name == "statistik_loeschen":
            await s.statistik_loeschen(d.get("id"), d["verlauf"])
        elif name in ("lichteffekte_setzen", "lichteffekt_testen"):
            await _lichter(hass, name, d)
        return None

    for name, schema in DIENSTE.items():
        hass.services.async_register(
            DOMAIN, name, ausfuehren, schema=schema,
            supports_response=SupportsResponse.OPTIONAL if name == "spieler_anlegen" else SupportsResponse.NONE,
        )


