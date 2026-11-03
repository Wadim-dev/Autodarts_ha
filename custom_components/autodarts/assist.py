"""Voice sentences for Assist (German, English, Russian), registered as sentence triggers.

They work with every Assist pipeline, also with an AI conversation agent (sentence
triggers are checked first). Nothing has to be set up by hand.
"""

from __future__ import annotations

from collections.abc import Callable
import inspect
import logging
import re
from typing import Any

from homeassistant.core import CALLBACK_TYPE, HomeAssistant
from homeassistant.exceptions import HomeAssistantError

from .spiel import Spielleiter

_LOGGER = logging.getLogger(__name__)

# command -> language -> sentences (Hassil templates, no punctuation)
SAETZE: dict[str, dict[str, list[str]]] = {
    "stand": {
        "de": ["wie steht (es|das spiel) [beim|im] darts", "[wie ist der] (darts stand|dartsstand|spielstand [beim|im] darts)",
               "wer (führt|ist dran|liegt vorne) [beim|im] darts"],
        "en": ["[what is the] darts score", "how is the darts [game] going", "who is (winning|leading|next) [at|in] darts"],
        "ru": ["какой (счёт|счет) в дартс[е]", "как (дела|идёт игра|идет игра) в дартс[е]", "кто (ведёт|ведет|выигрывает|бросает) в дартс[е]",
               "(счёт|счет) дартс"],
    },
    "rangliste": {
        "de": ["wer ist der beste [spieler] [beim|im] darts", "darts rangliste"],
        "en": ["who is the best [player] [at|in] darts", "darts ranking"],
        "ru": ["кто лучший [игрок] в дартс[е]", "рейтинг дартс"],
    },
    "starten": {
        "de": ["starte [eine|ein] darts (revanche|spiel)", "neues darts spiel", "starte darts {spiel}", "starte {spiel} [beim|im] darts"],
        "en": ["start [a] darts (rematch|game)", "new darts game", "start darts {spiel}", "start {spiel} [in|at] darts"],
        "ru": ["(начни|запусти) [новую] (игру|партию) в дартс", "реванш в дартс", "(начни|запусти) дартс {spiel}"],
    },
    "naechstes": {
        "de": ["nächstes darts match", "darts turnier weiter"],
        "en": ["next darts match", "continue [the] darts tournament"],
        "ru": ["следующий матч [в] дартс", "продолжи турнир [по] дартс[у]"],
    },
    "zurueck": {
        "de": ["darts rückgängig", "letzten dart zurück[nehmen]"],
        "en": ["undo [the] last dart", "darts undo"],
        "ru": ["отмени последний дротик", "дартс отмена броска"],
    },
    "abbrechen": {
        "de": ["darts spiel abbrechen", "brich das darts spiel ab"],
        "en": ["cancel [the] darts game", "stop [the] darts game"],
        "ru": ["(отмени|прерви|останови) игру в дартс"],
    },
}

TEXTE: dict[str, dict[str, str]] = {
    "de": {"kein": "Gerade läuft kein Darts-Spiel.", "dran": "{n} ist dran.", "rest": "Rest", "punkte": "Punkte", "legs": "Legs {s}.",
           "sieg": "{n} hat gewonnen.", "bulloff": "Gerade läuft das Bull-Off.", "turnier": "Im Turnier ist als Nächstes {a} gegen {b} dran.",
           "champion": "{n} hat das Turnier gewonnen.", "rang": "Rangliste: {s}.", "keiner": "Es gibt noch keine Spieler mit Wertung.",
           "gestartet": "Los geht's: {m}.", "unbekannt": "Das Spiel {s} kenne ich nicht.", "weiter": "Nächstes Match: {a} gegen {b}.",
           "zurueck": "Letzter Dart ist zurückgenommen.", "abgebrochen": "Spiel abgebrochen.", "fehler": "Das geht gerade nicht."},
    "en": {"kein": "No darts game is running.", "dran": "{n} to throw.", "rest": "left", "punkte": "points", "legs": "Legs {s}.",
           "sieg": "{n} won.", "bulloff": "The bull-off is running.", "turnier": "Next in the tournament: {a} against {b}.",
           "champion": "{n} won the tournament.", "rang": "Ranking: {s}.", "keiner": "No rated players yet.",
           "gestartet": "Game on: {m}.", "unbekannt": "I don't know the game {s}.", "weiter": "Next match: {a} against {b}.",
           "zurueck": "Last dart undone.", "abgebrochen": "Game cancelled.", "fehler": "That is not possible right now."},
    "ru": {"kein": "Сейчас игры в дартс нет.", "dran": "Бросает {n}.", "rest": "осталось", "punkte": "очков", "legs": "Леги {s}.",
           "sieg": "{n} победил.", "bulloff": "Идёт бросок на булл.", "turnier": "В турнире дальше {a} против {b}.",
           "champion": "{n} выиграл турнир.", "rang": "Рейтинг: {s}.", "keiner": "Пока нет игроков с рейтингом.",
           "gestartet": "Поехали: {m}.", "unbekannt": "Игру {s} я не знаю.", "weiter": "Следующий матч: {a} против {b}.",
           "zurueck": "Последний дротик отменён.", "abgebrochen": "Игра отменена.", "fehler": "Сейчас это не получится."},
}

# spoken game names -> settings
SPIELE: list[tuple[str, dict[str, Any]]] = [
    (r"cricket|крикет", {"spiel": "cricket"}),
    (r"shanghai|шанхай", {"spiel": "shanghai"}),
    (r"killer|киллер", {"spiel": "killer"}),
    (r"golf|гольф", {"spiel": "golf"}),
    (r"baseball|бейсбол", {"spiel": "baseball"}),
    (r"high ?score|хайскор", {"spiel": "highscore"}),
    (r"halve|halbier", {"spiel": "halve_it"}),
    (r"bob|боб", {"spiel": "bobs27"}),
    (r"uhr|clock|круг", {"spiel": "atc"}),
    (r"121", {"spiel": "checkout121"}),
    (r"doppel|double|дубл", {"spiel": "doppel"}),
    (r"(101|170|301|501|701|901)", {"spiel": "x01"}),
]


def spiel_aus_text(text: str) -> dict[str, Any] | None:
    """Settings for a spoken game name, None if unknown."""
    text = text.lower()
    for muster, e in SPIELE:
        if m := re.search(muster, text):
            if e["spiel"] == "x01":
                return {**e, "startwert": int(m.group(1))}
            return dict(e)
    return None


def stand_text(leiter: Spielleiter, sprache: str) -> str:
    """Spoken summary of the game (or tournament)."""
    tx = TEXTE[sprache]
    a = leiter.spiel_attribute()
    tur = a.get("turnier")
    phase = leiter.phase()
    if phase == "idle":
        if tur and tur.get("sieger"):
            return tx["champion"].format(n=tur["sieger"])
        if tur and tur.get("naechstes"):
            return tx["kein"] + " " + tx["turnier"].format(a=tur["naechstes"]["a"], b=tur["naechstes"]["b"])
        return tx["kein"]
    if phase == "bull_off":
        return tx["bulloff"]
    sp = a.get("spieler") or []
    teile = []
    if phase == "finished" and a.get("gewinner") is not None:
        teile.append(tx["sieg"].format(n=sp[a["gewinner"]]["name"]))
        if tur and tur.get("sieger"):
            teile.append(tx["champion"].format(n=tur["sieger"]))
        elif tur and tur.get("naechstes"):
            teile.append(tx["turnier"].format(a=tur["naechstes"]["a"], b=tur["naechstes"]["b"]))
        return " ".join(teile)
    einheit = tx["rest"] if (a.get("art") or "x01") == "x01" else tx["punkte"]
    teile.append(", ".join(f"{p['name']} {p.get('rest', 0)} {einheit}" for p in sp) + ".")
    if int((a.get("einstellungen") or {}).get("legs") or 1) > 1:
        teile.append(tx["legs"].format(s=" : ".join(str(p.get("legs", 0)) for p in sp)))
    if a.get("am_zug") is not None and a["am_zug"] < len(sp):
        teile.append(tx["dran"].format(n=sp[a["am_zug"]]["name"]))
    return " ".join(teile)


def rang_text(leiter: Spielleiter, sprache: str) -> str:
    tx = TEXTE[sprache]
    liste = sorted((s for s in leiter.spieler_attribute()["spieler"] if s["spiele"]), key=lambda s: -s["elo"])[:3]
    if not liste:
        return tx["keiner"]
    return tx["rang"].format(s=", ".join(f"{i + 1}. {s['name']} {s['elo']}" for i, s in enumerate(liste)))


async def ausfuehren(leiter: Spielleiter, befehl: str, sprache: str, slots: dict[str, Any]) -> str:
    """Run one voice command and return the answer."""
    tx = TEXTE[sprache]
    try:
        if befehl == "stand":
            return stand_text(leiter, sprache)
        if befehl == "rangliste":
            return rang_text(leiter, sprache)
        if befehl == "starten":
            e: dict[str, Any] = {}
            name = str(slots.get("spiel") or "").strip()
            if name.lower() not in ("", "spiel", "revanche", "game", "rematch"):
                gefunden = spiel_aus_text(name)
                if gefunden is None:
                    return tx["unbekannt"].format(s=name)
                e = gefunden
            await leiter.starten(None, e)
            return tx["gestartet"].format(m=leiter.spiel_attribute().get("modus") or "")
        if befehl == "naechstes":
            await leiter.turnier_weiter()
            sp = leiter.spiel_attribute().get("spieler") or []
            return tx["weiter"].format(a=sp[0]["name"], b=sp[1]["name"]) if len(sp) > 1 else tx["gestartet"].format(m="")
        if befehl == "zurueck":
            await leiter.rueckgaengig()
            return tx["zurueck"]
        if befehl == "abbrechen":
            await leiter.abbrechen()
            return tx["abgebrochen"]
    except HomeAssistantError as err:
        _LOGGER.debug("Voice command %s failed: %s", befehl, err)
        return tx["fehler"]
    return tx["fehler"]


def async_setup_assist(hass: HomeAssistant, leiter_holen: Callable[[], Spielleiter | None]) -> CALLBACK_TYPE | None:
    """Register the sentences; returns the function that removes them again."""
    if "conversation" not in hass.config.components:
        return None
    try:
        from homeassistant.components.conversation.agent_manager import get_agent_manager
    except ImportError:  # pragma: no cover - Assist changed its internals
        _LOGGER.warning("Assist sentences for Autodarts are not available in this Home Assistant version")
        return None
    abmelden: list[CALLBACK_TYPE] = []
    manager = get_agent_manager(hass)

    def anmelden(saetze: list[str], antwort: Any) -> CALLBACK_TYPE:
        # Home Assistant 2026.11 and newer: register_trigger(sentences, trigger_callback)
        if "sentences" in inspect.signature(manager.register_trigger).parameters:
            return manager.register_trigger(sentences=saetze, trigger_callback=antwort)  # type: ignore[call-arg]
        from homeassistant.components.conversation.trigger import TriggerDetails  # older versions

        return manager.register_trigger(TriggerDetails(sentences=saetze, callback=antwort))
    for befehl, sprachen in SAETZE.items():
        for sprache, saetze in sprachen.items():

            async def antwort(user_input: Any, result: Any, befehl: str = befehl, sprache: str = sprache) -> str | None:
                leiter = leiter_holen()
                if leiter is None:
                    return None
                slots = {k: v.value for k, v in result.entities.items()}
                return await ausfuehren(leiter, befehl, sprache, slots)

            abmelden.append(anmelden(saetze, antwort))

    def alle_abmelden() -> None:
        for f in abmelden:
            f()

    return alle_abmelden
