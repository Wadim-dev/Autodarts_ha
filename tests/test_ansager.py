"""Caller: announcements, sound packs and walk-on songs."""

from __future__ import annotations

import asyncio
from unittest.mock import patch

from homeassistant.components import media_source, tts  # noqa: F401  (loaded for patching)
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ServiceValidationError
import pytest
from pytest_homeassistant_custom_component.common import async_mock_service

from custom_components.autodarts import ansager as ansager_modul
from custom_components.autodarts.const import DOMAIN


@pytest.fixture
def lautsprecher(hass: HomeAssistant, tmp_path):
    hass.config.media_dirs = {"local": str(tmp_path)}
    hass.states.async_set("media_player.kueche", "idle", {"supported_features": ansager_modul.MEDIA_ANNOUNCE})
    hass.states.async_set("media_player.bad", "idle", {"supported_features": 0})
    hass.states.async_set("tts.piper", "unknown")
    return {
        "tts": async_mock_service(hass, "tts", "speak"),
        "play": async_mock_service(hass, "media_player", "play_media"),
        "stop": async_mock_service(hass, "media_player", "media_stop"),
        "pfad": tmp_path,
    }


async def _setzen(hass: HomeAssistant, **einst) -> None:
    await hass.services.async_call(DOMAIN, "ansager_setzen", {"einstellungen": {
        "aktiv": True, "lautsprecher": ["media_player.kueche"], **einst}}, blocking=True)


async def _fertig(hass: HomeAssistant, a: ansager_modul.Ansager) -> None:
    await asyncio.sleep(0)
    await asyncio.gather(*a._aufgaben, *([a._einlauf] if a._einlauf else []), return_exceptions=True)
    await hass.async_block_till_done()


async def test_einstellungen_und_uebersicht(hass: HomeAssistant, geladen, lautsprecher, hass_ws_client, hass_storage) -> None:
    pack = lautsprecher["pfad"] / "autodarts" / "caller" / "Classic"
    pack.mkdir(parents=True)
    (pack / "180.mp3").write_bytes(b"x")
    (pack / "notiz.txt").write_text("x")
    await _setzen(hass, pack="Classic", stimme="tts.piper", songs={"a1": "lied.mp3"}, unbekannt=1)
    assert hass_storage["autodarts.ansager"]["data"]["pack"] == "Classic"
    ws = await hass_ws_client(hass)
    await ws.send_json({"id": 1, "type": "autodarts/ansager"})
    r = (await ws.receive_json())["result"]
    assert r["packs"] == {"Classic": ["180"]} and r["songs"] == [] and r["stimmen"] == ["tts.piper"]
    assert r["einstellungen"]["songs"] == {"a1": "lied.mp3"} and "unbekannt" not in r["einstellungen"]
    assert (lautsprecher["pfad"] / "autodarts" / "walkon").is_dir()
    with pytest.raises(ServiceValidationError):
        await _setzen(hass, lautsprecher=["light.flur"])


async def test_ws_ohne_eintrag(hass: HomeAssistant, geladen, hass_ws_client) -> None:
    await hass.config_entries.async_unload(geladen.entry_id)
    ws = await hass_ws_client(hass)
    await ws.send_json({"id": 1, "type": "autodarts/ansager"})
    assert (await ws.receive_json())["result"]["packs"] == {}


async def test_aus_sagt_nichts(hass: HomeAssistant, geladen, lautsprecher) -> None:
    a = geladen.runtime_data.ansager
    a.ereignis("visit", {"player": "Anna", "score": 60})
    await _fertig(hass, a)
    assert not lautsprecher["tts"]


async def test_punkte_rest_und_pack(hass: HomeAssistant, geladen, lautsprecher) -> None:
    a = geladen.runtime_data.ansager
    await _setzen(hass)
    stand = {"art": "x01", "gewinner": None, "am_zug": 1, "weg": ["T20", "D16"],
             "spieler": [{"name": "Anna", "rest": 301}, {"name": "Ben", "rest": 100}]}
    with patch.object(geladen.runtime_data.spiel, "stand", stand):
        a.ereignis("dart", {})
        a.ereignis("visit", {"player": "Anna", "score": 140})
        a.ereignis("ton_forty", {"player": "Anna", "score": 140})
        await _fertig(hass, a)
        assert lautsprecher["tts"][-1].data == {"entity_id": "tts.piper", "media_player_entity_id": ["media_player.kueche"],
                                                "message": "140. Ben, you require 100", "cache": True}
        # a pack file is used when the key exists and nothing else must be said
        pack = lautsprecher["pfad"] / "autodarts" / "caller" / "Classic"
        pack.mkdir(parents=True)
        (pack / "180.MP3").write_bytes(b"x")
        await _setzen(hass, pack="Classic", rest=False, lautsprecher=["media_player.kueche", "media_player.bad"])
        a.ereignis("visit", {"player": "Anna", "score": 180})
        a.ereignis("one_eighty", {"player": "Anna", "score": 180})
        await _fertig(hass, a)
    aufrufe = [c.data for c in lautsprecher["play"]]
    url = "media-source://media_source/local/autodarts/caller/Classic/180.MP3"
    assert {"entity_id": ["media_player.kueche"], "media_content_id": url, "media_content_type": "music", "announce": True} in aufrufe
    assert {"entity_id": ["media_player.bad"], "media_content_id": url, "media_content_type": "music"} in aufrufe


@pytest.mark.parametrize(("ereignisse", "text"), [
    ([("visit", {"score": 26}), ("bust", {})], "No score!"),
    ([("visit", {}), ("checkout", {}), ("leg_won", {"player": "Anna"})], "Game shot, and the leg, Anna!"),
    ([("visit", {}), ("match_won", {"player": "Anna"})], "Game shot, and the match, Anna!"),
    ([("set_won", {"player": "Ben"})], "Game shot, and the set, Ben!"),
    ([("nine_darter", {"player": "Anna"}), ("leg_won", {"player": "Anna"})], "A nine-darter! Anna!"),
    ([("tournament_won", {"player": "Mia"})], "Mia wins the tournament!"),
    ([("shanghai", {"player": "Ben"})], "Shanghai, Ben!"),
])
async def test_ansagen(hass: HomeAssistant, geladen, ereignisse, text) -> None:
    a = geladen.runtime_data.ansager
    with patch.object(geladen.runtime_data.spiel, "stand", {"art": "x01", "gewinner": 0}):
        assert a.ansage(ereignisse)[1] == text


async def test_nicht_x01_und_abgeschaltet(hass: HomeAssistant, geladen) -> None:
    a = geladen.runtime_data.ansager
    with patch.object(geladen.runtime_data.spiel, "stand", {"art": "baseball"}):
        assert a.ansage([("visit", {"score": 40})]) == ("40", "40", ["40"])  # points of every game mode, no rest
    a.einst = {**a.einst, "ende": False, "punkte": False, "rest": False}
    with patch.object(geladen.runtime_data.spiel, "stand", {"art": "x01"}):
        assert a.ansage([("visit", {"score": 40}), ("leg_won", {"player": "A"})]) is None


async def test_einlauf_und_game_on(hass: HomeAssistant, geladen, lautsprecher) -> None:
    a = geladen.runtime_data.ansager
    await _setzen(hass, songs={"a1": "tiger.mp3"}, walkon_sekunden=5)
    with patch.object(ansager_modul.asyncio, "sleep", side_effect=_null):
        a.ereignis("game_started", {"players": ["Anna", "Ben"], "player_ids": ["a1", "b2"]})
        await _fertig(hass, a)
    texte = [c.data["message"] for c in lautsprecher["tts"]]
    assert texte == ["Ladies and gentlemen: Anna!", "Game on!"]
    assert lautsprecher["play"][-1].data["media_content_id"] == "media-source://media_source/local/autodarts/walkon/tiger.mp3"
    assert "announce" not in lautsprecher["play"][-1].data
    assert lautsprecher["stop"]


async def test_testen_und_fehler(hass: HomeAssistant, geladen, lautsprecher, caplog) -> None:
    await _setzen(hass)
    await hass.services.async_call(DOMAIN, "ansager_testen", {"text": "Hallo"}, blocking=True)
    assert lautsprecher["tts"][-1].data["message"] == "Hallo"
    await hass.services.async_call(DOMAIN, "ansager_testen", {}, blocking=True)
    assert lautsprecher["tts"][-1].data["message"] == "140. Alex, you require 92"  # an example visit
    hass.states.async_remove("tts.piper")
    await hass.services.async_call(DOMAIN, "ansager_testen", {}, blocking=True)
    assert "no voice" in caplog.text


async def test_deutsch(hass: HomeAssistant, geladen) -> None:
    hass.config.language = "de"
    with patch.object(geladen.runtime_data.spiel, "stand", {"art": "x01", "gewinner": 0}):
        assert geladen.runtime_data.ansager.ansage([("visit", {"score": 180})])[1] == "Einhundertachtzig!"


_echt = asyncio.sleep


async def _null(sekunden: float) -> None:
    await _echt(0)


async def test_handy_hoert_mit(hass: HomeAssistant, geladen, lautsprecher, hass_ws_client) -> None:
    """The game card on a phone gets every announcement as an address, also without speakers."""
    a = geladen.runtime_data.ansager
    ws = await hass_ws_client(hass)
    await ws.send_json({"id": 7, "type": "autodarts/ansager/hoeren"})
    assert (await ws.receive_json())["success"]

    class Item:
        def __init__(self, url: str) -> None:
            self.url = url

    async def aufloesen(_hass, media_id, _ziel):
        return Item("/api/tts_proxy/x.mp3" if media_id.startswith("tts:") else "/media/local/" + media_id.rsplit("local/", 1)[1])

    stand = {"art": "x01", "gewinner": 0, "spieler": []}
    with (patch.object(geladen.runtime_data.spiel, "stand", stand),
          patch("homeassistant.components.tts.generate_media_source_id", return_value="tts:140") as tts_id,
          patch("homeassistant.components.media_source.async_resolve_media", side_effect=aufloesen)):
        a.ereignis("visit", {"player": "Anna", "score": 140})
        await _fertig(hass, a)
        assert (await ws.receive_json())["event"] == {"url": "/api/tts_proxy/x.mp3"}
        assert tts_id.call_args.kwargs["engine"] == "tts.piper"
        assert not lautsprecher["tts"]  # caller switched off for the speakers
        await _setzen(hass, songs={"a1": "tiger.mp3"}, walkon_sekunden=5)
        with patch.object(ansager_modul.asyncio, "sleep", side_effect=_null):
            a.ereignis("game_started", {"players": ["Anna"], "player_ids": ["a1"]})
            await _fertig(hass, a)
    events = [(await ws.receive_json())["event"] for _ in range(4)]
    assert events[1]["url"].startswith("/media/local/autodarts/walkon/tiger.mp3?authSig=")
    assert events[2] == {"stop": True}
    assert lautsprecher["tts"] and lautsprecher["stop"]  # speakers too
    await ws.send_json({"id": 8, "type": "unsubscribe_events", "subscription": 7})
    await ws.receive_json()
    assert not a._hoerer


async def test_handy_ohne_eintrag(hass: HomeAssistant, geladen, hass_ws_client) -> None:
    await hass.config_entries.async_unload(geladen.entry_id)
    ws = await hass_ws_client(hass)
    await ws.send_json({"id": 1, "type": "autodarts/ansager/hoeren"})
    assert not (await ws.receive_json())["success"]


def _wav(pfad, frames: int = 800) -> bytes:
    import io
    import wave
    b = io.BytesIO()
    with wave.open(b, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(8000)
        w.writeframes(b"\x01\x00" * frames)
    pfad.write_bytes(b.getvalue())
    return b.getvalue()


async def test_pack_erzeugen_und_zusammensetzen(hass: HomeAssistant, geladen, lautsprecher, monkeypatch) -> None:
    """A pack is made from the voice (resumable) and a visit with rest is joined from its files."""
    from homeassistant.helpers import entity_registry as er

    monkeypatch.setattr(ansager_modul, "PAUSE", 0)

    er.async_get(hass).async_get_or_create("tts", ansager_modul.GOOGLE_AI, "x", suggested_object_id="gemini")
    hass.states.async_set("tts.gemini", "unknown")
    a = geladen.runtime_data.ansager
    await _setzen(hass, stimme="tts.gemini")
    ordner = lautsprecher["pfad"] / "autodarts" / "caller" / "Meisterschaft"
    ordner.mkdir(parents=True)
    _wav(ordner / "180.wav")  # already there: kept
    texte = []
    daten = _wav(lautsprecher["pfad"] / "x.wav")

    def mid(_hass, text, engine=None, options=None, cache=None):
        texte.append((text, engine, options))
        return "tts:" + text

    async def audio(_hass, _mid):
        return "wav", daten

    with (patch("homeassistant.components.tts.generate_media_source_id", side_effect=mid),
          patch("homeassistant.components.tts.async_get_media_source_audio", side_effect=audio)):
        await hass.services.async_call(DOMAIN, "ansager_pack_erzeugen", {"sprecher": "fenrir", "nur": ["180", "140", "require", "100", "leg"]}, blocking=True)
        await a._erzeuger
    assert a.erzeugung == {"pack": "Meisterschaft", "fertig": 5, "gesamt": 5, "laeuft": False, "fehler": None}
    assert len(texte) == 4 and all(t[2] == {"voice": "fenrir"} for t in texte)
    assert texte[-1][0] == "Game shot, and the leg!"  # the text as it is: a direction in front was read out loud
    assert {"140.wav", "require.wav", "100.wav", "leg.wav"} <= {f.name for f in ordner.iterdir()}
    assert "name_anna" in a.pack_texte(["Anna"]) and "163" not in a.pack_texte([])

    _wav(ordner / "name_ben.wav")
    await _setzen(hass, stimme="tts.gemini", pack="Meisterschaft")
    stand = {"art": "x01", "gewinner": None, "am_zug": 1, "weg": ["T20", "D16"],
             "spieler": [{"name": "Anna", "rest": 301}, {"name": "Ben", "rest": 100}]}
    with patch.object(geladen.runtime_data.spiel, "stand", stand):
        a.ereignis("visit", {"player": "Anna", "score": 140})
        await _fertig(hass, a)
        url = lautsprecher["play"][-1].data["media_content_id"]
        assert url.startswith("media-source://media_source/local/autodarts/caller/Meisterschaft/_mix/")
        import wave
        with wave.open(str(ordner / "_mix" / url.rsplit("/", 1)[1]), "rb") as w:
            assert w.getnframes() == 4 * 800 + 3 * 960
        # a missing file (no name for Anna) → spoken as it is
        stand["am_zug"] = 0
        stand["spieler"][0]["rest"] = 100
        a.ereignis("visit", {"player": "Ben", "score": 60})
        await _fertig(hass, a)
        assert lautsprecher["tts"][-1].data["message"] == "60. Anna, you require 100"
    # speak again with another speaker: files are replaced and the joined sounds removed
    with (patch("homeassistant.components.tts.generate_media_source_id", side_effect=mid),
          patch("homeassistant.components.tts.async_get_media_source_audio", side_effect=audio)):
        texte.clear()
        a.pack_erzeugen("Meisterschaft", [], "puck", ["180"], neu=True)
        await a._erzeuger
    assert len(texte) == 1 and not list((ordner / "_mix").glob("*.wav"))


async def test_pack_fehler(hass: HomeAssistant, geladen, lautsprecher) -> None:
    a = geladen.runtime_data.ansager
    await _setzen(hass)
    with (patch("homeassistant.components.tts.generate_media_source_id", return_value="tts:x"),
          patch("homeassistant.components.tts.async_get_media_source_audio", side_effect=ValueError("quota")),
          patch.object(ansager_modul.asyncio, "sleep", side_effect=_null)):
        a.pack_erzeugen("Test", [], None, ["180"])
        a.pack_erzeugen("Test", [], None, ["180"])  # already running: ignored
        await a._erzeuger
    assert a.erzeugung["fehler"] == "quota" and not a.erzeugung["laeuft"]
    hass.states.async_remove("tts.piper")
    a.pack_erzeugen("Test", [], None, None)
    await a._erzeuger
    assert a.erzeugung["fehler"] == "no voice"


async def test_pack_tageslimit_und_loeschen(hass: HomeAssistant, geladen, lautsprecher, hass_storage) -> None:
    a = geladen.runtime_data.ansager
    await _setzen(hass, pack="Alt")
    ordner = lautsprecher["pfad"] / "autodarts" / "caller" / "Alt"
    ordner.mkdir(parents=True)
    _wav(ordner / "180.wav")
    with (patch("homeassistant.components.tts.generate_media_source_id", return_value="tts:x"),
          patch("homeassistant.components.tts.async_get_media_source_audio",
                side_effect=ValueError("429 generate_requests_per_model_per_day"))):
        a.pack_erzeugen("Neu", [], None, ["140"])
        await a._erzeuger
    assert a.erzeugung["fehler"] == "daily limit"
    assert not (ordner.parent / "Neu").exists()  # no sound made: no empty pack left behind
    await hass.services.async_call(DOMAIN, "ansager_pack_loeschen", {"name": "Alt"}, blocking=True)
    assert not ordner.exists() and a.einst["pack"] == ""
    await hass.services.async_call(DOMAIN, "ansager_pack_loeschen", {"name": "Neu"}, blocking=True)


def _ton(pfad, teile, rate=8000) -> None:
    """A WAV of (seconds of sound, seconds of silence) parts."""
    import array
    import wave

    werte = array.array("h")
    for laut, still in teile:
        werte.extend([9000 if i % 2 else -9000 for i in range(int(laut * rate))])
        werte.extend([0] * int(still * rate))
    with wave.open(str(pfad), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(werte.tobytes())


async def test_pack_pruefen_schneidet_vorspann(hass: HomeAssistant, geladen, lautsprecher) -> None:
    """A spoken direction ("Say loudly …:") at the start of the pack sounds is cut off at the pause after it."""
    import wave

    a = geladen.runtime_data.ansager
    ordner = lautsprecher["pfad"] / "autodarts" / "caller" / "Meisterschaft Fenrir"
    ordner.mkdir(parents=True)
    # direction 1.0 s, pause 0.15 (too short), 1.2 s, pause 0.35 → the cut is at 2.7 s
    for k in ("140", "100", "60", "26"):
        _ton(ordner / f"{k}.wav", [(1.0, 0.15), (1.2, 0.35), (0.8, 0)])
    _ton(ordner / "leg.wav", [(1.0, 0.15), (1.25, 0.3), (0.5, 0.3), (0.6, 0)])  # own pause later: kept
    _ton(ordner / "require.wav", [(4.0, 0)])  # long but no pause: made again
    _ton(ordner / "bust.wav", [(0.9, 0)])  # never had the direction
    (ordner / "_mix").mkdir()
    _ton(ordner / "_mix" / "alt.wav", [(1, 0)])
    await _setzen(hass, pack="Meisterschaft Fenrir")

    bericht = await hass.services.async_call(DOMAIN, "ansager_pack_pruefen", {"name": "Meisterschaft Fenrir", "reparieren": False},
                                             blocking=True, return_response=True)
    assert bericht["vorspann"] == pytest.approx(2.7, abs=0.05)
    assert bericht["geschnitten"] == 5 and bericht["neu"] == ["require"] and bericht["ohne"] == 1
    assert not (ordner / "_original").exists()

    await hass.services.async_call(DOMAIN, "ansager_pack_pruefen", {"name": "Meisterschaft Fenrir"}, blocking=True)
    with wave.open(str(ordner / "140.wav"), "rb") as w:
        assert w.getnframes() / w.getframerate() == pytest.approx(0.86, abs=0.03)
    with wave.open(str(ordner / "leg.wav"), "rb") as w:
        assert w.getnframes() / w.getframerate() == pytest.approx(1.46, abs=0.03)
    assert not (ordner / "require.wav").exists() and (ordner / "_original" / "require.wav").exists()
    assert (ordner / "_original" / "140.wav").exists() and not (ordner / "_mix").exists()
    assert "require" not in a._pack and a.pruefung["repariert"]
    # a clean pack: nothing found, nothing changed
    assert (await a.pack_pruefen("Meisterschaft Fenrir", False))["vorspann"] is None
    assert (await a.pack_pruefen("../x"))["dateien"] == 0
