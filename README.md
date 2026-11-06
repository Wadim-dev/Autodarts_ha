<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Wadim-dev/DartNest_ha/main/docs/dark_logo.png">
    <img src="https://raw.githubusercontent.com/Wadim-dev/DartNest_ha/main/docs/logo.png" alt="DartNest for Autodarts" height="88">
  </picture>
</p>

<h3 align="center">Your dartboard, at home in Home Assistant.</h3>

<p align="center">
  Play, score, celebrate and track every dart – with ready-made screens for tablet and phone.<br>
  Works with <b>Autodarts</b> boards · 100 % local · no YAML, no code.
</p>

<p align="center">
  <a href="https://my.home-assistant.io/redirect/hacs_repository/?owner=Wadim-dev&repository=DartNest_ha&category=integration"><img src="https://my.home-assistant.io/badges/hacs_repository.svg" alt="Install from the Marketplace"></a>
</p>

<p align="center">
  <a href="https://github.com/Wadim-dev/DartNest_ha/releases"><img src="https://img.shields.io/github/v/release/Wadim-dev/DartNest_ha?style=flat-square&color=ff7a50" alt="Release"></a>
  <a href="https://github.com/Wadim-dev/DartNest_ha/actions/workflows/validate.yml"><img src="https://img.shields.io/github/actions/workflow/status/Wadim-dev/DartNest_ha/validate.yml?branch=main&label=checks&style=flat-square" alt="Checks"></a>
  <a href="custom_components/autodarts/quality_scale.yaml"><img src="https://img.shields.io/badge/quality%20scale-platinum-e5e4e2?style=flat-square" alt="Quality scale: Platinum"></a>
  <img src="https://img.shields.io/badge/100%25-local-00a37a?style=flat-square" alt="100 % local">
  <img src="https://img.shields.io/badge/languages-EN%20%7C%20DE-blue?style=flat-square" alt="English and German">
  <a href="LICENSE"><img src="https://img.shields.io/github/license/Wadim-dev/DartNest_ha?style=flat-square" alt="License"></a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/Wadim-dev/DartNest_ha/main/docs/images/hero.png" alt="DartNest on tablet and phone" width="900">
</p>

> **Unofficial project.** DartNest is a free hobby project and not affiliated with Autodarts. "Autodarts" is only named to say which boards it works with. See [Legal notice](#legal-notice).

---

## Why DartNest?

<table>
  <tr>
    <td width="33%" valign="top"><h3>🧩 Ready in two minutes</h3>Install, confirm the board that Home Assistant finds by itself – done. A new <b>DartNest</b> entry in the sidebar holds every screen. Nothing to configure, no YAML, no dashboard to build.</td>
    <td width="33%" valign="top"><h3>🎯 A real darts night</h3>29 games – X01, Cricket, training and party – for 1–8 players and bots, a caller with walk-on songs, stadium effects on a 180 and your lights flashing along.</td>
    <td width="33%" valign="top"><h3>🏠 Stays at home</h3>Talks only to the board PC in your own network. No cloud, no account, no subscription. Players and statistics never leave your Home Assistant.</td>
  </tr>
</table>

## Get started in 3 steps

1. **Install** – tap the *Marketplace* button above and install **DartNest**, then restart Home Assistant.
2. **Confirm your board** – *Settings → Devices & services* shows **Autodarts board found**. Tap *Add*. (Not found? *Add integration → DartNest* and type the IP address of the board PC.)
3. **Play** – open **DartNest** in the sidebar. That's it.

---

## Play

<p align="center"><img src="https://raw.githubusercontent.com/Wadim-dev/DartNest_ha/main/docs/images/play.png" alt="Game screen on a tablet and the keypad on a phone" width="900"></p>

Big scores, average, checkout ways and every dart where it landed. ✏️ Tap any visit to correct it · 📷 show the straightened camera image instead of the drawn board · 🖐️ no cameras or board off? a keypad appears by itself · 🔒 the screen stays awake during a game.

<p align="center"><img src="https://raw.githubusercontent.com/Wadim-dev/DartNest_ha/main/docs/images/games.png" alt="29 games in four groups" width="900"></p>

| X01 | Cricket (8) | Training (8) | Party (12) |
|---|---|---|---|
| 101 – 901<br>double / master in and out<br>legs and sets<br>teams · handicap<br>50/50 bull · round limit | Cricket · Cut-Throat · No Score<br>Tactics · Random · Hidden<br>Wild Mouse · Mickey Mouse | Around the Clock · Doubles<br>Singles · Bob's 27<br>121 Checkout · Checkout Training<br>Catch 40 · JDC Challenge | Count-Up · Shanghai · Killer<br>Halve-It · Bermuda · Golf<br>Baseball · Round the World<br>Gotcha · Nine Lives · Football · Scram |

<p align="center"><img src="https://raw.githubusercontent.com/Wadim-dev/DartNest_ha/main/docs/images/new-games.png" alt="Gotcha, Wild Mouse, Football and Scram" width="900"></p>

Every game knows its own rules: whose turn it is, what to aim for, who is ahead. A tie in a points game such as Count-Up or Golf goes to extra rounds. Bots from beginner to pro make every evening a match – even alone.

## Celebrate

<p align="center"><img src="https://raw.githubusercontent.com/Wadim-dev/DartNest_ha/main/docs/images/real.png" alt="Live camera image in the game and the 180 effect on a real board" width="900"></p>

**Stadium moments.** Spotlights and confetti on a 180, cracks on a bust, fireworks and a trophy for the match winner, a rainbow for the nine-darter.

<p align="center"><img src="https://raw.githubusercontent.com/Wadim-dev/DartNest_ha/main/docs/images/celebrate.png" alt="Caller, light effects and the light effect editor" width="900"></p>

**Caller.** Scores in every game, "you require 32", game shot and a walk-on song per player – on your speakers, on the phone, or both. Make a **championship pack** with a stage announcer voice in one tap, or upload your own sounds.
**Lights.** Let your lamps flash, pulse or burn like fire on a 180, a checkout or a won leg – 18 effects plus WLED effects and presets. Afterwards everything goes back to how it was. No YAML.

## Get better

<p align="center"><img src="https://raw.githubusercontent.com/Wadim-dev/DartNest_ha/main/docs/images/stats.png" alt="Players with statistics and the aim map" width="900"></p>

Average, first 9, checkout rate, rating, trend, badges, head to head and a ranking. The **aim map** shows where *you* score most with your own spread – often it is not the T20.

## Tournaments

<p align="center"><img src="https://raw.githubusercontent.com/Wadim-dev/DartNest_ha/main/docs/images/tournaments.png" alt="Tournament formats, double KO bracket and group stage" width="900"></p>

Four formats: **knockout** (3–32), **double KO** with winners and losers bracket (3–16), **groups + KO** (6–32) and a **league** (3–10). Play alone, as **teams of two** or with a **handicap** for beginners. The next match starts with one tap.

## On the TV

<p align="center"><img src="https://raw.githubusercontent.com/Wadim-dev/DartNest_ha/main/docs/images/tv.png" alt="Scoreboard on the TV, rest screen with clock and ranking, TV settings on the phone" width="900"></p>

Open **DartNest → TV**, tick your TV and tap **Show on TV** – the score appears big on **Fire TV, Google TV or Chromecast**, live with every dart. Between games the TV shows the clock, the ranking and the last games. Switch on **Show by itself when a game starts** and you never touch the remote. **Show the dartboard** puts your board next to the score – live from the camera, straightened, with the darts of the visit marked. Any other screen works too: open the link in its browser.

## Stream and highlights

<p align="center"><img src="https://raw.githubusercontent.com/Wadim-dev/DartNest_ha/main/docs/images/stream.png" alt="Stream overlay with score and replay, highlights card on the phone" width="900"></p>

Streaming your games? Add the **overlay link** from the TV card as a browser source in **OBS or Streamlabs** – a see-through scoreboard sits on top of your camera. Switch on **Highlights** and every **180, high finish and match dart** is saved as a short, straightened video from the board camera. Watch, download or delete them in the card; right after the dart they play once as a replay on the TV and in the overlay.

## On the LED clock

<p align="center"><img src="https://raw.githubusercontent.com/Wadim-dev/DartNest_ha/main/docs/images/pixel.png" alt="Score and 180 effect on an AWTRIX 3 LED clock, pixel display card on the phone" width="900"></p>

Got an **AWTRIX 3** (Ulanzi TC001) or a **PixelIt** clock? Open **DartNest → Pixel display**, tap **Add display** and type its IP address – DartNest finds out which one it is. While you play, the clock shows who is at the oche and what is left; a **180, checkout, bust, leg or win** flashes as a short effect. After the game the clock goes back to its own apps. No MQTT, no add-on, no automation.

## Board Manager inside Home Assistant

<p align="center"><img src="https://raw.githubusercontent.com/Wadim-dev/DartNest_ha/main/docs/images/manager.png" alt="Board Manager with cameras, power states and camera settings" width="900"></p>

All three cameras with the calibration grid, start/stop, calibrate, camera settings and board software updates – without opening another web page. **Smart plug friendly:** pick the plug of the board PC once under *Board Manager → Board PC power plug* – every DartNest screen then has the on/off button. DartNest shows *Off* and carries on by itself when the board is back. **Light on small PCs:** live views share one image source (at most 10 images per second, only while someone watches), the camera standby is shown as *Standby* and DartNest wakes the detection by itself when a game starts.

<sub>Screenshots with the German interface come from a real board at home.</sub>

## Everywhere

<p align="center"><img src="https://raw.githubusercontent.com/Wadim-dev/DartNest_ha/main/docs/images/everywhere.png" alt="Sidebar on PC and phone, tile and tile window" width="900"></p>

The same screens work on PC, tablet and phone, in English and German. Want them on your own dashboard? **Edit dashboard → Add card → search "DartNest"** – no resources to add.

**Talk to it:** "Alex 140", "What's the score?", "Undo" – voice commands in English, German and Russian through Assist.

---

## Requirements

- Home Assistant **2026.2** or newer
- An **Autodarts** board (Board Manager 1.x or 2.x) in your network – Linux PC, mini PC, Raspberry Pi or Windows
- Optional: speakers for the caller, lights for effects, a smart plug for the board PC

## Installation

[![Open your Home Assistant instance and open this repository in the Marketplace.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Wadim-dev&repository=DartNest_ha&category=integration)

### Marketplace (recommended)

1. Click the button above, or in Home Assistant open the **Marketplace**, choose **Add by link** and enter `https://github.com/Wadim-dev/DartNest_ha` (type **Integration**).
2. Install **DartNest** and restart Home Assistant.
3. Add the integration (see [Configuration](#configuration)).

New versions show up under **Settings → Updates** like any other Marketplace update.

### Manual

Copy `custom_components/autodarts` from the [latest release](https://github.com/Wadim-dev/DartNest_ha/releases/latest) into the `custom_components` folder of the Home Assistant configuration and restart Home Assistant.

## Setup

[![Open your Home Assistant instance and start setting up DartNest.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=autodarts)

Boards with Board Manager 2.x announce themselves in the network: Home Assistant shows **Autodarts board found** under **Settings → Devices & services** – just confirm. Otherwise add it by hand: **Settings → Devices & services → Add integration → DartNest.** The board must be switched on during setup.

| Parameter | Description |
|-----------|-------------|
| Host | IP address or host name of the board PC, e.g. `192.168.1.50` |
| Port | Port of the Board Manager, default `3180` |

There are no further options. To change the address later, use **three dots → Reconfigure** on the integration. If the board gets a new IP address and announces itself, the integration follows it automatically (only if the old address no longer answers).

**Data updates:** game state every second (every 30 s while the board is off), system values every 15 s, calibration points only after a new calibration, camera images only while they are shown.

---

## Everything in detail

For the curious and for automation fans. You do not need any of this to play.

<details>
<summary><b>Game screen in detail</b></summary>


The game card is made for a tablet next to the board (full screen button included):

- big scores, average and checkout suggestions for every player
- the current visit with the three darts, entered by the board or by tap
- the board as graphic **or as straightened live camera image** (tap the board to switch camera 1/2/3/graphic, "Grid" shows the calibration grid)
- visit history – tap any visit to correct it
- live statistics and the result screen with rematch
- optional **caller**: announces scores, "One hundred and eighty!", checkouts and what you require (the caller of Home Assistant with its voice and sound pack; the browser voice only as a fallback)
- keeps the screen awake during a game
- **effects** for what happens at a real board: dart flight with wobble, sparks on trebles and doubles, bull flash, "MISS" falling off, board jolt; big scenes for 180 (spotlights, shockwave, confetti), ton-forty, ton, three in a bed, bed & breakfast, no score (tumbleweed), bust (cracks and stamp), game shot, high finish, 170 "big fish", set, match (fireworks and trophy) and the nine-darter (rainbow). Sounds play only while the caller is on. The ✨ button switches effects off per device; they respect "reduce motion" and stop while the card is hidden.



</details>

<details>
<summary><b>Local games and rules</b></summary>

All games run completely inside Home Assistant, for 1–8 players, people and bots mixed (Scram is for exactly two, Killer needs at least two). The game card shows a short rule text for every game, highlights the current target on the board and has its own effects (nine marks, Shanghai, gotcha, goal, killer, hole in one …). Bots play every game.

**X01 and Cricket**

| Game | `spiel` | Rules in short | Options |
|------|---------|----------------|---------|
| X01 | `x01` | 101 … 901, see below | start value, in/out, legs, sets, 50/50 bull, round limit, handicap |
| Cricket | `cricket` | Close 15–20 and bull with three marks; extra marks score while an opponent has the number open | `variante`: `standard`, `cut_throat` (points go to the opponents, lowest wins), `no_score`; `zahlen`: `classic` (15–20), `tactics` (10–20), `random` (6 random numbers), `hidden` (6 random numbers, shown when someone hits them) |
| Wild Mouse | `wild_mouse` | Cricket on 20–15 and bull plus three extra targets: any double, any treble and 3 in a bed (three darts in the same field). A dart marks its own number first, then the double or treble | `variante`: `ohne_3b` (without 3 in a bed) |
| Mickey Mouse | `mickey` | Close 20–12, any double, any treble and bull; no points, first to close everything wins | – |

**Training**

| Game | `spiel` | Rules in short | Options |
|------|---------|----------------|---------|
| Around the Clock | `atc` | 1 to 20, then bull; first through wins | `variante`: `single` (any segment), `double`, `triple` |
| Doubles | `doppel` | Three darts at every double, one point per hit | – |
| Singles | `singles` | One visit at every number 1–20 and bull; single 1, double 2, treble 3 points | – |
| Bob's 27 | `bobs27` | Start 27; three darts at D1 … D20 and bull; hits add, no hit subtracts; below 0 you are out | – |
| 121 Checkout | `checkout121` | Nine darts to check out (double out); done +1, missed −1 | `runden` (attempts, default 10) |
| Checkout Training | `checkout` | Random finishes from 2 to 170, three visits each (double out); everyone gets the same finishes; most checkouts win | `runden` (default 10) |
| Catch 40 | `catch40` | Finishes 61 to 100, two visits each; 3 points with two darts, 2 with three, 1 in the second visit | – |
| JDC Challenge | `jdc` | Shanghai 10–15, one dart at every double and bull, Shanghai 15–20 – the junior darts test with 57 darts | – |

**Party**

| Game | `spiel` | Rules in short | Options |
|------|---------|----------------|---------|
| Count-Up | `highscore` | Most points in N visits | `runden` (default 8) |
| Shanghai | `shanghai` | Round n counts number n; single, double and treble in one visit wins at once | `runden`: 7 or 20 |
| Killer | `killer` | Hit your double to become a killer, then take the lives of the others with their double | `leben` (default 3) |
| Halve-It | `halve_it` | 15, 16, any double, 17, 18, any treble, 19, 20, bull; no hit halves your score | – |
| Bermuda | `bermuda` | Like Halve-It with 13 targets: 12, 13, 14, double, 15, 16, 17, treble, 18, 19, 20, bull, bullseye | `variante`: `ohne_halbieren` (no halving) |
| Golf | `golf` | Hole n = number n; last dart counts (treble 1, double 2, single 3, miss 5); fewest strokes win | `runden`: 9 or 18 holes |
| Baseball | `baseball` | Nine innings, inning n = number n; single 1, double 2, treble 3 runs | – |
| Round the World | `rtw` | 1 to 20, then bull; every hit scores its points; first to hit the bull wins | `variante`: `auf` (up), `ab` (down), `zufall` (random order) |
| Gotcha | `gotcha` | Everyone counts up from 0; land exactly on another player's score and they go back to 0; hit the target exactly to win | `zielwert` (101–1001, default 301); `variante`: `straight`, `double`, `master` (check-out) |
| Nine Lives | `nine_lives` | 1 to 20 in order; a visit without a hit on your number costs a life | `leben` (default 3) |
| Football | `football` | Hit the bull to get the ball, then every double is a goal; first to N goals wins | `zielwert` (goals, default 10) |
| Scram | `scram` | Two players: the stopper closes 20–15 and bull, the scorer scores on everything still open; then the roles swap | – |

Points games (Count-Up, Shanghai, Halve-It, Bermuda, Golf, Baseball) that end in a tie get extra rounds, up to five.
Every game can be played as first to N legs.

#### Without cameras: tap or type

While the board is offline the game card shows a **keypad** instead of the board by itself; when the board is back online the camera image returns. Above the keypad you choose how to enter:

- **Keys**: tap Double or Triple, then the number (1–20), or 25, Bull or Miss.
- **Total** (X01 only): type the points of the whole visit, e.g. `140`, and press OK.
- **Board**: tap the spot on the drawn board (outside the double ring = miss).
- **Camera** (only while the board is online): back to the camera image.

Your choice of Keys/Total/Board is remembered per device. **Tap the board** under the camera image switches to tapping while the board is online. On a keyboard type `T20`, `D16`, `S5`, `25`, `50` (or `B`) or `0` (or `M`) and press Enter; Enter alone finishes the visit, Backspace undoes the last dart.


#### Voice (Assist)

The integration registers sentences in German, English and Russian, nothing to set up. They also work with an AI conversation agent, because sentence triggers are checked first.

| Command | Examples |
|---------|----------|
| Score | "Wie steht es beim Darts", "Who is winning at darts", "Какой счёт в дартс" |
| Ranking | "Wer ist der beste beim Darts", "Darts ranking", "Кто лучший в дартс" |
| Start / rematch | "Starte Darts 501", "Starte Darts Cricket", "Start a darts rematch", "Начни дартс шанхай" |
| Next tournament match | "Nächstes Darts Match", "Next darts match" |
| Undo / cancel | "Darts rückgängig", "Darts Spiel abbrechen", "Cancel the darts game" |
| Enter a score (X01) | "Alex hat 140", "Darts 60", "Sam scored 100", "Alex 0" – for the player whose turn it is; a checkout is counted with a double |

#### Tournament

The lobby offers **Single game** and **Tournament** with four formats: **Knockout**, **Double KO**, **Groups + KO** and **League**. Teams and handicap work in every format. Knockout is for 3–32 players (bots too): a bracket with byes for the top seeds, every match played with the same game and settings. The card shows the round above the match ("Semi-final · Match 1 of 2"), the bracket after each match with a button for the next one, and a champion celebration at the end. Undo after a match takes its result back. The tournament is stored, so it survives restarts; it can be cancelled any time. The event `tournament_won` fires with the champion.

**League** (3–10 players): everyone plays everyone once. The card shows the table (played, wins, points, legs) and all matches; a win gives 2 points, then the leg difference counts.

**Double KO** (3–16 players): a loss in the winners bracket moves you to the losers bracket, the second loss ends the tournament. The winner of the losers bracket meets the winners-bracket champion in the grand final and has to win twice (a decider is played only if needed).

**Groups + KO** (6–32 players): 2 groups (up to 11 players), 4 (up to 23) or 8, filled by seeding. Everyone plays everyone in the group, the best two of each group go to the knockout stage, and two players of the same group do not meet in its first round. The card shows the group tables, the matches of the group being played, and the knockout bracket with placeholders such as "1 A" until the groups are done.


#### TV

Open **DartNest → TV** (or the **Settings** card → TV). The card shows a live preview of the TV screen.

- **Which TV?** lists the TVs Home Assistant knows: Fire TV and Android TV from the **Android Debug Bridge** integration, Google TV from **Android TV Remote**, Chromecast and TVs with Chromecast built-in from **Google Cast**. Tick one or more.
- **Show on TV** switches the TV on and opens the page; the button next to it takes it off again. The game card has the same TV button at the top once a TV is chosen.
- **Show by itself when a game starts**: the TV opens the scoreboard at every new game.
- **Show the dartboard**: the board appears next to the score with the darts of the current visit. **Camera 1–3** shows the live image of that camera, straightened with the calibration (coloured rings mark the darts, so the real ones stay visible); **Drawn** shows the drawn board. While the board is off or not detecting, the TV shows the drawn board and goes back to the camera by itself. The game card has a button at the top to switch the dartboard on the TV on or off during a game.
- **Link for any browser**: the page works on every screen in your home network (smart TV browser, old tablet, PC). It needs no login, so the link contains a secret key; **New link** makes a new one and the old one stops working.

The page shows the players with rest, legs and sets, average, last visit and checkout, the current visit dart by dart, 180, bust and leg effects, the bull-off and the result. All game modes work (Cricket with marks, teams with the member who throws). Between games: clock, date, ranking and the last games. Fire TV opens the page in the **Silk browser** (install it from the Amazon app store if it is missing; if it was switched off, the card says so – switch it on under *Settings → Applications → Manage installed applications → Silk Browser*).

#### Stream overlay

The TV card has a section **Stream overlay (OBS, Streamlabs)** with its own link (same secret key as the TV page). In OBS or Streamlabs add a source → **Browser**, paste the link, size **1920 × 1080**. The background is transparent: a compact scoreboard sits at the bottom left (players, rest, legs/sets, the current visit), and highlight replays appear at the top right. Bull-off and the result are shown too; between games the overlay is empty.

#### Highlights

Open **DartNest → Highlights** (or the **Settings** card → Highlights).

- **Record highlights**: while a game runs and the board detects, DartNest keeps the last seconds of the chosen **camera** (1–3). At a highlight it saves about 8 s before and 1.5 s after the dart as an MP4, straightened with the calibration (720 × 720; without calibration the plain camera image).
- **When**: 180, finish 100+ and match dart are on by default; leg won, nine-darter, 140+, every finish, bullseye and three in a bed can be added. One clip per visit, named after the best highlight.
- **Replay on the TV and the overlay**: the new clip plays once right after the effect.
- Tap a clip to play it, **Download** saves the MP4, **Delete** (tap twice) removes it. **Delete all clips** clears the list. The newest 30 are kept (`anzahl` up to 200); files are in **Media → dartnest/clips**.
- The game card has a button to save the last seconds by hand.

Needs ffmpeg, which every Home Assistant installation has.

#### Pixel display (AWTRIX 3, PixelIt)

Open **DartNest → Pixel display** (or the **Settings** card → Pixel display).

- **Add display**: type the IP address (AWTRIX shows it at start and in its menu under *Network*; otherwise look in your router). DartNest asks the display what it is (AWTRIX 3: `/api/stats`, PixelIt: `/api/matrixinfo`) and greets you with *DARTNEST*. Up to 6 displays.
- **Show the score**: while a game runs the display shows the name and the rest of the player at the oche (Cricket and other games: their big number, as on the TV), live with every dart. On AWTRIX it is its own app *dartnest* that DartNest switches to; it disappears by itself 15 minutes after the last update, so nothing stays behind if Home Assistant is off. PixelIt shows the text and goes back to its clock after the game.
- **Effects**: 180 (rainbow), checkout, high finish, 140+, bust, leg, set, nine-darter, bullseye and the winner flash for 5 seconds; one effect per visit, the most important one.
- After the game the winner stays for a minute, then the display is given back.
- **Test** greets on that display, **Remove** (tap twice) gives it back and removes it. The dot shows whether it answered the last time.

The card shows a live preview of the matrix. Everything runs over the local HTTP API of the clock; the **Awtrix display** blueprint (MQTT) below still works if you prefer it.

#### Caller

Open **DartNest → Caller**. The card goes from top to bottom in three steps; the big **Listen to a sample** button at the top plays an example visit ("140 · <player>, you require 92") at any time.

1. **Where should it play?** – **On this device** plays the announcements, walk-on songs and game sounds on the phone or tablet you are holding, while a game card is open (set per device; the speaker button of the game card switches the same). **On speakers** announces in Home Assistant itself, also with no dashboard open – tick one or more speakers.
2. **Which voice?** – pick one row: the normal voice (any text-to-speech of Home Assistant, e.g. Piper or Google Translate) or a sound pack. Each pack row shows how many sounds it has and what is missing. The ⋮ button of a pack opens its menu: use, make missing sounds, stop, delete. Deleting always asks once more, shows how many sounds go and cannot be done by a single tap.
3. **What should it announce?** – **scores** of every visit in every game mode, **"you require …"** (X01), **game shot** for leg, set and match, **specials** (nine-darter, Shanghai, Killer, tournament win) and **"Game on"**.

- **New championship pack** (with a Google AI voice): opens a window that explains what happens, lists the speakers (Fenrir, Orus, Puck …) with a short description and a **Sample** button each, and marks the ones that already have a pack. **Make pack** speaks every score, "you require", game shot, leg, set, match and your player names once and saves them as the pack "Meisterschaft <speaker>". A visit like "140 · Ben, you require 100" is then joined from these sounds and plays at once. A free Google AI key allows 100 sounds a day, so a full pack (about 180 sounds) takes two days: at the daily limit the pack waits and **continues by itself** a few hours later, also after a restart – nothing to tap. **Stop** in the pack menu ends that. New players: **Make missing sounds** in the pack menu. Sentences that are not in the pack are spoken live by the same speaker. Scores are spoken as words in the language of Home Assistant ("Einhundertvierzig!"), and when Home Assistant has speech recognition (e.g. Home Assistant Cloud) every score sound is **listened to** right after it is made: a sound that says the wrong number is spoken again. Packs made before 1.23 are checked once by themselves; **Check the sounds** in the pack menu does it again.
- **Own sound packs**: Media → My media → `autodarts` → `caller` → new folder, upload files named `180.mp3`, `140.mp3`, `bust.mp3`, `leg.mp3`, `set.mp3`, `match.mp3`, `game_on.mp3`, `nine.mp3` … The pack appears in step 2; whatever it does not have is spoken. Packs from 1.19 where the voice also read out a style direction are repaired with `autodarts.ansager_pack_pruefen`.
- **Walk-on songs**: upload music to Media → My media → `autodarts` → `walkon` and pick a song per player in the card. At the start of a game each player is introduced with their song (5–60 seconds), then "Game on".

Alexa/Echo speakers that support announcements get them as an announcement, so music keeps playing.

#### Aim map

On the players card, **Hit map → Aim** shows for every spot of the board how many points the player gets per visit when aiming there, calculated from their own average and spread. The white ring is the best aim point; the text compares it with T20.

#### Statistics and badges

The players card shows for every player: rating (Elo, also against bots), streak of days played, X01 key figures, a **hit map** of all fields (or the darts as dots, where the board detected a position) with the most hit fields, the **trend** of the X01 average over the last games, **badges** in bronze, silver and gold (180s, 100+ visits, high finish, short leg, best average, wins, games, darts, days in a row, nine marks, Shanghai, hole in one, allrounder) and the **head to head** record against every other player. A ranking by rating and a CSV export of all statistics are below the players. The game card shows the last visits of everybody next to the board. Statistics of Cricket, training and party games are kept per game (games, wins, best result; Cricket: best MPR) and shown on the players card.

#### X01

The game runs completely inside Home Assistant and is stored in `.storage/autodarts.spiel`, so it survives restarts.

- **Players**: up to 8 per game, any mix of people and bots. Bots throw with a realistic scatter for the chosen average (20–120).
- **Modes**: start value 101, 170, 301, 501, 701, 901; check-in and check-out `straight`, `double` or `master`; first to N legs or N sets of M legs.
- **Bull-off**: closest dart to the bull starts; ties throw again.
- **Teams**: tap **Teams** in the player list – players 1 + 2, 3 + 4 … form a team and throw in turn (works in every game and in tournaments). The card shows who of the team throws next. Team games do not count in personal statistics.
- **Handicap**: own start value per player (or team), set with − / + next to the name. Under *More settings*.
- **50/50 bull**: the outer bull counts 50 like the bullseye (and finishes like it). Under *More settings*.
- **Round limit**: after 10, 15 or 20 visits the leg goes to the lowest rest; on a tie the player who threw first in the leg. Under *More settings*.
- **Darts from the board** are counted automatically. Pulling the darts finishes the visit. Without the board (or for corrections) darts can be entered by hand.
- **Checkout suggestions** for up to three darts, respecting the check-out mode.
- **Statistics** are added to each player when a game ends; undo after the end takes them back again.

</details>

<details>
<summary><b>Light effects</b></summary>

Let your lights celebrate with you – no YAML needed.

1. Open **DartNest → Light effects** in the sidebar (or add the card **DartNest Light effects** to a dashboard).
2. Tap **New light effect**, choose the event (180, 140+, bust, checkout, leg won, match won, tournament won …), the effect (**colour, blink, flash, pulse, heartbeat, strobe, fade out, two colours, rainbow, rainbow wave, confetti, chaser, sparkle, police, fire, thunderstorm, light effect, WLED preset**), colour, brightness and duration, and tick the lights.
3. Tap **Test** to see it, then **Save**.

Effects run in Home Assistant itself, also when no dashboard is open. Afterwards every light goes back to exactly how it was (on/off, brightness, colour). A new effect on the same light takes over smoothly. Colour lights show the colour, other lights just light up. The rules are stored by the integration and can also be set with the action `autodarts.lichteffekte_setzen`.

#### WLED and lights with their own effects

- **Light effect** uses the effects built into a light – e.g. WLED *Fireworks*, *Chase*, *Twinkle* or the Hue effects. Only lights that have effects are offered, and the list shows the effects of the ticked lights. For WLED, **speed** and **intensity** sliders appear.
- **WLED preset** plays a preset you saved in WLED (e.g. a "Champion" animation for a match win). Only WLED lights are offered.
- Add WLED as usual under **Settings → Devices & services → WLED**; the strip shows up in the editor by itself. Afterwards the light, its effect, speed and intensity go back to how they were.

<p align="center"><img src="https://raw.githubusercontent.com/Wadim-dev/DartNest_ha/main/docs/images/wled.png" alt="WLED preset" width="700"></p>

</details>

<details>
<summary><b>Blueprints (one-click automations)</b></summary>

Ready-made automations. Click the button, confirm in Home Assistant, then fill in the form (Settings → Automations → Blueprints).

| Blueprint | What it does | |
|---|---|---|
| **Awtrix display** | Shows 180, checkout, bust, leg won … on an Awtrix 3 clock (Ulanzi TC001) via MQTT, rainbow for a 180. Not needed any more: the **Pixel display** card does this and shows the score too. | [![Import blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2FWadim-dev%2FDartNest_ha%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fautodarts%2Fawtrix.yaml) |
| **Caller on a speaker** | Announces the events on any speaker with text to speech ("One hundred and eighty!"). Sentences can be changed in the form. | [![Import blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2FWadim-dev%2FDartNest_ha%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fautodarts%2Fcaller.yaml) |
| **Push on wins** | Push notification to your phone for match wins, tournament wins, nine-darters … | [![Import blueprint](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2FWadim-dev%2FDartNest_ha%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Fautodarts%2Fnotify.yaml) |

</details>

<details>
<summary><b>Card options for your own dashboards</b></summary>


All options are optional. Entities of the integration are found automatically.

```yaml
type: custom:autodarts-overview-card
game_path: /dashboard-darts/game        # shortcut buttons (shown only when set)
manager_path: /dashboard-darts/manager
manager_label: Settings                 # own text and icon for that button
manager_icon: mdi:cog
players_path: /dashboard-darts/players
power_on: script.dartboard_on           # power button: script, switch, button or automation
power_off: script.dartboard_off
power_switch: switch.dartboard_plug     # smart plug, used for the "starting / shutting down" scene
power_sensor: sensor.dartboard_plug_power
pc_online: binary_sensor.dartboard_pc   # e.g. a ping or MQTT sensor of the board PC
info:                                   # small text in the scene
  - entity: sensor.darts_today
    name: Darts today
details:                                # line under the live darts
  - entity: input_number.highest_visit_today
    name: Highest today
```

**Tile** – the same as one compact row with the board scene behind it (live darts, status colour, running game). Tap opens a window that slides up from the bottom with the overview card, today's values and your own cards. Tapping a value inside opens a small sheet in the same style with the value and its last 24 hours. Close with X, the back button, tapping outside or pulling it down. The shortcut buttons (play, manager or settings, players) open their page as a second sheet over the window: DartNest reads the DartNest card of that view from your dashboard and shows it in the sheet. Pull it down, tap the back arrow or use the back button to return to the window. It takes every option of the overview card, plus:

```yaml
type: custom:autodarts-tile-card
name: Darts                             # title of the row and the window
today:                                  # values in the window under "Today"
  - entity: sensor.darts_average_today
    name: Average
    digits: 1
cards:                                  # any cards below, e.g. a statistics graph
  - type: statistics-graph
    entities: [sensor.darts_average_today]
sheets: false                           # open the pages as before instead of as sheets
```

<p align="center"><img src="https://raw.githubusercontent.com/Wadim-dev/DartNest_ha/main/docs/images/everywhere.png" alt="Tile and tile window" width="700"></p>

```yaml
type: custom:autodarts-game-card
back_path: /dashboard-darts/0           # back arrow; without it the arrow goes back in history
power_on: script.dartboard_on           # "Turn on" button when the board is off
hide_elements: ["#bottom-bar"]          # hide elements of your dashboard while the game is shown
effects: false                          # no effects and no ✨ button
```

```yaml
type: custom:autodarts-manager-card
pc_restart: button.dartboard_pc_restart # adds a "Restart PC" button
```

```yaml
type: custom:autodarts-players-card
```

```yaml
type: custom:autodarts-settings-card   # one menu: Board, Light effects, Caller, TV, Highlights, Pixel display
```

```yaml
type: custom:autodarts-tv-card         # TV settings on their own
```

```yaml
type: custom:autodarts-clips-card      # highlights: settings and clips
```

```yaml
type: custom:autodarts-pixel-card      # AWTRIX 3 / PixelIt LED clocks
```

`back_button: false` hides the back arrow on the three page cards.

</details>

<details>
<summary><b>Entities</b></summary>

All entities belong to the device **Autodarts Board**. Entity IDs below are for an English installation.

| Entity | Description |
|--------|-------------|
| `sensor.autodarts_board_connection` | `Online` / `Offline` |
| `sensor.autodarts_board_status` | Board status: `throw`, `takeout`, `calibrating`, `starting`, `stopped` … (`Offline` while off) |
| `sensor.autodarts_board_event` | Last event of the board *(disabled by default)* |
| `sensor.autodarts_board_throw_1` … `_3` | Field of dart 1–3 (`T20`, `D16`, `S25`, `D25`, `M`), attributes: points, number, multiplier, position `x`/`y`, bouncer |
| `sensor.autodarts_board_current_visit` | Points of the current visit |
| `sensor.autodarts_board_number_of_throws` | Darts on the board *(disabled by default)* |
| `binary_sensor.autodarts_board_detection_running` | Detection is running |
| `sensor.autodarts_board_game` | Local game: `idle` / `bull_off` / `running` / `finished` (shown translated), everything else as attributes (players, scores, checkout, visits, statistics) |
| `event.autodarts_board_game_event` | Fires on game events: `dart`, `triple`, `bull`, `bullseye`, `visit`, `ton`, `ton_forty`, `one_eighty`, `no_score`, `bust`, `three_in_a_bed`, `checkout`, `high_finish`, `nine_darter`, `leg_won`, `set_won`, `match_won`, and for the other games `nine_marks`, `shanghai`, `killer`, `eliminated`, `halved`, `hole_in_one`, plus `tournament_won`; attributes `player` and, depending on the event, `field`/`points` (darts), `score`/`darts`/`remaining` (visits) or `finish` (checkouts) |
| `sensor.autodarts_board_players` | Number of players, attributes with all players, statistics and recent games |
| `camera.autodarts_board_camera_1` … `_3` | Board cameras (attribute `kalibrierung` with the calibration points) |
| `camera.autodarts_board_detection_image`, `_live_image` | Detection image and live image |
| `button.autodarts_board_start_detection`, `_stop_detection`, `_reset_throws` | Controls |
| `button.autodarts_board_calibrate`, `_restart_board_software` | Configuration |
| `select.autodarts_board_camera_resolution`, `_camera_frame_rate_setting`, `_camera_standby` | Camera settings |
| `update.autodarts_board_board_software` | Board software version, install updates |
| `sensor.autodarts_board_cpu_load`, `_memory`, `_frame_rate`, `_camera_frame_rate`, `_calibration_deviation`, `_board_software` | Diagnostics |

While the board is off, connection and status show `Offline`; all other board entities are *unavailable*. The game and player sensors always stay available.

</details>

<details>
<summary><b>Actions</b></summary>

| Action | Description |
|--------|-------------|
| `autodarts.spiel_starten` | Start a game. Fields: `spiel` (see table above, default `x01`), `variante`, `zahlen`, `runden`, `leben`, `spieler` (list of player IDs, bots as `bot:55`, teams as `team:id1+id2`, up to 8), `startwert`, `einwurf`, `auswurf` (`straight`/`double`/`master`), `legs`, `sets`, `bull_off`, `bull_5050`, `max_runden` (0 = off), `handicap` (`{"<entry from spieler>": 301}`). Without fields the last settings and players are used (rematch). |
| `autodarts.spiel_abbrechen` | Cancel the running game (not counted). |
| `autodarts.turnier_starten` | Start a tournament: `turnier_modus` `ko` (3–32 `spieler`), `doppel_ko` (3–16), `gruppen` (6–32) or `liga` (3–10); same fields as `spiel_starten` (teams and handicap included), used for every match. Starts the first match. |
| `autodarts.aufnahme_eintragen` | Enter the score of a whole X01 visit (`punkte` 0–180, optional `spieler` = name of the player whose turn it is). |
| `autodarts.ansager_setzen` | Save the caller settings (`einstellungen`). The caller card does this for you. |
| `autodarts.ansager_testen` | Speak a test sentence (`text`); without text an example visit "140 · <player>, you require 92" from the chosen pack. `sprecher` plays a sample of a Google AI speaker. |
| `autodarts.ansager_pack_anhalten` | Stop making a pack; finished sounds stay and it does not continue by itself. |
| `autodarts.ansager_pack_pruefen` | Find a spoken direction at the start of the sounds of a pack (`name`) and cut it off; `reparieren: false` only reports. Originals stay in `_original`. With `anhoeren: true` every score sound is listened to (speech recognition) and wrong ones are spoken again – the button **Check the sounds** in the pack menu. |
| `autodarts.ansager_pack_loeschen` | Delete a sound pack (`name`). The caller card does this for you. |
| `autodarts.ansager_pack_erzeugen` | Make a sound pack with the chosen voice (`name`, `sprecher` for Google AI, `nur` for single sounds). The caller card does this for you. |
| `autodarts.fernseher_zeigen` | Open the scoreboard on the chosen TVs (or `geraete`). Fire TV/Android TV via the Android Debug Bridge integration (Silk browser), Google TV via Android TV Remote, Chromecast via Google Cast. |
| `autodarts.fernseher_beenden` | Take the scoreboard off the TVs (back to the home screen; Chromecast stops). |
| `autodarts.fernseher_setzen` | TV settings: `geraete` (media players), `auto` (show when a game starts), `brett` (dartboard next to the score), `ansicht` (`graphic`, `camera_1`, `camera_2`, `camera_3`), `neuer_link: true` makes a new link and the old one stops working. The TV card does this for you. |
| `autodarts.clips_setzen` | Highlight settings: `an`, `kamera` (`camera_1`–`camera_3`), `anlaesse` (`one_eighty`, `high_finish`, `match_won`, `leg_won`, `nine_darter`, `ton_forty`, `checkout`, `bullseye`, `three_in_a_bed`), `anzahl` (1–200 clips kept), `wiederholung` (replay on the TV and the overlay). The highlights card does this for you. |
| `autodarts.clip_speichern` | Save the last seconds of the board camera now (highlights must be on). |
| `autodarts.clip_loeschen` | Delete a clip (`id`) or all clips (`alle: true`). |
| `autodarts.pixel_hinzufuegen` | Add an AWTRIX 3 or PixelIt display by `adresse` (IP or host name); the type is found out; returns `{host, typ, name, version}`. |
| `autodarts.pixel_entfernen` | Remove a display (`adresse`) and give it back. |
| `autodarts.pixel_setzen` | `an` (show the score), `effekte` (180, checkout, bust, win …). The pixel display card does this for you. |
| `autodarts.pixel_testen` | Greet on one display (`adresse`) or all. |
| `autodarts.turnier_weiter` | Start the next match of the tournament. |
| `autodarts.turnier_abbrechen` | End the tournament (bracket is removed). |
| `autodarts.weiter` | Finish the current visit; missing darts count as miss. |
| `autodarts.rueckgaengig` | Undo the last dart (also after the end of a game). |
| `autodarts.wurf_aendern` | Correct, add or delete a dart: `aufnahme` (visit index, empty = current), `dart` (0–2), `feld` (`T20`, `D16`, `25`, `Bull`, `M`; empty deletes). |
| `autodarts.spieler_anlegen` | Create a player (`name`); returns `{"id": …}`. |
| `autodarts.spieler_aendern` | Rename (`name`) or delete (`loeschen: true`) a player by `id`. |
| `autodarts.lichteffekte_setzen` | Set all light effect rules at once (`regeln`: list of `ereignis`, `lichter`, `effekt`, `farbe`, `helligkeit`, `dauer`, `aktiv`). The light effects card does this for you. |
| `autodarts.lichteffekt_testen` | Play one light effect (`regel`) once without saving it. |
| `autodarts.statistik_loeschen` | Delete statistics of one player (`id`) or of all players; `verlauf: true` also clears the game history. |

Player IDs are listed in the attributes of `sensor.autodarts_board_players`. Wrong input (unknown field, no game running …) returns a clear, translated error message.

</details>

<details>
<summary><b>Automation examples</b></summary>

**Flash the lights on a 180** (easier: the [light effects card](#light-effects))

```yaml
triggers:
  - trigger: state
    entity_id: event.autodarts_board_game_event
    attribute: event_type
    to: one_eighty
actions:
  - action: light.turn_on
    target:
      entity_id: light.living_room
    data:
      flash: long
```

This triggers when the event type changes to `one_eighty`. To react to every 180, also two in a row, trigger on any state change of the entity and check the type:

```yaml
triggers:
  - trigger: state
    entity_id: event.autodarts_board_game_event
    not_from: unavailable
conditions:
  - condition: state
    entity_id: event.autodarts_board_game_event
    attribute: event_type
    state: one_eighty
```

The same works for every other moment, e.g. `match_won`, `bust` or `nine_darter`.

**Announce a 180 on your speakers**

```yaml
triggers:
  - trigger: state
    entity_id: sensor.autodarts_board_current_visit
    to: "180"
actions:
  - action: tts.speak
    target:
      entity_id: tts.home_assistant_cloud
    data:
      media_player_entity_id: media_player.living_room
      message: One hundred and eighty!
```

**Switch on the light at the board when detection starts**

```yaml
triggers:
  - trigger: state
    entity_id: binary_sensor.autodarts_board_detection_running
    to: "on"
actions:
  - action: light.turn_on
    target:
      entity_id: light.dartboard
```

**Start a 501 rematch with a button**

```yaml
actions:
  - action: autodarts.spiel_starten
```

**Start a Cricket game against a bot**

```yaml
actions:
  - action: autodarts.spiel_starten
    data:
      spiel: cricket
      variante: cut_throat
      spieler: ["a1b2c3d4", "bot:60"]
```

**Start a game against a bot**

```yaml
actions:
  - action: autodarts.spiel_starten
    data:
      spieler: ["a1b2c3d4", "bot:60"]
      startwert: 501
      auswurf: double
      legs: 3
```

**Notify the winner**

```yaml
triggers:
  - trigger: state
    entity_id: sensor.autodarts_board_game
    to: finished
actions:
  - action: notify.notify
    data:
      message: >
        {% set a = state_attr('sensor.autodarts_board_game', 'spieler') %}
        {{ a[state_attr('sensor.autodarts_board_game', 'gewinner')].name }} wins!
```

</details>

<details>
<summary><b>Use cases</b></summary>

- **Play at home without a screen:** start an X01 game from the dashboard on a tablet next to the board; scores, checkout ways and statistics update with every dart.
- **Switch the board on and off with the room:** power the board PC with a smart plug, switch it on when you enter the room and off when the board has been idle for a while.
- **Celebrate:** flash the lights on a 180, play a sound on a checkout, announce the remaining score on a speaker.
- **Keep an eye on the hardware:** get a notification when calibration drifts, a camera drops frames or a board software update is available.
- **Track progress:** long-term statistics per player, including bots as training partners.

</details>

<details>
<summary><b>Supported devices</b></summary>

| Device | Status |
|--------|--------|
| Autodarts board with **Board Manager 2.x** (local API on port 3180) | Supported, tested |
| Autodarts board with **Board Manager 1.x** | Supported (older state format is read as well) |
| Board Manager on Linux PC, mini PC, Raspberry Pi or Windows | Supported – only the network address matters |
| Other e-dartboards (Granboard, Scolia …) | Not supported |

One config entry is one board.

</details>

<details>
<summary><b>How it works</b></summary>

```
Board PC (Autodarts Board Manager, port 3180)
   │  GET /api/state every second · /api/system every 15 s · camera images on demand
   ▼
Home Assistant ── DartNest integration (board.py) ── entities, actions, local games (.storage)
   ▼
Dashboard cards (loaded automatically) · automations · voice assistants
```

Only the documented local endpoints of the Board Manager are used. The connection itself is the small typed async client `board.py` inside the integration, which uses the web session of Home Assistant. Nothing extra is installed. Camera images are only fetched while a card or the more-info dialog shows them.

</details>

<details>
<summary><b>Known limitations</b></summary>

- Games started in the Autodarts app are not imported (the Autodarts cloud is not used at all).
- The integration **polls** the Board Manager every second; there is no push connection yet.
- Camera settings depend on what the board's cameras report; some boards only offer one resolution or frame rate.
- One board per Home Assistant installation.
- The live camera stream is MJPEG from the board PC and uses its CPU while it is open.

</details>

<details>
<summary><b>Troubleshooting</b></summary>

| Problem | Solution |
|---------|----------|
| Setup says the Board Manager does not answer | Switch the board PC on, open `http://<ip>:3180` in a browser to check it, and make sure Home Assistant can reach that address. |
| Everything shows `Offline` / unavailable | The board PC is off or not reachable. The integration reconnects automatically within 30 seconds. |
| Cameras are black | Detection is stopped – press **Start**. The cameras only deliver images while detection runs. |
| Calibration grid is missing | The board is not calibrated yet, or the calibration points could not be read. Calibrate once in the Board Manager card. |
| Cards are not found | Restart Home Assistant after installing, then reload the browser (clear the app cache on phones). |
| Darts are not counted in the game | Check that `sensor.autodarts_board_throw_1` changes when you throw. Darts are ignored while a bot is throwing. |

For a bug report, download the diagnostics (**Settings → Devices & services → DartNest → three dots → Download diagnostics**). The board address and host name are removed automatically.

To get debug logs:

```yaml
logger:
  logs:
    custom_components.autodarts: debug
```

</details>

## FAQ

**Does it need the Autodarts cloud or a subscription?** No. Everything runs locally between Home Assistant and your board PC.

**Can I still use the Autodarts app?** Yes. The integration only reads the Board Manager; games in the app are not affected. The local games in Home Assistant are independent of the app.

**Can I switch the board PC off with a smart plug?** Yes, that is the intended use. Use the `power_*` options of the overview card for a power button with a nice start-up animation.

**Is my data shared?** No. Players, statistics and games stay in your Home Assistant.

## Removal

1. **Settings → Devices & services → DartNest → three dots → Delete.**
2. Delete the folder `custom_components/autodarts`, then restart Home Assistant.
3. Players, statistics and history are stored in `.storage/autodarts.spiel`; delete this file if you want to remove them too.

## Contributing

Private project, no outside contributions. The code meets all rules of the Home Assistant quality scale up to **Platinum** (see [quality_scale.yaml](custom_components/autodarts/quality_scale.yaml)). The repository runs hassfest, the test suite (98 % coverage), ruff and mypy --strict on every push.

## Legal notice

- **Unofficial.** This is a free, private, non-commercial hobby project. It is not made, endorsed, supported or reviewed by Autodarts or any manufacturer. "Autodarts" and all other product names and trademarks belong to their owners and are used here only to say which hardware this integration works with.
- **Local only.** The integration talks only to the Board Manager on your own board PC in your own network, through the same local interface its web page uses. It does not use, access, copy or change the Autodarts online services, apps, accounts or servers, does not log in anywhere and does not bypass any protection. Use of the Autodarts online services is governed by their own terms; this project does not change them.
- **Your data stays with you.** Player names, games and statistics are stored only in your Home Assistant. Nothing is sent to the author or anyone else. A voice for the caller (e.g. Google AI TTS) is chosen and connected by you, under that provider's terms.
- **No warranty, no liability.** The software is provided "as is" under the [MIT License](LICENSE), without any warranty. Use it at your own risk. Where the law does not allow liability to be excluded completely (e.g. for intent or gross negligence), liability is limited to the extent permitted by law.
- **Images.** Screenshots show demo players (Alex, Sam, Mia). Brand logos visible on boards in photos belong to their owners.

---

---

## Deutsch

<p align="center"><b>Dein Dartboard, zuhause in Home Assistant.</b><br>Spielen, zählen, feiern und jeden Dart auswerten – mit fertigen Seiten für Tablet und Handy. Für <b>Autodarts</b>-Boards, 100 % lokal, ohne YAML und ohne Code.</p>

**In drei Schritten startklar**

1. **Installieren:** oben auf den *Marketplace*-Knopf tippen, **DartNest** installieren, Home Assistant neu starten.
2. **Board bestätigen:** unter *Einstellungen → Geräte & Dienste* erscheint **Autodarts Board gefunden** – *Hinzufügen* tippen. (Nicht gefunden? *Integration hinzufügen → DartNest* und die IP-Adresse des Board-PCs eintragen, Port 3180.)
3. **Spielen:** in der Seitenleiste **DartNest** öffnen. Fertig.

**Was drin ist**

- **Spielen:** 29 Spiele: X01, 8 Cricket-Spiele (u. a. Tactics, Verdeckt, Wild Mouse, Mickey Mouse), 8 Trainings (u. a. Catch 40, JDC, Checkout-Training) und 12 Partyspiele (u. a. Gotcha, Fußball, Scram, Nine Lives, Bermuda) für 1–8 Spieler, Bots und 2er-Teams, mit Regeltext, Ziel auf der Scheibe, Korrektur per Antippen und Bull-Off. Ohne Kameras erscheint von selbst ein Tastenfeld.
- **Feiern:** Stadion-Effekte bei 180, Checkout und Matchgewinn; Ansager in allen Spielarten mit Einlaufmusik je Spieler über Lautsprecher, Handy oder beides, mit Meisterschafts-Pack (Bühnen-Ansager-Stimme per Knopfdruck, jeder Punkte-Ton per Spracherkennung geprüft) oder eigenen Tönen; 18 Lichteffekte plus WLED-Effekte und -Presets per Klick.
- **Besser werden:** Average, First 9, Checkout-Quote, Wertung, Trend, Abzeichen, direkter Vergleich, Rangliste und die **Zielhilfe** – wo du mit deiner Streuung am meisten triffst.
- **Turniere:** K.-o. (3–32 Spieler), Doppel-K.-o. mit Verliererrunde (3–16), Gruppen + K.-o. (6–32) oder Liga (3–10), auch als 2er-Teams oder mit Handicap.
- **Fernseher:** Spielstand groß auf Fire TV, Google TV oder Chromecast, live mit jedem Dart, auf Wunsch mit deiner Dartscheibe live aus der Kamera daneben; zwischen den Spielen Uhr, Rangliste und letzte Spiele. *DartNest → Fernseher*, Fernseher wählen, **Auf dem Fernseher zeigen** – oder von selbst bei jedem Spielstart.
- **Stream und Highlights:** Overlay-Link aus der Fernseher-Karte als Browser-Quelle in OBS oder Streamlabs – durchsichtiger Spielstand über deinem Kamerabild. **Highlights** speichert jede 180, jedes Finish ab 100 und den Match-Dart als kurzes, gerade gerücktes Video der Board-Kamera; ansehen, herunterladen oder löschen in der Karte *DartNest → Highlights*, auf Wunsch sofort als Wiederholung am Fernseher und im Overlay.
- **LED-Uhr:** AWTRIX 3 (Ulanzi TC001) oder PixelIt unter *DartNest → Pixel-Anzeige* mit der IP-Adresse hinzufügen – während des Spiels zeigt sie Name und Rest des Spielers am Oche, bei 180, Checkout, Bust und Sieg einen kurzen Effekt, danach wieder ihre eigenen Apps.
- **Board Manager in HA:** Kameras mit Kalibriernetz, Start/Stopp, Kalibrieren, Updates. Board-PC darf per Steckdose aus sein: Steckdose einmal unter *Board Manager → Steckdose des Board-PCs* wählen, dann hat jede DartNest-Seite den Ein/Aus-Knopf. Schont kleine PCs: Livebilder teilen sich eine Bildquelle (höchstens 10 Bilder/s, nur wenn jemand zusieht), Kamera-Standby wird als „Standby“ gezeigt und beim Spielstart selbst geweckt.
- **Überall:** PC, Tablet und Handy, Deutsch und Englisch, Sprachbefehle („Alex hat 140“) über Assist. Karten auch fürs eigene Dashboard: *Karte hinzufügen → „DartNest“ suchen*, z. B. die **DartNest-Kachel**: eine kompakte Zeile mit Board-Szene, Tippen öffnet ein Fenster mit allem.
- **Updates** kommen über den Marketplace unter *Einstellungen → Updates*.

**Rechtliches:** Kostenloses, privates, nicht kommerzielles Hobbyprojekt, kein offizielles Produkt von Autodarts. „Autodarts“ und andere Marken gehören ihren Inhabern und werden nur genannt, um zu sagen, mit welchen Boards DartNest funktioniert. DartNest spricht nur mit dem Board Manager im eigenen Netz, nutzt keine Online-Dienste, Konten oder Server von Autodarts und umgeht keine Schutzmaßnahmen. Spieler und Statistiken bleiben im eigenen Home Assistant. Nutzung auf eigene Gefahr, ohne Gewähr ([MIT-Lizenz](LICENSE)); die Haftung ist so weit ausgeschlossen, wie es gesetzlich zulässig ist (bei Vorsatz und grober Fahrlässigkeit nach deutschem Recht nicht).
