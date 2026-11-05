"""Voice sentences for Assist (German, English, Russian), registered as sentence triggers.

They work with every Assist pipeline, also with an AI conversation agent (sentence
triggers are checked first). Nothing has to be set up by hand.
"""

from __future__ import annotations

from collections.abc import Callable
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
           "zurueck": "Letzter Dart ist zurückgenommen.", "abgebrochen": "Spiel abgebrochen.", "fehler": "Das geht gerade nicht.",
           "eingetragen": "{n} {p}.", "nur_x01": "Punkte per Sprache gehen nur bei X01.", "geht_nicht": "{p} kann man mit drei Darts nicht werfen."},
    "en": {"kein": "No darts game is running.", "dran": "{n} to throw.", "rest": "left", "punkte": "points", "legs": "Legs {s}.",
           "sieg": "{n} won.", "bulloff": "The bull-off is running.", "turnier": "Next in the tournament: {a} against {b}.",
           "champion": "{n} won the tournament.", "rang": "Ranking: {s}.", "keiner": "No rated players yet.",
           "gestartet": "Game on: {m}.", "unbekannt": "I don't know the game {s}.", "weiter": "Next match: {a} against {b}.",
           "zurueck": "Last dart undone.", "abgebrochen": "Game cancelled.", "fehler": "That is not possible right now.",
           "eingetragen": "{n} {p}.", "nur_x01": "Scores by voice only work in X01.", "geht_nicht": "{p} cannot be thrown with three darts."},
    "ru": {"kein": "Сейчас игры в дартс нет.", "dran": "Бросает {n}.", "rest": "осталось", "punkte": "очков", "legs": "Леги {s}.",
           "sieg": "{n} победил.", "bulloff": "Идёт бросок на булл.", "turnier": "В турнире дальше {a} против {b}.",
           "champion": "{n} выиграл турнир.", "rang": "Рейтинг: {s}.", "keiner": "Пока нет игроков с рейтингом.",
           "gestartet": "Поехали: {m}.", "unbekannt": "Игру {s} я не знаю.", "weiter": "Следующий матч: {a} против {b}.",
           "zurueck": "Последний дротик отменён.", "abgebrochen": "Игра отменена.", "fehler": "Сейчас это не получится.",
           "eingetragen": "{n} {p}.", "nur_x01": "Очки голосом только в X01.", "geht_nicht": "{p} нельзя набрать тремя дротиками."},
}

# spoken game names -> settings
SPIELE: list[tuple[str, dict[str, Any]]] = [
    (r"121", {"spiel": "checkout121"}),
    (r"wild(e)? ?m(o|au)use?|дикая мышь", {"spiel": "wild_mouse"}),
    (r"mi(c)?ke?y|микки", {"spiel": "mickey"}),
    (r"hidden|verdeckt|скрыт", {"spiel": "cricket", "zahlen": "hidden"}),
    (r"tactics|тактик", {"spiel": "cricket", "zahlen": "tactics"}),
    (r"round the world|um die welt|вокруг света", {"spiel": "rtw"}),
    (r"count ?up|hochzähl", {"spiel": "highscore"}),
    (r"bermuda|бермуд", {"spiel": "bermuda"}),
    (r"gotcha|готча", {"spiel": "gotcha"}),
    (r"nine lives|neun leben|девять жизней", {"spiel": "nine_lives"}),
    (r"fu(ß|ss)ball|football|soccer|футбол", {"spiel": "football"}),
    (r"scram|скрам", {"spiel": "scram"}),
    (r"catch ?(40|forty|vierzig)", {"spiel": "catch40"}),
    (r"jdc", {"spiel": "jdc"}),
    (r"singles|einzel|синглы", {"spiel": "singles"}),
    (r"checkout|finish|чекаут", {"spiel": "checkout"}),
    (r"cricket|крикет", {"spiel": "cricket"}),
    (r"shanghai|шанхай", {"spiel": "shanghai"}),
    (r"killer|киллер", {"spiel": "killer"}),
    (r"golf|гольф", {"spiel": "golf"}),
    (r"baseball|бейсбол", {"spiel": "baseball"}),
    (r"high ?score|хайскор", {"spiel": "highscore"}),
    (r"halve|halbier", {"spiel": "halve_it"}),
    (r"bob|боб", {"spiel": "bobs27"}),
    (r"uhr|clock|круг", {"spiel": "atc"}),
    (r"doppel|double|дубл", {"spiel": "doppel"}),
    (r"(101|170|301|501|701|901)", {"spiel": "x01"}),
]


ZAHL = "(" + "|".join(str(i) for i in range(180, -1, -1)) + "|null|nichts|zero|ноль)"
NULL_WOERTER = {"null", "nichts", "zero", "ноль"}


def punkte_saetze(namen: list[str]) -> dict[str, list[str]]:
    """Sentences for entering a visit by voice ("Alex hat 140"), with the names of the players."""
    sauber = sorted({re.sub(r"[()\[\]{}|<>]", "", n).strip().lower() for n in namen} - {""})
    saetze = {"de": [f"darts {ZAHL} [punkte]"], "en": [f"darts {ZAHL} [points]"], "ru": [f"дартс {ZAHL} [очков|очка]"]}
    if sauber:
        n = "(" + "|".join(sauber) + ")"
        saetze["de"].insert(0, f"{n} [hat|wirft|warf|macht] {ZAHL} [punkte]")
        saetze["en"].insert(0, f"{n} [has|scored|scores|throws|threw] {ZAHL} [points]")
        saetze["ru"].insert(0, f"[у] {n} [набрал|набрала] {ZAHL} [очков|очка]")
    return saetze


def punkte_lesen(text: str, namen: list[str]) -> tuple[str | None, int | None]:
    """Player name and score from a spoken sentence."""
    text = text.lower()
    zahlen = re.findall(r"\d{1,3}", text)
    punkte = int(zahlen[-1]) if zahlen else (0 if NULL_WOERTER & set(re.findall(r"\w+", text)) else None)
    name = next((n for n in sorted(namen, key=len, reverse=True) if n.lower() in text), None)
    return name, punkte


async def punkte_eintragen(leiter: Spielleiter, text: str, sprache: str) -> str:
    """Run a spoken score and answer with the new state."""
    tx = TEXTE[sprache]
    namen = [s["name"] for s in leiter.daten.get("spieler", [])]
    name, punkte = punkte_lesen(text, namen)
    if punkte is None:
        return tx["fehler"]
    st = leiter.stand or {}
    wer = (st.get("spieler") or [{}])[st["am_zug"]].get("name", "") if st.get("spieler") and st.get("am_zug") is not None else ""
    try:
        await leiter.aufnahme_eintragen(name, punkte)
    except HomeAssistantError as err:
        schluessel = getattr(err, "translation_key", "")
        if schluessel == "not_your_turn":
            return tx["dran"].format(n=wer)
        if schluessel == "score_x01_only":
            return tx["nur_x01"]
        if schluessel == "invalid_score":
            return tx["geht_nicht"].format(p=punkte)
        if schluessel == "no_game":
            return tx["kein"]
        return tx["fehler"]
    rest = stand_text(leiter, sprache) if leiter.phase() == "running" else tx["sieg"].format(n=wer)
    return tx["eingetragen"].format(n=wer, p=punkte) + " " + rest


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
    punkte_abmelden: list[CALLBACK_TYPE] = []
    manager = get_agent_manager(hass)

    def anmelden(saetze: list[str], antwort: Any) -> CALLBACK_TYPE:
        # Home Assistant 2026.11 and newer: register_trigger(sentences, trigger_callback)
        # read the parameter names from the code object: inspect.signature() evaluates the
        # annotations, which fails on Python 3.14 for this method (2026.11)
        code = getattr(manager.register_trigger, "__code__", None)
        if code is not None and "sentences" in code.co_varnames[: code.co_argcount]:
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

            try:
                abmelden.append(anmelden(saetze, antwort))
            except Exception:  # voice must never stop the board from loading
                _LOGGER.warning("Assist sentences for Autodarts could not be registered", exc_info=True)
                for f in abmelden:
                    f()
                return None

    # scores by voice: the sentences carry the player names, so they follow the player list
    namen_alt: list[tuple[str, ...]] = []

    def punkte_anmelden() -> None:
        leiter = leiter_holen()
        namen = tuple(sorted(s["name"] for s in leiter.daten.get("spieler", []))) if leiter else ()
        if namen_alt and namen_alt[0] == namen:
            return
        namen_alt[:] = [namen]
        for f in punkte_abmelden:
            f()
        punkte_abmelden.clear()
        # one registration for all languages ("darts 60" is the same everywhere); answer in the speaker's language
        saetze = [x for liste in punkte_saetze(list(namen)).values() for x in liste]

        async def antwort(user_input: Any, result: Any) -> str | None:
            leiter = leiter_holen()
            sprache = str(getattr(user_input, "language", "") or "en")[:2]
            return await punkte_eintragen(leiter, user_input.text, sprache if sprache in TEXTE else "en") if leiter else None

        try:
            punkte_abmelden.append(anmelden(saetze, antwort))
        except Exception:
            _LOGGER.warning("Assist score sentences for Autodarts could not be registered", exc_info=True)

    punkte_anmelden()
    leiter = leiter_holen()
    if leiter is not None:
        abmelden.append(leiter.hoerer(punkte_anmelden))

    def alle_abmelden() -> None:
        for f in abmelden + punkte_abmelden:
            f()

    return alle_abmelden
