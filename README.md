<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="docs/dark_logo.png">
    <img src="docs/logo.png" alt="Autodarts for Home Assistant" height="96">
  </picture>
</p>

# Autodarts for Home Assistant

Unofficial, fully local integration for an [Autodarts](https://autodarts.io) board.
It talks directly to the Autodarts **Board Manager** on your board PC (no cloud, no account)
and adds a complete local **X01 game** with players, a bot and statistics to Home Assistant.

> Not affiliated with or endorsed by Autodarts. "Autodarts" is used only to describe compatibility.

## Features

- Live state of the board: connection, status, last event, the three darts of the current visit with position
- Diagnostics: calibration and calibration error per camera, CPU, memory, frame rates, board software version
- Buttons like in the Board Manager: start/stop detection, reset throws, calibrate, restart
- Camera settings: resolution, frame rate, standby time
- Cameras: the three board cameras, detection image and live image (snapshot and MJPEG stream);
  the calibration net of each camera is available as attribute `kalibrierung`
- Update entity for the board software
- Local X01 games: 1–6 players, bots (by average), straight/double/master in and out, legs and sets,
  bull-off, undo and correction of darts, per-player statistics and game history

The board PC may be switched off at any time (for example by a smart plug).
The integration stays loaded, shows `Offline` and continues automatically when the board answers again.

## Requirements

- Home Assistant 2026.2 or newer
- An Autodarts board with Board Manager reachable in your network (default port 3180)

## Installation

### HACS (recommended)

1. HACS → three dots → **Custom repositories** → add `https://github.com/Wadim-dev/autodarts_ha`, type **Integration**.
2. Search for **Autodarts**, install it and restart Home Assistant.

### Manual

Copy `custom_components/autodarts` into the `custom_components` folder of your Home Assistant configuration and restart.

## Configuration

**Settings → Devices & services → Add integration → Autodarts.** The board must be switched on during setup.

| Parameter | Description |
|-----------|-------------|
| Host | IP address or host name of the board PC, e.g. `192.168.1.50` |
| Port | Port of the Board Manager, default `3180` |

## Actions

All actions work on the local game of the configured board.

| Action | Description |
|--------|-------------|
| `autodarts.spiel_starten` | Start an X01 game. Fields: `spieler` (player IDs, bots as `bot:55`), `startwert`, `einwurf`, `auswurf` (`straight`/`double`/`master`), `legs`, `sets`, `bull_off`. Without fields the last settings are used. |
| `autodarts.spiel_abbrechen` | Cancel the running game without result. |
| `autodarts.weiter` | Finish the current visit; missing darts count as miss. |
| `autodarts.rueckgaengig` | Undo the last dart. |
| `autodarts.wurf_aendern` | Correct, add or delete a dart (`aufnahme`, `dart` 0–2, `feld` like `T20`, `D16`, `25`, `Bull`, `M`; empty deletes). |
| `autodarts.spieler_anlegen` | Create a player (`name`); returns the new `id`. |
| `autodarts.spieler_aendern` | Rename (`name`) or delete (`loeschen`) a player by `id`. |
| `autodarts.statistik_loeschen` | Delete statistics of one player (`id`) or all; optionally the game history (`verlauf`). |

## Removal

1. **Settings → Devices & services → Autodarts → three dots → Delete.**
2. If installed with HACS, remove it in HACS as well, then restart Home Assistant.

Players, statistics and history are stored in `.storage/autodarts.spiel`; delete this file if you want to remove them too.

## Languages

English and German.

---

### Deutsch (Kurzfassung)

Inoffizielle, komplett lokale Integration für ein Autodarts-Board: Board-Zustand, Kameras, Kalibrierung und
ein lokales X01-Spiel mit Spielern, Bot und Statistik. Installation über HACS (benutzerdefiniertes Repository),
Einrichtung über **Einstellungen → Geräte & Dienste → Integration hinzufügen → Autodarts**.
