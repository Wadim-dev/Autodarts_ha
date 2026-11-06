"""Highlight clips: recording, saving at a 180, list, delete, files for the cards and the TV page."""

from __future__ import annotations

import asyncio
import math
from pathlib import Path
import shutil
import subprocess

from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ServiceValidationError
from homeassistant.setup import async_setup_component
import pytest

from custom_components.autodarts import clips as clips_modul
from custom_components.autodarts.const import DOMAIN

from .conftest import BASIS, board_mock


async def _dienst(hass: HomeAssistant, dienst: str, **daten):
    return await hass.services.async_call(DOMAIN, dienst, daten, blocking=True, return_response=dienst == "spieler_anlegen")


def _kal(f) -> dict:
    """Calibration points of a camera that sees the board through the mapping f(mm) -> px."""
    radien = (170, 162, 107, 99)
    ringe = [[list(f(r * math.sin(math.radians(9 + 18 * k)), -r * math.cos(math.radians(9 + 18 * k)))) for k in range(20)] for r in radien]
    return {"ringe": ringe, "bull": list(f(0, 0))}


def test_ecken() -> None:
    # straight camera: 2 px per mm, bull at (640, 360)
    eck = clips_modul.ecken(_kal(lambda x, y: (640 + 2 * x, 360 + 2 * y)))
    assert eck is not None
    assert [tuple(round(v) for v in p) for p in eck] == [(190, -90), (1090, -90), (190, 810), (1090, 810)]

    # tilted camera (perspective): the corners come back exactly
    def schraeg(x: float, y: float) -> tuple[float, float]:
        w = 1 + 0.0008 * x
        return ((640 + 1.6 * x + 0.3 * y) / w, (360 + 0.2 * x + 1.4 * y) / w)

    eck = clips_modul.ecken(_kal(schraeg))
    assert eck is not None
    for p, (x, y) in zip(eck, ((-225, -225), (225, -225), (-225, 225), (225, 225)), strict=True):
        assert math.dist(p, schraeg(x, y)) < 0.01
    assert clips_modul.ecken(None) is None and clips_modul.ecken({"ringe": [[[1, 1]] * 3]}) is None


@pytest.fixture
async def mit_http(hass: HomeAssistant, aioclient_mock, mock_entry, monkeypatch):
    monkeypatch.setattr(clips_modul, "TAKT", 0.02)
    monkeypatch.setattr(clips_modul, "NACHHER", 0.1)
    monkeypatch.setattr(clips_modul, "VORHER", 1.0)
    assert await async_setup_component(hass, "http", {})
    board_mock(aioclient_mock)
    aioclient_mock.get(f"{BASIS}/api/img/cams/0", content=b"jpeg")
    mock_entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(mock_entry.entry_id)
    await hass.async_block_till_done()
    yield mock_entry
    await hass.config_entries.async_unload(mock_entry.entry_id)
    await hass.async_block_till_done()


async def test_clip_bei_180(hass: HomeAssistant, mit_http, hass_client, hass_client_no_auth, monkeypatch) -> None:
    kodiert: list[tuple] = []

    def kodieren(ffmpeg, bilder, fps, eck, video: Path, vorschau: Path, mitte) -> bool:
        kodiert.append((len(bilder), fps, eck, mitte))
        video.write_bytes(b"mp4")
        vorschau.write_bytes(b"jpg")
        return True

    monkeypatch.setattr(clips_modul, "_kodieren", kodieren)
    c = mit_http.runtime_data.clips
    attr = lambda: hass.states.get("sensor.autodarts_board_players").attributes["clips"]  # noqa: E731
    assert attr()["an"] is False and attr()["anlaesse"] == ["one_eighty", "high_finish", "match_won"] and attr()["liste"] == []

    anna = (await _dienst(hass, "spieler_anlegen", name="Anna"))["id"]
    ben = (await _dienst(hass, "spieler_anlegen", name="Ben"))["id"]
    await _dienst(hass, "spiel_starten", spieler=[anna, ben], startwert=501)
    with pytest.raises(ServiceValidationError) as fehler:
        await _dienst(hass, "clip_speichern")
    assert fehler.value.translation_key == "clips_off"
    await asyncio.sleep(0.1)
    assert not c._laeuft()  # off: nothing is recorded

    await _dienst(hass, "clips_setzen", an=True)
    await asyncio.sleep(0.3)
    assert c._laeuft() and len(c._puffer) > 3
    for i in range(3):
        await _dienst(hass, "wurf_aendern", dart=i, feld="T20")
    await _dienst(hass, "weiter")
    for _ in range(50):
        await asyncio.sleep(0.05)
        if attr()["liste"]:
            break
    liste = attr()["liste"]
    assert len(liste) == 1 and liste[0]["art"] == "one_eighty" and liste[0]["spieler"] == "Anna" and liste[0]["wert"] == 180
    assert kodiert[0][0] > 3
    cid = liste[0]["id"]
    assert (c.ordner / f"{cid}.mp4").exists() and (c.ordner / f"{cid}.jpg").exists()

    # replay on the TV page, the file for the cards (login) and for the TV page (secret link)
    tv = mit_http.runtime_data.fernseher
    assert tv.live()["clip"]["id"] == cid
    token = tv.url().rsplit("/", 1)[1]
    assert (await (await hass_client()).get(f"/api/autodarts/clip/{cid}.mp4")).status == 200
    ohne = await hass_client_no_auth()
    assert (await ohne.get(f"/api/autodarts/clip/{cid}.mp4")).status == 401
    assert (await ohne.get(f"/autodarts/tv/{token}/clip/{cid}.jpg")).status == 200
    assert (await ohne.get(f"/autodarts/tv/{token}/clip/../../secrets.yaml")).status == 404
    assert (await ohne.get(f"/autodarts/tv/falsch/clip/{cid}.mp4")).status == 404
    assert (await ohne.get(f"/autodarts/tv/{token}/overlay")).status == 200

    # button "save clip" and the limit
    await _dienst(hass, "clips_setzen", anzahl=1, wiederholung=False)
    assert tv.live()["clip"] is None
    await _dienst(hass, "clip_speichern")
    for _ in range(50):
        await asyncio.sleep(0.05)
        if attr()["liste"][0]["id"] != cid:
            break
    liste = attr()["liste"]
    assert len(liste) == 1 and liste[0]["art"] == "manual" and not (c.ordner / f"{cid}.mp4").exists()

    await _dienst(hass, "clip_loeschen", id=liste[0]["id"])
    assert attr()["liste"] == [] and not list(c.ordner.glob("*.mp4"))

    # game over: recording stops
    await _dienst(hass, "spiel_abbrechen")
    await asyncio.sleep(0.1)
    assert not c._laeuft()


@pytest.mark.skipif(shutil.which("ffmpeg") is None, reason="ffmpeg not installed")
def test_kodieren_mit_ffmpeg(tmp_path: Path) -> None:
    bild = tmp_path / "b.jpg"
    subprocess.run(["ffmpeg", "-v", "error", "-f", "lavfi", "-i", "testsrc=size=640x360", "-frames:v", "1", str(bild)], check=True)
    bilder = [bild.read_bytes()] * 12
    eck = [(100.0, 20.0), (540.0, 0.0), (80.0, 340.0), (560.0, 350.0)]
    assert clips_modul._kodieren("ffmpeg", bilder, 6.0, eck, tmp_path / "c.mp4", tmp_path / "c.jpg", 5)
    assert (tmp_path / "c.mp4").stat().st_size > 1000 and (tmp_path / "c.jpg").exists()
    assert clips_modul._kodieren("ffmpeg", bilder, 6.0, None, tmp_path / "d.mp4", tmp_path / "d.jpg", 5)
    assert not clips_modul._kodieren("ffmpeg", [b"kaputt"] * 8, 6.0, None, tmp_path / "e.mp4", tmp_path / "e.jpg", 2)
