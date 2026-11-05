"""Actions (services) for local X01 games. Registered once in async_setup."""

from __future__ import annotations

from typing import Any

from homeassistant.components.websocket_api import async_register_command
from homeassistant.components.websocket_api.connection import ActiveConnection
from homeassistant.components.websocket_api.decorators import async_response, websocket_command
from homeassistant.components.websocket_api.messages import event_message
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
    "turnier_starten": vol.Schema({**START, vol.Optional("turnier_modus", default="ko"): vol.In(["ko", "liga"])}),
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
    "aufnahme_eintragen": vol.Schema({
        vol.Optional("spieler"): cv.string,
        vol.Required("punkte"): vol.All(vol.Coerce(int), vol.Range(0, 180)),
    }),
    "ansager_setzen": vol.Schema({vol.Required("einstellungen"): dict}),
    "ansager_testen": vol.Schema({vol.Optional("text"): cv.string, vol.Optional("sprecher"): cv.string}),
    "ansager_pack_anhalten": vol.Schema({}),
    "ansager_pack_erzeugen": vol.Schema({
        vol.Optional("name", default="Meisterschaft"): vol.All(cv.string, vol.Match(r"^[\w\- ]{1,40}$")),
        vol.Optional("sprecher"): cv.string,
        vol.Optional("nur"): vol.All(cv.ensure_list, [cv.string]),
        vol.Optional("neu", default=False): cv.boolean,
    }),
    "ansager_pack_pruefen": vol.Schema({vol.Required("name"): vol.All(cv.string, vol.Match(r"^[\w\- ]{1,40}$")),
                                        vol.Optional("reparieren", default=True): cv.boolean,
                                        vol.Optional("anhoeren", default=False): cv.boolean}),
    "ansager_pack_loeschen": vol.Schema({vol.Required("name"): vol.All(cv.string, vol.Match(r"^[\w\- ]{1,40}$"))}),
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


@websocket_command({vol.Required("type"): "autodarts/ansager"})
@async_response
async def ws_ansager(hass: HomeAssistant, connection: ActiveConnection, msg: dict[str, Any]) -> None:
    """Caller settings, voices, sound packs and walk-on songs for the caller card."""
    eintraege = hass.config_entries.async_loaded_entries(DOMAIN)
    if not eintraege:
        connection.send_result(msg["id"], {"einstellungen": {}, "stimmen": [], "packs": {}, "songs": []})
        return
    connection.send_result(msg["id"], await eintraege[0].runtime_data.ansager.uebersicht())


@websocket_command({vol.Required("type"): "autodarts/ansager/hoeren"})
@callback
def ws_ansager_hoeren(hass: HomeAssistant, connection: ActiveConnection, msg: dict[str, Any]) -> None:
    """The game card plays the caller on this phone or tablet: sends {"url"} or {"stop"} per announcement."""
    eintraege = hass.config_entries.async_loaded_entries(DOMAIN)
    if not eintraege:
        connection.send_error(msg["id"], "not_loaded", "Autodarts is not set up")
        return

    @callback
    def senden(daten: dict[str, Any]) -> None:
        connection.send_message(event_message(msg["id"], daten))

    connection.subscriptions[msg["id"]] = eintraege[0].runtime_data.ansager.hoeren(senden)
    connection.send_result(msg["id"])


async def _ansager(hass: HomeAssistant, name: str, d: dict[str, Any]) -> dict[str, Any] | None:
    ansager = _eintrag(hass).runtime_data.ansager
    if name == "ansager_testen":
        await ansager.testen(d.get("text"), d.get("sprecher"))
        return None
    if name == "ansager_pack_anhalten":
        await ansager.pack_anhalten()
        return None
    if name == "ansager_pack_erzeugen":
        namen = [str(p.get("name") or "") for p in _eintrag(hass).runtime_data.spiel.daten["spieler"]]
        ansager.pack_erzeugen(d["name"], namen, d.get("sprecher"), d.get("nur"), d["neu"])
        return None
    if name == "ansager_pack_pruefen":
        if d["anhoeren"]:  # listen to every score sound (speech-to-text), wrong ones are spoken again
            return {"gestartet": ansager.pack_anhoeren(d["name"])}
        return await ansager.pack_pruefen(d["name"], d["reparieren"])
    if name == "ansager_pack_loeschen":
        await ansager.pack_loeschen(d["name"])
        return None
    try:
        await ansager.setzen(d["einstellungen"])
    except vol.Invalid as err:
        raise ServiceValidationError(
            translation_domain=DOMAIN, translation_key="caller_settings", translation_placeholders={"error": str(err)}
        ) from err
    return None


def async_setup_services(hass: HomeAssistant) -> None:
    """Register all actions of the integration."""
    async_register_command(hass, ws_lichteffekte)
    async_register_command(hass, ws_ansager)
    async_register_command(hass, ws_ansager_hoeren)

    async def ausfuehren(call: ServiceCall) -> ServiceResponse:
        s = _leiter(hass)
        d = call.data
        name = call.service
        if name == "spiel_starten":
            await s.starten(d.get("spieler"), {k: d.get(k) for k in EINSTELLUNGEN})
        elif name == "turnier_starten":
            await s.turnier_starten(d.get("spieler"), {k: d.get(k) for k in EINSTELLUNGEN}, d["turnier_modus"])
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
        elif name == "aufnahme_eintragen":
            await s.aufnahme_eintragen(d.get("spieler"), d["punkte"])
        elif name == "spieler_anlegen":
            sid = await s.spieler_anlegen(d["name"])
            return {"id": sid} if call.return_response else None
        elif name == "spieler_aendern":
            await s.spieler_aendern(d["id"], d.get("name"), d["loeschen"])
        elif name == "statistik_loeschen":
            await s.statistik_loeschen(d.get("id"), d["verlauf"])
        elif name in ("lichteffekte_setzen", "lichteffekt_testen"):
            await _lichter(hass, name, d)
        elif name in ("ansager_setzen", "ansager_testen", "ansager_pack_erzeugen", "ansager_pack_loeschen", "ansager_pack_pruefen", "ansager_pack_anhalten"):
            antwort = await _ansager(hass, name, d)
            return antwort if call.return_response else None
        return None

    for name, schema in DIENSTE.items():
        hass.services.async_register(
            DOMAIN, name, ausfuehren, schema=schema,
            supports_response=SupportsResponse.OPTIONAL if name in ("spieler_anlegen", "ansager_pack_pruefen") else SupportsResponse.NONE,
        )


