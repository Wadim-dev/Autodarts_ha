# Changelog

Each version lists the changes in English and German. The release notes on GitHub
and in the Home Assistant update dialog are taken from this file automatically.

## 1.32.1

- **No more flicker in windows.** Some Home Assistant cards finish loading a moment after a window opens, for example the 24-hour history in the info window or cards added with `cards`. They used to send a rebuild signal to the whole tile, so the window was drawn again and flickered. Now only that card is rebuilt. Cards inside windows also skip the glass blur, because the window already has one. That makes scrolling smoother and saves battery.

**Deutsch**

- **Kein Flackern mehr in Fenstern.** Manche Home-Assistant-Karten laden kurz nach dem Öffnen eines Fensters nach, zum Beispiel der 24-Stunden-Verlauf im Infofenster oder Karten aus `cards`. Sie haben dabei die ganze Kachel neu aufbauen lassen, das Fenster wurde neu gezeichnet und flackerte. Jetzt wird nur diese eine Karte neu gebaut. Außerdem bekommen Karten im Fenster keinen eigenen Milchglas-Effekt mehr, das Fenster hat schon einen. Das Scrollen wird flüssiger und schont den Akku.

## 1.32.0

- **Pages slide up over the window.** In the tile window, **Play**, **Settings** (or Manager) and **Players** no longer leave for another page. The page slides up as a second sheet over the window. Pull it down, tap the back arrow or use the back button, and the darts window is there again. DartNest takes the card of that page from your dashboard, so nothing needs to be set up. `sheets: false` keeps the old behaviour.

**Deutsch**

- **Seiten gleiten über das Fenster.** Im Kachel-Fenster wechseln **Spielen**, **Einstellungen** (bzw. Manager) und **Spieler** nicht mehr auf eine andere Seite. Die Seite gleitet als zweites Fenster über das Darts-Fenster. Nach unten ziehen, Zurück-Pfeil oder Zurück-Taste, und das Darts-Fenster ist wieder zu sehen. DartNest nimmt die Karte dieser Seite aus dem Dashboard, einrichten muss man nichts. `sheets: false` behält das alte Verhalten.

## 1.31.1

- **Smoother window.** On phones the window sometimes appeared at once and then jumped, instead of sliding up. The browser moved focus to the close button and scrolled the window with it; the window now takes focus itself, so it slides up smoothly.

**Deutsch**

- **Flüssigeres Fenster.** Am Handy war das Fenster manchmal sofort da und ruckte dann, statt hochzugleiten. Der Browser setzte den Fokus auf den Schließen-Knopf und schob das Fenster dabei mit; jetzt nimmt das Fenster den Fokus selbst und gleitet sauber hoch.

## 1.31.0

- **The tile window slides up.** Tapping the DartNest tile now lets its window slide up from the bottom, and closing it (X, back button, Esc, tapping outside, pulling down) lets it slide back down.
- **Details in the same style.** Inside the window, tapping the board scene or a dart value no longer closes the window for the Home Assistant more-info dialog. A small sheet in the DartNest style slides up instead, with the value, since when and its last 24 hours. Back or X returns to the window.

**Deutsch**

- **Das Kachel-Fenster gleitet hoch.** Tippen auf die DartNest-Kachel lässt das Fenster jetzt von unten hochgleiten, beim Schließen (X, Zurück-Taste, Esc, daneben tippen, nach unten ziehen) gleitet es wieder nach unten weg.
- **Details im selben Stil.** Im Fenster schließt das Antippen der Board-Szene oder eines Wurfs das Fenster nicht mehr für das Home-Assistant-Infofenster. Stattdessen gleitet ein kleines Fenster im DartNest-Stil hoch, mit dem Wert, seit wann und den letzten 24 Stunden. Zurück oder X führt wieder ins Fenster.

## 1.30.1

- **Lighter on the board PC.** Live views no longer open their own camera stream each. DartNest now asks the board for single images only while somebody watches – a card, the TV page or the highlight recorder – at most 10 per second, and every viewer gets the same image. Before, each live view made the board prepare 30 images per second. A busy board gets more time between images.
- **Camera standby is shown as standby.** When the board stops the detection after the standby time without a throw, the cards show **Standby – wakes up with the next game** instead of "Detection stopped". During a game that is still being played (last change less than 45 minutes ago), DartNest wakes the detection by itself after a pause. A stop with the **Stop** button stays a stop.
- **CPU as share of the whole PC.** The board counts every core up to 100 %, so a 4-core PC showed up to 400 %. The CPU sensor now shows the share of the whole PC (for example 37 % instead of 148 %).

**Deutsch**

- **Schonender für den Board-PC.** Livebilder öffnen nicht mehr jeweils einen eigenen Kamerastrom. DartNest holt einzelne Bilder vom Board nur, solange jemand zusieht – eine Karte, die Fernseher-Seite oder die Highlight-Aufnahme –, höchstens 10 pro Sekunde, und alle Zuschauer bekommen dasselbe Bild. Vorher musste das Board für jedes Livebild 30 Bilder pro Sekunde aufbereiten. Ein ausgelastetes Board bekommt mehr Zeit zwischen den Bildern.
- **Kamera-Standby wird als Standby gezeigt.** Stoppt das Board die Erkennung nach der Standby-Zeit ohne Wurf, zeigen die Karten **Standby – wacht beim nächsten Spiel auf** statt „Erkennung gestoppt“. Während eines Spiels, das noch gespielt wird (letzte Änderung vor weniger als 45 Minuten), weckt DartNest die Erkennung nach einer Pause selbst. Ein Stopp mit dem Knopf **Stop** bleibt ein Stopp.
- **CPU als Anteil am ganzen PC.** Das Board zählt jeden Kern bis 100 %, ein PC mit 4 Kernen zeigte also bis zu 400 %. Der CPU-Sensor zeigt jetzt den Anteil am ganzen PC (zum Beispiel 37 % statt 148 %).

## 1.30.0

- **Score on the LED clock.** New tab **DartNest → Pixel display** for **AWTRIX 3** (Ulanzi TC001 and self-built) and **PixelIt**: tap **Add display**, type the IP address – DartNest finds out which one it is and greets with DARTNEST. While a game runs the clock shows the name and the rest of the player at the oche, live with every dart. 180 (rainbow), checkout, bust, leg and the win flash as a short effect. After the game the winner stays for a minute, then the clock goes back to its own apps. Local HTTP, no MQTT or automation needed.
- The card shows a live preview of the matrix, the displays with online dot, **Test** and **Remove**. Settings menu card: new button **Pixel display**. New actions `autodarts.pixel_hinzufuegen`, `pixel_entfernen`, `pixel_setzen`, `pixel_testen`.

**Deutsch**

- **Spielstand auf der LED-Uhr.** Neuer Reiter **DartNest → Pixel-Anzeige** für **AWTRIX 3** (Ulanzi TC001 und Eigenbau) und **PixelIt**: **Anzeige hinzufügen** tippen, IP-Adresse eingeben – DartNest erkennt selbst, welche es ist, und grüßt mit DARTNEST. Während eines Spiels zeigt die Uhr Name und Rest des Spielers am Oche, live mit jedem Dart. 180 (Regenbogen), Checkout, Bust, Leg und der Sieg blinken als kurzer Effekt. Nach dem Spiel bleibt der Sieger eine Minute, danach zeigt die Uhr wieder ihre eigenen Apps. Lokal über HTTP, ohne MQTT oder Automation.
- Die Karte zeigt eine Live-Vorschau der Matrix, die Anzeigen mit Online-Punkt, **Test** und **Entfernen**. Einstellungs-Menükarte: neuer Knopf **Pixel-Anzeige**. Neue Aktionen `autodarts.pixel_hinzufuegen`, `pixel_entfernen`, `pixel_setzen`, `pixel_testen`.

## 1.29.1

- A busy board no longer drops out: when the board PC is at full load (for example at the start of a game) and misses an answer, DartNest now asks again right away and only counts the board as off after three missed answers in a row. Before, a single late answer showed the board as off for 30 seconds with black cameras.
- Highlights record with less load on the board PC (5 images per second, and slower while the board answers late).
- Nothing fills up: no new clip when less than 1 GB is free on the disk, leftover clip files that are not in the list are removed at start, and the clip list and TV settings are no longer written into the history database.

**Deutsch**

- Ein ausgelastetes Board fällt nicht mehr aus: Ist der Board-PC voll ausgelastet (zum Beispiel beim Spielstart) und verpasst eine Antwort, fragt DartNest sofort nach und wertet das Board erst nach drei verpassten Antworten in Folge als aus. Vorher zeigte eine einzige späte Antwort das Board 30 Sekunden lang als aus, mit schwarzen Kameras.
- Highlights nehmen mit weniger Last für den Board-PC auf (5 Bilder pro Sekunde, langsamer, solange das Board spät antwortet).
- Nichts läuft voll: kein neuer Clip, wenn weniger als 1 GB frei ist; übrig gebliebene Clip-Dateien, die nicht in der Liste stehen, werden beim Start entfernt; Clip-Liste und Fernseher-Einstellungen landen nicht mehr in der Verlaufsdatenbank.

## 1.29.0

- **Highlights.** New tab **DartNest → Highlights**: switch on **Record highlights** and every 180, finish of 100 or more and the match dart is saved as a short video (about 8 s before and 1.5 s after the dart) from the board camera, straightened with the calibration. Choose the camera and more occasions (leg won, nine-darter, 140+, every finish, bullseye, three in a bed). Clips appear as tiles: tap to play, download or delete; the newest 30 are kept, the files are also in **Media → dartnest/clips**.
- **Instant replay:** right after the effect the new clip plays once on the TV and in the stream overlay (can be switched off).
- **Stream overlay for OBS and Streamlabs:** the TV card has a second link – add it as a browser source (1920 × 1080). The background is see-through, a compact scoreboard sits at the bottom left, replays at the top right.
- Game card: new button to save the last seconds as a clip by hand. Settings menu card: new button **Highlights**. New actions `autodarts.clips_setzen`, `clip_speichern`, `clip_loeschen`.

**Deutsch**

- **Highlights.** Neuer Reiter **DartNest → Highlights**: **Highlights aufnehmen** einschalten, und jede 180, jedes Finish ab 100 und der Match-Dart wird als kurzes Video (etwa 8 s vor und 1,5 s nach dem Dart) der Board-Kamera gespeichert, gerade gerückt mit der Kalibrierung. Kamera und weitere Anlässe wählbar (Leg gewonnen, Neun-Darter, 140+, jedes Finish, Bullseye, Three in a Bed). Die Clips erscheinen als Kacheln: antippen zum Abspielen, Herunterladen oder Löschen; die neuesten 30 bleiben, die Dateien liegen auch unter **Medien → dartnest/clips**.
- **Sofort-Wiederholung:** Direkt nach dem Effekt läuft der neue Clip einmal am Fernseher und im Stream-Overlay (abschaltbar).
- **Stream-Overlay für OBS und Streamlabs:** Die Fernseher-Karte hat einen zweiten Link – als Browser-Quelle einfügen (1920 × 1080). Der Hintergrund ist durchsichtig, unten links ein kompakter Spielstand, oben rechts die Wiederholungen.
- Spielkarte: neuer Knopf, um die letzten Sekunden von Hand als Clip zu speichern. Einstellungs-Menükarte: neuer Knopf **Highlights**. Neue Aktionen `autodarts.clips_setzen`, `clip_speichern`, `clip_loeschen`.

## 1.28.0

- **Your dartboard on the TV.** Switch on **Show the dartboard** in the TV card: the TV shows the board next to the score, with the darts of the current visit marked. Choose **Camera 1–3** for the live camera image, straightened like in the game card (rings mark the darts, so you still see the real ones), or **Drawn** for the drawn board. While the board does not detect (off, detection stopped) the TV shows the drawn board by itself and switches back to the camera when it runs again.
- New button at the top of the game card: dartboard on the TV on or off. `autodarts.fernseher_setzen` has the new fields `brett` and `ansicht`.

**Deutsch**

- **Deine Dartscheibe auf dem Fernseher.** In der Fernseher-Karte **Dartscheibe zeigen** einschalten: Der Fernseher zeigt die Scheibe neben dem Spielstand, die Darts der aktuellen Aufnahme sind markiert. **Kamera 1–3** zeigt das Live-Bild der Kamera, gerade gerückt wie in der Spielkarte (Ringe markieren die Darts, die echten bleiben sichtbar), **Gezeichnet** die gezeichnete Scheibe. Solange das Board nicht erkennt (aus, Erkennung gestoppt), zeigt der Fernseher von selbst die gezeichnete Scheibe und schaltet zurück auf die Kamera, sobald es wieder läuft.
- Neuer Knopf oben in der Spielkarte: Dartscheibe am Fernseher an oder aus. `autodarts.fernseher_setzen` hat die neuen Felder `brett` und `ansicht`.

## 1.27.1

- Fire TV: when the Silk browser is switched off, **Show on TV** now says so and how to switch it on, instead of doing nothing. Other start problems of the TV are shown as a message too.

**Deutsch**

- Fire TV: Ist der Silk-Browser ausgeschaltet, sagt **Auf dem Fernseher zeigen** das jetzt samt Weg zum Einschalten, statt nichts zu tun. Andere Startprobleme des Fernsehers erscheinen ebenfalls als Meldung.

## 1.27.0

- **Scoreboard on the TV.** New tab **DartNest → TV**: tick your Fire TV, Google TV or Chromecast and tap **Show on TV**. The TV shows the game big and live with every dart – scores, legs and sets, average, checkout, the current visit, 180/bust/leg effects, bull-off and the result, in every game mode and with teams. Between games it shows the clock, the ranking and the last games. **Show by itself when a game starts** opens it at every new game. The page also works in any browser at home (link in the card, no login).
- **Settings menu card** (`custom:autodarts-settings-card`): one card with big buttons for Board, Light effects, Caller and TV – each opens its settings, the back arrow returns to the menu.
- TV button at the top of the game card once a TV is chosen. New actions `autodarts.fernseher_zeigen`, `fernseher_beenden`, `fernseher_setzen`.

**Deutsch**

- **Spielstand auf dem Fernseher.** Neuer Reiter **DartNest → Fernseher**: Fire TV, Google TV oder Chromecast anhaken und **Auf dem Fernseher zeigen** tippen. Der Fernseher zeigt das Spiel groß und live mit jedem Dart – Punkte, Legs und Sätze, Average, Checkout, die aktuelle Aufnahme, Effekte bei 180/Bust/Leg, Bull-Off und Ergebnis, in allen Spielarten und mit Teams. Zwischen den Spielen zeigt er Uhr, Rangliste und die letzten Spiele. **Von selbst zeigen, wenn ein Spiel startet** öffnet ihn bei jedem neuen Spiel. Die Seite geht auch in jedem Browser zu Hause (Link in der Karte, ohne Anmeldung).
- **Einstellungs-Menükarte** (`custom:autodarts-settings-card`): eine Karte mit großen Knöpfen für Board, Lichteffekte, Ansager und Fernseher – jeder öffnet seine Einstellungen, der Zurück-Pfeil führt ins Menü.
- Fernseher-Knopf oben in der Spielkarte, sobald ein Fernseher gewählt ist. Neue Aktionen `autodarts.fernseher_zeigen`, `fernseher_beenden`, `fernseher_setzen`.

## 1.26.0

- **Tournaments in four formats.** New: **Double KO** for 3–16 players (winners and losers bracket, grand final where the losers-bracket winner has to win twice) and **Groups + KO** for 6–32 players (2, 4 or 8 groups, the best two of each go on, players of the same group do not meet in the first KO round). Knockout and league stay. The lobby has **Single game / Tournament** and four format tiles with player ranges and a short rule.
- **Teams of two.** Tap **Teams** in the player list: players 1 + 2, 3 + 4 … throw in turn, in every game and in tournaments. The card and the caller name the team member whose turn it is, bots can be team members. Team games do not count in personal statistics.
- **Handicap** for X01: own start value per player or team, set with − / + next to the name.
- **50/50 bull** for X01: the outer bull counts 50 and finishes like the bullseye.
- **Round limit** for X01 (10, 15 or 20 visits): then the lowest rest wins the leg.
- New bracket views for the losers bracket, the grand final and the group stage, and the match banner shows the phase ("Losers bracket · Round 2", "Group B · Match 3 of 6", "Grand final").

**Deutsch**

- **Turniere in vier Formaten.** Neu: **Doppel-K.-o.** für 3–16 Spieler (Gewinner- und Verliererrunde, großes Finale, in dem der Sieger der Verliererrunde zweimal gewinnen muss) und **Gruppen + K.-o.** für 6–32 Spieler (2, 4 oder 8 Gruppen, die besten zwei kommen weiter, Spieler derselben Gruppe treffen in der ersten K.-o.-Runde nicht aufeinander). K.-o. und Liga bleiben. Die Neues-Spiel-Seite hat **Einzelspiel / Turnier** und vier Format-Kacheln mit Spielerzahl und kurzer Regel.
- **2er-Teams.** In der Spielerliste **Teams** antippen: Spieler 1 + 2, 3 + 4 … werfen abwechselnd, in jedem Spiel und im Turnier. Karte und Ansager nennen, wer im Team dran ist, Bots können mitspielen. Team-Spiele zählen nicht in der persönlichen Statistik.
- **Handicap** bei X01: eigener Startwert je Spieler oder Team, mit − / + neben dem Namen.
- **50/50 Bull** bei X01: Das äußere Bull zählt 50 und checkt wie das Bullseye.
- **Rundenlimit** bei X01 (10, 15 oder 20 Aufnahmen): danach gewinnt der niedrigste Rest das Leg.
- Neue Turnierbaum-Ansichten für Verliererrunde, großes Finale und Gruppenphase; das Banner über dem Match zeigt die Phase („Verliererrunde · Runde 2“, „Gruppe B · Spiel 3 von 6“, „Großes Finale“).

## 1.25.1

- The power button now also appears in the DartNest sidebar. Pick the plug of the board PC once under **Board Manager → Board PC power plug** (optionally with its power meter, a shut-down script and a "PC running" sensor); every DartNest card uses it. Cards with their own `power_on` keep it. New action `autodarts.strom_setzen`.

**Deutsch**

- Der Ein/Aus-Knopf erscheint jetzt auch in der DartNest-Seitenleiste. Die Steckdose des Board-PCs einmal unter **Board Manager → Steckdose des Board-PCs** wählen (optional mit Leistungsmesser, Herunterfahr-Skript und „PC läuft“-Sensor); alle DartNest-Karten nutzen sie. Karten mit eigenem `power_on` behalten ihre Einstellung. Neue Aktion `autodarts.strom_setzen`.

## 1.25.0

- **29 games.** New in Cricket: **Tactics** and **Hidden** numbers (six random numbers that show up when someone hits them), **Wild Mouse** (plus any double, any treble and 3 in a bed) and **Mickey Mouse** (20–12, doubles, trebles, bull). New training: **Singles**, **Checkout Training** (random finishes, the same for everyone), **Catch 40** and the **JDC Challenge**. New party games: **Bermuda**, **Round the World**, **Gotcha**, **Nine Lives**, **Football** and **Scram**. Highscore is now called **Count-Up** (8 visits).
- New-game screen: the games of a group are tiles with a short line, a badge shows games for a fixed number of players, and the start button tells you when the player count does not fit.
- Every game has its own rule text, targets on the board, effects (gotcha, goal, role swap …), caller sentences, voice commands and bots.
- A tie in Count-Up, Shanghai, Halve-It, Bermuda, Golf or Baseball goes to extra rounds (up to five).
- Checkout ways in Gotcha, 121 and Checkout Training only show what is possible with the darts left in the visit.

**Deutsch**

- **29 Spiele.** Neu bei Cricket: **Tactics** und **verdeckte** Zahlen (sechs zufällige Zahlen, die erst beim Treffen aufgedeckt werden), **Wild Mouse** (dazu beliebiges Double, Triple und 3 in a Bed) und **Mickey Mouse** (20–12, Doubles, Triples, Bull). Neue Trainings: **Singles**, **Checkout-Training** (zufällige Finishes, für alle gleich), **Catch 40** und die **JDC Challenge**. Neue Partyspiele: **Bermuda**, **Round the World**, **Gotcha**, **Nine Lives**, **Fußball** und **Scram**. Highscore heißt jetzt **Count-Up** (8 Aufnahmen).
- Neues-Spiel-Seite: Die Spiele einer Gruppe sind Kacheln mit einer kurzen Zeile, ein Abzeichen zeigt Spiele mit fester Spielerzahl, und der Start-Knopf sagt, wenn die Spielerzahl nicht passt.
- Jedes Spiel hat eigenen Regeltext, Ziele auf der Scheibe, Effekte (Gotcha, Tor, Rollentausch …), Ansager-Sätze, Sprachbefehle und Bots.
- Gleichstand bei Count-Up, Shanghai, Halve-It, Bermuda, Golf oder Baseball geht in Extra-Runden (bis zu fünf).
- Checkout-Wege bei Gotcha, 121 und Checkout-Training zeigen nur, was mit den restlichen Darts der Aufnahme geht.

## 1.24.0

- New card **DartNest Tile** (`custom:autodarts-tile-card`): the board as one compact row with the board scene behind it – status colour, live darts as dots, the running game or today's values. Tap opens a window with the overview card (live darts, power, play, settings, players), today's values (`today`) and any own cards (`cards`). Pull down, ✕ or the back button closes it. CSS animations only, paused when not visible.

**Deutsch**

- Neue Karte **DartNest-Kachel** (`custom:autodarts-tile-card`): das Board als kompakte Zeile mit der Board-Szene dahinter – Statusfarbe, Live-Würfe als Punkte, das laufende Spiel oder die Werte von heute. Tippen öffnet ein Fenster mit der Übersichtskarte (Live-Würfe, Ein/Aus, Spielen, Einstellungen, Spieler), den Werten von heute (`today`) und beliebigen eigenen Karten (`cards`). Nach unten ziehen, ✕ oder Zurück schließt es. Nur CSS-Animationen, angehalten, wenn nicht sichtbar.

## 1.23.0

- Caller: the championship pack says the right number in the right language. Scores went to the voice as digits ("100!"), so it had to guess the language – some sounds came out in English in a German pack, some said another number (a 100 announced as 180). Scores are now spoken as words in the language of Home Assistant ("Einhundert!").
- Every score sound is listened to with the speech recognition of Home Assistant (e.g. Home Assistant Cloud) right after it is made; a sound that says the wrong number is spoken again (up to three times).
- Packs made before 1.23 are listened to once by themselves after the update. Wrong sounds are spoken again in the background, the old sound plays until the new one is there, and it continues by itself after the Google daily limit. New button **Check the sounds** in the pack menu, new option `anhoeren` for `autodarts.ansager_pack_pruefen`.
- Live sentences say the score as a word too.

**Deutsch**

- Ansager: Das Meisterschafts-Pack sagt die richtige Zahl in der richtigen Sprache. Die Punkte gingen als Ziffern („100!“) an die Stimme, die die Sprache raten musste – manche Töne kamen auf Englisch in einem deutschen Pack, manche sagten eine andere Zahl (eine 100 als 180 angesagt). Jetzt werden die Punkte als Wort in der Sprache von Home Assistant gesprochen („Einhundert!“).
- Jeder Punkte-Ton wird direkt nach dem Erzeugen mit der Spracherkennung von Home Assistant (z. B. Home Assistant Cloud) angehört; sagt er die falsche Zahl, wird er neu gesprochen (bis zu drei Mal).
- Packs von vor 1.23 werden nach dem Update einmal von selbst angehört. Falsche Töne werden im Hintergrund neu gesprochen, bis dahin spielt der alte Ton, und nach dem Google-Tageslimit geht es von selbst weiter. Neuer Knopf **Töne prüfen** im Pack-Menü, neue Option `anhoeren` für `autodarts.ansager_pack_pruefen`.
- Live-Sätze sagen die Punkte ebenfalls als Wort.

## 1.22.2

- The Marketplace lists the integration as "DartNest for Autodarts", so it is easy to find. In Home Assistant it is still called DartNest.

**Deutsch**

- Im Marketplace heißt die Integration jetzt „DartNest for Autodarts“, damit man sie leicht findet. In Home Assistant heißt sie weiter DartNest.

## 1.22.1

- README with real screenshots from a home board, the Platinum quality scale badge and the championship pack in the highlights.
- The automatic checks install ffmpeg, so all tests run on GitHub too.

**Deutsch**

- README mit echten Bildern von einem Board zuhause, Platinum-Abzeichen und dem Meisterschafts-Pack bei den Highlights.
- Die automatischen Prüfungen installieren ffmpeg, damit alle Tests auch auf GitHub laufen.

## 1.22.0

- **New name: DartNest.** The integration, its logo, the sidebar entry and the cards are now called DartNest, so it is clear that this is an unofficial project and not a product of Autodarts. It still works with Autodarts boards. Nothing changes for you: entity IDs, actions, dashboards and settings stay the same.
- New logo and icon (house with target and dart).
- The repository moved to [Wadim-dev/DartNest_ha](https://github.com/Wadim-dev/DartNest_ha); the old address forwards there.
- Updates come through the Marketplace. The extra update entity for the folder `custom_templates/autodarts_update` is now off by default (existing installations keep it).
- New README with screenshots and a legal notice.

**Deutsch**
- **Neuer Name: DartNest.** Integration, Logo, Seitenleiste und Karten heißen jetzt DartNest. So ist klar, dass es ein inoffizielles Projekt ist und kein Produkt von Autodarts. Es funktioniert weiter mit Autodarts-Boards. Für dich ändert sich nichts: Entitäten, Aktionen, Dashboards und Einstellungen bleiben gleich.
- Neues Logo und Symbol (Haus mit Zielscheibe und Dart).
- Das Repository heißt jetzt [Wadim-dev/DartNest_ha](https://github.com/Wadim-dev/DartNest_ha); die alte Adresse leitet weiter.
- Updates kommen über den Marketplace. Die zusätzliche Update-Entität für den Ordner `custom_templates/autodarts_update` ist für neue Installationen standardmäßig aus (bestehende behalten sie).
- Neue README mit Bildern und Rechtshinweis.

## 1.21.0

- Caller card rebuilt to explain itself: a big **Listen to a sample** button on top, then three steps – where it plays, which voice or pack (one row each, with sounds and what is missing), what it announces. Walk-on songs and the live voice fold away.
- Packs have a ⋮ menu (use, make missing sounds, stop, delete). Deleting asks in a window that shows how many sounds go – no more one-tap delete.
- **New championship pack** opens a window with the speakers, a short description and a **Sample** button each; speakers that already have a pack are marked. Only one pack is made at a time.
- At the daily limit of the voice a pack waits and continues by itself about three hours later, also after a restart. New action `autodarts.ansager_pack_anhalten` stops it; `autodarts.ansager_testen` takes `sprecher` for a sample.

**Deutsch**
- Ansager-Karte neu und selbsterklärend: oben ein großer Knopf **Probe hören**, darunter drei Schritte – wo es läuft, welche Stimme oder welches Pack (je eine Zeile mit Tönen und was fehlt), was angesagt wird. Einlaufmusik und Live-Stimme sind einklappbar.
- Packs haben ein ⋮-Menü (benutzen, fehlende Töne erzeugen, anhalten, löschen). Löschen fragt in einem Fenster nach und zeigt, wie viele Töne verschwinden – kein Löschen mehr mit einem Tipp.
- **Neues Meisterschafts-Pack** öffnet ein Fenster mit den Sprechern, kurzer Beschreibung und je einem Knopf **Probe**; Sprecher mit fertigem Pack sind markiert. Es wird immer nur ein Pack gleichzeitig erzeugt.
- Beim Tageslimit der Stimme wartet ein Pack und macht etwa drei Stunden später von selbst weiter, auch nach einem Neustart. Neue Aktion `autodarts.ansager_pack_anhalten` hält es an; `autodarts.ansager_testen` nimmt `sprecher` für eine Probe.

## 1.20.2

- `autodarts.ansager_pack_pruefen` finds the end of the spoken direction per sound: a sound of one word ("140!", "Game on!") is cut at its last pause, sounds of several words (leg, set …) at the pause nearest to where the direction ends in the others. Measured on a real pack the direction ends between 3 and 4.2 seconds.

**Deutsch**
- `autodarts.ansager_pack_pruefen` findet das Ende der mitgesprochenen Anweisung je Ton: Ein Ton aus einem Wort („140!“, „Game on!“) wird an seiner letzten Pause geschnitten, Töne aus mehreren Wörtern (Leg, Satz …) an der Pause, die dem Ende der Anweisung in den anderen am nächsten liegt. Gemessen an einem echten Pack endet die Anweisung zwischen 3 und 4,2 Sekunden.

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
