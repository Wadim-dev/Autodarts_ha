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
                                                "message": "One hundred and forty. Ben, you require 100", "cache": True}
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
        assert a.ansage([("visit", {"score": 40})]) == ("40", "Forty", ["40"])  # points of every game mode, no rest
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
    assert lautsprecher["tts"][-1].data["message"] == "One hundred and forty. Alex, you require 92"  # an example visit
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
    assert a.erzeugung == {"pack": "Meisterschaft", "fertig": 5, "gesamt": 5, "laeuft": False, "fehler": None, "falsch": []}
    assert len(texte) == 4 and all(t[2] == {"preferred_format": "wav", "voice": "fenrir"} for t in texte)
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
        assert lautsprecher["tts"][-1].data["message"] == "Sixty. Anna, you require 100"
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
    import math
    import wave

    werte = array.array("h")
    for laut, still in teile:
        werte.extend([int(9000 * math.sin(2 * math.pi * 300 * i / rate)) for i in range(int(laut * rate))])
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


async def test_pack_pruefen_mp3(hass: HomeAssistant, geladen, lautsprecher, tmp_path) -> None:
    """MP3 sounds (how Home Assistant saves a voice) are converted to WAV, cut and can then be joined."""
    import subprocess
    import wave

    ordner = lautsprecher["pfad"] / "autodarts" / "caller" / "Meisterschaft Orus"
    ordner.mkdir(parents=True)
    for k in ("140", "100", "60", "26", "92", "require", "name_alex"):
        _ton(tmp_path / "q.wav", [(1.0, 0.15), (1.2, 0.35), (0.8, 0)], rate=24000)
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(tmp_path / "q.wav"), str(ordner / f"{k}.mp3")], check=True)
    a = geladen.runtime_data.ansager
    await _setzen(hass, pack="Meisterschaft Orus")
    bericht = await a.pack_pruefen("Meisterschaft Orus")
    assert bericht["geschnitten"] == 7 and bericht["vorspann"] == pytest.approx(2.7, abs=0.1)
    assert sorted(f.name for f in ordner.glob("*.mp3")) == [] and len(list((ordner / "_original").glob("*.mp3"))) == 7
    with wave.open(str(ordner / "140.wav"), "rb") as w:
        assert w.getnframes() / w.getframerate() == pytest.approx(0.86, abs=0.08)
    await hass.services.async_call(DOMAIN, "ansager_testen", {}, blocking=True)
    assert "/Meisterschaft Orus/_mix/" in lautsprecher["play"][-1].data["media_content_id"]  # joined, not spoken


async def test_pack_als_wav_gespeichert(hass: HomeAssistant, geladen, lautsprecher, tmp_path, monkeypatch) -> None:
    """A sound the voice gives as MP3 is saved as WAV."""
    import subprocess

    monkeypatch.setattr(ansager_modul, "PAUSE", 0)
    _ton(tmp_path / "q.wav", [(0.5, 0)], rate=24000)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(tmp_path / "q.wav"), str(tmp_path / "q.mp3")], check=True)
    ordner = lautsprecher["pfad"] / "autodarts" / "caller" / "P"
    ordner.mkdir(parents=True)
    (ordner / "180.mp3").write_bytes(b"alt")
    a = geladen.runtime_data.ansager
    await _setzen(hass)

    async def audio(_hass, _mid):
        return "mp3", (tmp_path / "q.mp3").read_bytes()

    with (patch("homeassistant.components.tts.generate_media_source_id", return_value="tts:x"),
          patch("homeassistant.components.tts.async_get_media_source_audio", side_effect=audio)):
        a.pack_erzeugen("P", [], None, ["180"], neu=True)
        await a._erzeuger
    assert sorted(f.name for f in ordner.iterdir()) == ["180.wav"]


def test_pruefen_wie_gemessen(tmp_path) -> None:
    """As measured on a real pack: the direction ends between 3.0 and 4.2 s, some have a pause inside it."""
    for k, teile in {
        "26": [(2.0, 0.3), (0.5, 0.25), (1.6, 0)], "140": [(3.0, 0.3), (1.6, 0)], "game_on": [(2.8, 0.3), (1.4, 0)],
        "require": [(3.9, 0.3), (0.9, 0)], "180": [(3.3, 0.3), (2.0, 0)], "leg": [(3.5, 0.3), (0.8, 0.3), (1.0, 0)],
    }.items():
        _ton(tmp_path / f"{k}.wav", teile)
    bericht = ansager_modul._pruefen(tmp_path, True)
    assert bericht["geschnitten"] == 6 and not bericht["neu"]
    import wave
    for k, rest in {"26": 1.6, "140": 1.6, "game_on": 1.4, "require": 0.9, "leg": 2.1}.items():
        with wave.open(str(tmp_path / f"{k}.wav"), "rb") as w:
            assert w.getnframes() / w.getframerate() == pytest.approx(rest + 0.06, abs=0.04), k


async def test_pack_macht_von_selbst_weiter(hass: HomeAssistant, geladen, lautsprecher, monkeypatch, hass_ws_client) -> None:
    """At the daily limit a pack waits and continues by itself; stop ends that; a sample uses the speaker."""
    from homeassistant.helpers import entity_registry as er

    monkeypatch.setattr(ansager_modul, "PAUSE", 0)
    er.async_get(hass).async_get_or_create("tts", ansager_modul.GOOGLE_AI, "x", suggested_object_id="gemini")
    hass.states.async_set("tts.gemini", "unknown")
    a = geladen.runtime_data.ansager
    await _setzen(hass, stimme="tts.gemini")
    gewartet = []
    monkeypatch.setattr(a, "_wecken", lambda s: gewartet.append(s))
    with (patch("homeassistant.components.tts.generate_media_source_id", return_value="tts:x"),
          patch("homeassistant.components.tts.async_get_media_source_audio", side_effect=ValueError("429 PerDay"))):
        await hass.services.async_call(DOMAIN, "ansager_pack_erzeugen", {"sprecher": "orus", "name": "Meisterschaft Orus"}, blocking=True)
        await a._erzeuger
        await hass.async_block_till_done()
    assert gewartet == [ansager_modul.NOCHMAL] and a._auftrag == {"pack": "Meisterschaft Orus", "sprecher": "orus"}
    ws = await hass_ws_client(hass)
    await ws.send_json({"id": 1, "type": "autodarts/ansager"})
    antwort = (await ws.receive_json())["result"]
    assert antwort["auftrag"]["pack"] == "Meisterschaft Orus"
    await hass.services.async_call(DOMAIN, "ansager_pack_anhalten", {}, blocking=True)
    assert a._auftrag == {} and a.erzeugung["fehler"] == "stopped"
    await hass.services.async_call(DOMAIN, "ansager_testen", {"sprecher": "puck"}, blocking=True)
    assert lautsprecher["tts"][-1].data["options"] == {"voice": "puck"} and lautsprecher["tts"][-1].data["message"] == "One hundred and eighty!"


async def test_wecker_setzt_fort(hass: HomeAssistant, geladen, lautsprecher) -> None:
    a = geladen.runtime_data.ansager
    a._auftrag = {"pack": "P", "sprecher": None}
    with patch.object(a, "pack_erzeugen") as erz:
        a._wecken(0)
        await hass.async_block_till_done()
        from homeassistant.util import dt as dt_util
        from pytest_homeassistant_custom_component.common import async_fire_time_changed
        async_fire_time_changed(hass, dt_util.utcnow())
        await hass.async_block_till_done()
    assert erz.call_args[0][0] == "P"
    await a.beenden()


def test_zahlwort_und_passt() -> None:
    """Scores go to the voice as words; what speech-to-text heard is compared with the number."""
    z, p = ansager_modul._zahlwort, ansager_modul._passt
    assert [z(n, "de") for n in (1, 11, 16, 21, 100, 101, 117, 141, 180)] == [
        "Eins", "Elf", "Sechzehn", "Einundzwanzig", "Einhundert", "Einhunderteins", "Einhundertsiebzehn",
        "Einhunderteinundvierzig", "Einhundertachtzig"]
    assert [z(n, "en") for n in (7, 15, 40, 99, 100, 141)] == [
        "Seven", "Fifteen", "Forty", "Ninety-nine", "One hundred", "One hundred and forty-one"]
    assert p("100.", 100, "de") and p("Einhundert!", 100, "de") and p("Hundert", 100, "de") and p("hundert vierzig", 140, "de")
    assert p("180", 100, "de") is False and p("One hundred and eighty!", 100, "de") is False and p("Vierzig", 140, "de") is False
    assert p("a hundred and forty", 140, "en") and p("1 hundred", 100, "en") is False
    assert p("", 5, "de") is None and p("...", 5, "de") is None and p("No score", 0, "en") is None


class _Ohr:
    """A speech-to-text entity that hears the given answers one after the other."""

    def __init__(self, antworten: list[str]) -> None:
        from homeassistant.components import stt

        self.antworten = antworten
        self.bytes: list[int] = []
        self.supported_languages = ["de-DE", "en-US"]
        self.supported_formats = [stt.AudioFormats.WAV]
        self.supported_codecs = [stt.AudioCodecs.PCM]
        self.supported_sample_rates = [stt.AudioSampleRates.SAMPLERATE_16000]

    async def internal_async_process_audio_stream(self, meta, strom):
        from homeassistant.components import stt

        assert meta.language == "en-US" and meta.sample_rate == stt.AudioSampleRates.SAMPLERATE_16000
        self.bytes.append(sum([len(b) async for b in strom]))
        text = self.antworten.pop(0)
        if text == "!":
            raise ValueError("cloud down")  # noqa: TRY003
        return stt.SpeechResult(text, stt.SpeechResultState.SUCCESS if text != "?" else stt.SpeechResultState.ERROR)


@pytest.fixture
def ohr(hass: HomeAssistant, geladen, monkeypatch):
    from homeassistant.components import stt

    o = _Ohr([])
    monkeypatch.setattr(geladen.runtime_data.ansager, "_stt", lambda: "stt.ohr")
    monkeypatch.setattr(stt, "async_get_speech_to_text_entity", lambda _h, eid: o if eid == "stt.ohr" else None)
    monkeypatch.setattr(ansager_modul, "PAUSE", 0)
    return o


async def test_pack_erzeugen_hoert_nach(hass: HomeAssistant, geladen, lautsprecher, ohr) -> None:
    """A score sound that does not say its number is spoken again, at most three times."""
    a = geladen.runtime_data.ansager
    await _setzen(hass)
    ordner = lautsprecher["pfad"] / "autodarts" / "caller" / "Meisterschaft Fenrir"
    texte = []
    daten = _wav(lautsprecher["pfad"] / "x.wav")

    def mid(_hass, text, engine=None, options=None, cache=None):
        texte.append(text)
        return "tts:" + text

    async def audio(_hass, _mid):
        return "wav", daten

    ohr.antworten = ["180", "100", "120", "One hundred and twenty", "One hundred and eighty"]
    with (patch("homeassistant.components.tts.generate_media_source_id", side_effect=mid),
          patch("homeassistant.components.tts.async_get_media_source_audio", side_effect=audio)):
        a.pack_erzeugen("Meisterschaft Fenrir", [], "fenrir", ["100", "140", "leg"])
        await a._erzeuger
    assert texte == ["One hundred!", "One hundred!", "One hundred and forty!", "One hundred and forty!",
                     "One hundred and forty!", "Game shot, and the leg!"]
    assert a.erzeugung["falsch"] == ["140"] and a.erzeugung["fertig"] == 3 and all(ohr.bytes)
    assert {"100.wav", "140.wav", "leg.wav"} <= {f.name for f in ordner.iterdir()}
    assert a._gehoert == {"Meisterschaft Fenrir": True}  # made new: every score was listened to


async def test_pack_anhoeren(hass: HomeAssistant, geladen, lautsprecher, ohr, hass_storage, hass_ws_client) -> None:
    """Packs made before 1.23 are listened to once; wrong sounds are made again, the old one plays until then."""
    a = geladen.runtime_data.ansager
    basis = lautsprecher["pfad"] / "autodarts" / "caller"
    ordner = basis / "Meisterschaft Fenrir"
    ordner.mkdir(parents=True)
    for k in ("100", "140", "26", "0", "bust"):
        _wav(ordner / f"{k}.wav")
    (basis / "Eigenes").mkdir()
    await _setzen(hass, pack="Meisterschaft Fenrir")
    assert await hass.async_add_executor_job(a._ungehoert) == ["Meisterschaft Fenrir"]  # own packs are not listened to

    ohr.antworten = ["26", "100", "180"]
    daten = _wav(lautsprecher["pfad"] / "x.wav")

    async def audio(_hass, _mid):
        ohr.antworten.append("140")  # the new sound is right
        return "wav", daten

    with (patch("homeassistant.components.tts.generate_media_source_id", return_value="tts:x"),
          patch("homeassistant.components.tts.async_get_media_source_audio", side_effect=audio)):
        await hass.services.async_call(DOMAIN, "ansager_pack_pruefen", {"name": "Meisterschaft Fenrir", "anhoeren": True}, blocking=True)
        await a._hoerprobe
        assert a.pruefung["falsch"] == ["140"] and a.pruefung["fertig"] == 3 and not a.pruefung["laeuft"]
        assert a._auftrag == {"pack": "Meisterschaft Fenrir", "sprecher": "fenrir", "nur": ["140"]}
        await a._erzeuger
        await hass.async_block_till_done()
    assert a._auftrag == {} and a.erzeugung["fertig"] == 1 and not a.erzeugung["falsch"]
    assert hass_storage["autodarts.ansager_gehoert"]["data"] == {"Meisterschaft Fenrir": True}
    assert await hass.async_add_executor_job(a._ungehoert) == []
    ws = await hass_ws_client(hass)
    await ws.send_json({"id": 1, "type": "autodarts/ansager"})
    r = (await ws.receive_json())["result"]
    assert r["hoeren"] is True and r["gehoert"] == {"Meisterschaft Fenrir": True}

    # speech-to-text that does not work: nothing is changed, it is tried again later
    await a._gehoert_setzen("Meisterschaft Fenrir", None)
    ohr.antworten = ["!", "?", "26"]
    assert a.pack_anhoeren("Meisterschaft Fenrir")
    assert not a.pack_anhoeren("Meisterschaft Fenrir")  # already running
    await a._hoerprobe
    assert a.pruefung["unklar"] == 2 and "Meisterschaft Fenrir" not in a._gehoert
    await hass.services.async_call(DOMAIN, "ansager_pack_loeschen", {"name": "Meisterschaft Fenrir"}, blocking=True)


async def test_anhoeren_ohne_spracherkennung(hass: HomeAssistant, geladen, lautsprecher) -> None:
    a = geladen.runtime_data.ansager
    assert a._stt() is None and not a.pack_anhoeren("Meisterschaft Fenrir")
    assert await a._anhoeren(lautsprecher["pfad"], "100") is None


async def test_wecker_macht_weiter(hass: HomeAssistant, geladen, lautsprecher, ohr) -> None:
    """After the daily limit or a restart: sounds to make again continue, then packs not listened to yet."""
    from datetime import timedelta

    from homeassistant.util import dt as dt_util
    from pytest_homeassistant_custom_component.common import async_fire_time_changed

    a = geladen.runtime_data.ansager
    await _setzen(hass, pack="Eigenes")
    ordner = lautsprecher["pfad"] / "autodarts" / "caller" / "Meisterschaft Puck"
    ordner.mkdir(parents=True)
    _wav(ordner / "100.wav")
    daten = _wav(lautsprecher["pfad"] / "x.wav")

    async def audio(_hass, _mid):
        return "wav", daten

    with (patch("homeassistant.components.tts.generate_media_source_id", return_value="tts:x"),
          patch("homeassistant.components.tts.async_get_media_source_audio", side_effect=audio)):
        await a._auftrag_setzen({"pack": "Meisterschaft Puck", "sprecher": "puck", "nur": ["100"]})
        ohr.antworten = ["100"]
        a._wecken(10)
        async_fire_time_changed(hass, dt_util.utcnow() + timedelta(seconds=11))
        await hass.async_block_till_done()
        await a._erzeuger
        assert a._auftrag == {} and a.einst["pack"] == "Eigenes"  # made again, the pack in use stays
        await a._auftrag_setzen({"pack": "Meisterschaft Puck", "nur": []})
        a._wecken(10)
        async_fire_time_changed(hass, dt_util.utcnow() + timedelta(seconds=22))
        await hass.async_block_till_done()
        assert a._auftrag == {}
        await a._gehoert_setzen("Meisterschaft Puck", None)
        ohr.antworten = ["100"]
        a._wecken(10)
        async_fire_time_changed(hass, dt_util.utcnow() + timedelta(seconds=33))
        await hass.async_block_till_done()
        await a._hoerprobe
        assert a._gehoert == {"Meisterschaft Puck": True}
    await a.beenden()
