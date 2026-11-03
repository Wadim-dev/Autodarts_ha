# Changelog

Each version lists the changes in English and German. The release notes on GitHub
and in the Home Assistant update dialog are taken from this file automatically.

## 1.12.0

- New sidebar entry **Autodarts** with all cards as tabs (board, play, players, light effects, Board Manager). Nothing to set up.
- Works on the phone too (menu button on narrow screens).

**Deutsch**
- Neuer Eintrag **Autodarts** in der Seitenleiste mit allen Karten als Reiter (Board, Spielen, Spieler, Lichteffekte, Board Manager). Nichts einzurichten.
- Funktioniert auch am Handy (Menüknopf bei schmalem Bildschirm).

## 1.11.0

- Light effects on game events: colour, blink, flash, rainbow or pulse on any lights, set up by click in the new lights card. Afterwards every light goes back to how it was.
- Blueprints with import button: Awtrix display, caller on a speaker, push notification to the phone.
- New actions `lichteffekte_setzen` and `lichteffekt_testen`.

**Deutsch**
- Lichteffekte bei Spielereignissen: Farbe, Blinken, Blitz, Regenbogen oder Pulsieren auf beliebigen Lampen, per Klick in der neuen Lichter-Karte eingerichtet. Danach sind alle Lampen wieder wie vorher.
- Blueprints mit Import-Knopf: Awtrix-Anzeige, Ansager über Lautsprecher, Push aufs Handy.
- Neue Aktionen `lichteffekte_setzen` und `lichteffekt_testen`.

## 1.10.0

- Platinum quality scale: the board connection is now the typed async library [aioautodarts](https://pypi.org/project/aioautodarts/) and uses Home Assistant's shared web session.
- Board errors are still shown as translated messages.

**Deutsch**
- Platin-Stufe: Die Board-Verbindung steckt jetzt in der eigenen Bibliothek aioautodarts und nutzt die gemeinsame Web-Sitzung von Home Assistant.
- Board-Fehler werden weiter übersetzt angezeigt.

## 1.9.2

- Fix: setup failed on Home Assistant 2026.11 with Python 3.14 (Assist sentences). The voice part can no longer block the integration.

**Deutsch**
- Behoben: Einrichtung schlug unter Home Assistant 2026.11 mit Python 3.14 fehl (Assist-Sätze). Der Sprachteil kann die Integration nicht mehr blockieren.

## 1.9.1

- Assist sentences work with the changed conversation API of Home Assistant 2026.11.

**Deutsch**
- Assist-Sätze laufen mit der geänderten Schnittstelle von Home Assistant 2026.11.

## 1.9.0

- Tap input on the drawn board or keyboard input (T20 + Enter) for boards without cameras; on by itself while the board is offline.
- Assist sentences in German, English and Russian: score, ranking, start, next match, undo, cancel.

**Deutsch**
- Eingabe per Tippen auf die gezeichnete Scheibe oder Tastatur (T20 + Enter) für Boards ohne Kameras; schaltet sich ein, solange das Board offline ist.
- Sprachbefehle über Assist auf Deutsch, Englisch und Russisch: Punktestand, Rangliste, Start, nächstes Match, Rückgängig, Abbrechen.

## 1.8.0

- Knockout tournament for 3–16 players: bracket with byes, round banner, next-match button, champion celebration, undo-safe results.
- New event `tournament_won` and actions `turnier_starten`, `turnier_weiter`, `turnier_abbrechen`.

**Deutsch**
- K.-o.-Turnier für 3–16 Spieler: Turnierbaum mit Freilosen, Runden-Banner, Knopf „Nächstes Match“, Siegerfeier, Ergebnisse sicher beim Rückgängig.
- Neues Ereignis `tournament_won` und Aktionen `turnier_starten`, `turnier_weiter`, `turnier_abbrechen`.

## 1.7.0

- Player profiles: hit map, X01 average trend, Elo rating, streak of days, head to head, bronze/silver/gold badges, ranking and CSV export.
- The game card shows the last visits next to the board. Bots up to average 120.

**Deutsch**
- Spielerprofile: Trefferbild, Average-Verlauf, Elo-Wertung, Tage-Serie, direkter Vergleich, Abzeichen in Bronze/Silber/Gold, Rangliste und CSV-Export.
- Die Spielkarte zeigt die letzten Aufnahmen neben der Scheibe. Bots bis Average 120.

## 1.6.0

- New games: Cricket (standard, cut-throat, no score), Around the Clock, Bob's 27, doubles, 121 checkout, highscore, Shanghai, Killer, Halve-It, Golf, Baseball.
- Up to 8 players and bots in every game, short rule text, cricket board, target marked on the dartboard, statistics per game.

**Deutsch**
- Neue Spiele: Cricket (Standard, Cut-Throat, ohne Punkte), Around the Clock, Bob's 27, Doppel, 121 Checkout, Highscore, Shanghai, Killer, Halve-It, Golf, Baseball.
- Bis 8 Spieler und Bots in jedem Spiel, kurze Regeln, Cricket-Tafel, Ziel auf der Scheibe markiert, Statistik je Spiel.

## 1.5.0

- Event entity for darts, 180, bust, checkouts, legs, sets and the match – usable in automations.
- Effects for these moments in the game card (can be switched off per device).

**Deutsch**
- Ereignis-Entität für Darts, 180, Bust, Checkouts, Legs, Sets und Match – nutzbar in Automationen.
- Effekte für diese Momente in der Spielkarte (pro Gerät abschaltbar).

## 1.4.0

- Gold quality scale: board discovery via zeroconf, follows a new board address, reconfigure flow, diagnostics download, icons and device classes.

**Deutsch**
- Gold-Stufe: Board wird im Netz gefunden, folgt einer neuen Adresse, Adresse nachträglich änderbar, Diagnose-Download, Symbole und Geräteklassen.

## 1.3.0

- Four dashboard cards (overview, game, Board Manager, players) included and loaded automatically.
- Entity names translated (English/German).

**Deutsch**
- Vier Dashboard-Karten (Übersicht, Spiel, Board Manager, Spieler) dabei und automatisch geladen.
- Entitätsnamen übersetzt (Englisch/Deutsch).
