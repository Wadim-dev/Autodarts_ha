# Changelog

Each version lists the changes in English and German. The release notes on GitHub
and in the Home Assistant update dialog are taken from this file automatically.

## 1.20.1

- Championship pack: sounds are saved as WAV. Home Assistant gives voices as MP3 by default, so visits like "140 · Ben, you require 100" could not be joined and were spoken live instead.
- `autodarts.ansager_pack_pruefen` converts MP3 sounds of a pack to WAV (also when nothing has to be cut) and shows a few lengths and pauses in its answer.

**Deutsch**
- Meisterschafts-Pack: Töne werden als WAV gespeichert. Home Assistant liefert Stimmen standardmäßig als MP3, deshalb konnten Aufnahmen wie „140 · Ben, du brauchst 100“ nicht zusammengesetzt werden und wurden live gesprochen.
- `autodarts.ansager_pack_pruefen` wandelt MP3-Töne eines Packs in WAV um (auch wenn nichts abzuschneiden ist) und zeigt in der Antwort einige Längen und Pausen.

## 1.20.0

- Caller: scores are announced in every game mode (Cricket, Baseball, Shanghai …), not only X01.
- **Test** plays an example visit: "140 · <player>, you require 92", joined from the chosen pack.
- The style direction in front of the text is gone: Google AI read it out loud also in its short form. Live sentences now use the speaker of the chosen championship pack, so the voice does not change.
- New action `autodarts.ansager_pack_pruefen`: finds a spoken direction at the start of the sounds of a pack and cuts it off at the pause after it; sounds where that does not work are made again with the next "Make championship pack". Originals stay in `_original`.

**Deutsch**
- Ansager: Punkte werden in allen Spielarten angesagt (Cricket, Baseball, Shanghai …), nicht nur bei X01.
- **Testen** spielt ein Beispiel: „140 · <Spieler>, du brauchst 92“, zusammengesetzt aus dem gewählten Pack.
- Die Stil-Anweisung vor dem Text ist weg: Google AI hat sie auch in kurzer Form mitgesprochen. Freie Sätze nutzen jetzt den Sprecher des gewählten Meisterschafts-Packs, die Stimme wechselt also nicht mehr.
- Neue Aktion `autodarts.ansager_pack_pruefen`: findet eine mitgesprochene Anweisung am Anfang der Pack-Töne und schneidet sie an der Pause danach ab; Töne, bei denen das nicht geht, werden beim nächsten „Meisterschafts-Pack erzeugen“ neu gesprochen. Originale bleiben in `_original`.

## 1.19.3

- Championship pack: the ✓ on a speaker now only shows when its pack really has sounds; tapping a speaker without sounds no longer selects an empty pack.
- A pack that got no sound (for example because the daily limit was already reached) no longer leaves an empty folder behind.

**Deutsch**
- Meisterschafts-Pack: Das ✓ am Sprecher erscheint nur noch, wenn sein Pack wirklich Töne hat; Antippen eines Sprechers ohne Töne wählt kein leeres Pack mehr aus.
- Ein Pack ohne einen einzigen Ton (z. B. weil das Tageslimit schon erreicht war) hinterlässt keinen leeren Ordner mehr.

## 1.19.2

- Championship pack: each Google AI speaker gets its own pack ("Meisterschaft Fenrir", "Meisterschaft Orus" …). Tapping a speaker that already has a pack switches to it at once; the pack just made is used right away.
- Pack making waits between sounds (Google AI allows 10 a minute) and stops cleanly at the daily limit (100 a day) with a hint to continue tomorrow.
- New button "Delete pack" and action `autodarts.ansager_pack_loeschen`.

**Deutsch**
- Meisterschafts-Pack: Jeder Google-AI-Sprecher bekommt ein eigenes Pack („Meisterschaft Fenrir“, „Meisterschaft Orus“ …). Antippen eines Sprechers mit fertigem Pack schaltet sofort um; das gerade erzeugte Pack wird gleich benutzt.
- Pack-Erzeugung wartet zwischen den Tönen (Google AI erlaubt 10 pro Minute) und hält beim Tageslimit (100 am Tag) sauber an, mit Hinweis zum Fortsetzen am nächsten Tag.
- Neuer Knopf „Pack löschen“ und Aktion `autodarts.ansager_pack_loeschen`.

## 1.19.1

- Championship pack: shorter style direction – Google AI read the long one out loud. "Make championship pack" speaks everything again after choosing another speaker (action option `neu`).

**Deutsch**
- Meisterschafts-Pack: kürzere Stil-Anweisung – Google AI hat die lange mit vorgelesen. „Meisterschafts-Pack erzeugen“ spricht nach Wahl eines anderen Sprechers alles neu (Aktions-Option `neu`).

## 1.19.0

- **Championship pack**: new button in the caller card. The chosen voice speaks every score, "you require", game shot, leg, set, match and the player names once and saves them as the pack "Meisterschaft" – with Google AI in the style of a world championship stage announcer (speaker selectable). Runs in the background, can be continued. New action `autodarts.ansager_pack_erzeugen`.
- Visits with a checkout hint ("140 · Ben, you require 100") are joined from the pack sounds instead of being spoken.
- Live sentences of a Google AI voice use the same style (switch "Live sentences in championship style").

**Deutsch**
- **Meisterschafts-Pack**: neuer Knopf in der Ansager-Karte. Die gewählte Stimme spricht alle Punkte, „du brauchst“, Game shot, Leg, Satz, Match und die Spielernamen einmal und speichert sie als Pack „Meisterschaft“ – mit Google AI im Stil eines WM-Bühnen-Ansagers (Sprecher wählbar). Läuft im Hintergrund, fortsetzbar. Neue Aktion `autodarts.ansager_pack_erzeugen`.
- Aufnahmen mit Rest-Hinweis („140 · Ben, du brauchst 100“) werden aus den Pack-Tönen zusammengesetzt statt gesprochen.
- Freie Sätze einer Google-AI-Stimme kommen im selben Stil (Schalter „Freie Sätze im WM-Stil“).

## 1.18.0

- **Caller on the phone**: the speaker button in the game card (and the new switch "On this device" in the caller card) plays the caller on this phone or tablet – same voice, sound pack and walk-on songs as on the speakers. Speakers, phone or both, freely combined. Before, the phone used the browser voice, which many phones (e.g. the Android app) do not have.

**Deutsch**
- **Ansager aufs Handy**: Der Lautsprecher-Knopf in der Spielkarte (und der neue Schalter „Auf diesem Gerät“ in der Ansager-Karte) spielt den Ansager auf diesem Handy oder Tablet – gleiche Stimme, gleiches Sound-Pack und Einlaufmusik wie auf den Lautsprechern. Lautsprecher, Handy oder beides, frei kombinierbar. Vorher nutzte das Handy die Browser-Stimme, die viele Handys (z. B. die Android-App) nicht haben.

## 1.17.0

- **Keypad** in the game card: while the board is offline a keypad replaces the drawn board by itself (Double/Triple + 1–20, 25, Bull, Miss); for X01 also **Total** for the whole visit. When the board is back online the camera returns. Keys, Total, Board and Camera can be switched above the keypad.

**Deutsch**
- **Tastenfeld** in der Spielkarte: Ist das Board offline, ersetzt ein Tastenfeld von selbst die gezeichnete Scheibe (Double/Triple + 1–20, 25, Bull, Daneben); bei X01 auch **Summe** für die ganze Aufnahme. Ist das Board wieder online, kommt die Kamera zurück. Über dem Tastenfeld umschaltbar: Tasten, Summe, Scheibe, Kamera.

## 1.16.1

- Overview card: new options `manager_label` and `manager_icon` give the Board Manager button its own text and icon (e.g. "Settings" for a page with Board Manager, light effects and caller).

**Deutsch**
- Übersichtskarte: neue Optionen `manager_label` und `manager_icon` geben dem Board-Manager-Knopf eigenen Text und eigenes Symbol (z. B. „Einstellungen“ für eine Seite mit Board Manager, Lichteffekten und Ansager).

## 1.16.0

- **Caller**: new card and sidebar tab. Announces scores, "you require …", game shot, specials and "Game on" on any speakers; own sound packs by upload (Media → autodarts → caller), missing sounds are spoken. Walk-on song per player at the start of a game.
- **Scores by voice**: "Alex hat 140", "Darts 60", "Sam scored 100" enters a whole X01 visit for the player whose turn it is. New action `autodarts.aufnahme_eintragen`.
- **Tournaments**: knockout now for up to 32 players, new **league** for 3–10 players (everyone against everyone, table with points and leg difference).
- **Aim map** on the players card: best aim point for the player's own average and spread.

**Deutsch**
- **Ansager**: neue Karte und neuer Reiter. Sagt Punkte, „du brauchst …“, Game shot, Besonderes und „Game on“ über beliebige Lautsprecher an; eigene Sound-Packs per Hochladen (Medien → autodarts → caller), was fehlt, spricht die Stimme. Einlaufmusik je Spieler zum Spielbeginn.
- **Punkte per Sprache**: „Alex hat 140“, „Darts 60“ trägt eine ganze X01-Aufnahme für den Spieler am Zug ein. Neue Aktion `autodarts.aufnahme_eintragen`.
- **Turniere**: K.-o. jetzt bis 32 Spieler, neu **Liga** für 3–10 Spieler (jeder gegen jeden, Tabelle mit Punkten und Leg-Differenz).
- **Zielhilfe** auf der Spielerseite: bester Zielpunkt für den eigenen Average und die eigene Streuung.

## 1.15.0

- Eleven new light effects: heartbeat, strobe, fade out, two colours, rainbow wave, confetti, chaser, sparkle, police, fire and thunderstorm. Wave, chaser, sparkle and police spread over several lights. The effect buttons are now a tidy grid.

**Deutsch**
- Elf neue Lichteffekte: Herzschlag, Stroboskop, Ausblenden, zwei Farben, Regenbogen-Welle, Konfetti, Lauflicht, Funkeln, Polizei, Feuer und Gewitter. Welle, Lauflicht, Funkeln und Polizei verteilen sich auf mehrere Lampen. Die Effekt-Knöpfe stehen jetzt ordentlich im Raster.

## 1.14.1

- Updates of the integration can now come as small patches for big files, so they arrive faster. If a patch does not fit, nothing is changed.

**Deutsch**
- Updates der Integration können jetzt bei großen Dateien als kleine Änderungen kommen und sind dadurch schneller da. Passt eine Änderung nicht, bleibt alles unverändert.

## 1.14.0

- Light effects: new effect **Light effect** uses the light's own effects (WLED *Fireworks*, *Chase* …, Hue effects) with speed and intensity for WLED.
- New effect **WLED preset** plays a preset saved in WLED.
- Afterwards effect, speed and intensity go back to how they were. The editor only offers lights that fit the chosen effect.

**Deutsch**
- Lichteffekte: neuer Effekt **Lampen-Effekt** nutzt die eigenen Effekte der Lampe (WLED *Fireworks*, *Chase* …, Hue-Effekte), bei WLED mit Tempo und Stärke.
- Neuer Effekt **WLED-Preset** spielt ein in WLED gespeichertes Preset ab.
- Danach kommen Effekt, Tempo und Stärke zurück wie vorher. Der Editor zeigt nur Lampen, die zum gewählten Effekt passen.

## 1.13.0

- Private project from now on: the board client is built into the integration (`board.py`), nothing is installed from PyPI.
- New update entity **Integration**: a new version placed in `custom_templates/autodarts_update` shows up under Settings → Updates, with release notes; installing restarts Home Assistant.
- New game event `game_started` with the players (groundwork for walk-on songs and the caller).

**Deutsch**
- Ab jetzt privates Projekt: Die Board-Verbindung steckt direkt in der Integration (`board.py`), von PyPI wird nichts mehr installiert.
- Neuer Update-Eintrag **Integration**: Eine neue Version im Ordner `custom_templates/autodarts_update` erscheint unter Einstellungen → Updates, mit Versionshinweisen; Installieren startet Home Assistant neu.
- Neues Spielereignis `game_started` mit den Spielern (Grundlage für Walk-on-Songs und den Ansager).

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
