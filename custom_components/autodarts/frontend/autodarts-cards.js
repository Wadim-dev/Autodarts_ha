/* DartNest cards for Home Assistant (shipped with the DartNest integration for Autodarts boards, loaded automatically).
   custom:autodarts-overview-card  Board scene with live darts, optional power on/off, shortcuts
   custom:autodarts-tile-card      The same as one compact row with the scene behind it; tap opens a window with everything
   custom:autodarts-game-card      Local X01 game: lobby, bull-off, match, result, corrections, caller
   custom:autodarts-manager-card   Board Manager: cameras with calibration grid, controls, system values, settings
   custom:autodarts-players-card   Players, overall statistics, recent games
   custom:autodarts-lights-card    Light effects on game events
   Entities are found automatically (platform "autodarts"), texts follow the HA language (English/German).
   Animations are CSS only and pause when the card is not visible; camera images load only while visible. */
(() => {
  if (customElements.get('autodarts-game-card')) return;

  /* ---------- texts ---------- */
  const TEXTE = {
    en: {
      dart: 'Dart', visit: 'Visit', on: 'Turn on', off: 'Turn off', off_q: 'Really turn off?', play: 'Play', manager: 'Board Manager', players: 'Players',
      sc_off: 'Board off', sc_starting: 'Starting …', sc_stopping: 'Shutting down …', sc_ready: 'Ready – throw!', sc_takeout: 'Remove darts', sc_calib: 'Calibrating …', sc_stopped: 'Detection stopped', sc_standby: 'Standby – wakes up with the next game', sc_lost: 'Connection lost',
      dart_of: 'Dart {n} of 3 · {s} so far', visit_pts: 'Visit {s} points', pc_running: 'PC is running, Autodarts is starting', about_minute: 'Takes about a minute', plug_after: 'The plug switches off afterwards',
      plug_on: 'Plug on', ready_hint: 'Throw a dart to start', game_running: 'Game running', back: 'Back', missing: 'DartNest integration not found',
      new_game: 'New game', game_over: 'Game over', darts: 'Darts', local: 'Local in Home Assistant', cancel_game: 'Cancel game', caller: 'Caller', fullscreen: 'Full screen',
      nobody: 'Nobody yet – tap below.', of6: '{n} of 8', shuffle: 'Shuffle order', new_player: 'New player', bot: 'Bot', bot_level: 'Bot level (average)', average: 'Average',
      game: 'Game', start_value: 'Start value', legs_per_set: 'Legs per set', first_to: 'First to', checkout: 'Check-out', checkin: 'Check-in', more: 'More settings',
      sets_first: 'Sets (first to)', no_sets: 'no sets', sets_to: 'Sets: first to {n}', bulloff_who: 'Bull-off (who starts)', bulloff_onoff: 'Bull-off {v}', off_w: 'off', on_w: 'on',
      board_off_hint: 'The board is off. Without the board you can only enter darts by hand.', start_game: 'Start game', move_up: 'move up', remove: 'remove',
      out: 'out', aims_bull: 'throws at bull …', waits: 'waits', tie: 'Tie – throw again', bulloff_title: 'Bull-off – closest to the bull starts', one_dart: '1 dart each',
      undo: 'Undo', enter: 'Enter', missed: 'Missed', next: 'Next', leg_won: '{n} wins the leg – remove darts', bust: 'Bust – remove darts', remove_darts: 'Remove darts',
      throws_now: '{n} throws …', to_start_d: '{n} – double to start', to_start_m: '{n} – double or treble to start', your_turn: '{n} to throw', pts: 'pts', rest: 'Rest {n}',
      visits: 'Visits', leg: 'Leg', set: 'Set', statistics: 'Statistics', cancel_noscore: 'Cancel game (not counted)', really_cancel: 'Really cancel?', no_visit: 'No visit yet.', tap_fix: 'Tap to correct.',
      first9: 'First 9', highest: 'Highest', best_finish: 'Highest finish', best_leg: 'Best leg', n_darts: '{n} darts', wins: '{n} wins!', rematch: 'Rematch', undo_last: 'Undo last dart',
      single: 'Single', double: 'Double', treble: 'Triple', clear: 'Clear', cancel: 'Cancel', create: 'Create', name: 'Name', cancel_q: 'Cancel game?', cancel_text: 'The game ends without being counted.',
      keep_playing: 'Keep playing', which_dart: 'Which dart?', close: 'Close', enter_dart: 'Enter or change dart {n}', visit_dart: 'Visit {a}, dart {d}', last: 'last',
      tap_mode: 'Tap the board', tap_on: 'Tap input on: tap the board where the dart landed, outside = miss. Keyboard: T20, D16, 25, 50, 0 + Enter; Enter alone = next, Backspace = undo.', tap_full: 'Three darts – tap Next',
      cam: 'Camera {n}', cams_off: 'Cameras off', graphic: 'graphic', tap_view: 'Tap: next camera / graphic', grid: 'Grid',
      first_leg: 'First to {n} leg', first_legs: 'First to {n} legs', sets_legs: 'First to {s} sets of {l} legs', din: 'Double In', min: 'Master In', sout: 'Straight Out', dout: 'Double Out', mout: 'Master Out',
      say_180: 'One hundred and eighty!', say_bust: 'Bust', say_game: 'Game shot, and the match, {n}!', say_set: 'Game shot, and the set, {n}!', say_leg: 'Game shot, {n}!', say_0: 'No score',
      say_need: '{n}, you require {r}', caller_on: 'Caller on',
      online: 'Online', offline: 'Offline', connection: 'Connection', detection: 'Detection', running: 'running', stopped: 'stopped', fps: 'Frame rate', cameras: 'Cameras', cpu: 'CPU', memory: 'Memory',
      calibrated: 'Calibrated', yes: 'yes', no: 'no', controls: 'Controls', start: 'Start', stop: 'Stop', reset: 'Reset', calibrate: 'Calibrate', calibrate_q: 'Calibrate now?',
      restart_sw: 'Restart software', restart_pc: 'Restart PC', sure: 'Sure?', extra_imgs: 'Detection & live image', detection_img: 'Detection', live_img: 'Live image', cam_settings: 'Camera settings',
      resolution: 'Resolution', standby: 'Standby after', minutes: '{n} min', standby_hint: 'Without a throw the board stops the detection after this time and saves power and computing time. DartNest wakes it by itself when a game starts, and during a game that is still being played.',
      software: 'Software & updates', board_sw: 'Board software', vision: 'Detection (vision)', host: 'Computer', kernel: 'Kernel', install: 'Install', open_orig: 'Open original Board Manager', home_only: 'Only in your home network.',
      tap_cam: 'Tap a camera = large and live', calib_grid: 'Calibration grid', cams_start: 'Cameras off – start detection',
      st_throw: 'ready', st_takeout: 'remove darts', st_calibrating: 'calibrating', st_starting: 'starting', st_stopped: 'stopped', st_standby: 'standby',
      players_stats: 'Players & statistics', n_players: '{p} players · {g} games saved', no_players: 'No players yet. Add yourself and your opponents – every game then counts towards the statistics.',
      games_wins: '{g} games · {w} wins', best_avg: 'Best avg', n180: '180s', legs: 'Legs', rename: 'Rename', del_stats: 'Delete statistics', del_player: 'Delete player', really_del: 'Really delete?',
      recent: 'Recent games', no_game_yet: 'No finished game yet.', reset_all: 'Reset everything', del_all: 'Delete statistics of all players and game history', del_all_q: 'Sure? This cannot be undone',
      players_stay: 'The players themselves are kept.', save: 'Save',
      effects: 'Effects', fx_nine: 'NINE-DARTER', fx_perfect: 'The perfect leg', fx_match: 'and the match, {n}', fx_set: 'and the set, {n}', fx_leg: 'Leg {n}', fx_bust: 'BUST',

      g_x01: 'X01', g_cricket: 'Cricket', g_training: 'Training', g_party: 'Party', game_type: 'Game type',
      a_cricket: 'Cricket', a_atc: 'Around the Clock', a_bobs27: "Bob's 27", a_doppel: 'Doubles', a_checkout121: '121 Checkout', a_highscore: 'Highscore',
      a_shanghai: 'Shanghai', a_killer: 'Killer', a_halve_it: 'Halve-It', a_golf: 'Golf', a_baseball: 'Baseball',
      h_cricket: 'Close 15–20 and the bull with three marks each. Extra marks on a number you closed score points as long as an opponent has it open.',
      h_cut_throat: 'Cut-Throat: your extra marks give points to every opponent who has the number open. Lowest score wins.',
      h_no_score: 'No points: whoever closes all numbers first wins.',
      h_atc: 'Hit 1 to 20 in order, then the bull. First one through wins.',
      h_bobs27: 'Start with 27. Three darts at D1, D2 … D20 and the bull. Every hit adds the double, no hit subtracts it. Below 0 you are out.',
      h_doppel: 'Three darts at every double from D1 to D20 and the bull. Every hit is a point.',
      h_checkout121: 'Check out 121 with nine darts (double out). Done: next target +1, missed: −1. Most checkouts win.',
      h_highscore: 'Score as many points as possible in a fixed number of visits.',
      h_shanghai: 'Round n only counts number n. Single, double and treble of it in one visit (Shanghai) wins at once.',
      h_killer: 'Everyone gets a number. Hit your double to become a killer, then hit the doubles of the others to take their lives. Careful: as a killer, your own double costs you a life.',
      h_halve_it: 'Targets 15, 16, any double, 17, 18, any treble, 19, 20, bull. Start with 40 – no hit on the target halves your score.',
      h_golf: 'Hole n is number n. The last dart counts: treble 1, double 2, single 3, miss 5 strokes. Stop early with Next. Fewest strokes win.',
      h_baseball: 'Nine innings, inning n is number n. Single 1, double 2, treble 3 runs. Most runs win.',
      variant: 'Variant', v_standard: 'Standard', v_cut_throat: 'Cut-Throat', v_no_score: 'No score', numbers: 'Numbers', z_classic: '15–20', z_tactics: '10–20', z_random: 'Random',
      area: 'Segment', any: 'any', rounds: 'Visits', holes: 'Holes', lives: 'Lives', target: 'Target', round_of: 'Round {n} of {m}', inning_of: 'Inning {n} of {m}', hole_of: 'Hole {n} of {m}',
      mpr: 'MPR', marks: 'Marks', hits: 'hits', out_w: 'out', done_w: 'done', attempt: 'Attempt {n} of 3', target_n: 'Target {n}', golf_hint: 'Last dart counts – Next keeps it',
      any_double: 'any double', any_triple: 'any treble', points: 'Points', strokes: 'Strokes', runs: 'Runs', checks: 'Checkouts', best: 'Best', killer_w: 'Killer', number_w: 'Number',
      hit_double: '{n}: hit D{z} to become a killer', killer_aims: '{n} is a killer – hit the doubles of the others', place: 'Place', ranking: 'Ranking', score: 'Score',
      fx_win: 'WINNER', fx_marks: '{n} MARKS', fx_killer: 'KILLER', fx_life: 'HIT!', fx_out: 'OUT', fx_halved: 'HALVED', fx_hio: 'HOLE IN ONE', fx_homerun: 'HOME RUN',
      single_game: 'Single game', tournament: 'Tournament', start_tour: 'Start tournament', tour_hint: 'Knockout for 3–16 players, byes are drawn automatically. Every match uses the settings below.', of16: '{n} of 16',
      t_final: 'Final', t_semi: 'Semi-final', t_quarter: 'Quarter-final', t_last16: 'Round of 16', t_round: 'Round {n}', match_of: 'Match {n} of {m}', bye: 'bye',
      next_match: 'Next match: {a} vs {b}', champion: 'Tournament winner', fx_champion: 'CHAMPION', end_tour: 'End tournament', cancel_tour: 'Cancel tournament', tour_running: 'Tournament running', bracket: 'Bracket', really_tour: 'Cancel the tournament?',
      fx_done: 'DONE', fx_check: 'CHECKED', fx_missed: 'MISSED', fx_closed: '{z} closed', fx_lives: '{n} lives left', fx_life1: '1 life left',
      elo: 'Rating', streak: 'Streak', n_days: '{n} days', n_day: '1 day', best_streak: 'Best streak', heatmap: 'Hit map', t_fields: 'Fields', t_points: 'Darts', top_fields: 'Most hit fields',
      trend: 'Trend (X01 average, last games)', badges: 'Badges', vs: 'Head to head', export: 'Export statistics (CSV)', no_data: 'No data yet – play a game.', n_of: '{a} of {b}',
      ranking_elo: 'Ranking', wins_losses: '{w} wins · {l} losses', gold: 'Gold', silver: 'Silver', bronze: 'Bronze', next_at: 'next at {n}', points_hint: 'Only darts detected by the board have a position.',
      b_n180: '180s', b_ton: '100+ visits', b_high_finish: 'High finish', b_kurzes_leg: 'Short leg (darts)', b_average: 'Best average', b_siege: 'Wins', b_spiele: 'Games', b_darts: 'Darts thrown',
      b_serie: 'Days in a row', b_nine_marks: 'Nine marks', b_shanghai: 'Shanghai', b_hole_in_one: 'Hole in one', b_allrounder: 'Allrounder (game types)',
      d_overview: 'Dartboard scene with live darts, optional power on/off and shortcuts', d_game: 'Local games (X01, Cricket, training, party): lobby, bull-off, match, result', d_manager: 'Cameras, controls, system values, settings', d_players: 'Players, overall statistics, recent games', d_lights: 'Light effects on game events (180, bust, checkout …)', tab_board: 'Board', lights_title: 'Light effects', n_rules: '{n} rules', no_rules: 'No light effect yet. Choose an event, lights and an effect – the lights go back to how they were afterwards.', new_rule: 'New light effect', edit_rule: 'Edit light effect', trigger: 'Event', effect: 'Effect', color: 'Colour', brightness: 'Brightness', duration: 'Duration', seconds: '{n} s', lights: 'Lights', search: 'Search …', test: 'Test', active: 'active', inactive: 'off', delete: 'Delete', no_lights: 'Choose at least one light.', n_lights: '{n} lights', e_farbe: 'Colour', e_blinken: 'Blink', e_blitz: 'Flash', e_regenbogen: 'Rainbow', e_pulsieren: 'Pulse', e_lampe: 'Light effect', e_preset: 'WLED preset', fx_name: 'Effect of the light', preset_name: 'Preset', speed: 'Speed', intensity: 'Intensity', only_fx: 'Only lights with their own effects are shown (e.g. WLED, Hue).', only_wled: 'Only WLED lights are shown.', no_wled: 'No WLED device yet. Add it under Settings → Devices & services → WLED, then it shows up here.', no_fx: 'Choose a light first.', lights_hint: 'Effects run in Home Assistant, also when the dashboard is closed. Colour lights show the colour, others only light up.', ev_game_started: 'Game started', ev_dart: 'Every dart', ev_triple: 'Triple', ev_bull: 'Bull (25)', ev_bullseye: 'Bullseye', ev_visit: 'Every visit', ev_ton: '100+', ev_ton_forty: '140+', ev_one_eighty: '180', ev_no_score: 'No score', ev_bust: 'Bust', ev_three_in_a_bed: 'Three in a bed', ev_checkout: 'Checkout', ev_high_finish: 'High finish (100+)', ev_nine_darter: 'Nine-darter', ev_leg_won: 'Leg won', ev_set_won: 'Set won', ev_match_won: 'Match won', ev_nine_marks: 'Nine marks (Cricket)', ev_shanghai: 'Shanghai', ev_killer: 'Becomes killer', ev_eliminated: 'Player out', ev_halved: 'Halved (Halve-It)', ev_hole_in_one: 'Hole in one', ev_tournament_won: 'Tournament won'
    },
    de: {
      dart: 'Dart', visit: 'Aufnahme', on: 'Einschalten', off: 'Ausschalten', off_q: 'Wirklich aus?', play: 'Spielen', manager: 'Board Manager', players: 'Spieler',
      sc_off: 'Board aus', sc_starting: 'Startet …', sc_stopping: 'Fährt herunter …', sc_ready: 'Bereit – wirf!', sc_takeout: 'Darts ziehen', sc_calib: 'Kalibriert …', sc_stopped: 'Erkennung gestoppt', sc_standby: 'Standby – wacht beim nächsten Spiel auf', sc_lost: 'Verbindung kurz weg',
      dart_of: 'Dart {n} von 3 · bisher {s}', visit_pts: 'Aufnahme {s} Punkte', pc_running: 'PC läuft, Autodarts startet', about_minute: 'Dauert etwa eine Minute', plug_after: 'Steckdose geht danach aus',
      plug_on: 'Steckdose an', ready_hint: 'Wirf einen Dart zum Start', game_running: 'Spiel läuft', back: 'Zurück', missing: 'Integration „DartNest“ nicht gefunden',
      new_game: 'Neues Spiel', game_over: 'Spielende', darts: 'Darts', local: 'Lokal in Home Assistant', cancel_game: 'Spiel abbrechen', caller: 'Ansage', fullscreen: 'Vollbild',
      nobody: 'Noch niemand dabei – unten antippen.', of6: '{n} von 8', shuffle: 'Reihenfolge mischen', new_player: 'Neuer Spieler', bot: 'Bot', bot_level: 'Bot-Stärke (Average)', average: 'Average',
      game: 'Spiel', start_value: 'Startwert', legs_per_set: 'Legs je Satz', first_to: 'Erster bis', checkout: 'Auswurf', checkin: 'Einwurf', more: 'Weitere Einstellungen',
      sets_first: 'Sets (erster bis)', no_sets: 'ohne Sets', sets_to: 'Sets: erster bis {n}', bulloff_who: 'Bull-Off (wer anfängt)', bulloff_onoff: 'Bull-Off {v}', off_w: 'aus', on_w: 'an',
      board_off_hint: 'Das Board ist aus. Ohne Board kannst du nur von Hand eintragen.', start_game: 'Spiel starten', move_up: 'nach oben', remove: 'entfernen',
      out: 'raus', aims_bull: 'wirft auf Bull …', waits: 'wartet', tie: 'Gleichstand – nochmal werfen', bulloff_title: 'Bull-Off – wer am nächsten am Bull ist, fängt an', one_dart: 'je 1 Dart',
      undo: 'Zurück', enter: 'Eintragen', missed: 'Daneben', next: 'Weiter', leg_won: '{n} gewinnt das Leg – Darts ziehen', bust: 'Überworfen – Darts ziehen', remove_darts: 'Darts ziehen',
      throws_now: '{n} wirft …', to_start_d: '{n} – Double zum Starten', to_start_m: '{n} – Double oder Triple zum Starten', your_turn: '{n} ist dran', pts: 'Pkt.', rest: 'Rest {n}',
      visits: 'Aufnahmen', leg: 'Leg', set: 'Satz', statistics: 'Statistik', cancel_noscore: 'Spiel abbrechen (ohne Wertung)', really_cancel: 'Wirklich abbrechen?', no_visit: 'Noch keine Aufnahme.', tap_fix: 'Antippen zum Korrigieren.',
      first9: 'First 9', highest: 'Höchste', best_finish: 'Höchstes Finish', best_leg: 'Bestes Leg', n_darts: '{n} Darts', wins: '{n} gewinnt!', rematch: 'Revanche', undo_last: 'Letzten Dart zurücknehmen',
      single: 'Single', double: 'Double', treble: 'Triple', clear: 'Löschen', cancel: 'Abbrechen', create: 'Anlegen', name: 'Name', cancel_q: 'Spiel abbrechen?', cancel_text: 'Das Spiel endet ohne Wertung.',
      keep_playing: 'Weiterspielen', which_dart: 'Welchen Dart ändern?', close: 'Schließen', enter_dart: 'Dart {n} eintragen oder ändern', visit_dart: 'Aufnahme {a}, Dart {d}', last: 'zuletzt',
      tap_mode: 'Scheibe antippen', tap_on: 'Antippen an: tippe auf die Stelle, wo der Dart steckt, außerhalb = daneben. Tastatur: T20, D16, 25, 50, 0 + Enter; nur Enter = Weiter, Rücktaste = Zurück.', tap_full: 'Drei Darts – Weiter tippen',
      cam: 'Kamera {n}', cams_off: 'Kameras aus', graphic: 'Grafik', tap_view: 'Antippen: nächste Kamera / Grafik', grid: 'Netz',
      first_leg: 'Erster bis {n} Leg', first_legs: 'Erster bis {n} Legs', sets_legs: 'Erster bis {s} Sets à {l} Legs', din: 'Double In', min: 'Master In', sout: 'Straight Out', dout: 'Double Out', mout: 'Master Out',
      say_180: 'Einhundertachtzig!', say_bust: 'Überworfen', say_game: 'Game shot! Spiel für {n}', say_set: 'Game shot! Satz für {n}', say_leg: 'Game shot! Leg für {n}', say_0: 'No score',
      say_need: '{n}, du brauchst {r}', caller_on: 'Ansage an',
      online: 'Online', offline: 'Offline', connection: 'Verbindung', detection: 'Erkennung', running: 'läuft', stopped: 'gestoppt', fps: 'Bildrate', cameras: 'Kameras', cpu: 'CPU', memory: 'Speicher',
      calibrated: 'Kalibriert', yes: 'ja', no: 'nein', controls: 'Steuerung', start: 'Start', stop: 'Stop', reset: 'Reset', calibrate: 'Kalibrieren', calibrate_q: 'Jetzt kalibrieren?',
      restart_sw: 'Software neu starten', restart_pc: 'PC neu starten', sure: 'Sicher?', extra_imgs: 'Erkennungsbild & Live-Bild', detection_img: 'Erkennung', live_img: 'Live-Bild', cam_settings: 'Kamera-Einstellungen',
      resolution: 'Auflösung', standby: 'Standby nach', minutes: '{n} Minuten', standby_hint: 'Ohne Wurf stoppt das Board nach dieser Zeit die Erkennung und spart Strom und Rechenleistung. DartNest weckt sie von selbst, wenn ein Spiel startet, und während eines Spiels, das noch gespielt wird.',
      software: 'Software & Updates', board_sw: 'Board-Software', vision: 'Erkennung (Vision)', host: 'Rechner', kernel: 'Kernel', install: 'Installieren', open_orig: 'Original Board Manager öffnen', home_only: 'Nur im Heimnetz.',
      tap_cam: 'Kamera antippen = groß und live', calib_grid: 'Kalibriernetz', cams_start: 'Kameras aus – Erkennung starten',
      st_throw: 'bereit', st_takeout: 'Darts ziehen', st_calibrating: 'kalibriert', st_starting: 'startet', st_stopped: 'gestoppt', st_standby: 'Standby',
      players_stats: 'Spieler & Statistik', n_players: '{p} Spieler · {g} Spiele gespeichert', no_players: 'Noch keine Spieler. Lege dich und deine Mitspieler an – danach zählt jedes Spiel in die Statistik.',
      games_wins: '{g} Spiele · {w} Siege', best_avg: 'Bester Avg', n180: '180er', legs: 'Legs', rename: 'Umbenennen', del_stats: 'Statistik löschen', del_player: 'Spieler löschen', really_del: 'Wirklich löschen?',
      recent: 'Letzte Spiele', no_game_yet: 'Noch kein Spiel beendet.', reset_all: 'Alles zurücksetzen', del_all: 'Statistik aller Spieler und Spielverlauf löschen', del_all_q: 'Sicher? Lässt sich nicht rückgängig machen',
      players_stay: 'Die Spieler selbst bleiben.', save: 'Speichern',
      effects: 'Effekte', fx_nine: 'NEUN-DARTER', fx_perfect: 'Das perfekte Leg', fx_match: 'Spiel für {n}', fx_set: 'Satz für {n}', fx_leg: 'Leg für {n}', fx_bust: 'ÜBERWORFEN',

      g_x01: 'X01', g_cricket: 'Cricket', g_training: 'Training', g_party: 'Party', game_type: 'Spielart',
      a_cricket: 'Cricket', a_atc: 'Rund um die Uhr', a_bobs27: "Bob's 27", a_doppel: 'Doppel-Training', a_checkout121: '121 Checkout', a_highscore: 'Highscore',
      a_shanghai: 'Shanghai', a_killer: 'Killer', a_halve_it: 'Halve-It', a_golf: 'Golf', a_baseball: 'Baseball',
      h_cricket: 'Schließe 15–20 und Bull mit je drei Treffern (Marks). Weitere Treffer auf deinen geschlossenen Zahlen bringen Punkte, solange ein Gegner sie noch offen hat.',
      h_cut_throat: 'Cut-Throat: Deine zusätzlichen Treffer geben jedem Gegner Punkte, der die Zahl noch offen hat. Wenigste Punkte gewinnen.',
      h_no_score: 'Ohne Punkte: Wer zuerst alle Zahlen schließt, gewinnt.',
      h_atc: 'Triff 1 bis 20 der Reihe nach, dann Bull. Wer zuerst durch ist, gewinnt.',
      h_bobs27: 'Start mit 27. Je drei Darts auf D1, D2 … D20 und Bull. Jeder Treffer bringt das Doppelte, kein Treffer kostet es. Unter 0 bist du raus.',
      h_doppel: 'Je drei Darts auf jedes Doppel von D1 bis D20 und Bull. Jeder Treffer ist ein Punkt.',
      h_checkout121: 'Checke 121 mit neun Darts aus (Double Out). Geschafft: nächstes Ziel +1, verfehlt: −1. Die meisten Checkouts gewinnen.',
      h_highscore: 'So viele Punkte wie möglich in einer festen Zahl von Aufnahmen.',
      h_shanghai: 'In Runde n zählt nur die Zahl n. Single, Double und Triple davon in einer Aufnahme (Shanghai) gewinnt sofort.',
      h_killer: 'Jeder bekommt eine Zahl. Triff dein Double, dann bist du Killer und nimmst den anderen mit ihrem Double Leben. Vorsicht: Als Killer kostet dich dein eigenes Double ein Leben.',
      h_halve_it: 'Ziele 15, 16, ein Double, 17, 18, ein Triple, 19, 20, Bull. Start mit 40 – kein Treffer aufs Ziel halbiert deinen Stand.',
      h_golf: 'Loch n ist die Zahl n. Der letzte Dart zählt: Triple 1, Double 2, Single 3, daneben 5 Schläge. Mit Weiter früher aufhören. Wenigste Schläge gewinnen.',
      h_baseball: 'Neun Innings, Inning n ist die Zahl n. Single 1, Double 2, Triple 3 Runs. Die meisten Runs gewinnen.',
      variant: 'Variante', v_standard: 'Standard', v_cut_throat: 'Cut-Throat', v_no_score: 'Ohne Punkte', numbers: 'Zahlen', z_classic: '15–20', z_tactics: '10–20', z_random: 'Zufall',
      area: 'Bereich', any: 'alle', rounds: 'Aufnahmen', holes: 'Löcher', lives: 'Leben', target: 'Ziel', round_of: 'Runde {n} von {m}', inning_of: 'Inning {n} von {m}', hole_of: 'Loch {n} von {m}',
      mpr: 'MPR', marks: 'Marks', hits: 'Treffer', out_w: 'raus', done_w: 'fertig', attempt: 'Versuch {n} von 3', target_n: 'Ziel {n}', golf_hint: 'Letzter Dart zählt – Weiter behält ihn',
      any_double: 'beliebiges Double', any_triple: 'beliebiges Triple', points: 'Punkte', strokes: 'Schläge', runs: 'Runs', checks: 'Checkouts', best: 'Bestes', killer_w: 'Killer', number_w: 'Zahl',
      hit_double: '{n}: triff D{z}, um Killer zu werden', killer_aims: '{n} ist Killer – triff die Doubles der anderen', place: 'Platz', ranking: 'Rangliste', score: 'Stand',
      fx_win: 'SIEG', fx_marks: '{n} MARKS', fx_killer: 'KILLER', fx_life: 'TREFFER!', fx_out: 'RAUS', fx_halved: 'HALBIERT', fx_hio: 'HOLE IN ONE', fx_homerun: 'HOME RUN',
      single_game: 'Einzelspiel', tournament: 'Turnier', start_tour: 'Turnier starten', tour_hint: 'K.-o. für 3–16 Spieler, Freilose werden automatisch verteilt. Jedes Match nutzt die Einstellungen unten.', of16: '{n} von 16',
      t_final: 'Finale', t_semi: 'Halbfinale', t_quarter: 'Viertelfinale', t_last16: 'Achtelfinale', t_round: 'Runde {n}', match_of: 'Match {n} von {m}', bye: 'Freilos',
      next_match: 'Nächstes Match: {a} gegen {b}', champion: 'Turniersieger', fx_champion: 'CHAMPION', end_tour: 'Turnier beenden', cancel_tour: 'Turnier abbrechen', tour_running: 'Turnier läuft', bracket: 'Turnierbaum', really_tour: 'Turnier wirklich abbrechen?',
      fx_done: 'GESCHAFFT', fx_check: 'GECHECKT', fx_missed: 'VERFEHLT', fx_closed: '{z} zu', fx_lives: 'noch {n} Leben', fx_life1: 'noch 1 Leben',
      elo: 'Wertung', streak: 'Serie', n_days: '{n} Tage', n_day: '1 Tag', best_streak: 'Beste Serie', heatmap: 'Trefferbild', t_fields: 'Felder', t_points: 'Darts', top_fields: 'Häufigste Felder',
      trend: 'Trend (X01-Average, letzte Spiele)', badges: 'Abzeichen', vs: 'Direkter Vergleich', export: 'Statistik exportieren (CSV)', no_data: 'Noch keine Daten – spiel eine Runde.', n_of: '{a} von {b}',
      ranking_elo: 'Rangliste', wins_losses: '{w} Siege · {l} Niederlagen', gold: 'Gold', silver: 'Silber', bronze: 'Bronze', next_at: 'nächste Stufe bei {n}', points_hint: 'Nur vom Board erkannte Darts haben eine Position.',
      b_n180: '180er', b_ton: '100+-Aufnahmen', b_high_finish: 'High Finish', b_kurzes_leg: 'Kurzes Leg (Darts)', b_average: 'Bester Average', b_siege: 'Siege', b_spiele: 'Spiele', b_darts: 'Geworfene Darts',
      b_serie: 'Tage in Folge', b_nine_marks: 'Neun Marks', b_shanghai: 'Shanghai', b_hole_in_one: 'Hole in One', b_allrounder: 'Allrounder (Spielarten)',
      d_overview: 'Dartscheibe mit Live-Würfen, optional Ein/Aus und Abkürzungen', d_game: 'Lokale Spiele (X01, Cricket, Training, Party): Lobby, Bull-Off, Spiel, Ergebnis', d_manager: 'Kameras, Steuerung, Systemwerte, Einstellungen', d_players: 'Spieler, Gesamtstatistik, letzte Spiele', d_lights: 'Lichteffekte bei Spielereignissen (180, Überworfen, Checkout …)', tab_board: 'Board', lights_title: 'Lichteffekte', n_rules: '{n} Regeln', no_rules: 'Noch kein Lichteffekt. Wähle ein Ereignis, Lampen und einen Effekt – danach gehen die Lampen zurück, wie sie waren.', new_rule: 'Neuer Lichteffekt', edit_rule: 'Lichteffekt ändern', trigger: 'Ereignis', effect: 'Effekt', color: 'Farbe', brightness: 'Helligkeit', duration: 'Dauer', seconds: '{n} s', lights: 'Lampen', search: 'Suchen …', test: 'Testen', active: 'an', inactive: 'aus', delete: 'Löschen', no_lights: 'Wähle mindestens eine Lampe.', n_lights: '{n} Lampen', e_farbe: 'Farbe', e_blinken: 'Blinken', e_blitz: 'Aufblitzen', e_regenbogen: 'Regenbogen', e_pulsieren: 'Pulsieren', e_lampe: 'Lampen-Effekt', e_preset: 'WLED-Preset', fx_name: 'Effekt der Lampe', preset_name: 'Preset', speed: 'Tempo', intensity: 'Stärke', only_fx: 'Es werden nur Lampen mit eigenen Effekten gezeigt (z. B. WLED, Hue).', only_wled: 'Es werden nur WLED-Lampen gezeigt.', no_wled: 'Noch kein WLED-Gerät. Unter Einstellungen → Geräte & Dienste → WLED hinzufügen, dann erscheint es hier.', no_fx: 'Wähle zuerst eine Lampe.', lights_hint: 'Die Effekte laufen in Home Assistant, auch wenn das Dashboard zu ist. Farblampen zeigen die Farbe, andere leuchten nur auf.', ev_game_started: 'Spiel gestartet', ev_dart: 'Jeder Dart', ev_triple: 'Triple', ev_bull: 'Bull (25)', ev_bullseye: 'Bullseye', ev_visit: 'Jede Aufnahme', ev_ton: '100+', ev_ton_forty: '140+', ev_one_eighty: '180', ev_no_score: 'Kein Treffer', ev_bust: 'Überworfen', ev_three_in_a_bed: 'Three in a bed', ev_checkout: 'Checkout', ev_high_finish: 'High Finish (100+)', ev_nine_darter: 'Neun-Darter', ev_leg_won: 'Leg gewonnen', ev_set_won: 'Satz gewonnen', ev_match_won: 'Spiel gewonnen', ev_nine_marks: 'Neun Marks (Cricket)', ev_shanghai: 'Shanghai', ev_killer: 'Wird Killer', ev_eliminated: 'Spieler raus', ev_halved: 'Halbiert (Halve-It)', ev_hole_in_one: 'Hole in One', ev_tournament_won: 'Turnier gewonnen'
    }
  };
  // texts of the further light effects (1.15)
  Object.assign(TEXTE.en, {e_herzschlag: 'Heartbeat', e_stroboskop: 'Strobe', e_ausblenden: 'Fade out', e_wechsel: 'Two colours', e_welle: 'Rainbow wave', e_konfetti: 'Confetti', e_lauflicht: 'Chaser', e_funkeln: 'Sparkle', e_polizei: 'Police', e_feuer: 'Fire', e_gewitter: 'Thunderstorm', color2: 'Second colour', fx_more: 'Several lights: wave, chaser, sparkle and police spread over them.' });
  Object.assign(TEXTE.de, {e_herzschlag: 'Herzschlag', e_stroboskop: 'Stroboskop', e_ausblenden: 'Ausblenden', e_wechsel: 'Zwei Farben', e_welle: 'Regenbogen-Welle', e_konfetti: 'Konfetti', e_lauflicht: 'Lauflicht', e_funkeln: 'Funkeln', e_polizei: 'Polizei', e_feuer: 'Feuer', e_gewitter: 'Gewitter', color2: 'Zweite Farbe', fx_more: 'Mehrere Lampen: Welle, Lauflicht, Funkeln und Polizei verteilen sich auf sie.' });
  // texts of the caller card (1.16)
  Object.assign(TEXTE.en, { caller_title: 'Caller', d_caller: 'Announces scores, checkouts and walk-on songs on your speakers', caller_off_hint: 'Off', caller_on_hint: 'On', caller_run: 'Caller on', speakers: 'Speakers', voice: 'Voice', no_voice: 'No voice yet. Add one under Settings → Voice assistants (e.g. Piper, Google Translate).', pack: 'Sound pack', only_voice: 'Voice only', n_files: '{n} sounds', pack_hint: 'Own packs: Media → My media → autodarts → caller → new folder, upload sounds named like 180.mp3, 140.mp3, bust.mp3, leg.mp3, match.mp3, game_on.mp3. Missing sounds are spoken.', say_what: 'Announce', c_punkte: 'Scores', c_rest: 'You require …', c_ende: 'Game shot', c_besondere: 'Specials (9-darter, Shanghai …)', c_game_on: 'Game on', c_walkon: 'Walk-on songs', walkons: 'Walk-on songs', walk_secs: 'Play time', no_song: 'none', songs_hint: 'Songs: Media → My media → autodarts → walkon → upload music files. They play at the start of a game, then "Game on".', no_songs: 'No songs yet.', no_players_yet: 'Create players first.', no_speakers: 'Choose at least one speaker.', test_caller: 'Test', saved: 'Saved' });
  Object.assign(TEXTE.de, { caller_title: 'Ansager', d_caller: 'Sagt Punkte, Checkouts und Einlaufmusik über deine Lautsprecher an', caller_off_hint: 'Aus', caller_on_hint: 'An', caller_run: 'Ansager an', speakers: 'Lautsprecher', voice: 'Stimme', no_voice: 'Noch keine Stimme. Unter Einstellungen → Sprachassistenten eine hinzufügen (z. B. Piper, Google Translate).', pack: 'Sound-Pack', only_voice: 'Nur Stimme', n_files: '{n} Töne', pack_hint: 'Eigene Packs: Medien → Meine Medien → autodarts → caller → neuer Ordner, Töne hochladen mit Namen wie 180.mp3, 140.mp3, bust.mp3, leg.mp3, match.mp3, game_on.mp3. Was fehlt, spricht die Stimme.', say_what: 'Was ansagen', c_punkte: 'Punkte', c_rest: 'Du brauchst …', c_ende: 'Game shot', c_besondere: 'Besonderes (9-Darter, Shanghai …)', c_game_on: 'Game on', c_walkon: 'Einlaufmusik', walkons: 'Einlaufmusik', walk_secs: 'Spieldauer', no_song: 'keine', songs_hint: 'Lieder: Medien → Meine Medien → autodarts → walkon → Musikdateien hochladen. Sie laufen zum Spielbeginn, danach „Game on“.', no_songs: 'Noch keine Lieder.', no_players_yet: 'Lege zuerst Spieler an.', no_speakers: 'Wähle mindestens einen Lautsprecher.', test_caller: 'Testen', saved: 'Gespeichert' });
  // texts of tournaments up to 32 and the league (1.16)
  Object.assign(TEXTE.en, { tour_ko: 'Knockout', tour_liga: 'League', tour_hint: 'Knockout for 3–32 players, byes are drawn automatically. Every match uses the settings below.', liga_hint: 'League for 3–10 players: everyone plays everyone once. Win = 2 points, then leg difference.', of16: '{n} of {m}', t_last32: 'Round of 32', liga: 'League', liga_match: 'Match {n} of {m}', table: 'Table', fixtures: 'Matches', t_pl: 'P', t_w: 'W', t_pts: 'Pts', t_legs: 'Legs' });
  Object.assign(TEXTE.de, { tour_ko: 'K.-o.', tour_liga: 'Liga', tour_hint: 'K.-o. für 3–32 Spieler, Freilose werden automatisch verteilt. Jedes Match nutzt die Einstellungen unten.', liga_hint: 'Liga für 3–10 Spieler: jeder spielt einmal gegen jeden. Sieg = 2 Punkte, danach zählt die Leg-Differenz.', of16: '{n} von {m}', t_last32: 'Sechzehntelfinale', liga: 'Liga', liga_match: 'Spiel {n} von {m}', table: 'Tabelle', fixtures: 'Spiele', t_pl: 'Sp', t_w: 'S', t_pts: 'Pkt', t_legs: 'Legs' });
  Object.assign(TEXTE.en, { tour_mode: 'Tournament', tour_dko: 'Double KO', tour_gr: 'Groups + KO', s_tko: 'Lose once and you are out', s_tdko: 'Out after two losses', s_tgr: 'Groups first, then knockout', s_tliga: 'Everyone plays everyone',
    dko_hint: 'Double KO for 3–16 players: a loss in the winners bracket sends you to the losers bracket, the second loss ends the tournament. In the grand final the losers-bracket winner has to win twice.',
    gr_hint: 'Groups + KO for 6–32 players: 2, 4 or 8 groups, everyone plays everyone in the group. The best two of each group go on to the knockout stage, and players of the same group do not meet in its first round.',
    needs_tour: '{f} needs {a}–{b} players', t_winners: 'Winners bracket', t_losers: 'Losers bracket', t_grand: 'Grand final', t_decider: 'Decider', t_group: 'Group {g}', t_groups: 'Groups', t_ko_stage: 'Knockout stage',
    teams: 'Teams', n_teams: '{n} teams', team_n: 'Team {n}', teams_odd: 'For teams, add an even number of players.', teams_hint: 'Players 1 + 2, 3 + 4 … form a team and throw in turn. Shuffle for random teams. Team games do not count in personal statistics.',
    handicap: 'Handicap', handicap_hint: 'Own start value per player: tap − or + next to the name. Weaker players start lower.', bull5050: '50/50 bull', bull5050_hint: 'Outer bull counts 50', round_limit: 'Round limit', rl_short: '{n} rounds' });
  Object.assign(TEXTE.de, { tour_mode: 'Turnier', tour_dko: 'Doppel-K.-o.', tour_gr: 'Gruppen + K.-o.', s_tko: 'Wer verliert, ist raus', s_tdko: 'Raus nach zwei Niederlagen', s_tgr: 'Erst Gruppen, dann K.-o.', s_tliga: 'Jeder gegen jeden',
    dko_hint: 'Doppel-K.-o. für 3–16 Spieler: Wer in der Gewinnerrunde verliert, spielt in der Verliererrunde weiter, erst die zweite Niederlage beendet das Turnier. Im großen Finale muss der Sieger der Verliererrunde zweimal gewinnen.',
    gr_hint: 'Gruppen + K.-o. für 6–32 Spieler: 2, 4 oder 8 Gruppen, in der Gruppe spielt jeder gegen jeden. Die besten zwei jeder Gruppe kommen in die K.-o.-Runde, Spieler derselben Gruppe treffen dort nicht gleich aufeinander.',
    needs_tour: '{f} braucht {a}–{b} Spieler', t_winners: 'Gewinnerrunde', t_losers: 'Verliererrunde', t_grand: 'Großes Finale', t_decider: 'Entscheidungsspiel', t_group: 'Gruppe {g}', t_groups: 'Gruppen', t_ko_stage: 'K.-o.-Runde',
    teams: 'Teams', n_teams: '{n} Teams', team_n: 'Team {n}', teams_odd: 'Für Teams eine gerade Anzahl Spieler hinzufügen.', teams_hint: 'Spieler 1 + 2, 3 + 4 … bilden ein Team und werfen abwechselnd. Mischen ergibt zufällige Teams. Team-Spiele zählen nicht in der persönlichen Statistik.',
    handicap: 'Handicap', handicap_hint: 'Eigener Startwert je Spieler: − oder + neben dem Namen tippen. Schwächere starten niedriger.', bull5050: '50/50 Bull', bull5050_hint: 'Äußeres Bull zählt 50', round_limit: 'Rundenlimit', rl_short: '{n} Runden' });
  // keypad (1.17)
  // 1.25.0: more games
  Object.assign(TEXTE.en, {
    a_highscore: 'Count-Up', a_wild_mouse: 'Wild Mouse', a_mickey: 'Mickey Mouse', a_checkout: 'Checkout training', a_catch40: 'Catch 40', a_jdc: 'JDC Challenge', a_singles: 'Singles training',
    a_bermuda: 'Bermuda', a_rtw: 'Round the World', a_gotcha: 'Gotcha', a_nine_lives: 'Nine Lives', a_football: 'Football', a_scram: 'Scram',
    s_cricket: 'Close the numbers, score', s_wild_mouse: 'Cricket plus D, T, bed', s_mickey: 'Close 20–12, no points',
    s_atc: '1 to 20 and bull', s_doppel: 'Every double', s_bobs27: 'Doubles, start at 27', s_checkout121: 'Check out 121 and up', s_checkout: 'Random finishes',
    s_catch40: 'Finishes 61 to 100', s_jdc: 'Shanghai & doubles', s_singles: 'Every number once',
    s_shanghai: 'S, D, T in one visit', s_killer: 'Take their lives', s_halve_it: 'Miss and you halve', s_golf: 'Fewest strokes', s_baseball: 'Nine innings', s_highscore: 'Most points',
    s_bermuda: 'Halve-It, 13 targets', s_rtw: 'Race round the board', s_gotcha: 'Hit their score', s_nine_lives: '1 to 20, three lives', s_football: 'Bull, then doubles', s_scram: 'Stopper vs scorer',
    h_highscore: 'Count-Up: every dart counts its points. Most points after the visits win. A tie plays extra visits.',
    h_hidden: 'Hidden Cricket: six numbers and the bull, but the numbers stay hidden until somebody hits one. Then Cricket rules.',
    h_wild_mouse: 'Cricket on 20–15 and the bull plus three extra targets: any double, any treble and three in a bed (three darts in the same bed). A dart marks its own number first, otherwise the doubles or trebles. Closed targets score while an opponent has them open.',
    h_mickey: 'Close 20 to 12, three doubles, three trebles and the bull. No points – whoever closes everything first wins.',
    h_checkout: 'A random finish from 2 to 170. Check it out with a double within three visits. Most checkouts win.',
    h_catch40: 'Check out 61, 62 … 100 with a double, two visits each. 2 darts = 3 points, 3 darts = 2, second visit = 1. Maximum 120.',
    h_jdc: 'Part 1: Shanghai on 10–15 (single, double and treble in one visit = +100). Part 2: one dart at each double D1–D20 (50 each) and the bull (100). Part 3: Shanghai on 15–20.',
    h_singles: 'One visit at each number 1–20, then the bull. Single 1, double 2, treble 3 points. Maximum 186.',
    h_bermuda: 'Targets 12, 13, 14, any double, 15, 16, 17, any treble, 18, 19, 20, bull, bullseye. Start at 0 – no hit halves your points.',
    h_rtw: 'Hit 1 to 20 – up, down or in random order – then the bull. Every hit scores its points, the next dart already aims at the next number. First at the bull wins.',
    h_gotcha: 'Everyone counts up from 0 to the target. Land exactly on another player\'s score and they go back to 0. Overshooting is a bust. Hit the target exactly to win.',
    h_nine_lives: 'Hit 1 to 20 in order. A visit without hitting your number costs a life. First through or last one with lives wins.',
    h_football: 'Hit the bull to get the ball, then every double is a goal. First to the goals wins.',
    h_scram: 'Two players. The stopper closes 20–15 and the bull with three marks each, the scorer scores on everything still open. Then roles swap. Most points win.',
    z_hidden: 'Hidden', with_3b: 'On', without_3b: 'Off', halve_on: 'Halve', halve_off: 'Nothing', o_up: '1 → 20', o_down: '20 → 1',
    goals: 'Goals', order: 'Order', on_miss: 'No hit', three_bed: '3 in a bed', lbl_D: 'Dbl', lbl_T: 'Tpl', lbl_3B: '3·Bed',
    needs_exact: '{g} needs exactly {n} players.', needs_min: '{g} needs at least {n} players.',
    attempt2: 'Attempt {n} of 2', part_of: 'Part {n} of 3', to_go: '{n} to go', goals_w: 'goals', stopper: 'Stopper', scorer: 'Scorer',
    get_ball: '{n}: hit the bull to get the ball', has_ball: '{n} has the ball – every double is a goal', is_stopper: '{n} is the stopper – close the numbers', is_scorer: '{n} scores on open numbers',
    fx_gotcha: 'GOTCHA', fx_goal: 'GOAL', fx_swap: 'SWAP', fx_ball: 'BALL', back_to_0: '{n} back to 0', tie_extra: 'Tie – extra visit',
    ev_goal: 'Goal (football)', ev_gotcha: 'Gotcha', has_ball_s: 'has the ball', needs_bull: 'needs the bull first'
  });
  Object.assign(TEXTE.de, {
    a_highscore: 'Count-Up', a_wild_mouse: 'Wild Mouse', a_mickey: 'Mickey Mouse', a_checkout: 'Checkout-Training', a_catch40: 'Catch 40', a_jdc: 'JDC Challenge', a_singles: 'Singles-Training',
    a_bermuda: 'Bermuda', a_rtw: 'Rund um die Welt', a_gotcha: 'Gotcha', a_nine_lives: 'Neun Leben', a_football: 'Fußball', a_scram: 'Scram',
    s_cricket: 'Zahlen schließen, punkten', s_wild_mouse: 'Cricket plus D, T, Bed', s_mickey: '20–12 schließen',
    s_atc: '1 bis 20 und Bull', s_doppel: 'Jedes Doppel', s_bobs27: 'Doppel, Start bei 27', s_checkout121: 'Ab 121 auschecken', s_checkout: 'Zufällige Finishes',
    s_catch40: 'Finishes 61 bis 100', s_jdc: 'Shanghai & Doppel', s_singles: 'Jede Zahl einmal',
    s_shanghai: 'S, D, T in einer Runde', s_killer: 'Leben abnehmen', s_halve_it: 'Daneben halbiert', s_golf: 'Wenigste Schläge', s_baseball: 'Neun Innings', s_highscore: 'Meiste Punkte',
    s_bermuda: 'Halve-It, 13 Ziele', s_rtw: 'Wettlauf ums Board', s_gotcha: 'Stand treffen', s_nine_lives: '1 bis 20, drei Leben', s_football: 'Bull, dann Doppel', s_scram: 'Stopper vs. Scorer',
    h_highscore: 'Count-Up: Jeder Dart zählt seine Punkte. Die meisten Punkte nach den Aufnahmen gewinnen. Bei Gleichstand gibt es Extra-Aufnahmen.',
    h_hidden: 'Verdecktes Cricket: sechs Zahlen und Bull, aber die Zahlen sind verdeckt, bis jemand eine trifft. Dann gelten die Cricket-Regeln.',
    h_wild_mouse: 'Cricket auf 20–15 und Bull plus drei Extra-Ziele: beliebiges Double, beliebiges Triple und 3 in a Bed (drei Darts im selben Feld). Ein Dart markiert zuerst seine eigene Zahl, sonst Doubles oder Triples. Geschlossene Ziele punkten, solange ein Gegner sie offen hat.',
    h_mickey: 'Schließe 20 bis 12, drei Doubles, drei Triples und Bull. Ohne Punkte – wer zuerst alles zu hat, gewinnt.',
    h_checkout: 'Ein zufälliges Finish von 2 bis 170. Checke es mit einem Double in drei Aufnahmen. Die meisten Checkouts gewinnen.',
    h_catch40: 'Checke 61, 62 … 100 mit einem Double, je zwei Aufnahmen. 2 Darts = 3 Punkte, 3 Darts = 2, zweite Aufnahme = 1. Höchstens 120.',
    h_jdc: 'Teil 1: Shanghai auf 10–15 (Single, Double und Triple in einer Aufnahme = +100). Teil 2: je ein Dart auf D1–D20 (je 50) und Bull (100). Teil 3: Shanghai auf 15–20.',
    h_singles: 'Je eine Aufnahme auf 1–20, dann Bull. Single 1, Double 2, Triple 3 Punkte. Höchstens 186.',
    h_bermuda: 'Ziele 12, 13, 14, beliebiges Double, 15, 16, 17, beliebiges Triple, 18, 19, 20, Bull, Bullseye. Start bei 0 – kein Treffer halbiert deine Punkte.',
    h_rtw: 'Triff 1 bis 20 – auf-, absteigend oder zufällig –, dann Bull. Jeder Treffer zählt seine Punkte, der nächste Dart zielt schon auf die nächste Zahl. Wer zuerst Bull trifft, gewinnt.',
    h_gotcha: 'Alle zählen von 0 hoch bis zum Ziel. Wer genau auf dem Stand eines anderen landet, schickt ihn zurück auf 0. Zu viel ist überworfen. Wer das Ziel genau trifft, gewinnt.',
    h_nine_lives: 'Triff 1 bis 20 der Reihe nach. Eine Aufnahme ohne Treffer auf deine Zahl kostet ein Leben. Wer zuerst durch ist oder als Letzter noch Leben hat, gewinnt.',
    h_football: 'Triff Bull, dann hast du den Ball. Danach ist jedes Double ein Tor. Wer zuerst die Tore hat, gewinnt.',
    h_scram: 'Zwei Spieler. Der Stopper schließt 20–15 und Bull mit je drei Marks, der Scorer punktet auf allem, was noch offen ist. Dann Rollentausch. Die meisten Punkte gewinnen.',
    z_hidden: 'Verdeckt', with_3b: 'An', without_3b: 'Aus', halve_on: 'Halbieren', halve_off: 'Nichts', o_up: '1 → 20', o_down: '20 → 1',
    goals: 'Tore', order: 'Reihenfolge', on_miss: 'Kein Treffer', three_bed: '3 in a Bed', lbl_D: 'Dbl', lbl_T: 'Tpl', lbl_3B: '3·Bed',
    needs_exact: '{g} braucht genau {n} Spieler.', needs_min: '{g} braucht mindestens {n} Spieler.',
    attempt2: 'Versuch {n} von 2', part_of: 'Teil {n} von 3', to_go: 'noch {n}', goals_w: 'Tore', stopper: 'Stopper', scorer: 'Scorer',
    get_ball: '{n}: triff Bull, dann hast du den Ball', has_ball: '{n} hat den Ball – jedes Double ist ein Tor', is_stopper: '{n} ist Stopper – schließe die Zahlen', is_scorer: '{n} punktet auf offenen Zahlen',
    fx_gotcha: 'GOTCHA', fx_goal: 'TOR', fx_swap: 'WECHSEL', fx_ball: 'BALL', back_to_0: '{n} zurück auf 0', tie_extra: 'Gleichstand – Extra-Aufnahme',
    ev_goal: 'Tor (Fußball)', ev_gotcha: 'Gotcha', has_ball_s: 'hat den Ball', needs_bull: 'braucht erst Bull'
  });

  Object.assign(TEXTE.en, { kp_keys: 'Keys', kp_sum: 'Total', kp_board: 'Board', kp_cam: 'Camera', kp_miss: 'Miss', kp_sum_hint: 'points of the visit' });
  Object.assign(TEXTE.de, { kp_keys: 'Tasten', kp_sum: 'Summe', kp_board: 'Scheibe', kp_cam: 'Kamera', kp_miss: 'Daneben', kp_sum_hint: 'Punkte der Aufnahme' });
  // caller on this device (1.18)
  Object.assign(TEXTE.en, { caller_run: 'On speakers', phone_run: 'On this device', phone_hint: 'Plays the caller and the game sounds on this phone or tablet while a game card is open. Same as the speaker button in the game card.', d_caller: 'Announces scores, checkouts and walk-on songs on your speakers and phones' });
  Object.assign(TEXTE.de, { caller_run: 'Über Lautsprecher', phone_run: 'Auf diesem Gerät', phone_hint: 'Spielt Ansager und Spieltöne auf diesem Handy oder Tablet, solange eine Spielkarte offen ist. Wie der Lautsprecher-Knopf in der Spielkarte.', d_caller: 'Sagt Punkte, Checkouts und Einlaufmusik über Lautsprecher und Handys an' });
  // caller card step by step (1.21)
  Object.assign(TEXTE.en, { k_try: 'Listen to a sample', k_try_hint: 'Plays "140 · {n}, you require 92" where you switched it on below.', k_no_out: 'Switch on below where you want to hear the caller.',
    k_s1: '1 · Where do you hear it?', k_s2: '2 · Which voice?', k_s3: '3 · What is announced?', k_s4: 'Walk-on songs', k_pick_sp: 'Choose speakers', k_n_sel: '{n} chosen',
    k_live: 'Normal voice', k_live_sub: '{v} · speaks live', k_voice_set: 'Voice for live speech', k_own: 'Upload your own sounds',
    k_done: 'Ready · {n} sounds', k_run: 'Being made … {n} of {m}', k_wait: '{f} of {m} · continues by itself (Google allows 100 a day)', k_part: 'Incomplete · {n} missing', k_ownp: 'Own pack · {n} sounds', k_empty: 'Empty',
    k_new: 'New championship pack', k_new_text: 'Google speaks every score, "you require", game shot and your player names once ({m} sounds) and saves them, so later they play at once, also without internet. Google allows 100 sounds a day: a pack takes up to 2 days. It runs in the background and continues by itself.',
    k_choose: 'Choose a speaker', k_sample: 'Sample', k_have: 'already there', k_make: 'Make pack', k_make_rest: 'Make missing sounds', k_cancel: 'Cancel', k_close: 'Close', k_busy: '"{p}" is being made right now. A new pack can start when it is ready or stopped.',
    k_use: 'Use this pack', k_in_use: 'In use', k_go_on: 'Make missing sounds', k_stop: 'Stop', k_del: 'Delete …', k_del_q: 'Delete "{p}"?', k_del_text: 'All {n} sounds of this pack are deleted. This cannot be undone. Making it again takes up to 2 days because of the Google limit.', k_del_ok: 'Delete for good',
    k_err: 'Stopped: {e}', k_stopped: 'Stopped. Tap "Make missing sounds" to continue.', k_need_google: 'Championship packs need the voice "Google AI" (Settings → Voice assistants). Without it the normal voice speaks.',
    sp_fenrir: 'excited', sp_algenib: 'gravelly', sp_alnilam: 'firm', sp_orus: 'firm, deep', sp_puck: 'upbeat', sp_charon: 'calm' });
  Object.assign(TEXTE.de, { k_try: 'Probe hören', k_try_hint: 'Spielt „140 · {n}, du brauchst 92“ dort, wo du es unten eingeschaltet hast.', k_no_out: 'Schalte unten ein, wo du den Ansager hören willst.',
    k_s1: '1 · Wo hörst du den Ansager?', k_s2: '2 · Welche Stimme?', k_s3: '3 · Was wird angesagt?', k_s4: 'Einlaufmusik', k_pick_sp: 'Lautsprecher wählen', k_n_sel: '{n} gewählt',
    k_live: 'Normale Stimme', k_live_sub: '{v} · spricht live', k_voice_set: 'Stimme für Live-Sätze', k_own: 'Eigene Töne hochladen',
    k_done: 'Fertig · {n} Töne', k_run: 'Wird erzeugt … {n} von {m}', k_wait: '{f} von {m} · macht von selbst weiter (Google erlaubt 100 am Tag)', k_part: 'Unvollständig · {n} fehlen', k_ownp: 'Eigenes Pack · {n} Töne', k_empty: 'Leer',
    k_new: 'Neues Meisterschafts-Pack', k_new_text: 'Google spricht einmal alle Punkte, „du brauchst“, Game shot und eure Spielernamen ({m} Töne) und speichert sie. Danach kommen die Ansagen sofort, auch ohne Internet. Google erlaubt 100 Töne am Tag, ein Pack dauert also bis zu 2 Tage. Es läuft im Hintergrund und macht von selbst weiter.',
    k_choose: 'Sprecher wählen', k_sample: 'Probe', k_have: 'schon da', k_make: 'Pack erzeugen', k_make_rest: 'Fehlende Töne erzeugen', k_cancel: 'Abbrechen', k_close: 'Schließen', k_busy: '„{p}“ wird gerade erzeugt. Ein neues Pack geht, wenn es fertig oder angehalten ist.',
    k_use: 'Dieses Pack benutzen', k_in_use: 'Wird benutzt', k_go_on: 'Fehlende Töne erzeugen', k_stop: 'Anhalten', k_del: 'Löschen …', k_del_q: '„{p}“ löschen?', k_del_text: 'Alle {n} Töne dieses Packs werden gelöscht. Das lässt sich nicht rückgängig machen. Neu erzeugen dauert wegen des Google-Limits bis zu 2 Tage.', k_del_ok: 'Endgültig löschen',
    k_err: 'Angehalten: {e}', k_stopped: 'Angehalten. „Fehlende Töne erzeugen“ macht weiter.', k_need_google: 'Meisterschafts-Packs brauchen die Stimme „Google AI“ (Einstellungen → Sprachassistenten). Ohne sie spricht die normale Stimme.',
    sp_fenrir: 'aufgeregt', sp_algenib: 'rau', sp_alnilam: 'bestimmt', sp_orus: 'fest, tief', sp_puck: 'fröhlich', sp_charon: 'ruhig' });
  // listening to the score sounds (1.23)
  Object.assign(TEXTE.en, { k_listen: 'Check the sounds', k_listening: 'Listening to the sounds … {n} of {m}', k_redo: '{n} sounds said the wrong number · being spoken again',
    k_listen_ok: 'All scores checked', k_listen_hint: 'Home Assistant listens to every score sound once (speech recognition). A sound that says the wrong number is spoken again in the background; until then the old one plays.' });
  Object.assign(TEXTE.de, { k_listen: 'Töne prüfen', k_listening: 'Hört die Töne an … {n} von {m}', k_redo: '{n} Töne sagten die falsche Zahl · werden neu gesprochen',
    k_listen_ok: 'Alle Punkte geprüft', k_listen_hint: 'Home Assistant hört jeden Punkte-Ton einmal an (Spracherkennung). Sagt ein Ton die falsche Zahl, wird er im Hintergrund neu gesprochen, bis dahin spielt der alte.' });
  const SPRECHER = [['fenrir', 'Fenrir'], ['algenib', 'Algenib'], ['alnilam', 'Alnilam'], ['orus', 'Orus'], ['puck', 'Puck'], ['charon', 'Charon']];
  // aim map (1.16)
  Object.assign(TEXTE.en, { t_aim: 'Aim', aim_best: 'Best aim point', aim_avg: 'about Ø {n} per visit', aim_vs: 'T20 gives Ø {n} – {d} more here.', aim_t20: 'T20 is the right target for you.', aim_hint: 'Calculated from your average (Ø {a}, spread about {s} mm). Red = most points.', aim_no_avg: 'Play an X01 game first.' });
  Object.assign(TEXTE.de, { t_aim: 'Zielen', aim_best: 'Bester Zielpunkt', aim_avg: 'etwa Ø {n} pro Aufnahme', aim_vs: 'Auf T20 Ø {n} – hier {d} mehr.', aim_t20: 'T20 ist für dich das richtige Ziel.', aim_hint: 'Berechnet aus deinem Average (Ø {a}, Streuung etwa {s} mm). Rot = die meisten Punkte.', aim_no_avg: 'Spiele zuerst ein X01-Spiel.' });
  const sprache = h => { const l = String((h && ((h.locale && h.locale.language) || h.language)) || navigator.language || 'en'); return l.slice(0, 2) === 'de' ? 'de' : 'en'; };
  let SPR = sprache(null);
  const t = (k, v) => { let s = (TEXTE[SPR] || TEXTE.en)[k]; if (s === undefined) s = TEXTE.en[k] || k; if (v) Object.keys(v).forEach(x => { s = s.split('{' + x + '}').join(v[x]); }); return s; };

  /* ---------- helpers ---------- */
  const BASIS = `
:host{display:block}
ha-card{padding:14px;box-sizing:border-box}
.titel{display:flex;align-items:center;gap:8px;font-weight:600;font-size:13px;letter-spacing:.02em;color:var(--secondary-text-color);margin:14px 2px 8px}
.titel ha-icon{--mdc-icon-size:16px}
button{font:inherit;color:inherit;border:none;cursor:pointer;-webkit-tap-highlight-color:transparent;transition:transform .12s ease,background .25s ease,box-shadow .25s ease,color .25s ease,opacity .25s ease}
button:active{transform:scale(.95)}
button:disabled{opacity:.38;cursor:default;transform:none}
.feld{background:color-mix(in srgb,var(--primary-text-color) 7%,transparent);border:1px solid color-mix(in srgb,var(--primary-text-color) 10%,transparent)}
:host .scharf{animation:ad-scharf .9s ease-in-out infinite}
@keyframes ad-scharf{50%{box-shadow:0 0 0 5px color-mix(in srgb,var(--sr-f,#e53935) 35%,transparent)}}
@media (prefers-reduced-motion:reduce){:host .scharf{animation:none}}
.klein{font-size:12px;color:var(--secondary-text-color);margin:10px 2px 0;line-height:1.4}`;
  const st = (h, id) => (h && id && h.states[id]) || null;
  const zst = (h, id) => (st(h, id) || {}).state;
  const an = (h, id) => zst(h, id) === 'on';
  const da = (h, id) => { const s = zst(h, id); return s !== undefined && s !== 'unavailable' && s !== 'unknown'; };
  const num = (h, id) => { const v = parseFloat(zst(h, id)); return isNaN(v) ? 0 : v; };
  let LOC = 'en';
  const zahl = (x, d) => Number(x).toLocaleString(LOC, { minimumFractionDigits: d || 0, maximumFractionDigits: d || 0 });
  const aktion = (h, dom, srv, data) => {
    try { window.dispatchEvent(new CustomEvent('haptic', { detail: 'medium', bubbles: true, composed: true })); } catch (e) {}
    h.callService(dom, srv, data);
  };
  // switch on / off / press any kind of entity (script, switch, button, automation, scene …)
  const ausloesen = (h, id, aus) => {
    const dom = String(id).split('.')[0];
    if (dom === 'button' || dom === 'input_button') aktion(h, dom, 'press', { entity_id: id });
    else if (dom === 'automation') aktion(h, dom, 'trigger', { entity_id: id });
    else aktion(h, dom === 'script' || dom === 'scene' ? dom : (dom || 'homeassistant'), aus && dom !== 'script' && dom !== 'scene' ? 'turn_off' : 'turn_on', { entity_id: id });
  };
  const gehe = pfad => { history.pushState(null, '', pfad); window.dispatchEvent(new CustomEvent('location-changed', { detail: { replace: false } })); };
  const att = (h, id) => (st(h, id) || {}).attributes || {};
  // power plug of the board PC, chosen once in the Board Manager card; a card's own power_* options win
  const stromCfg = h => {
    const s = att(h, E(h, 'sensor.players')).strom || {};
    return s.schalter || s.einschalten ? { power_on: s.einschalten || s.schalter, power_off: s.ausschalten || s.schalter, power_switch: s.schalter || undefined, power_sensor: s.leistung || undefined, pc_online: s.pc_online || undefined } : {};
  };
  const ft = f => ({ S25: '25', D25: 'Bull', M: 'Miss' }[f] || f || '–');
  const pkt = f => { if (!f || f === 'M') return 0; return ({ S: 1, D: 2, T: 3 }[f[0]] || 0) * parseInt(f.slice(1), 10); };
  const esc = x => String(x == null ? '' : x).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const mehrInfo = (el, id) => { if (!id) return; const ev = new Event('hass-more-info', { bubbles: true, composed: true }); ev.detail = { entityId: id }; el.dispatchEvent(ev); };

  // Entities of the integration, found by their translation key (independent of entity IDs and language)
  const ALT = {
    'sensor.connection': 'sensor.autodarts_board_verbindung', 'sensor.status': 'sensor.autodarts_board_status', 'sensor.visit_score': 'sensor.autodarts_board_aktuelle_aufnahme',
    'sensor.throw_1': 'sensor.autodarts_board_wurf_1', 'sensor.throw_2': 'sensor.autodarts_board_wurf_2', 'sensor.throw_3': 'sensor.autodarts_board_wurf_3',
    'sensor.game': 'sensor.autodarts_board_spiel', 'sensor.players': 'sensor.autodarts_board_spieler'
  };
  let entCache = null, entQuelle = null;
  const E = (h, key) => {
    if (h && h.entities !== entQuelle) {
      entQuelle = h.entities; entCache = {};
      Object.values(h.entities || {}).forEach(e => { if (e && e.platform === 'autodarts' && e.translation_key) entCache[e.entity_id.split('.')[0] + '.' + e.translation_key] = e.entity_id; });
    }
    return (entCache && entCache[key]) || ALT[key] || null;
  };
  const boardOnline = h => { const v = zst(h, E(h, 'sensor.connection')); return v !== undefined && v !== 'Offline' && v !== 'unavailable'; };
  const boardUrl = h => {
    const id = E(h, 'sensor.connection'), e = h && h.entities && h.entities[id], d = e && h.devices && h.devices[e.device_id];
    return (d && d.configuration_url) || null;
  };
  const sprachePruefen = h => { SPR = sprache(h); LOC = (h && h.locale && h.locale.language) || (SPR === 'de' ? 'de-DE' : 'en'); };
  // game phase from the attributes (language independent)
  const phase = a => ({ bulloff: 'bulloff', laeuft: 'running', beendet: 'finished' }[a && a.phase] || 'idle');
  const modusText = e => {
    if (e && e.spiel && e.spiel !== 'x01') {
      const teile = [t('a_' + e.spiel)];
      if (e.spiel === 'cricket') { teile.push(t('v_' + (e.variante || 'standard'))); if (['tactics', 'random', 'hidden'].includes(e.zahlen)) teile.push(t('z_' + e.zahlen)); }
      if (e.spiel === 'gotcha') teile.push(String(e.zielwert || 301));
      if (e.spiel === 'football') teile.push((e.zielwert || 10) + ' ' + t('goals'));
      if (e.spiel === 'atc' && e.variante && e.variante !== 'single') teile.push(t(e.variante === 'double' ? 'double' : 'treble'));
      if (+e.legs > 1) teile.push(t('first_legs', { n: e.legs }));
      return teile.join(' · ');
    }
    if (!e || !e.startwert) return '';
    const teile = [String(e.startwert)];
    if (e.einwurf === 'double') teile.push(t('din')); else if (e.einwurf === 'master') teile.push(t('min'));
    teile.push(t({ straight: 'sout', double: 'dout', master: 'mout' }[e.auswurf] || 'dout'));
    if (e.sets) teile.push(t('sets_legs', { s: e.sets, l: e.legs })); else teile.push(t(+e.legs > 1 ? 'first_legs' : 'first_leg', { n: e.legs }));
    return teile.join(' · ');
  };
  // tap twice: first tap asks, second tap confirms (4 s)
  function zweimal(karte, knopf, frage, los) {
    const lbl = b => b.querySelector('.lbl');
    if (karte._scharf === knopf) {
      karte._scharf = null; clearTimeout(karte._st); knopf.classList.remove('scharf');
      lbl(knopf).textContent = knopf.dataset.lbl; los(); return;
    }
    if (karte._scharf) { karte._scharf.classList.remove('scharf'); lbl(karte._scharf).textContent = karte._scharf.dataset.lbl; }
    karte._scharf = knopf; knopf.classList.add('scharf'); lbl(knopf).textContent = frage;
    clearTimeout(karte._st);
    karte._st = setTimeout(() => { knopf.classList.remove('scharf'); lbl(knopf).textContent = knopf.dataset.lbl; karte._scharf = null; }, 4000);
  }

  /* ---------- Overview card with scene ---------- */
  const G = 'var(--green-color,#43a047)', A = 'var(--amber-color,#ffc107)', R = 'var(--red-color,#e53935)', GR = 'var(--disabled-color,#9e9e9e)', B = 'var(--blue-color,#2196f3)';
  const SZ = {
    aus: ['sc_off', 'mdi:power-sleep'], startet: ['sc_starting', 'mdi:timer-sand'], runter: ['sc_stopping', 'mdi:power'], bereit: ['sc_ready', 'mdi:target'],
    ziehen: ['sc_takeout', 'mdi:hand-back-left-outline'], kalib: ['sc_calib', 'mdi:crosshairs-gps'], gestoppt: ['sc_stopped', 'mdi:stop-circle-outline'], standby: ['sc_standby', 'mdi:sleep'], weg: ['sc_lost', 'mdi:wifi-alert']
  };
  const ORDER = [20, 1, 18, 4, 13, 6, 10, 15, 2, 17, 3, 19, 7, 16, 8, 11, 14, 9, 12, 5];
  const CX = 166, CY = 78, K = 50 / 170;
  const pol = (r, w) => { const a = (w - 90) * Math.PI / 180; return [CX + r * Math.cos(a), CY + r * Math.sin(a)]; };
  const f1 = v => v.toFixed(2);
  const sektor = (r1, r2, w1, w2, fill) => {
    const [a, b] = pol(r2, w1), [c, d] = pol(r2, w2), [e, f] = pol(r1, w2), [g, hh] = pol(r1, w1);
    return '<path d="M' + f1(a) + ' ' + f1(b) + 'A' + r2 + ' ' + r2 + ' 0 0 1 ' + f1(c) + ' ' + f1(d) + 'L' + f1(e) + ' ' + f1(f) + 'A' + r1 + ' ' + r1 + ' 0 0 0 ' + f1(g) + ' ' + f1(hh) + 'Z" fill="' + fill + '"/>';
  };
  const scheibe = () => {
    const R1 = 15.9 * K, T1 = 99 * K, T2 = 107 * K, D1 = 162 * K, D2 = 170 * K;
    let s = '';
    ORDER.forEach((n, i) => {
      const w1 = i * 18 - 9, w2 = w1 + 18, dunkel = i % 2 === 0;
      const ein = dunkel ? 'url(#adS)' : 'url(#adW)', farbe = dunkel ? '#b3261e' : '#1f7a3a';
      s += sektor(R1, T1, w1, w2, ein) + sektor(T1, T2, w1, w2, farbe) + sektor(T2, D1, w1, w2, ein) + sektor(D1, D2, w1, w2, farbe);
      const [x, y] = pol(55.5, i * 18);
      s += '<text x="' + f1(x) + '" y="' + f1(y + 2.4) + '">' + n + '</text>';
    });
    let d = '';
    for (let i = 0; i < 20; i++) { const [a, b] = pol(R1, i * 18 - 9), [c, e] = pol(D2, i * 18 - 9); d += 'M' + f1(a) + ' ' + f1(b) + 'L' + f1(c) + ' ' + f1(e); }
    s += '<path d="' + d + '" stroke="#c9ced3" stroke-opacity=".55" stroke-width=".35"/>';
    s += [R1, T1, T2, D1, D2].map(r => '<circle cx="' + CX + '" cy="' + CY + '" r="' + f1(r) + '" fill="none" stroke="#c9ced3" stroke-opacity=".55" stroke-width=".35"/>').join('');
    s += '<circle cx="' + CX + '" cy="' + CY + '" r="' + f1(R1) + '" fill="#1f7a3a" stroke="#c9ced3" stroke-opacity=".6" stroke-width=".35"/><circle cx="' + CX + '" cy="' + CY + '" r="' + f1(6.35 * K) + '" fill="#b3261e"/>';
    return s;
  };
  const kameras = () => [30, 150, 270].map(w => { const [x, y] = pol(66, w); return '<g transform="translate(' + f1(x) + ' ' + f1(y) + ') rotate(' + (w + 180) + ')"><rect x="-4" y="-3" width="8" height="6" rx="1.6" fill="#202428" stroke="#3b4248" stroke-width=".6"/><circle cx="0" cy="3" r="1.6" fill="#0a0c0e" stroke="#5d666d" stroke-width=".5"/><circle cx="-.4" cy="2.6" r=".45" fill="#9fd3ff" fill-opacity=".7"/></g>'; }).join('');
  const DART = '<g class="dart"><g class="dartin" transform="scale(1.7)"><ellipse cx="1.6" cy="1.4" rx="3" ry="1" fill="#000" fill-opacity=".35"/>' +
    '<path d="M0 0L3 3" stroke="#d8dde1" stroke-width=".7"/><path d="M2.6 2.6L8.6 8.6" stroke="url(#adBar)" stroke-width="2.4" stroke-linecap="round"/>' +
    '<path d="M3.6 3.6l4 4" stroke="#fff" stroke-opacity=".35" stroke-width=".5"/><path d="M8.4 8.4L12 12" stroke="#2b2f33" stroke-width="1"/>' +
    '<path d="M11 11l5.5 1.5l-1.5 -1.5l1.5 -5.5z" style="fill:var(--fl,#e53935)" stroke="#000" stroke-opacity=".3" stroke-width=".3"/></g></g>';
  const position = (txt, i, a) => {
    if (a && typeof a.x === 'number' && typeof a.y === 'number') {
      const r = Math.hypot(a.x, a.y), f = r > 1.18 ? 1.18 / r : 1;
      return [CX + a.x * f * 50, CY - a.y * f * 50];
    }
    const x = String(txt || '').toUpperCase().trim();
    if (!x || x === '-' || x === 'UNAVAILABLE' || x === 'UNKNOWN') return null;
    const j = [-4, 3, 0][i];
    if (['50', 'DB', 'BULL', 'D25', 'BULLSEYE'].includes(x)) return pol(1.2 + i * .6, i * 120);
    if (['25', 'SB', 'S25'].includes(x)) return pol(3.4, 40 + i * 120);
    if (x[0] === 'M') return pol(59.5, 200 + i * 35);
    const m = x.match(/^([SDT]?)(\d{1,2})$/); if (!m) return null;
    const idx = ORDER.indexOf(parseInt(m[2], 10)); if (idx < 0) return null;
    const r = m[1] === 'T' ? 30.3 : m[1] === 'D' ? 48.8 : 41 + j / 2;
    return pol(r, idx * 18 + j);
  };
  const SZENE = '<svg viewBox="0 0 240 170">' +
    '<defs><radialGradient id="adWand" cx=".7" cy=".45" r=".7"><stop offset="0" stop-color="#3a3f47"/><stop offset="1" stop-color="#15181c"/></radialGradient>' +
    '<radialGradient id="adS" cx="166" cy="78" r="50" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#2a2a2a"/><stop offset="1" stop-color="#121212"/></radialGradient>' +
    '<radialGradient id="adW" cx="166" cy="78" r="50" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="#f3ead2"/><stop offset="1" stop-color="#d9caa3"/></radialGradient>' +
    '<radialGradient id="adLicht" cx=".5" cy=".5" r=".5"><stop offset=".78" style="stop-color:var(--ring)" stop-opacity="0"/><stop offset=".86" style="stop-color:var(--ring)" stop-opacity=".55"/><stop offset="1" style="stop-color:var(--ring)" stop-opacity="0"/></radialGradient>' +
    '<linearGradient id="adBar" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e9edf0"/><stop offset=".5" stop-color="#8d969d"/><stop offset="1" stop-color="#5a6268"/></linearGradient>' +
    '<linearGradient id="adPc" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3b4046"/><stop offset="1" stop-color="#1b1e21"/></linearGradient></defs>' +
    '<rect width="240" height="170" fill="url(#adWand)"/>' +
    '<path d="M0 150h240v20H0z" fill="#3b2a1e"/><path d="M0 150h240" stroke="#5a4130" stroke-width="1.5"/>' +
    '<circle class="schein" cx="' + CX + '" cy="' + CY + '" r="84" fill="url(#adLicht)"/>' +
    '<circle cx="' + CX + '" cy="' + CY + '" r="62" fill="#0f1113"/><circle cx="' + CX + '" cy="' + CY + '" r="62" fill="none" stroke="#000" stroke-opacity=".5" stroke-width="2"/>' +
    '<circle cx="' + CX + '" cy="' + CY + '" r="52" fill="#141414"/>' +
    '<g class="zahlen" fill="#e8e8e8" font-size="6" font-weight="700" text-anchor="middle" font-family="Arial,sans-serif">' + scheibe() + '</g>' +
    '<circle class="ring" cx="' + CX + '" cy="' + CY + '" r="66" fill="none" style="stroke:var(--ring)" stroke-width="3"/>' +
    '<circle class="scan" cx="' + CX + '" cy="' + CY + '" r="66" fill="none" stroke="#fff" stroke-width="3" stroke-dasharray="40 375" stroke-linecap="round"/>' +
    '<circle cx="' + CX + '" cy="' + CY + '" r="68" fill="none" stroke="#2a2f34" stroke-width="1.2"/>' + kameras() +
    '<g class="darts">' + [0, 1, 2].map(i => '<g class="d d' + i + '">' + DART + '</g>').join('') + '</g>' +
    '<g class="pc"><ellipse cx="224" cy="161" rx="15" ry="2" fill="#000" fill-opacity=".45"/><rect x="209" y="150" width="30" height="10" rx="2" fill="url(#adPc)"/><rect x="209" y="150" width="30" height="1.2" rx=".6" fill="#fff" fill-opacity=".18"/>' +
    '<circle class="pcled" cx="234" cy="155" r="1.1" style="fill:var(--pcl)"/><path d="M213 154.5h10" stroke="#555c63" stroke-width=".8" stroke-dasharray="1 1"/>' +
    '<path d="M209 156C200 156 196 148 186 146" fill="none" stroke="#111" stroke-width="1"/></g>' +
    '<rect class="dunkel" width="240" height="170" fill="#05070a"/>' +
    '</svg>';
  const B_CSS = `
.szene{position:relative;overflow:hidden;cursor:pointer;height:180px;border-radius:18px;background:#15181c;--ring:#ffffff;--pcl:#43a047}
.szene svg{position:absolute;right:0;top:0;height:100%;width:auto;aspect-ratio:240/170;display:block}
.ueber{position:absolute;inset:0 auto 0 0;width:58%;padding:14px 16px;box-sizing:border-box;display:flex;flex-direction:column;justify-content:flex-end;color:#fff;text-shadow:0 1px 3px rgba(0,0,0,.65);
 background:linear-gradient(90deg,rgba(9,11,14,.9),rgba(9,11,14,.65) 55%,transparent)}
.zt{display:flex;align-items:center;gap:8px;font-size:22px;font-weight:700;line-height:1.2}
.zt ha-icon{--mdc-icon-size:24px;color:#fff;filter:drop-shadow(0 1px 2px rgba(0,0,0,.6))}
.art{font-size:13px;color:rgba(255,255,255,.82);margin-top:2px}
.ring,.scan,.schein,.dunkel,.pcled,.d{transition:opacity .6s ease}
.scan{opacity:0;transform-box:fill-box;transform-origin:center}
.dunkel{opacity:0;pointer-events:none}
.d{opacity:0}.d.an{opacity:1}
.d.an .dart{animation:ad-rein .35s cubic-bezier(.2,.9,.3,1.3) both}
.dart{transform-box:fill-box;transform-origin:0 0}
.d1{--fl:#1e88e5}.d2{--fl:#fdd835}
:host([sz=aus]) .ring,:host([sz=aus]) .schein,:host([sz=aus]) .pcled{opacity:0}
:host([sz=aus]) .dunkel{opacity:.45}
:host([sz=startet]) .szene,:host([sz=runter]) .szene{--ring:#ffb300;--pcl:#ffb300}
:host([sz=startet]) .ring,:host([sz=startet]) .schein,:host([sz=runter]) .ring,:host([sz=runter]) .schein,:host([sz=startet]) .pcled,:host([sz=runter]) .pcled{animation:ad-atmen 1.6s ease-in-out infinite}
:host([sz=startet]) .dunkel,:host([sz=runter]) .dunkel{opacity:.25}
:host([sz=ziehen]) .szene{--ring:#ffb300}
:host([sz=ziehen]) .d.an{animation:ad-blink 1.1s ease-in-out infinite}
:host([sz=kalib]) .szene{--ring:#4dd0c4}
:host([sz=kalib]) .scan{opacity:.9;animation:ad-dreh 1.4s linear infinite}
:host([sz=gestoppt]) .szene,:host([sz=standby]) .szene{--ring:#64b5f6}
:host([sz=gestoppt]) .schein,:host([sz=standby]) .schein{opacity:.35}
:host([sz=weg]) .szene{--ring:#ffb300}
:host([sz=weg]) .ring{animation:ad-blink 1.2s ease-in-out infinite}
:host([still]) *{animation-play-state:paused!important}
@media (prefers-reduced-motion:reduce){*{animation:none!important}}
@keyframes ad-atmen{0%,100%{opacity:.3}50%{opacity:1}}
@keyframes ad-blink{0%,100%{opacity:.35}50%{opacity:1}}
@keyframes ad-dreh{to{transform:rotate(360deg)}}
@keyframes ad-rein{0%{transform:translate(9px,9px) scale(1.5);opacity:0}100%{transform:none;opacity:1}}
.live{display:none;grid-template-columns:repeat(3,1fr) 1.25fr;gap:8px;margin-top:10px}
:host([online]) .live{display:grid}
.w{border-radius:16px;padding:8px 4px;text-align:center;display:flex;flex-direction:column;gap:1px;cursor:pointer}
.w small{font-size:11.5px;color:var(--secondary-text-color);font-weight:600}
.w b{font-size:19px;font-weight:700;line-height:1.2}
.w.sum{background:color-mix(in srgb,var(--green-color,#43a047) 16%,transparent);border-color:color-mix(in srgb,var(--green-color,#43a047) 40%,transparent)}
.w.sum b{font-size:24px}
.w.leer b{color:var(--secondary-text-color);font-weight:500}
.zeile{display:none;font-size:13px;color:var(--secondary-text-color);margin:8px 2px 0}
.zeile b{color:var(--primary-text-color)}
:host([online]) .zeile.hat{display:block}
.knoepfe{display:grid;grid-template-columns:repeat(var(--n,4),1fr);gap:8px;margin-top:10px}
.knoepfe.haupt4{grid-template-columns:1.4fr 1fr 1fr 1fr}
.knoepfe:empty{display:none}
.laeuft{display:flex;align-items:center;gap:10px;width:100%;margin-top:10px;border-radius:14px;padding:10px 12px;text-align:left;font-size:13.5px;line-height:1.35}
.laeuft>ha-icon{--mdc-icon-size:20px;color:var(--red-color,#e53935);flex:none}.laeuft span{flex:1;min-width:0}.laeuft u{text-decoration:none;color:var(--red-color,#e53935);font-weight:700}
.k{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:5px;min-height:70px;border-radius:18px;padding:8px 4px;font-size:13px;font-weight:600;--sr-f:var(--k)}
.k ha-icon{--mdc-icon-size:24px;color:var(--k)}
.k.haupt{flex-direction:row;gap:10px;font-size:16px;color:#fff;background:linear-gradient(135deg,color-mix(in srgb,var(--k) 92%,#fff 8%),color-mix(in srgb,var(--k) 70%,#000 30%));box-shadow:0 4px 14px color-mix(in srgb,var(--k) 35%,transparent)}
.k.haupt ha-icon{color:#fff;--mdc-icon-size:28px}
@media (max-width:520px){.szene{height:160px}.ueber{width:62%}.zt{font-size:20px}.knoepfe.haupt4{grid-template-columns:1fr 1fr 1fr}.k.haupt{grid-column:1/-1;min-height:56px}}`;
  class AutodartsOverviewCard extends HTMLElement {
    static getStubConfig() { return {}; }
    setConfig(c) { this._orig = Object.assign({}, c || {}); this._c = Object.assign({}, this._orig); this._stromKey = null; if (this._r) { this._r = null; this.shadowRoot.innerHTML = ''; } }
    getCardSize() { return 5; }
    getGridOptions() { return { columns: 12, min_columns: 6 }; }
    set hass(h) {
      this._h = h; sprachePruefen(h);
      const sc = this._orig.power_on ? {} : stromCfg(h), key = JSON.stringify(sc);
      if (key !== this._stromKey) { this._stromKey = key; this._c = Object.assign({}, sc, this._orig); this._r = null; }
      if (!this._r || this._spr !== SPR) this._bauen();
      this._zeichnen();
    }
    _bauen() {
      this._spr = SPR;
      this._r = this.shadowRoot || this.attachShadow({ mode: 'open' });
      const c = this._c;
      const k = (cls, id, lbl, icon, f) => '<button class="k ' + cls + '" data-id="' + id + '" data-lbl="' + lbl + '" style="--k:' + f + '"><ha-icon icon="' + icon + '"></ha-icon><span class="lbl">' + lbl + '</span></button>';
      const kn = [];
      if (c.power_on) kn.push(k('haupt', 'ein', t('on'), 'mdi:power', G));
      if (c.game_path) kn.push(k('feld', 'spielen', t('play'), 'mdi:bullseye-arrow', R));
      if (c.manager_path) kn.push(k('feld', 'mgr', c.manager_label || t('manager'), c.manager_icon || 'mdi:camera-iris', 'var(--purple-color,#9c27b0)'));
      if (c.players_path) kn.push(k('feld', 'spieler', t('players'), 'mdi:account-group', B));
      this._r.innerHTML = '<style>' + BASIS + B_CSS + '</style><ha-card><div class="szene">' + SZENE +
        '<div class="ueber"><div class="zt"><ha-icon></ha-icon><span class="zn"></span></div><div class="art"></div></div></div>' +
        '<div class="live">' + [0, 1, 2].map(i => '<div class="w feld" data-i="' + i + '"><small>' + t('dart') + ' ' + (i + 1) + '</small><b>–</b></div>').join('') +
        '<div class="w feld sum"><small>' + t('visit') + '</small><b>0</b></div></div>' +
        '<div class="zeile"></div><button class="laeuft feld"></button>' +
        '<div class="knoepfe' + (c.power_on && kn.length === 4 ? ' haupt4' : '') + '" style="--n:' + kn.length + '">' + kn.join('') + '</div></ha-card>';
      this._sicht = true;
      const still = () => this.toggleAttribute('still', !this._sicht || document.hidden);
      if (!this._io && 'IntersectionObserver' in window) { this._io = new IntersectionObserver(e => { this._sicht = e[0].isIntersecting; still(); }); this._io.observe(this); }
      if (!this._vis) { this._vis = still; document.addEventListener('visibilitychange', still); }
      this._r.querySelector('.szene').addEventListener('click', () => mehrInfo(this, E(this._h, 'sensor.status')));
      this._r.querySelectorAll('.w').forEach(w => w.addEventListener('click', () => mehrInfo(this, E(this._h, w.classList.contains('sum') ? 'sensor.visit_score' : 'sensor.throw_' + (+w.dataset.i + 1)))));
      this._r.querySelector('.knoepfe').addEventListener('click', e => {
        const b = e.target.closest('button'); if (!b || b.disabled) return; const h = this._h, id = b.dataset.id;
        if (id === 'ein') {
          if (b.dataset.modus === 'aus') zweimal(this, b, t('off_q'), () => { this._runterBis = Date.now() + 180000; this._startBis = 0; ausloesen(h, c.power_off || c.power_on, true); this._zeichnen(); });
          else { this._startBis = Date.now() + 180000; this._runterBis = 0; ausloesen(h, c.power_on, false); this._zeichnen(); }
        } else if (id === 'mgr') gehe(c.manager_path);
        else if (id === 'spielen') gehe(c.game_path);
        else if (id === 'spieler') gehe(c.players_path);
      });
      this._r.querySelector('.laeuft').addEventListener('click', () => c.game_path && gehe(c.game_path));
    }
    _szene() {
      const h = this._h, c = this._c, jetzt = Date.now();
      const v = zst(h, E(h, 'sensor.connection')), s = zst(h, E(h, 'sensor.status')), pc = an(h, c.pc_online);
      const online = v !== undefined && v !== 'Offline' && v !== 'unavailable' && s !== 'Offline';
      const dose = zst(h, c.power_switch), watt = da(h, c.power_sensor) ? num(h, c.power_sensor) : null;
      if (this._runterBis > jetzt && (pc || online || (dose === 'on' && (watt === null || watt > 6)))) return 'runter';
      if (online) {
        if (s === 'throw') return 'bereit';
        if (s === 'takeout' || s === 'takeoutInProgress') return 'ziehen';
        if (s === 'calibrating') return 'kalib';
        if (s === 'starting') return 'startet';
        if (s === 'standby') return 'standby';
        if (s === 'stopped' || s === 'stopping') return 'gestoppt';
        return 'weg';
      }
      if (pc) return 'startet';
      if (this._startBis > jetzt && (dose === undefined || dose === 'on')) return 'startet';
      if (dose === 'on' && watt !== null && watt > 6) return 'startet';
      return 'aus';
    }
    _info(liste) {
      return (liste || []).map(x => { const e = typeof x === 'string' ? { entity: x } : x, s = st(this._h, e.entity); if (!s) return '';
        const v = parseFloat(s.state), w = isNaN(v) ? s.state : zahl(v, e.digits || 0);
        return esc(e.name || s.attributes.friendly_name || e.entity) + ' <b>' + esc(w) + '</b>'; }).filter(Boolean).join(' · ');
    }
    _zeichnen() {
      const h = this._h, r = this._r, c = this._c;
      const sz = this._szene(), [name, icon] = SZ[sz];
      if (this.getAttribute('sz') !== sz) this.setAttribute('sz', sz);
      const online = ['bereit', 'ziehen', 'kalib', 'gestoppt', 'standby', 'weg'].includes(sz) || (sz === 'startet' && zst(h, E(h, 'sensor.status')) === 'starting');
      this.toggleAttribute('online', online);
      const ic = r.querySelector('.zt ha-icon'); if (ic.getAttribute('icon') !== icon) ic.setAttribute('icon', icon);
      r.querySelector('.zn').textContent = t(name);
      let n = 0;
      [1, 2, 3].forEach((nr, i) => {
        const id = E(h, 'sensor.throw_' + nr), x = zst(h, id), p = online ? position(x, i, att(h, id)) : null, d = r.querySelector('.d' + i);
        if (p) { n++; d.setAttribute('transform', 'translate(' + f1(p[0]) + ' ' + f1(p[1]) + ')'); }
        d.classList.toggle('an', !!p);
        const w = r.querySelector('.w[data-i="' + i + '"]'), leer = !x || x === '-' || x === 'unavailable';
        w.classList.toggle('leer', leer); w.querySelector('b').textContent = leer ? '–' : x;
      });
      const summe = Math.round(num(h, E(h, 'sensor.visit_score')));
      r.querySelector('.sum b').textContent = summe;
      const dose = zst(h, c.power_switch), watt = da(h, c.power_sensor) ? Math.round(num(h, c.power_sensor)) : null;
      const info = this._info(c.info).replace(/<\/?b>/g, '');
      let art = info || (sz === 'bereit' ? t('ready_hint') : '');
      if (sz === 'bereit' && n > 0 && n < 3) art = t('dart_of', { n: n + 1, s: summe });
      else if (sz === 'ziehen') art = t('visit_pts', { s: summe });
      else if (sz === 'startet') art = an(h, c.pc_online) ? t('pc_running') : t('about_minute');
      else if (sz === 'runter') art = c.power_switch ? t('plug_after') : '';
      else if (sz === 'aus' && dose === 'on') art = t('plug_on') + (watt !== null ? ' · ' + watt + ' W' : '') + (art ? ' · ' + art : '');
      r.querySelector('.art').textContent = art;
      const zl = r.querySelector('.zeile'), zt = this._info(c.details);
      if (zl.innerHTML !== zt) zl.innerHTML = zt;
      zl.classList.toggle('hat', !!zt);
      const ein = r.querySelector('[data-id="ein"]');
      if (ein) {
        const pc = an(h, c.pc_online);
        const aus = !!c.power_off && (pc || online || sz === 'startet' || sz === 'runter' || (dose === 'on' && (watt === null || watt >= 3)));
        const modus = aus ? 'aus' : 'ein';
        if (ein.dataset.modus !== modus && !ein.classList.contains('scharf')) {
          ein.dataset.modus = modus;
          ein.dataset.lbl = aus ? t('off') : t('on');
          ein.querySelector('.lbl').textContent = ein.dataset.lbl;
          ein.style.setProperty('--k', aus ? R : G);
          ein.style.setProperty('--sr-f', aus ? R : G);
        }
        ein.disabled = sz === 'runter' || (!aus && (online || sz === 'startet'));
      }
      const spId = E(h, 'sensor.game'), sa = att(h, spId), ph = phase(sa), lf = r.querySelector('.laeuft');
      let lt = '';
      if (ph === 'running' || ph === 'bulloff') {
        lt = '<ha-icon icon="mdi:bullseye-arrow"></ha-icon><span><b>' + (ph === 'bulloff' ? 'Bull-Off' : t('game_running')) + '</b> · ' +
          (sa.spieler || []).map((p, i) => (i === sa.am_zug ? '<u>' + esc(p.name) + '</u>' : esc(p.name)) + ' ' + p.rest).join(' · ') + '</span>' + (c.game_path ? '<ha-icon icon="mdi:chevron-right"></ha-icon>' : '');
      }
      if (lf.innerHTML !== lt) lf.innerHTML = lt;
      lf.style.display = lt ? '' : 'none';
    }
  }
  customElements.define('autodarts-overview-card', AutodartsOverviewCard);

  /* ---------- Tile: one compact row with the board scene behind it, tap opens a window (1.24) ---------- */
  // power plug of the board PC for every card (1.25.1)
  Object.assign(TEXTE.en, { plug_title: 'Board PC power plug', plug_none: 'None', plug_switch: 'Power plug', plug_leistung: 'Power meter (optional)', plug_einschalten: 'Switch on with (optional)', plug_ausschalten: 'Shut down with (optional)', plug_pc_online: 'PC running (optional)', plug_pick: 'Choose …',
    plug_hint: 'The plug the board PC is connected to. Every DartNest card – also in the sidebar – then shows the power button. With a power meter DartNest knows when the PC is really off. Have a script that shuts the PC down first? Choose it under “Shut down with”, otherwise the plug is simply switched off.' });
  Object.assign(TEXTE.de, { plug_title: 'Steckdose des Board-PCs', plug_none: 'Keine', plug_switch: 'Steckdose', plug_leistung: 'Leistungsmesser (optional)', plug_einschalten: 'Einschalten mit (optional)', plug_ausschalten: 'Herunterfahren mit (optional)', plug_pc_online: 'PC läuft (optional)', plug_pick: 'Auswählen …',
    plug_hint: 'Die Steckdose, an der der Board-PC hängt. Alle DartNest-Karten – auch in der Seitenleiste – zeigen dann den Ein/Aus-Knopf. Mit Leistungsmesser erkennt DartNest, wann der PC wirklich aus ist. Du hast ein Skript, das den PC erst herunterfährt? Dann wähle es bei „Herunterfahren mit“, sonst wird einfach die Steckdose ausgeschaltet.' });
  Object.assign(TEXTE.en, { d_tile: 'One compact row with the board scene behind it; tap opens a window with live darts, power, shortcuts and today', tile_tap: 'Tap for play, power and settings', today: 'Today', t_close: 'Close' });
  Object.assign(TEXTE.de, { d_tile: 'Eine kompakte Zeile mit der Board-Szene dahinter; Tippen öffnet ein Fenster mit Live-Würfen, Ein/Aus, Abkürzungen und Heute', tile_tap: 'Antippen für Spielen, Ein/Aus und Einstellungen', today: 'Heute', t_close: 'Schließen' });
  /* ---------- sheet kit (1.31.0): windows slide up from the bottom and away downwards,
     sub-windows (details of a value, choice lists) in the same style instead of the Home Assistant more-info dialog ---------- */
  const FE_CSS = `
dialog{padding:0;border:0;margin:0;width:100%;max-width:100%;height:100%;max-height:100%;background:transparent;color:var(--primary-text-color);overflow:hidden}
dialog[open]{display:flex;align-items:flex-end;justify-content:center}
dialog::backdrop{background:var(--mdc-dialog-scrim-color,rgba(0,0,0,.5));animation:fe-schleier .3s ease}
dialog.zu::backdrop{opacity:0;transition:opacity .24s ease}
.blatt{width:min(560px,100%);max-height:92%;overflow-y:auto;overscroll-behavior:contain;box-sizing:border-box;border-radius:26px 26px 0 0;
 padding:6px 8px calc(14px + env(safe-area-inset-bottom,0px));
 background:var(--ha-bottom-sheet-surface-background,var(--ha-dialog-surface-background,var(--card-background-color,var(--primary-background-color))));
 -webkit-backdrop-filter:var(--ha-bottom-sheet-surface-backdrop-filter,none);backdrop-filter:var(--ha-bottom-sheet-surface-backdrop-filter,none);
 box-shadow:var(--dialog-box-shadow,0 -8px 40px rgba(0,0,0,.35));animation:fe-rauf .34s cubic-bezier(.2,.85,.25,1)}
dialog.zu .blatt{transform:translateY(100%)!important;transition:transform .24s cubic-bezier(.4,0,1,1)!important}
.griff{width:40px;height:4px;border-radius:9px;margin:4px auto 6px;background:color-mix(in srgb,var(--primary-text-color) 25%,transparent)}
.fkopf{display:flex;align-items:center;gap:10px;padding:0 6px 8px 10px;font-size:17px;font-weight:700}
.fkopf ha-icon,.fkopf ha-state-icon{--mdc-icon-size:22px;color:var(--fe-f,var(--primary-color))}
.fkopf span{flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.fkopf button:focus:not(:focus-visible){outline:none}
.fkopf button{width:38px;height:38px;flex:none;border-radius:50%;display:flex;align-items:center;justify-content:center;border:0;cursor:pointer;color:inherit;background:color-mix(in srgb,var(--primary-text-color) 9%,transparent);-webkit-tap-highlight-color:transparent}
@keyframes fe-rauf{from{transform:translateY(100%)}}
@keyframes fe-rein{from{transform:translateY(60px);opacity:0}}
@keyframes fe-schleier{from{opacity:0}}
@media (min-width:700px){dialog[open]{align-items:center}.blatt{border-radius:26px;max-height:88%;animation-name:fe-rein}dialog.zu .blatt{transform:translateY(40px)!important;opacity:0;transition:transform .2s ease-in,opacity .2s ease-in!important}}
@media (prefers-reduced-motion:reduce){.blatt{animation:none}dialog.zu .blatt,dialog.zu::backdrop{transition:none!important}}`;
  // Aufklapp-Knopf im Fenster (wie „Programme & Optionen“)
  const FE_KLAPP = `
.klapp-k{display:flex;align-items:center;gap:8px;width:100%;margin:10px 0 0;padding:10px 12px;border:0;border-radius:14px;cursor:pointer;font:inherit;font-size:13px;font-weight:600;color:var(--secondary-text-color);background:color-mix(in srgb,var(--primary-text-color) 6%,transparent);-webkit-tap-highlight-color:transparent;transition:transform .12s ease}
.klapp-k:active{transform:scale(.98)}
.klapp-k span{flex:1;text-align:left}
.klapp-k ha-icon{--mdc-icon-size:20px;transition:transform .2s}
.klapp-k.offen ha-icon.pf{transform:rotate(180deg)}`;
  const feRuhig = () => !!(window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches);
  // Fenster nach unten weggleiten lassen, dann schließen
  const zuGleiten = d => {
    if (!d.open || d.classList.contains('zu')) return;
    if (feRuhig()) { d.close(); return; }
    d.classList.add('zu');
    setTimeout(() => { d.classList.remove('zu'); if (d.open) d.close(); }, 230);
  };
  // Nach unten ziehen schließt (nur ganz oben gescrollt, nicht auf Knöpfen); nach oben = normal scrollen
  const ziehenZu = (bl, d) => {
    let y0 = null, dy = 0, zieh = false;
    const ende = () => {
      if (zieh) {
        if (dy > Math.min(140, bl.offsetHeight * 0.25)) { bl.style.transition = 'transform .2s cubic-bezier(.4,0,1,1)'; bl.style.transform = 'translateY(100%)'; setTimeout(() => d.close(), 190); }
        else { bl.style.transition = 'transform .2s ease'; bl.style.transform = ''; }
      }
      y0 = null; zieh = false;
    };
    bl.addEventListener('touchstart', e => { y0 = e.touches.length === 1 && !e.composedPath().some(x => x.tagName === 'BUTTON' || x.tagName === 'INPUT' || x.tagName === 'SELECT') ? e.touches[0].clientY : null; dy = 0; zieh = false; }, { passive: true });
    bl.addEventListener('touchmove', e => {
      if (y0 === null) return;
      const dd = e.touches[0].clientY - y0;
      if (!zieh) { if (Math.abs(dd) < 8) return; if (dd < 0 || bl.scrollTop > 0) { y0 = null; return; } zieh = true; bl.style.transition = 'none'; }
      dy = Math.max(0, dd); bl.style.transform = 'translateY(' + dy + 'px)'; e.preventDefault();
    }, { passive: false });
    bl.addEventListener('touchend', ende); bl.addEventListener('touchcancel', ende);
  };
  // Grundgerüst eines Fensters: Schleier antippen, X, Esc, Zurück-Taste (history-Merker), Ziehen
  const fensterGeruest = (d, bl, merker, beimZu) => {
    const f = { hist: false };
    d.addEventListener('click', e => { if (e.target === d) zuGleiten(d); });
    d.addEventListener('cancel', e => { e.preventDefault(); zuGleiten(d); });
    const x = bl.querySelector('.fzu'); if (x) x.addEventListener('click', () => zuGleiten(d));
    const pop = () => { if (!(history.state && history.state[merker])) { f.hist = false; zuGleiten(d); } };
    // eine Abkürzung im Fenster öffnet eine andere Seite: schließen, ohne zurückzugehen
    const weg = () => { if (d.open && !(history.state && history.state[merker])) { f.hist = false; d.close(); } };
    d.addEventListener('close', () => {
      window.removeEventListener('popstate', pop); window.removeEventListener('location-changed', weg);
      bl.style.transition = ''; bl.style.transform = '';
      if (beimZu) beimZu();
      if (f.hist) { f.hist = false; history.back(); }
    });
    ziehenZu(bl, d);
    f.auf = () => {
      if (d.open) return false;
      bl.style.transition = ''; bl.style.transform = '';
      try { d.showModal(); } catch (e) { d.setAttribute('open', ''); }
      bl.scrollTop = 0;
      try { const s = Object.assign({}, history.state); s[merker] = 1; history.pushState(s, ''); f.hist = true; window.addEventListener('popstate', pop); window.addEventListener('location-changed', weg); } catch (e) {}
      return true;
    };
    return f;
  };
  const U_CSS = `
:host{display:contents}
.uw{display:flex;align-items:baseline;flex-wrap:wrap;gap:4px 10px;padding:2px 10px 12px}
.uw b{font-size:28px;font-weight:700;line-height:1.15}
.uw small{font-size:12.5px;color:var(--secondary-text-color)}
.graf{padding:0 2px;min-height:40px;--ha-card-background:color-mix(in srgb,var(--primary-text-color) 5%,transparent);--ha-card-box-shadow:none;--ha-card-border-width:0;--ha-card-border-radius:18px}
.liste{display:flex;flex-direction:column;gap:6px;padding:2px 4px 4px}
.liste button{display:flex;align-items:center;gap:12px;width:100%;padding:12px 14px;border-radius:14px;font:inherit;font-size:14px;font-weight:600;text-align:left;color:var(--primary-text-color);background:color-mix(in srgb,var(--primary-text-color) 6%,transparent);border:0;cursor:pointer;-webkit-tap-highlight-color:transparent;transition:transform .12s ease,background .25s ease}
.liste button:active{transform:scale(.97)}
.liste button span{flex:1}
.liste button ha-icon{--mdc-icon-size:20px;color:var(--fe-f,var(--primary-color));visibility:hidden}
.liste button.an{background:color-mix(in srgb,var(--fe-f,var(--primary-color)) 20%,transparent)}
.liste button.an ha-icon{visibility:visible}`;
  const feZeit = x => { const d = new Date(x); if (isNaN(d)) return ''; const hm = String(d.getHours()).padStart(2, '0') + ':' + String(d.getMinutes()).padStart(2, '0');
    return t('since', { t: d.toDateString() === new Date().toDateString() ? hm : d.getDate() + '.' + (d.getMonth() + 1) + '. ' + hm }); };
  class FeUnterfenster extends HTMLElement {
    constructor() {
      super();
      const r = this.attachShadow({ mode: 'open' });
      r.innerHTML = '<style>' + FE_CSS + U_CSS + '</style><dialog><div class="blatt"><div class="griff"></div><div class="fkopf"><ha-state-icon></ha-state-icon><ha-icon class="wi"></ha-icon><span class="ft"></span>' +
        '<button class="fzu" aria-label="' + t('t_close') + '"><ha-icon icon="mdi:close"></ha-icon></button></div><div class="koerper"></div></div></dialog>';
      const d = this._d = r.querySelector('dialog'), bl = r.querySelector('.blatt');
      this._f = fensterGeruest(d, bl, 'unterFenster', () => { this._id = null; this._wahl = null; this._graf = null; r.querySelector('.koerper').innerHTML = ''; });
      // Infos aus dem Unterfenster heraus (z. B. Verlauf antippen): Wert wechseln statt noch ein Fenster
      bl.addEventListener('hass-more-info', e => { e.stopPropagation(); const id = e.detail && e.detail.entityId; if (id && id !== this._id) this.info(id); });
      r.querySelector('.koerper').addEventListener('click', e => {
        const b = e.target.closest('[data-o]'); if (!b || !this._wahl) return;
        const los = this._wahl; this._wahl = null; los(b.dataset.o); zuGleiten(d);
      });
    }
    set hass(h) { this._h = h; if (this._graf) this._graf.hass = h; if (this._id) this._zeichnen(); }
    _kopf(id, icon, titel) {
      const r = this.shadowRoot, si = r.querySelector('ha-state-icon'), wi = r.querySelector('.wi');
      si.style.display = id ? '' : 'none'; wi.style.display = id ? 'none' : '';
      if (id) { si.hass = this._h; si.stateObj = this._h.states[id]; } else wi.setAttribute('icon', icon || 'mdi:format-list-bulleted');
      r.querySelector('.ft').textContent = titel;
    }
    // Infos zu einem Wert: großer Wert, seit wann, Verlauf der letzten 24 Stunden
    info(id) {
      const h = this._h, s = h && h.states[id]; if (!s) return;
      this._id = id; this._wahl = null;
      const k = this.shadowRoot.querySelector('.koerper');
      k.innerHTML = '<div class="uw"><b></b><small></small></div><div class="graf"></div>';
      this._graf = null;
      if (window.loadCardHelpers) window.loadCardHelpers().then(hl => {
        if (this._id !== id) return;
        const c = hl.createCardElement({ type: 'history-graph', hours_to_show: 24, entities: [{ entity: id, name: ' ' }] });
        c.hass = this._h; this._graf = c; k.querySelector('.graf').appendChild(c);
      }).catch(() => {});
      this._zeichnen();
      this._f.auf();
    }
    _zeichnen() {
      const h = this._h, s = h.states[this._id]; if (!s) return;
      this._kopf(this._id, null, s.attributes.friendly_name || this._id);
      const w = h.formatEntityState ? h.formatEntityState(s) : s.state + (s.attributes.unit_of_measurement ? ' ' + s.attributes.unit_of_measurement : '');
      const r = this.shadowRoot, b = r.querySelector('.uw b'), z = r.querySelector('.uw small'); if (!b) return;
      if (b.textContent !== w) b.textContent = w;
      const t = feZeit(s.last_changed); if (z.textContent !== t) z.textContent = t;
    }
    // Auswahlliste im Fensterstil: optionen = [[wert, text]], los(wert) beim Antippen
    wahl(titel, icon, optionen, aktuell, los) {
      this._id = null; this._graf = null; this._wahl = los;
      this._kopf(null, icon, titel);
      const esc = x => String(x).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;');
      this.shadowRoot.querySelector('.koerper').innerHTML = '<div class="liste">' + optionen.map(([o, t]) =>
        '<button data-o="' + esc(o) + '" class="' + (o === aktuell ? 'an' : '') + '"><span>' + esc(t) + '</span><ha-icon icon="mdi:check"></ha-icon></button>').join('') + '</div>';
      this._f.auf();
    }
  }
  Object.assign(TEXTE.en, { since: 'since {t}' });
  Object.assign(TEXTE.de, { since: 'seit {t} Uhr' });
  if (!customElements.get('autodarts-info-sheet')) customElements.define('autodarts-info-sheet', FeUnterfenster);
  const infoFenster = (host, root) => { if (!host._uf) { host._uf = document.createElement('autodarts-info-sheet'); root.appendChild(host._uf); } host._uf.hass = host._h; return host._uf; };

  const SZ_F = { aus: GR, startet: A, runter: A, bereit: G, ziehen: A, kalib: '#26a69a', gestoppt: B, standby: B, weg: A };
  const K_CSS = `
ha-card{display:flex;align-items:center;gap:12px;cursor:pointer;position:relative;overflow:hidden;padding:14px;box-sizing:border-box}
.ic,.tx,.ak,.pf{position:relative;z-index:1}
.bg{position:absolute;inset:0;z-index:0;pointer-events:none;opacity:.55;-webkit-mask-image:linear-gradient(90deg,transparent 25%,#000 70%);mask-image:linear-gradient(90deg,transparent 25%,#000 70%)}
.bg .szene{height:100%;border-radius:0;cursor:inherit}
.bg .szene svg{right:-6px;top:-30%;height:160%}
.ic{width:42px;height:42px;border-radius:14px;display:flex;align-items:center;justify-content:center;background:color-mix(in srgb,var(--f) 20%,transparent);color:var(--f);flex:none}
.ic ha-icon{--mdc-icon-size:24px}
.tx{flex:1;min-width:0}
.tx b{display:block;font-size:15px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.tx span{display:block;font-size:12.5px;color:var(--secondary-text-color);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.ak{flex:none;display:flex;gap:4px}
.ak i{width:9px;height:9px;border-radius:50%;background:var(--c);box-shadow:0 0 8px var(--c)}
.pf{--mdc-icon-size:22px;color:var(--secondary-text-color)}
:host{--fe-f:var(--f)}
.inhalt>*{display:block;margin-top:8px}
.inhalt>*:first-child{margin-top:0}
.inhalt{--ha-card-background:transparent;--ha-card-box-shadow:none;--ha-card-border-width:0}
.hgitter{display:grid;grid-template-columns:repeat(auto-fill,minmax(80px,1fr));gap:8px;padding:0 8px}
.hgitter .w{cursor:default}
`;
  class AutodartsTileCard extends AutodartsOverviewCard {
    static getStubConfig() { return {}; }
    getCardSize() { return 1; }
    set hass(h) {
      this._h = h; sprachePruefen(h);
      if (!this._r || this._spr !== SPR) this._bauen();
      this._zeichnen();
      if (this._d && this._d.open) this._innenHass();
      if (this._uf) this._uf.hass = h;
    }
    _bauen() {
      this._spr = SPR;
      const r = this._r = this.shadowRoot || this.attachShadow({ mode: 'open' });
      r.innerHTML = '<style>' + BASIS + B_CSS + K_CSS + FE_CSS + '</style><ha-card><div class="bg"><div class="szene">' + SZENE + '</div></div>' +
        '<div class="ic"><ha-icon></ha-icon></div><div class="tx"><b></b><span></span></div><span class="ak"></span><ha-icon class="pf" icon="mdi:chevron-right"></ha-icon></ha-card>' +
        '<dialog><div class="blatt"><div class="griff"></div><div class="fkopf"><ha-icon icon="mdi:bullseye-arrow"></ha-icon><span>' + esc(this._c.name || 'Darts') + '</span>' +
        '<button class="fzu" aria-label="' + t('t_close') + '"><ha-icon icon="mdi:close"></ha-icon></button></div><div class="inhalt"></div></div></dialog>';
      r.querySelector('ha-card').addEventListener('click', () => this._auf());
      const d = this._d = r.querySelector('dialog'), bl = this._bl = r.querySelector('.blatt');
      // 1.31.0: the window slides up and away downwards (X, tap outside, Esc, back button, pull down); a shortcut to another page closes it
      this._f = fensterGeruest(d, bl, 'adFenster', () => this._zu());
      // details of a value open a sub-window in the same style instead of the Home Assistant more-info dialog
      bl.addEventListener('hass-more-info', e => { e.stopPropagation(); if (e.detail && e.detail.entityId) infoFenster(this, r).info(e.detail.entityId); });
      this._sicht = true;
      const still = () => this.toggleAttribute('still', document.hidden || (!this._sicht && !d.open));
      this._still = still;
      if (this._io) this._io.disconnect();
      if ('IntersectionObserver' in window) { this._io = new IntersectionObserver(e => { this._sicht = e[0].isIntersecting; still(); }); if (this.isConnected) this._io.observe(this); }
      if (!this._vis) { this._vis = () => this._still && this._still(); document.addEventListener('visibilitychange', this._vis); }
      this._innen = null; this._uf = null;
    }
    connectedCallback() { if (this._io) this._io.observe(this); }
    disconnectedCallback() { if (this._io) this._io.disconnect(); if (this._d && this._d.open) { this._f.hist = false; this._d.close(); } }
    // window content: the overview card with the same options, then today's values and own cards (only made when opened)
    async _inhalt() {
      if (this._innen) return;
      const c = this._c, box = this._r.querySelector('.inhalt');
      const ov = document.createElement('autodarts-overview-card');
      const oc = Object.assign({}, c); delete oc.type; delete oc.cards; delete oc.today; delete oc.name;
      ov.setConfig(oc);
      this._innen = [ov];
      box.appendChild(ov);
      if (c.today && c.today.length) {
        const heute = document.createElement('div');
        heute.className = 'heute';
        this._innen.push(heute);
        box.appendChild(heute);
      }
      if (c.cards && c.cards.length && window.loadCardHelpers) {
        try {
          const hilfe = await window.loadCardHelpers();
          c.cards.forEach(cc => { const el = hilfe.createCardElement(cc); this._innen.push(el); box.appendChild(el); });
        } catch (e) {}
      }
      this._innenHass();
    }
    _innenHass() {
      (this._innen || []).forEach(el => {
        if (el.className === 'heute') {
          const w = (this._c.today || []).map(x => { const e = typeof x === 'string' ? { entity: x } : x, s = st(this._h, e.entity); if (!s) return '';
            const v = parseFloat(s.state);
            return '<div class="w feld" data-id="' + esc(e.entity) + '"><small>' + esc(e.name || s.attributes.friendly_name || e.entity) + '</small><b>' + esc(isNaN(v) ? s.state : zahl(v, e.digits || 0)) + '</b></div>'; }).join('');
          const html = '<div class="titel" style="margin:6px 10px 8px"><ha-icon icon="mdi:calendar-today"></ha-icon>' + t('today') + '</div><div class="hgitter">' + w + '</div>';
          if (el._html !== html) { el._html = html; el.innerHTML = html; }
        } else el.hass = this._h;
      });
    }
    _auf() {
      if (!this._f.auf()) return;
      this._still();
      this._inhalt();
    }
    _zu() { this._still(); }
    _zeichnen() {
      const h = this._h, r = this._r, c = this._c;
      const sz = this._szene(), [name, icon] = SZ[sz];
      if (this.getAttribute('sz') !== sz) this.setAttribute('sz', sz);
      const online = ['bereit', 'ziehen', 'kalib', 'gestoppt', 'standby', 'weg'].includes(sz);
      this.style.setProperty('--f', SZ_F[sz]);
      const ic = r.querySelector('.ic ha-icon'); if (ic.getAttribute('icon') !== icon) ic.setAttribute('icon', icon);
      let n = 0;
      const punkte = [1, 2, 3].map((nr, i) => {
        const id = E(h, 'sensor.throw_' + nr), x = zst(h, id), p = online ? position(x, i, att(h, id)) : null, d = r.querySelector('.d' + i);
        if (p) { n++; d.setAttribute('transform', 'translate(' + f1(p[0]) + ' ' + f1(p[1]) + ')'); }
        d.classList.toggle('an', !!p);
        return p ? ['#e53935', '#1e88e5', '#fdd835'][i] : '';
      });
      const summe = Math.round(num(h, E(h, 'sensor.visit_score')));
      const sa = att(h, E(h, 'sensor.game')), ph = phase(sa);
      let unter = this._info(c.info).replace(/<\/?b>/g, '');
      if (ph === 'running' || ph === 'bulloff') {
        unter = (ph === 'bulloff' ? 'Bull-Off' : t('game_running')) + ' · ' + (sa.spieler || []).map(p => p.name + ' ' + p.rest).join(' · ');
      } else if (sz === 'bereit' && n > 0 && n < 3) unter = t('dart_of', { n: n + 1, s: summe });
      else if (sz === 'ziehen') unter = t('visit_pts', { s: summe });
      else if (sz === 'startet') unter = an(h, c.pc_online) ? t('pc_running') : t('about_minute');
      else if (sz === 'aus' && !unter) unter = t('tile_tap');
      r.querySelector('.tx b').textContent = (c.name || 'Darts') + ' · ' + t(name);
      r.querySelector('.tx span').textContent = unter;
      const ak = punkte.filter(Boolean).map(f => '<i style="--c:' + f + '"></i>').join('');
      const akEl = r.querySelector('.ak'); if (akEl.innerHTML !== ak) akEl.innerHTML = ak;
    }
  }
  customElements.define('autodarts-tile-card', AutodartsTileCard);

  /* ---------- shared parts of the page cards ---------- */
  const SEITEN_CSS = `
ha-card{padding:14px 14px 16px;container-type:inline-size}
.start{display:flex;align-items:center;justify-content:center;gap:10px;width:100%;min-height:62px;border-radius:20px;font-size:18px;font-weight:800;color:#fff;margin-top:4px;
 background:linear-gradient(135deg,#43a047,#2e7d32);box-shadow:0 6px 18px rgba(46,125,50,.35)}
.start ha-icon{--mdc-icon-size:26px}
.kopf{display:flex;align-items:center;gap:6px;margin:-2px -4px 12px}
.kopf .ti{flex:1;min-width:0;font-size:20px;font-weight:700;line-height:1.2}
.kopf .ti small{display:block;font-size:12.5px;font-weight:500;color:var(--secondary-text-color);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.kx{display:flex;gap:2px}
.ik{width:42px;height:42px;border-radius:14px;display:flex;align-items:center;justify-content:center;background:transparent;flex:none}
.ik:hover{background:color-mix(in srgb,var(--primary-text-color) 8%,transparent)}
.ik ha-icon{--mdc-icon-size:22px}
.ik.an ha-icon{color:var(--primary-color)}
:host([ohne-zurueck]) .ik[data-act=zurueck]{display:none}
.blk{border-radius:20px;padding:12px;margin-bottom:10px}
.bt{display:flex;align-items:center;gap:8px;font-weight:700;font-size:14px;margin:0 2px 10px}
.bt .rechts{margin-left:auto;font-weight:500;color:var(--secondary-text-color);font-size:12.5px}
.chips{display:flex;flex-wrap:wrap;gap:8px}
.chip{display:inline-flex;align-items:center;gap:6px;border-radius:999px;padding:9px 14px;font-size:14px;font-weight:600}
.chip ha-icon{--mdc-icon-size:18px}
.seg{display:flex;flex-wrap:wrap;gap:6px}
.seg button{border-radius:12px;padding:9px 12px;font-size:14px;font-weight:600;min-width:44px}
.seg button.an,.chip.an{background:var(--primary-color);color:var(--text-primary-color,#fff);border-color:transparent}
.reihe{display:flex;align-items:center;justify-content:space-between;gap:10px;flex-wrap:wrap;padding:8px 2px}
.reihe>span{font-size:14px;color:var(--secondary-text-color)}
.stepper{display:flex;align-items:center;gap:6px}
.stepper button{width:40px;height:40px;border-radius:12px;font-size:20px;font-weight:700}
.stepper b{min-width:92px;text-align:center;font-size:15px}
.auf{display:flex;align-items:center;gap:10px;width:100%;border-radius:16px;padding:12px 14px;margin-top:10px;font-size:14.5px;font-weight:600;text-align:left}
.auf ha-icon{--mdc-icon-size:20px;color:var(--secondary-text-color)}
.auf .pf{margin-left:auto;transition:transform .2s ease}
.auf.offen .pf{transform:rotate(180deg)}
.aufinhalt{padding:8px 2px 2px}
.warn{display:flex;align-items:center;gap:10px;border-radius:16px;padding:10px 12px;margin-bottom:10px;font-size:13.5px;background:color-mix(in srgb,var(--amber-color,#ffc107) 16%,transparent);border:1px solid color-mix(in srgb,var(--amber-color,#ffc107) 40%,transparent)}
.warn ha-icon{color:var(--amber-color,#ffc107);flex:none}.warn span{flex:1}
.warn button{border-radius:12px;padding:8px 12px;font-weight:700;background:var(--green-color,#43a047);color:#fff}
.tab{width:100%;border-collapse:collapse;font-size:13.5px}
.tab th,.tab td{padding:7px 6px;text-align:right;border-bottom:1px solid color-mix(in srgb,var(--primary-text-color) 8%,transparent);white-space:nowrap}
.tab th:first-child,.tab td:first-child{text-align:left}
.tab th{font-weight:600;color:var(--secondary-text-color);font-size:12px}
.leer{color:var(--secondary-text-color);font-size:13.5px;padding:6px 2px}
.modal{position:fixed;inset:0;z-index:99;display:flex;align-items:center;justify-content:center;padding:16px;box-sizing:border-box;background:rgba(0,0,0,.5)}
.modal[hidden]{display:none}
.mbox{width:min(560px,100%);max-height:92vh;overflow:auto;box-sizing:border-box;padding:16px;border-radius:24px;background:var(--card-background-color,#1c1f24);box-shadow:0 10px 40px rgba(0,0,0,.5)}
.mbox h3{margin:0 0 12px;font-size:17px}
.mbox input{width:100%;box-sizing:border-box;font:inherit;font-size:16px;padding:12px 14px;border-radius:14px;color:var(--primary-text-color);background:color-mix(in srgb,var(--primary-text-color) 7%,transparent);border:1px solid color-mix(in srgb,var(--primary-text-color) 18%,transparent);outline:none}
.mknoepfe{display:flex;gap:8px;justify-content:flex-end;margin-top:14px}
.mknoepfe button{border-radius:14px;padding:11px 16px;font-weight:700}
.mknoepfe .ja{background:var(--primary-color);color:var(--text-primary-color,#fff)}
.zahlgitter{display:grid;grid-template-columns:repeat(5,1fr);gap:6px;margin-top:10px}
.zahlgitter button{border-radius:12px;padding:12px 0;font-size:16px;font-weight:700}
.sonder{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin-top:6px}
.sonder button{border-radius:12px;padding:12px 0;font-size:14px;font-weight:700}`;
  const auf = (key, offen, icon, titel, rechts) => '<button class="auf feld' + (offen ? ' offen' : '') + '" data-act="tgl" data-x="' + key + '"><ha-icon icon="' + icon + '"></ha-icon><span>' + titel + '</span>' +
    (rechts ? '<small style="margin-left:auto;color:var(--secondary-text-color);font-weight:500">' + rechts + '</small>' : '') + '<ha-icon class="pf" icon="mdi:chevron-down"' + (rechts ? ' style="margin-left:6px"' : '') + '></ha-icon></button>';
  const z1 = x => zahl(x || 0, 1);
  // base for the page cards: header, click handling, dialog, redraw only on change
  class DartsSeite extends HTMLElement {
    static getStubConfig() { return {}; }
    setConfig(c) { this._c = Object.assign({}, c || {}); this._auf = this._auf || {}; this.toggleAttribute('ohne-zurueck', this._c.back_button === false); }
    getCardSize() { return 12; }
    getGridOptions() { return { columns: 'full' }; }
    set hass(h) {
      this._h = h; sprachePruefen(h);
      if (!this._r) this._grund();
      if (this._spr !== SPR) { this._spr = SPR; this._alt = null; this._kxAlt = null; this._werteAlt = null; this._r.querySelector('[data-act=zurueck]').title = t('back'); }
      this._zeichnen();
    }
    _grund() {
      this._r = this.attachShadow({ mode: 'open' });
      this._r.innerHTML = '<style>' + BASIS + SEITEN_CSS + (this.constructor.CSS || '') + '</style><ha-card><div class="kopf">' +
        '<button class="ik" data-act="zurueck" title="' + t('back') + '"><ha-icon icon="mdi:arrow-left"></ha-icon></button><div class="ti"><span class="tt"></span><small class="ts"></small></div><span class="kx"></span></div>' +
        '<div class="inhalt"></div></ha-card><div class="modal" hidden><div class="mbox"></div></div>';
      this._in = this._r.querySelector('.inhalt');
      this._sicht = true;
      if ('IntersectionObserver' in window) new IntersectionObserver(e => { this._sicht = e[0].isIntersecting; this._sichtbar && this._sichtbar(); }).observe(this);
      document.addEventListener('visibilitychange', () => this._sichtbar && this._sichtbar());
      this._r.addEventListener('click', e => {
        const b = e.target.closest('[data-act]'); if (!b || b.disabled) return;
        const a = b.dataset.act;
        if (a === 'zurueck') { if (document.fullscreenElement) document.exitFullscreen(); if (this._zurueck) this._zurueck(); else if (this._c.back_path) gehe(this._c.back_path); else history.back(); return; }
        if (a === 'tgl') { this._auf[b.dataset.x] = !this._auf[b.dataset.x]; this._alt = null; this._zeichnen(); return; }
        if (a === 'mzu') { this._modal(null); return; }
        if (e.target.closest('.modal') && !e.target.closest('.mbox')) { this._modal(null); return; }
        this._klick(a, b, e);
      });
      this._r.querySelector('.modal').addEventListener('click', e => { if (e.target.classList.contains('modal')) this._modal(null); });
    }
    _setze(html) { if (this._alt !== html) { this._alt = html; this._in.innerHTML = html; } }
    _kopf(x, s, extra) {
      const r = this._r;
      if (r.querySelector('.tt').textContent !== x) r.querySelector('.tt').textContent = x;
      if (r.querySelector('.ts').textContent !== (s || '')) r.querySelector('.ts').textContent = s || '';
      if (this._kxAlt !== extra) { this._kxAlt = extra; r.querySelector('.kx').innerHTML = extra || ''; }
    }
    _modal(html) {
      const m = this._r.querySelector('.modal');
      if (!html) { m.hidden = true; this._m = null; return; }
      m.querySelector('.mbox').innerHTML = html; m.hidden = false;
      const i = m.querySelector('input'); if (i) setTimeout(() => i.focus(), 50);
    }
    _dienst(srv, data) { aktion(this._h, 'autodarts', srv, data || {}); }
    _fehlt() {
      if (E(this._h, 'sensor.game') && st(this._h, E(this._h, 'sensor.game'))) return false;
      this._kopf('DartNest', t('missing')); this._setze('<div class="leer">' + t('missing') + '</div>'); return true;
    }
  }

  /* ---------- Game card (lobby, bull-off, X01, result) ---------- */
  const STARTWERTE = [101, 170, 301, 501, 701, 901];
  const MODUS = [['straight', 'Straight'], ['double', 'Double'], ['master', 'Master']];
  const BOTS = [20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120];
  // order inside a group = order of the tiles in the lobby
  const GRUPPE = { x01: 'x01', cricket: 'cricket', wild_mouse: 'cricket', mickey: 'cricket',
    atc: 'training', doppel: 'training', bobs27: 'training', checkout121: 'training', checkout: 'training', catch40: 'training', jdc: 'training', singles: 'training',
    shanghai: 'party', killer: 'party', halve_it: 'party', golf: 'party', baseball: 'party', highscore: 'party',
    bermuda: 'party', rtw: 'party', gotcha: 'party', nine_lives: 'party', football: 'party', scram: 'party' };
  const ART_ICON = { x01: 'mdi:numeric', cricket: 'mdi:grid', training: 'mdi:dumbbell', party: 'mdi:party-popper',
    wild_mouse: 'mdi:rodent', mickey: 'mdi:mouse-variant',
    atc: 'mdi:clock-outline', bobs27: 'mdi:numeric-2-circle-outline', doppel: 'mdi:circle-double', checkout121: 'mdi:flag-checkered', highscore: 'mdi:trending-up',
    checkout: 'mdi:flag-outline', catch40: 'mdi:hand-back-right-outline', jdc: 'mdi:medal-outline', singles: 'mdi:numeric-1-circle-outline',
    shanghai: 'mdi:dice-multiple-outline', killer: 'mdi:skull-outline', halve_it: 'mdi:division', golf: 'mdi:golf', baseball: 'mdi:baseball',
    bermuda: 'mdi:triangle-outline', rtw: 'mdi:earth', gotcha: 'mdi:hand-pointing-right', nine_lives: 'mdi:cat', football: 'mdi:soccer', scram: 'mdi:swap-horizontal-bold' };
  // players per game: [min, max]
  const ART_SPIELER = { scram: [2, 2], killer: [2, 8] };
  // games played like Cricket (marks table)
  const CRICKETARTIG = ['cricket', 'wild_mouse', 'mickey'];
  // games that check out a number (rest, attempt, way)
  const CHECKARTIG = ['checkout121', 'checkout', 'catch40'];
  // options per game: [setting, [[value, text key or text], …]]
  const ART_OPT = {
    cricket: [['variante', [['standard', 'v_standard'], ['cut_throat', 'v_cut_throat'], ['no_score', 'v_no_score']]], ['zahlen', [['classic', 'z_classic'], ['tactics', 'z_tactics'], ['random', 'z_random'], ['hidden', 'z_hidden']]]],
    atc: [['variante', [['single', 'any'], ['double', 'double'], ['triple', 'treble']]]],
    checkout121: [['runden', [[5, '5'], [10, '10'], [20, '20']]]],
    highscore: [['runden', [[5, '5'], [8, '8'], [10, '10'], [20, '20']]]],
    shanghai: [['runden', [[7, '1–7'], [20, '1–20']]]],
    golf: [['runden', [[9, '9'], [18, '18']]]],
    killer: [['leben', [[1, '1'], [3, '3'], [5, '5']]]],
    wild_mouse: [['variante', [['mit_3b', 'with_3b'], ['ohne_3b', 'without_3b']]]],
    checkout: [['runden', [[5, '5'], [10, '10'], [20, '20']]]],
    bermuda: [['variante', [['mit_halbieren', 'halve_on'], ['ohne_halbieren', 'halve_off']]]],
    rtw: [['variante', [['auf', 'o_up'], ['ab', 'o_down'], ['zufall', 'z_random']]]],
    gotcha: [['zielwert', [[101, '101'], [301, '301'], [501, '501']]], ['variante', [['straight', 'Straight'], ['double', 'Double'], ['master', 'Master']]]],
    nine_lives: [['leben', [[1, '1'], [3, '3'], [5, '5']]]],
    football: [['zielwert', [[5, '5'], [10, '10']]]]
  };
  const OPT_TITEL = { variante: 'variant', zahlen: 'numbers', runden: 'rounds', leben: 'lives', zielwert: 'target' };
  const OPT_TITEL_ART = { 'gotcha:variante': 'checkout', 'football:zielwert': 'goals', 'rtw:variante': 'order', 'bermuda:variante': 'on_miss', 'wild_mouse:variante': 'three_bed', 'golf:runden': 'holes' };
  const OPT_STANDARD = { variante: { cricket: 'standard', atc: 'single', wild_mouse: 'mit_3b', bermuda: 'mit_halbieren', rtw: 'auf', gotcha: 'straight' },
    runden: { checkout121: 10, highscore: 8, shanghai: 7, golf: 9, checkout: 10 }, zielwert: { gotcha: 301, football: 10 } };
  // marks in cricket: /, X, circled X
  const MARK = ['', '<svg viewBox="0 0 24 24"><path d="M6 19L18 5"/></svg>', '<svg viewBox="0 0 24 24"><path d="M6 19L18 5M6 5l12 14"/></svg>',
    '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9.5"/><path d="M7.5 16.5l9-9M7.5 7.5l9 9"/></svg>'];
  const BRETT_CX = 60, BRETT_K = 52;
  const brettP = (r, w) => { const a = (w - 90) * Math.PI / 180; return [BRETT_CX + r * Math.cos(a), BRETT_CX + r * Math.sin(a)]; };
  // position of a dart on the drawn board (viewBox 0 0 120 120)
  const brettPos = (d, i) => {
    const P = brettP, k = BRETT_K / 170;
    if (typeof d.x === 'number' && typeof d.y === 'number') { const r = Math.hypot(d.x, d.y), f = r > 1.12 ? 1.12 / r : 1; return [60 + d.x * f * BRETT_K, 60 - d.y * f * BRETT_K]; }
    const x = d.f || '';
    if (x === 'D25') return P(1, i * 120); if (x === 'S25') return P(3.5, i * 120); if (x === 'M' || !x) return P(57, 200 + i * 30);
    const n = parseInt(x.slice(1), 10), w = ORDER.indexOf(n) * 18 + [-4, 3, 0][i];
    return P(x[0] === 'T' ? 103 * k : x[0] === 'D' ? 166 * k : (x[0] === 'S' ? 135 * k : 50), w);
  };
  // highlight of the current target on the drawn board: a number (whole wedge), D/T ring of a number, any double/treble ring, bull
  const zielMarke = ziel => {
    if (!ziel) return '';
    const P = brettP, k = BRETT_K / 170;
    const bogen = (r1, r2, w1, w2) => { const [a, b] = P(r2, w1), [c, d] = P(r2, w2), [e, g] = P(r1, w2), [i, j] = P(r1, w1); return 'M' + f1(a) + ' ' + f1(b) + 'A' + r2 + ' ' + r2 + ' 0 0 1 ' + f1(c) + ' ' + f1(d) + 'L' + f1(e) + ' ' + f1(g) + 'A' + r1 + ' ' + r1 + ' 0 0 0 ' + f1(i) + ' ' + f1(j) + 'Z'; };
    let d = '';
    if (ziel === 'DB') d = 'M60 ' + f1(60 - 6.35 * k) + 'a' + f1(6.35 * k) + ' ' + f1(6.35 * k) + ' 0 1 0 .01 0Z';
    else if (ziel === 'B' || ziel === 'S25' || ziel === 'D25' || ziel === '25') d = 'M60 ' + f1(60 - 15.9 * k) + 'a' + f1(15.9 * k) + ' ' + f1(15.9 * k) + ' 0 1 0 .01 0Z';
    else if (ziel === 'D' || ziel === 'T') { const r = ziel === 'D' ? [162, 170] : [99, 107]; d = 'M60 ' + f1(60 - r[1] * k) + 'a' + f1(r[1] * k) + ' ' + f1(r[1] * k) + ' 0 1 0 .01 0ZM60 ' + f1(60 - r[0] * k) + 'a' + f1(r[0] * k) + ' ' + f1(r[0] * k) + ' 0 1 0 .01 0Z'; }
    else {
      const m = /^([SDT]?)(\d+)$/.exec(ziel); if (!m) return '';
      const w1 = ORDER.indexOf(+m[2]) * 18 - 9; if (w1 < -9) return '';
      const r = { D: [162, 170], T: [99, 107], S: [15.9, 162], '': [15.9, 170] }[m[1]];
      d = bogen(r[0] * k, r[1] * k, w1, w1 + 18);
    }
    return '<path class="zm" d="' + d + '" fill-rule="evenodd"/>';
  };
  // field at a point of the drawn board (viewBox units) – for tap input
  const feldAn = (x, y) => {
    const dx = x - BRETT_CX, dy = y - BRETT_CX, r = Math.hypot(dx, dy) * 170 / BRETT_K;
    if (r <= 6.35) return 'D25'; if (r <= 15.9) return 'S25'; if (r > 170) return 'M';
    const w = ((Math.atan2(dy, dx) * 180 / Math.PI + 90) % 360 + 360) % 360, n = ORDER[Math.round(w / 18) % 20];
    return (r > 162 ? 'D' : r > 99 && r <= 107 ? 'T' : 'S') + n;
  };
  const brett = (darts, ziel) => {
    const P = brettP;
    const sek = (r1, r2, w1, w2, f) => { const [a, b] = P(r2, w1), [c, d] = P(r2, w2), [e, g] = P(r1, w2), [i, j] = P(r1, w1); return '<path d="M' + f1(a) + ' ' + f1(b) + 'A' + r2 + ' ' + r2 + ' 0 0 1 ' + f1(c) + ' ' + f1(d) + 'L' + f1(e) + ' ' + f1(g) + 'A' + r1 + ' ' + r1 + ' 0 0 0 ' + f1(i) + ' ' + f1(j) + 'Z" fill="' + f + '"/>'; };
    const k = BRETT_K / 170;
    let s = '<svg viewBox="0 0 120 120"><circle cx="60" cy="60" r="60" fill="#111"/>';
    ORDER.forEach((n, i) => {
      const w1 = i * 18 - 9, w2 = w1 + 18, d = i % 2 === 0, e = d ? '#1c1c1c' : '#e9dfc4', f = d ? '#c62828' : '#2e7d32';
      s += sek(15.9 * k, 99 * k, w1, w2, e) + sek(99 * k, 107 * k, w1, w2, f) + sek(107 * k, 162 * k, w1, w2, e) + sek(162 * k, 170 * k, w1, w2, f);
      const [x, y] = P(56.5, i * 18); s += '<text x="' + f1(x) + '" y="' + f1(y + 1.8) + '">' + n + '</text>';
    });
    s += '<circle cx="60" cy="60" r="' + f1(15.9 * k) + '" fill="#2e7d32"/><circle cx="60" cy="60" r="' + f1(6.35 * k) + '" fill="#c62828"/>' + zielMarke(ziel);
    (darts || []).forEach((d, i) => {
      const p = brettPos(d, i);
      s += '<g transform="translate(' + f1(p[0]) + ' ' + f1(p[1]) + ')"><circle r="3.6" fill="' + ['#ff5252', '#40c4ff', '#ffd740'][i] + '" stroke="#000" stroke-width="1"/><text y="1.6" font-size="4.4" fill="#000">' + (i + 1) + '</text></g>';
    });
    return s + '</svg>';
  };

  // hit map: every field coloured by how often it was hit, or the darts as dots
  const HEAT = ['#1e3a5f', '#2a6fb0', '#22a7a0', '#7cc644', '#f2c12e', '#f07b22', '#e53935'];
  const heatBrett = (felder, xy, punkte) => {
    if (punkte) {
      let s = brett([]).replace('</svg>', '');
      (xy || []).forEach(([x, y]) => { const r = Math.hypot(x, y), f = r > 1.12 ? 1.12 / r : 1; s += '<circle cx="' + f1(60 + x * f * BRETT_K) + '" cy="' + f1(60 - y * f * BRETT_K) + '" r="1.4" fill="#00e5ff" fill-opacity=".75" stroke="#000" stroke-width=".3"/>'; });
      return s + '</svg>';
    }
    const P = brettP, k = BRETT_K / 170, max = Math.max(1, ...Object.values(felder || {}));
    const farbe = n => { if (!n) return '#262626'; const q = Math.pow(n / max, .6); return HEAT[Math.min(HEAT.length - 1, Math.floor(q * (HEAT.length - 1) + .0001))]; };
    const sek = (r1, r2, w1, w2, f) => { const [a, b] = P(r2, w1), [c, d] = P(r2, w2), [e, g] = P(r1, w2), [i, j] = P(r1, w1); return '<path d="M' + f1(a) + ' ' + f1(b) + 'A' + r2 + ' ' + r2 + ' 0 0 1 ' + f1(c) + ' ' + f1(d) + 'L' + f1(e) + ' ' + f1(g) + 'A' + r1 + ' ' + r1 + ' 0 0 0 ' + f1(i) + ' ' + f1(j) + 'Z" fill="' + f + '" stroke="#111" stroke-width=".35"/>'; };
    const n = f => (felder || {})[f] || 0;
    let s = '<svg viewBox="0 0 120 120"><circle cx="60" cy="60" r="60" fill="#111"/>';
    ORDER.forEach((z, i) => {
      const w1 = i * 18 - 9, w2 = w1 + 18;
      s += sek(15.9 * k, 99 * k, w1, w2, farbe(n('S' + z))) + sek(99 * k, 107 * k, w1, w2, farbe(n('T' + z))) + sek(107 * k, 162 * k, w1, w2, farbe(n('S' + z))) + sek(162 * k, 170 * k, w1, w2, farbe(n('D' + z)));
      const [x, y] = P(56.5, i * 18); s += '<text x="' + f1(x) + '" y="' + f1(y + 1.8) + '">' + z + '</text>';
    });
    s += '<circle cx="60" cy="60" r="' + f1(15.9 * k) + '" fill="' + farbe(n('S25')) + '" stroke="#111" stroke-width=".35"/><circle cx="60" cy="60" r="' + f1(6.35 * k) + '" fill="' + farbe(n('D25')) + '" stroke="#111" stroke-width=".35"/>';
    return s + '</svg>';
  };
  // aim map: points per dart for every aim point, with the player's spread (taken from the average)
  const feldMm = (x, y) => {
    const r = Math.hypot(x, y);
    if (r <= 6.35) return 'D25'; if (r <= 15.9) return 'S25'; if (r > 170) return 'M';
    const n = ORDER[Math.floor(((Math.atan2(x, y) * 180 / Math.PI + 9) % 360 + 360) % 360 / 18) % 20];
    return (r >= 99 && r <= 107 ? 'T' : r >= 162 ? 'D' : 'S') + n;
  };
  const wertMm = (x, y) => {
    const r = Math.hypot(x, y);
    if (r <= 6.35) return 50; if (r <= 15.9) return 25; if (r > 170) return 0;
    const n = ORDER[Math.floor(((Math.atan2(x, y) * 180 / Math.PI + 9) % 360 + 360) % 360 / 18) % 20];
    return r >= 99 && r <= 107 ? 3 * n : r >= 162 ? 2 * n : n;
  };
  // board values on a 2 mm raster, blurred with the player's spread = points per dart for every aim point
  const AIM_R = 86, AIM_N = 2 * AIM_R + 1;
  let aimRaster = null;
  const raster = () => aimRaster || (aimRaster = Float32Array.from({ length: AIM_N * AIM_N }, (_, k) => wertMm((k % AIM_N - AIM_R) * 2, (AIM_R - Math.floor(k / AIM_N)) * 2)));
  const kern = sg => { const m = Math.min(AIM_R, Math.ceil(1.5 * sg)), g = []; let w = 0; for (let k = -m; k <= m; k++) { const v = Math.exp(-(k * k * 4) / (2 * sg * sg)); g.push(v); w += v; } return { m, g: g.map(v => v / w) }; };
  const amPunkt = (sg, i0, j0) => { const r = raster(), { m, g } = kern(sg); let s = 0; for (let j = -m; j <= m; j++) { const jj = j0 + j; if (jj < 0 || jj >= AIM_N) continue; for (let i = -m; i <= m; i++) { const ii = i0 + i; if (ii >= 0 && ii < AIM_N) s += r[jj * AIM_N + ii] * g[i + m] * g[j + m]; } } return s; };
  const verwischen = sg => {
    const r = raster(), { m, g } = kern(sg), a = new Float32Array(r.length), b = new Float32Array(r.length);
    for (let j = 0; j < AIM_N; j++) for (let i = 0; i < AIM_N; i++) { let s = 0; for (let k = -m; k <= m; k++) { const ii = i + k; if (ii >= 0 && ii < AIM_N) s += r[j * AIM_N + ii] * g[k + m]; } a[j * AIM_N + i] = s; }
    for (let j = 0; j < AIM_N; j++) for (let i = 0; i < AIM_N; i++) { let s = 0; for (let k = -m; k <= m; k++) { const jj = j + k; if (jj >= 0 && jj < AIM_N) s += a[jj * AIM_N + i] * g[k + m]; } b[j * AIM_N + i] = s; }
    return b;
  };
  const T20_IJ = [AIM_R, AIM_R - 52];
  const aimCache = {};
  const aimKarte = avg => {
    const key = Math.round(avg);
    if (aimCache[key]) return aimCache[key];
    let lo = 1, hi = 160; // spread (mm) that gives this average when aiming at T20
    for (let n = 0; n < 18; n++) { const m = (lo + hi) / 2; if (amPunkt(m, ...T20_IJ) * 3 > key) lo = m; else hi = m; }
    const sg = (lo + hi) / 2, b = verwischen(sg), zellen = [];
    let best = [-1, 0, 0], min = 1e9;
    for (let j = 0; j < AIM_N; j++) for (let i = 0; i < AIM_N; i++) {
      const x = (i - AIM_R) * 2, y = (AIM_R - j) * 2;
      if (Math.hypot(x, y) > 170) continue;
      const e = b[j * AIM_N + i];
      if (e > best[0]) best = [e, x, y];
      if (e < min) min = e;
      if (i % 3 === 2 && j % 3 === 2) zellen.push([x, y, e]);
    }
    const t20 = b[T20_IJ[1] * AIM_N + T20_IJ[0]];
    if (best[0] - t20 < 0.5 / 3) best = [t20, 0, 104]; // less than half a point per visit: stay on T20
    return (aimCache[key] = { sg, zellen, best, min, t20, feld: feldMm(best[1], best[2]) });
  };
  const aimBrett = k => {
    const K = BRETT_K / 170, S = 6 * K, h = f1(S * 1.04), wege = HEAT.map(() => ''), span = Math.max(1e-6, k.best[0] - k.min);
    k.zellen.forEach(([x, y, e]) => { const i = Math.min(HEAT.length - 1, Math.floor(Math.pow((e - k.min) / span, 1.6) * HEAT.length)); wege[i] += 'M' + f1(60 + x * K - S / 2) + ' ' + f1(60 - y * K - S / 2) + 'h' + h + 'v' + h + 'h-' + h + 'z'; });
    let s = '<svg viewBox="0 0 120 120"><defs><clipPath id="aimc"><circle cx="60" cy="60" r="' + f1(170 * K) + '"/></clipPath></defs><circle cx="60" cy="60" r="60" fill="#111"/><g clip-path="url(#aimc)">' +
      wege.map((d, i) => d ? '<path d="' + d + '" fill="' + HEAT[i] + '"/>' : '').join('') + '</g><g fill="none" stroke="#000" stroke-opacity=".5" stroke-width=".35">' +
      [6.35, 15.9, 99, 107, 162, 170].map(r => '<circle cx="60" cy="60" r="' + f1(r * K) + '"/>').join('') +
      ORDER.map((n, i) => { const [a, b] = brettP(15.9 * K, i * 18 - 9), [c, d] = brettP(170 * K, i * 18 - 9); return '<path d="M' + f1(a) + ' ' + f1(b) + 'L' + f1(c) + ' ' + f1(d) + '"/>'; }).join('') + '</g>';
    ORDER.forEach((n, i) => { const [x, y] = brettP(56.5, i * 18); s += '<text x="' + f1(x) + '" y="' + f1(y + 1.8) + '">' + n + '</text>'; });
    return s + '<g transform="translate(' + f1(60 + k.best[1] * K) + ' ' + f1(60 - k.best[2] * K) + ')"><circle r="3.4" fill="none" stroke="#fff" stroke-width="1.1"/><circle r="1" fill="#fff"/></g></svg>';
  };
  const linie = (werte, b, h) => {
    if (werte.length < 2) return '';
    const lo = Math.min(...werte), hi = Math.max(...werte), sp = hi - lo || 1;
    const pt = werte.map((v, i) => f1(i * b / (werte.length - 1)) + ',' + f1(h - 4 - (v - lo) / sp * (h - 8)));
    return '<svg viewBox="0 0 ' + b + ' ' + h + '" preserveAspectRatio="none" class="spark"><polyline points="' + pt.join(' ') + '" fill="none" stroke="var(--primary-color)" stroke-width="2" vector-effect="non-scaling-stroke"/>' +
      '<circle cx="' + pt[pt.length - 1].split(',')[0] + '" cy="' + pt[pt.length - 1].split(',')[1] + '" r="3" fill="var(--primary-color)"/></svg>';
  };
  const MEDAILLE = ['#5f6368', '#cd7f32', '#c0c7d0', '#ffc83d'];
  // calibration: camera image (px) -> board (mm, centre 0, y down, 20 on top)
  const RADIEN = [170, 162, 107, 99];
  const mul3 = (a, b) => a.map(r => [0, 1, 2].map(j => r[0] * b[0][j] + r[1] * b[1][j] + r[2] * b[2][j]));
  const inv3 = m => {
    const [a, b, c] = m[0], [d, e, f] = m[1], [g, h, i] = m[2], A2 = e * i - f * h, B2 = f * g - d * i, C2 = d * h - e * g, det = a * A2 + b * B2 + c * C2;
    return [[A2 / det, (c * h - b * i) / det, (b * f - c * e) / det], [B2 / det, (a * i - c * g) / det, (c * d - a * f) / det], [C2 / det, (b * g - a * h) / det, (a * e - b * d) / det]];
  };
  const proj = (m, x, y) => { const w = m[2][0] * x + m[2][1] * y + m[2][2]; return [(m[0][0] * x + m[0][1] * y + m[0][2]) / w, (m[1][0] * x + m[1][1] * y + m[1][2]) / w]; };
  const homCache = new Map();
  const entzerrung = kal => {
    // least squares over all calibration points (4 rings × 20 + bull); once per calibration
    if (!kal || !kal.ringe) return null;
    const key = JSON.stringify(kal); if (homCache.has(key)) return homCache.get(key);
    const src = [], dst = [];
    kal.ringe.forEach((r, j) => (r || []).forEach((p, k) => { const w = (9 + 18 * k) * Math.PI / 180; src.push(p); dst.push([RADIEN[j] * Math.sin(w), -RADIEN[j] * Math.cos(w)]); }));
    if (Array.isArray(kal.bull)) { src.push(kal.bull); dst.push([0, 0]); }
    let H = null;
    if (src.length >= 8) {
      let mx = 0, my = 0, sd = 0; src.forEach(p => { mx += p[0]; my += p[1]; }); mx /= src.length; my /= src.length;
      src.forEach(p => { sd += Math.hypot(p[0] - mx, p[1] - my); }); const sc = Math.SQRT2 * src.length / sd;
      const M = Array.from({ length: 8 }, () => new Array(9).fill(0));
      src.forEach((p, n) => {
        const x = (p[0] - mx) * sc, y = (p[1] - my) * sc, u = dst[n][0] / 170, v = dst[n][1] / 170;
        [[x, y, 1, 0, 0, 0, -u * x, -u * y, u], [0, 0, 0, x, y, 1, -v * x, -v * y, v]].forEach(r => { for (let i = 0; i < 8; i++) for (let j = 0; j < 9; j++) M[i][j] += r[i] * r[j]; });
      });
      let ok = true;
      for (let i = 0; i < 8 && ok; i++) {
        let m = i; for (let r = i + 1; r < 8; r++) if (Math.abs(M[r][i]) > Math.abs(M[m][i])) m = r;
        [M[i], M[m]] = [M[m], M[i]]; if (Math.abs(M[i][i]) < 1e-12) { ok = false; break; }
        for (let r = 0; r < 8; r++) if (r !== i) { const f = M[r][i] / M[i][i]; for (let j = i; j < 9; j++) M[r][j] -= f * M[i][j]; }
      }
      if (ok) { const hv = M.map((r, i) => r[8] / r[i]); H = mul3(mul3([[170, 0, 0], [0, 170, 0], [0, 0, 1]], [[hv[0], hv[1], hv[2]], [hv[3], hv[4], hv[5]], [hv[6], hv[7], 1]]), [[sc, 0, -sc * mx], [0, sc, -sc * my], [0, 0, 1]]); }
    }
    homCache.set(key, H); return H;
  };
  const netzLinien = () => {
    const P = (r, w) => [r * Math.sin(w * Math.PI / 180), -r * Math.cos(w * Math.PI / 180)];
    const ringe = [170, 162, 107, 99, 15.9, 6.35].map(r => { const l = []; for (let w = 0; w <= 360; w += 5) l.push(P(r, w)); return l; });
    const strahlen = []; for (let k = 0; k < 20; k++) strahlen.push([P(15.9, 9 + 18 * k), P(170, 9 + 18 * k)]);
    return ringe.concat(strahlen);
  };
  const pfad = (linien, f) => linien.map(l => 'M' + l.map(p => { const q = f ? f(p) : p; return q[0].toFixed(1) + ' ' + q[1].toFixed(1); }).join('L')).join('');
  const NETZ_MM = pfad(netzLinien());
  const dartMM = (d, i) => {
    if (typeof d.x === 'number' && typeof d.y === 'number') { const r = Math.hypot(d.x, d.y), f = r > 1.25 ? 1.25 / r : 1; return [d.x * f * 170, -d.y * f * 170]; }
    const P = (r, w) => [r * Math.sin(w * Math.PI / 180), -r * Math.cos(w * Math.PI / 180)], x = d.f || '';
    if (x === 'D25') return P(3, i * 120); if (x === 'S25') return P(11, i * 120); if (x === 'M' || !x) return P(190, 200 + i * 30);
    const w = ORDER.indexOf(parseInt(x.slice(1), 10)) * 18 + [-4, 3, 0][i];
    return P(x[0] === 'T' ? 103 : x[0] === 'D' ? 166 : 135, w);
  };
  const SPIEL_CSS = `
:host(:fullscreen){background:var(--primary-background-color,#111);overflow:auto;display:block}
:host(:fullscreen) ha-card{min-height:100vh;border-radius:0}
.lobby .sliste{display:grid;gap:6px;margin-bottom:10px}
.sp{display:flex;align-items:center;gap:10px;border-radius:14px;padding:8px 8px 8px 12px}
.sp .nr{width:24px;height:24px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:12.5px;font-weight:700;background:var(--primary-color);color:var(--text-primary-color,#fff);flex:none}
.sp .nm{flex:1;font-weight:600;font-size:15px}
.sp .nm small{font-weight:500;color:var(--secondary-text-color);margin-left:6px}
.sp button{width:36px;height:36px;border-radius:10px;background:transparent;display:flex;align-items:center;justify-content:center}
.sp button ha-icon{--mdc-icon-size:20px;color:var(--secondary-text-color)}
.spieler{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:8px}
.sk{position:relative;border-radius:20px;padding:10px 12px 10px;transition:background .25s ease,box-shadow .25s ease,opacity .25s ease;opacity:.78}
.sk.aktiv{opacity:1;background:color-mix(in srgb,var(--red-color,#e53935) 14%,transparent);border-color:color-mix(in srgb,var(--red-color,#e53935) 55%,transparent);box-shadow:0 0 0 2px color-mix(in srgb,var(--red-color,#e53935) 45%,transparent)}
.sk .sn{display:flex;align-items:center;gap:6px;font-weight:700;font-size:15px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.sk .sn ha-icon{--mdc-icon-size:16px;color:var(--secondary-text-color)}
.sk .lg{margin-left:auto;font-size:12.5px;font-weight:700;padding:2px 8px;border-radius:999px;background:color-mix(in srgb,var(--primary-text-color) 10%,transparent)}
.sk .sr{font-size:54px;font-weight:800;line-height:1.05;letter-spacing:-.03em;margin:4px 0 2px;font-variant-numeric:tabular-nums}
.sk .sa{font-size:12.5px;color:var(--secondary-text-color);line-height:1.4}
.sk .sw{display:flex;gap:4px;margin-top:6px;flex-wrap:wrap}
.sk .sw span,.weg span{font-size:12.5px;font-weight:700;padding:3px 8px;border-radius:8px;background:color-mix(in srgb,var(--green-color,#43a047) 20%,transparent);color:var(--green-color,#43a047)}
.mitte{display:grid;grid-template-columns:1fr;gap:10px;margin-top:10px}
.aufn{border-radius:20px;padding:12px;text-align:center;display:flex;flex-direction:column;justify-content:center}
.aufn .hinw{display:flex;align-items:center;justify-content:center;gap:8px;font-size:15px;font-weight:700;margin-bottom:10px;min-height:22px}
.aufn .hinw ha-icon{--mdc-icon-size:20px}
.aufn.bust .hinw{color:var(--red-color,#e53935)}.aufn.check .hinw{color:var(--green-color,#43a047)}
.dartsz{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}
.dz{border-radius:16px;padding:10px 4px;display:flex;flex-direction:column;align-items:center;gap:2px;min-height:64px;justify-content:center}
.dz b{font-size:26px;font-weight:800;line-height:1.1}
.dz small{font-size:12px;color:var(--secondary-text-color)}
.dz.leer b{color:var(--secondary-text-color);font-weight:500}
.dz:nth-child(1){--dc:#ff5252}.dz:nth-child(2){--dc:#40c4ff}.dz:nth-child(3){--dc:#ffd740}
.dz:not(.leer){box-shadow:inset 0 -3px 0 var(--dc)}
.summe{display:flex;align-items:baseline;justify-content:center;gap:12px;margin-top:10px}
.summe b{font-size:42px;font-weight:800;line-height:1;font-variant-numeric:tabular-nums}
.summe span{font-size:14px;color:var(--secondary-text-color)}
.weg{display:flex;justify-content:center;gap:6px;margin-top:10px;flex-wrap:wrap}
.weg span{font-size:15px;padding:5px 12px}
.brett{display:flex;align-items:center;justify-content:center}
.brett svg{width:min(100%,300px);height:auto}
.brett.live{position:relative;width:min(100%,420px);aspect-ratio:1;margin:0 auto;border-radius:50%;overflow:hidden;background:transparent;cursor:pointer;clip-path:circle(50%);isolation:isolate}
.brett.live svg{position:absolute;inset:0;width:100%;height:100%}
.brett.grafik{cursor:pointer;position:relative}
.brett.tippen{cursor:crosshair;position:relative}.brett.tippen svg{width:min(100%,440px);touch-action:manipulation}
.brett .tipp{position:absolute;left:4px;bottom:4px;display:flex;align-items:center;gap:4px;border-radius:10px;padding:4px 9px;font-size:12px;font-weight:700;background:rgba(0,0,0,.55);color:#fff;border:0;cursor:pointer;z-index:2}
.brett .tipp ha-icon{--mdc-icon-size:16px}.brett .tipp.an{background:var(--primary-color)}
.kseg{display:flex;gap:6px;margin:0 auto 8px;width:100%;max-width:460px}.kseg button{flex:1;display:flex;align-items:center;justify-content:center;gap:5px;padding:8px 4px;border-radius:12px;font:inherit;font-size:13px;font-weight:700;color:inherit;cursor:pointer;min-width:0}
.kseg button ha-icon{--mdc-icon-size:17px}.kseg button.an,.kp .k.an{background:var(--primary-color);color:#fff;border-color:var(--primary-color)}
.kp{display:grid;gap:7px;width:100%;max-width:460px;margin:0 auto}.kgrid{display:grid;grid-template-columns:repeat(5,1fr);gap:7px}.kgrid.k2{grid-template-columns:1fr 1fr}.kgrid.k3{grid-template-columns:repeat(3,1fr)}
.kp .k{min-height:54px;border-radius:14px;font:inherit;font-size:21px;font-weight:800;color:inherit;cursor:pointer;touch-action:manipulation;display:flex;align-items:center;justify-content:center;gap:1px;font-variant-numeric:tabular-nums}
.kp .k i{font-style:normal;font-size:13px;opacity:.7}.kp .k:disabled{opacity:.35;cursor:default}.kp .k.miss{color:var(--red-color,#e53935)}.kp .k.ok{background:var(--primary-color);color:#fff;border:0}
.ksum{display:flex;align-items:baseline;justify-content:center;gap:10px;border-radius:14px;padding:10px}.ksum b{font-size:40px;font-weight:800;line-height:1}.ksum small{font-size:12.5px;color:var(--secondary-text-color)}
.tasten{position:absolute;right:4px;bottom:4px;border-radius:10px;padding:4px 10px;font-size:15px;font-weight:800;background:var(--primary-color);color:#fff;z-index:2;letter-spacing:.04em}
.lvh,.lv{position:absolute;inset:0}
.lv img{position:absolute;left:0;top:0;max-width:none;transform-origin:0 0;display:block}
.netz path{fill:none;stroke:#00e5a8;stroke-width:1.2;vector-effect:non-scaling-stroke;opacity:.85}
.brett .pf circle{stroke:#000;stroke-width:2}.brett .pf text{font-size:19px;font-weight:800;fill:#000;text-anchor:middle}
.bk{position:absolute;bottom:4%;left:50%;transform:translateX(-50%);display:flex;gap:6px}
.bk button,.bk span{font-size:11.5px;font-weight:700;color:#fff;padding:4px 9px;border-radius:10px;background:rgba(0,0,0,.6)}
.bk button.an{background:rgba(0,150,110,.85)}
.brett text{font-size:5px;font-weight:700;fill:#ddd;text-anchor:middle;font-family:Arial,sans-serif}
.brett g text{fill:#000;font-size:4.4px}
.leiste{display:grid;grid-template-columns:1fr 1fr 1.3fr;gap:8px;margin-top:10px}
.lk{display:flex;align-items:center;justify-content:center;gap:8px;min-height:56px;border-radius:18px;font-size:15px;font-weight:700}
.lk ha-icon{--mdc-icon-size:22px}
.lk.weiter{color:#fff;background:linear-gradient(135deg,var(--primary-color),color-mix(in srgb,var(--primary-color) 70%,#000))}
.vl{display:grid;gap:4px}
.vz{display:grid;grid-template-columns:minmax(70px,1fr) 2fr 48px 48px;align-items:center;gap:8px;padding:6px 8px;border-radius:12px;font-size:13.5px;cursor:pointer}
.vz:hover{background:color-mix(in srgb,var(--primary-text-color) 6%,transparent)}
.vz b{text-align:right}.vz .r{text-align:right;color:var(--secondary-text-color)}
.vz.bu b{color:var(--red-color,#e53935)}.vz.co b{color:var(--green-color,#43a047)}
.sieg{text-align:center;padding:18px 8px 8px}
.sieg ha-icon{--mdc-icon-size:56px;color:var(--amber-color,#ffc107)}
.sieg h2{margin:6px 0 2px;font-size:28px}
.sieg div{color:var(--secondary-text-color)}
.zweier{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:12px}
.bo{display:grid;gap:6px}
.boz{display:flex;align-items:center;gap:10px;border-radius:14px;padding:10px 12px;font-size:15px}
.boz.aktiv{box-shadow:0 0 0 2px var(--red-color,#e53935)}
.boz b{flex:1}.boz span{color:var(--secondary-text-color)}
.viele .sk{padding:8px 10px}.viele .sk .sr{font-size:38px;margin:2px 0 0}.viele .sk .sa{font-size:11.5px}
@container (min-width:700px){.mitte{grid-template-columns:1.4fr 1fr}.sk .sr{font-size:64px}}
@container (max-width:420px){.sk .sr{font-size:44px}.spieler{grid-template-columns:repeat(auto-fit,minmax(130px,1fr))}.dz b{font-size:22px}}
.arten{display:grid;grid-template-columns:repeat(4,1fr);gap:6px}
.arten button{display:flex;flex-direction:column;align-items:center;gap:4px;border-radius:14px;padding:10px 4px;font-size:13px;font-weight:700}
.arten button ha-icon{--mdc-icon-size:22px}
.arten button.an,.achips button.an{background:color-mix(in srgb,var(--primary-color) 22%,transparent);border-color:var(--primary-color);color:var(--primary-color)}
.achips{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px}
.achips button{display:flex;align-items:center;gap:6px;border-radius:999px;padding:7px 12px;font-size:13.5px;font-weight:600}
.achips button ha-icon{--mdc-icon-size:18px}
.atiles{display:grid;grid-template-columns:repeat(auto-fill,minmax(158px,1fr));gap:6px;margin-top:10px}
.atiles button{display:flex;align-items:center;gap:10px;border-radius:14px;padding:9px 10px;text-align:left;min-width:0;position:relative}
.atiles button>ha-icon{--mdc-icon-size:22px;flex:none;opacity:.85}
.atiles .an1{display:flex;flex-direction:column;min-width:0;line-height:1.2}
.atiles .an1 b{font-size:13.5px;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.atiles .an1 small{font-size:11.5px;color:var(--secondary-text-color);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.atiles .spz{position:absolute;top:5px;right:7px;display:flex;align-items:center;gap:1px;font-size:10.5px;font-weight:700;color:var(--secondary-text-color)}
.atiles .spz ha-icon{--mdc-icon-size:12px}
.atiles button.an{background:color-mix(in srgb,var(--primary-color) 22%,transparent);border-color:var(--primary-color)}
.atiles button.an b,.atiles button.an>ha-icon{color:var(--primary-color);opacity:1}
.atiles button.passtnicht{opacity:.5}
.regel{display:flex;gap:8px;align-items:flex-start;font-size:13px;line-height:1.45;color:var(--secondary-text-color);margin:10px 2px 2px}
.regel ha-icon{--mdc-icon-size:18px;flex:none;margin-top:1px}
.zm{fill:rgba(0,229,255,.28);stroke:#00e5ff;stroke-width:.9;animation:ad-ziel 1.6s ease-in-out infinite}
@keyframes ad-ziel{50%{fill:rgba(0,229,255,.12)}}
@media (prefers-reduced-motion:reduce){.zm{animation:none}}
.ziel{display:inline-flex;align-items:center;gap:8px;margin:10px auto 0;padding:6px 16px;border-radius:999px;font-weight:800;font-size:20px;background:color-mix(in srgb,#00e5ff 18%,transparent);color:var(--primary-text-color);border:1px solid color-mix(in srgb,#00e5ff 55%,transparent)}
.ziel small{font-size:12.5px;font-weight:600;color:var(--secondary-text-color)}
.sk .zk{display:inline-flex;align-items:center;gap:4px;font-size:12px;font-weight:700;padding:2px 8px;border-radius:8px;margin-top:6px;background:color-mix(in srgb,#00e5ff 16%,transparent)}
.sk.raus{opacity:.38;filter:grayscale(1)}
.sk .herz{color:var(--red-color,#e53935);letter-spacing:1px}
.sk .kil{font-size:11px;font-weight:800;padding:2px 7px;border-radius:999px;background:var(--red-color,#e53935);color:#fff;margin-left:4px}
.ct{display:grid;gap:0;border-radius:18px;overflow:hidden}
.ct .r{display:grid;grid-template-columns:var(--sp);align-items:center;min-height:40px;border-top:1px solid color-mix(in srgb,var(--primary-text-color) 8%,transparent)}
.ct .r:first-child{border-top:none}
.ct .r>*{text-align:center;padding:4px 2px;height:100%;display:flex;align-items:center;justify-content:center;box-sizing:border-box}
.ct .kopf>*{font-weight:700;font-size:14px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;padding:8px 4px}
.ct .z{font-weight:800;font-size:18px}
.ct .r.zu .z{color:var(--secondary-text-color);text-decoration:line-through;opacity:.6}
.ct .r.zu .m svg{opacity:.45}
.ct .akt{background:color-mix(in srgb,var(--red-color,#e53935) 12%,transparent)}
.ct .m svg{width:26px;height:26px;fill:none;stroke:currentColor;stroke-width:2.6;stroke-linecap:round}
.ct .m.v3 svg{stroke:var(--green-color,#43a047)}
.ct .pk>*{font-size:28px;font-weight:800;font-variant-numeric:tabular-nums}
.ct .mp>*{font-size:12.5px;color:var(--secondary-text-color)}
.ct .r.verd .z{color:var(--secondary-text-color);font-size:16px;letter-spacing:.05em}
.ct .z{white-space:nowrap}
.zleiste{display:grid;grid-template-columns:repeat(7,1fr);gap:4px;margin:8px 0 10px;padding:6px;border-radius:16px}
.zleiste>div{display:flex;flex-direction:column;align-items:center;gap:2px;padding:4px 0}
.zleiste b{font-size:17px;font-weight:800}
.zleiste .m svg{width:22px;height:22px;fill:none;stroke:currentColor;stroke-width:2.6;stroke-linecap:round}
.zleiste .m{min-height:22px}
.zleiste .zu b{color:var(--secondary-text-color);text-decoration:line-through;opacity:.6}
.zleiste .zu .m svg{stroke:var(--green-color,#43a047)}
.sk .sr small.ball{font-size:.55em;vertical-align:middle}
.rang{display:grid;gap:6px;margin-top:12px}
.rang div{display:grid;grid-template-columns:32px 1fr auto;align-items:center;gap:8px;padding:10px 12px;border-radius:14px;font-size:15px}
.rang b{font-size:20px;font-variant-numeric:tabular-nums}
.rang span:first-child{font-weight:800;color:var(--secondary-text-color)}
.rang .g span:first-child{color:var(--amber-color,#ffc107)}
.vor{display:flex;flex-wrap:wrap;justify-content:center;gap:5px;margin-top:10px}
.vor span{display:inline-flex;align-items:center;gap:5px;font-size:12.5px;font-weight:800;padding:3px 9px;border-radius:999px;background:color-mix(in srgb,var(--primary-text-color) 8%,transparent)}
.vor span:first-child{background:color-mix(in srgb,var(--primary-color) 20%,transparent)}
.vor i{font-style:normal;font-weight:600;color:var(--secondary-text-color)}
.vor .b{color:var(--red-color,#e53935)}.vor .c{color:var(--green-color,#43a047)}
.seg.breit{margin:0 0 10px;flex-wrap:nowrap}.seg.breit button{flex:1;display:flex;align-items:center;justify-content:center;gap:4px}
.tban{display:flex;align-items:center;gap:8px;justify-content:center;margin:0 0 10px;padding:7px 12px;border-radius:14px;font-weight:700;font-size:14px;background:color-mix(in srgb,var(--amber-color,#ffc107) 18%,transparent)}
.tban ha-icon{--mdc-icon-size:20px;color:var(--amber-color,#ffc107)}.tban small{font-weight:600;color:var(--secondary-text-color)}
.baum{display:flex;gap:14px;overflow-x:auto;padding:4px 2px 8px;scrollbar-width:thin}
.brd{display:flex;flex-direction:column;gap:8px;min-width:118px;flex:1}.brd>div{display:flex;flex-direction:column;justify-content:space-around;gap:10px;flex:1}
.liga>small{display:block;font-size:11.5px;font-weight:700;color:var(--secondary-text-color);text-transform:uppercase;letter-spacing:.04em;margin:6px 2px}
.ltab{width:100%;border-collapse:collapse;font-size:13.5px}.ltab th{font-size:11px;color:var(--secondary-text-color);font-weight:700;text-align:right;padding:4px 6px}.ltab td{padding:6px;text-align:right;border-top:1px solid color-mix(in srgb,var(--primary-text-color) 8%,transparent)}
.ltab td:nth-child(2){text-align:left;font-weight:600;width:100%}.ltab td:first-child{color:var(--secondary-text-color);text-align:left}.ltab tr.w td{color:var(--green-color,#43a047)}
.tarten{grid-template-columns:repeat(auto-fill,minmax(230px,1fr));margin:0 0 10px}.tarten .an1 b{padding-right:48px}
.baum.fin{justify-content:center}.baum.fin .brd{flex:0 1 300px}
.tsek{display:block;font-size:11.5px;font-weight:700;color:var(--secondary-text-color);text-transform:uppercase;letter-spacing:.04em;margin:10px 2px 4px}.tsek:first-child{margin-top:2px}
.grps{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:8px}.grp{border-radius:14px;padding:8px 10px}.grp>small{font-weight:800;font-size:12.5px}.grp.akt{box-shadow:0 0 0 2px color-mix(in srgb,var(--amber-color,#ffc107) 35%,transparent)}.grp .lsl{margin-top:8px;grid-template-columns:1fr}
.tkopf{display:flex;align-items:center;gap:8px;font-size:12px;font-weight:800;color:var(--secondary-text-color);text-transform:uppercase;letter-spacing:.04em;margin:8px 2px 2px}.tkopf:first-child{margin-top:0}.tkopf .hc{margin-left:auto}
.hc{display:inline-flex;align-items:center;gap:2px;flex:none}.hc button{width:28px;height:28px;border-radius:9px;font-size:15px;font-weight:700}.hc b{min-width:34px;text-align:center;font-size:13px}
.reihe small.rk{display:block;font-size:11.5px;font-weight:500;color:var(--secondary-text-color)}
.sk>.wf{font-size:12px;font-weight:600;color:var(--secondary-text-color);margin:1px 0 -2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.lsl{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:6px}.lsp{display:flex;align-items:center;gap:8px;border-radius:12px;padding:7px 10px;font-size:13px}.lsp span{flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.lsp span:last-child{text-align:right}
.lsp b{min-width:34px;text-align:center}.lsp .w{font-weight:700}.lsp .l{opacity:.55}.lsp.akt{border-color:var(--primary-color)}
.brd>small{font-size:11.5px;font-weight:700;color:var(--secondary-text-color);text-align:center;text-transform:uppercase;letter-spacing:.04em}
.bm{border-radius:12px;overflow:hidden;font-size:13px;border:1px solid color-mix(in srgb,var(--primary-text-color) 10%,transparent)}
.bm.akt{border-color:var(--amber-color,#ffc107);box-shadow:0 0 0 2px color-mix(in srgb,var(--amber-color,#ffc107) 35%,transparent)}
.bm div{display:flex;align-items:center;gap:6px;padding:5px 9px;min-height:18px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.bm div+div{border-top:1px solid color-mix(in srgb,var(--primary-text-color) 8%,transparent)}
.bm .w{font-weight:800;color:var(--green-color,#43a047)}.bm .l{opacity:.45;text-decoration:line-through}.bm .o{color:var(--secondary-text-color);font-style:italic}
.champ{text-align:center;padding:14px 8px 6px}.champ .pk{font-size:58px;line-height:1;display:inline-block;animation:champ 1.2s cubic-bezier(.2,1.6,.4,1) both}
.champ h2{margin:6px 0 0;font-size:26px}.champ div{color:var(--secondary-text-color);font-weight:600}
@keyframes champ{0%{transform:scale(.2) rotate(-25deg);opacity:0}100%{transform:none;opacity:1}}`;
  const KAMERA_KEYS = ['camera.camera_1', 'camera.camera_2', 'camera.camera_3'];
  /* ---------- effects: one-shot animations for what happens at the board ----------
     Triggered only by new darts and finished visits (never by undo or corrections), CSS transforms and
     opacity only, removed from the page when done, off while the card is hidden. Optional sounds use
     Web Audio (no files) and only play while the caller is switched on. */
  const FX_CSS = `
ha-card{position:relative}
.fx{position:absolute;inset:0;pointer-events:none;overflow:hidden;z-index:5;border-radius:inherit;container-type:size}
.fxp{position:absolute;left:0;top:0;width:0;height:0}
.fxd{position:absolute;left:-5px;top:-5px;width:58px;height:58px;transform-origin:5px 5px;animation:fx-flug .24s cubic-bezier(.35,0,.85,.35) both,fx-wipp .55s .24s ease-out,fx-weg .35s 1.25s ease-in forwards}
.fxd.miss{animation:fx-flug .24s cubic-bezier(.35,0,.85,.35) both,fx-fall .7s .3s cubic-bezier(.5,0,.9,.6) forwards}
@keyframes fx-flug{0%{transform:translate(150px,210px) scale(3) rotate(-10deg);opacity:0;filter:blur(3px)}30%{opacity:1}100%{transform:none;opacity:1;filter:none}}
@keyframes fx-wipp{0%{transform:rotate(0)}20%{transform:rotate(-7deg)}45%{transform:rotate(4deg)}70%{transform:rotate(-2deg)}100%{transform:rotate(0)}}
@keyframes fx-weg{to{opacity:0}}
@keyframes fx-fall{0%{transform:none}25%{transform:translate(6px,-8px) rotate(25deg)}100%{transform:translate(24px,170px) rotate(115deg);opacity:0}}
.fxr{position:absolute;left:-30px;top:-30px;width:60px;height:60px;border-radius:50%;border:3px solid var(--k,#fff);animation:fx-ring .6s .2s ease-out both}
@keyframes fx-ring{0%{transform:scale(.1);opacity:.95}100%{transform:scale(1.6);opacity:0}}
.fxs{position:absolute;left:0;top:-1.5px;width:16px;height:3px;border-radius:3px;background:linear-gradient(90deg,#fff,var(--k,#ffb300));transform-origin:0 50%;animation:fx-funke .5s .22s ease-out both}
@keyframes fx-funke{0%{transform:rotate(var(--a)) translateX(2px) scaleX(.3);opacity:1}100%{transform:rotate(var(--a)) translateX(var(--w,34px)) scaleX(1);opacity:0}}
.fxb{position:absolute;left:-70px;top:-70px;width:140px;height:140px;border-radius:50%;background:radial-gradient(circle,var(--k) 0%,transparent 65%);animation:fx-blitz .7s .2s ease-out both;mix-blend-mode:screen}
@keyframes fx-blitz{0%{transform:scale(.2);opacity:1}100%{transform:scale(1.4);opacity:0}}
.fxc{position:absolute;left:0;top:0;transform:translate(-50%,-150%);white-space:nowrap;font-weight:900;font-size:13px;letter-spacing:.06em;padding:3px 9px;border-radius:999px;color:#fff;background:var(--k,#333);box-shadow:0 2px 10px rgba(0,0,0,.4);animation:fx-chip 1.3s .2s ease-out both}
@keyframes fx-chip{0%{transform:translate(-50%,-60%) scale(.4);opacity:0}15%{transform:translate(-50%,-160%) scale(1.12);opacity:1}30%{transform:translate(-50%,-150%) scale(1)}80%{opacity:1}100%{transform:translate(-50%,-230%);opacity:0}}
.fx-treffer{animation:fx-brett .22s ease-out}
@keyframes fx-brett{0%{transform:none}35%{transform:translate(1.5px,1px) scale(.992)}70%{transform:translate(-1px,0)}100%{transform:none}}
ha-card.fx-wackeln{animation:fx-wackeln .5s cubic-bezier(.36,.07,.19,.97)}
@keyframes fx-wackeln{10%,90%{transform:translateX(-2px)}20%,80%{transform:translateX(4px)}30%,50%,70%{transform:translateX(-7px)}40%,60%{transform:translateX(7px)}}
ha-card.fx-stoss{animation:fx-stoss .45s ease-out}
@keyframes fx-stoss{0%{transform:none}20%{transform:scale(1.012) translateY(-2px)}45%{transform:scale(.996) translateY(1px)}100%{transform:none}}
.gross{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;animation:fx-aus .5s var(--ende,2.5s) ease-in forwards}
@keyframes fx-aus{to{opacity:0}}
.gross .bg{position:absolute;inset:0;background:radial-gradient(ellipse at 50% 45%,rgba(0,0,0,.2),rgba(0,0,0,.78));animation:fx-ein .3s both}
.gross.bust .bg{background:radial-gradient(ellipse at 50% 45%,rgba(120,0,0,.25),rgba(60,0,0,.85))}
.gross.gold .bg{background:radial-gradient(ellipse at 50% 40%,rgba(80,55,0,.35),rgba(0,0,0,.82))}
@keyframes fx-ein{from{opacity:0}}
.gross .wort{position:relative;font-weight:900;font-size:clamp(46px,22cqmin,170px);line-height:.92;letter-spacing:-.02em;padding:0 .08em;
 background:linear-gradient(180deg,#fffbe6 0%,#ffe57f 30%,#ffb300 52%,#a86b00 56%,#ffd54f 80%,#fff3c4 100%);-webkit-background-clip:text;background-clip:text;color:transparent;
 filter:drop-shadow(0 5px 0 rgba(0,0,0,.35)) drop-shadow(0 0 28px rgba(255,190,0,.55));animation:fx-slam .6s cubic-bezier(.2,1.5,.4,1) both}
.gross .wort.lang{font-size:clamp(30px,11cqmin,96px)}
.gross.silber .wort{background:linear-gradient(180deg,#ffffff 0%,#e0e6ec 45%,#7b8794 55%,#cfd8dc 80%,#ffffff 100%);-webkit-background-clip:text;background-clip:text;filter:drop-shadow(0 4px 0 rgba(0,0,0,.35)) drop-shadow(0 0 22px rgba(160,200,255,.5))}
.gross.gruen .wort{background:linear-gradient(180deg,#f1fff4 0%,#b9f6ca 35%,#00c853 55%,#007e33 60%,#69f0ae 85%,#e8fff0 100%);-webkit-background-clip:text;background-clip:text;filter:drop-shadow(0 5px 0 rgba(0,0,0,.35)) drop-shadow(0 0 30px rgba(0,230,118,.6))}
.gross.grau .wort{background:linear-gradient(180deg,#fafafa,#9e9e9e 55%,#616161 60%,#bdbdbd);-webkit-background-clip:text;background-clip:text;filter:drop-shadow(0 4px 0 rgba(0,0,0,.35));animation:fx-plumps .9s cubic-bezier(.3,1.4,.5,1) both}
.gross.bust .wort{color:#ff1744;background:none;-webkit-text-stroke:3px #fff;filter:drop-shadow(0 6px 0 rgba(0,0,0,.45)) drop-shadow(0 0 26px rgba(255,23,68,.7));animation:fx-stempel .45s cubic-bezier(.2,1.6,.4,1) both}
.gross.regenbogen .wort{background:linear-gradient(90deg,#ff1744,#ff9100,#ffea00,#00e676,#00b0ff,#d500f9,#ff1744);background-size:200% 100%;-webkit-background-clip:text;background-clip:text;animation:fx-slam .6s cubic-bezier(.2,1.5,.4,1) both,fx-farben 1.6s linear infinite}
@keyframes fx-farben{to{background-position:200% 0}}
@keyframes fx-slam{0%{transform:scale(3.4);opacity:0}55%{opacity:1}100%{transform:scale(1)}}
@keyframes fx-stempel{0%{transform:scale(2.6) rotate(-14deg);opacity:0}100%{transform:scale(1) rotate(-8deg);opacity:1}}
@keyframes fx-plumps{0%{transform:translateY(-120cqh)}100%{transform:none}}
.gross .glanz{position:absolute;inset:0;overflow:hidden}
.gross .glanz::after{content:'';position:absolute;top:-20%;bottom:-20%;width:18%;left:-30%;background:linear-gradient(90deg,transparent,rgba(255,255,255,.75),transparent);transform:skewX(-20deg);animation:fx-glanz .9s .55s ease-in-out both;mix-blend-mode:overlay}
@keyframes fx-glanz{to{left:120%}}
.gross .unter{position:relative;margin-top:10px;font-size:clamp(13px,5cqmin,26px);font-weight:800;color:#fff;letter-spacing:.16em;text-transform:uppercase;text-shadow:0 2px 8px rgba(0,0,0,.7);animation:fx-hoch .5s .35s both}
.gross .unter2{position:relative;margin-top:4px;font-size:clamp(12px,3.6cqmin,18px);font-weight:600;color:rgba(255,255,255,.85);animation:fx-hoch .5s .5s both}
@keyframes fx-hoch{from{transform:translateY(14px);opacity:0}}
.gross .welle{position:absolute;left:50%;top:50%;width:46cqmin;height:46cqmin;margin:-23cqmin 0 0 -23cqmin;border-radius:50%;border:6px solid rgba(255,214,79,.85);animation:fx-welle .9s .18s ease-out both}
.gross.silber .welle{border-color:rgba(200,225,255,.8)}.gross.gruen .welle{border-color:rgba(105,240,174,.85)}
@keyframes fx-welle{0%{transform:scale(.2);opacity:1}100%{transform:scale(2.6);opacity:0}}
.gross .strahl{position:absolute;top:-30%;width:34%;height:160%;background:linear-gradient(180deg,rgba(255,255,255,.32),rgba(255,255,255,0) 75%);transform-origin:50% 0;filter:blur(6px)}
.gross .strahl.l{left:-4%;animation:fx-schwenk-l 2.6s ease-in-out both}.gross .strahl.r{right:-4%;animation:fx-schwenk-r 2.6s ease-in-out both}
@keyframes fx-schwenk-l{0%{transform:rotate(-40deg);opacity:0}20%{opacity:1}50%{transform:rotate(-8deg)}100%{transform:rotate(-34deg);opacity:.6}}
@keyframes fx-schwenk-r{0%{transform:rotate(40deg);opacity:0}20%{opacity:1}50%{transform:rotate(8deg)}100%{transform:rotate(34deg);opacity:.6}}
.gross .riss{position:absolute;inset:0;width:100%;height:100%}
.gross .riss path{fill:none;stroke:rgba(255,255,255,.85);stroke-width:2.2;stroke-linecap:round;stroke-dasharray:400;stroke-dashoffset:400;animation:fx-riss .35s .3s ease-out forwards;filter:drop-shadow(0 0 3px rgba(255,80,80,.9))}
@keyframes fx-riss{to{stroke-dashoffset:0}}
.kf{position:absolute;left:50%;top:42%;width:9px;height:15px;border-radius:2px;background:var(--c);animation:fx-konfetti var(--t,2.4s) cubic-bezier(.15,.6,.35,1) var(--v,0s) both}
.kf.rund{width:10px;height:10px;border-radius:50%}
@keyframes fx-konfetti{0%{transform:translate(-50%,-50%) scale(.3);opacity:1}30%{transform:translate(var(--x),var(--y)) rotate(calc(var(--r) * .4)) rotateY(180deg);opacity:1}100%{transform:translate(calc(var(--x) * 1.25),calc(var(--y) + 75cqh)) rotate(var(--r)) rotateY(900deg);opacity:0}}
.fw{position:absolute;width:0;height:0}
.fw i{position:absolute;left:-3px;top:-3px;width:6px;height:6px;border-radius:50%;background:var(--c);box-shadow:0 0 8px 2px var(--c);animation:fx-feuer 1.25s var(--v) cubic-bezier(.1,.7,.3,1) both}
@keyframes fx-feuer{0%{transform:rotate(var(--a)) translateX(0);opacity:0}8%{opacity:1}70%{opacity:1}100%{transform:rotate(var(--a)) translateX(var(--w)) translateY(28px);opacity:0}}
.fw b{position:absolute;left:-2px;top:0;width:4px;height:40cqh;background:linear-gradient(180deg,#fff,transparent);border-radius:2px;animation:fx-rakete .45s calc(var(--v) - .45s) ease-out both}
@keyframes fx-rakete{0%{transform:translateY(60cqh) scaleY(.4);opacity:0}30%{opacity:1}100%{transform:translateY(0) scaleY(.1);opacity:0}}
.gross .pokal{font-size:clamp(50px,20cqmin,120px);line-height:1;filter:drop-shadow(0 0 30px rgba(255,200,0,.8));animation:fx-pokal 1s cubic-bezier(.2,1.4,.4,1) both}
@keyframes fx-pokal{0%{transform:translateY(60cqh) scale(.4)}100%{transform:none}}
.gross .schwimmt{position:absolute;bottom:14%;left:0;font-size:clamp(40px,16cqmin,90px);animation:fx-schwimm 2.8s .2s ease-in-out both}
@keyframes fx-schwimm{0%{transform:translateX(-30cqw) scaleX(-1)}50%{transform:translateX(45cqw) translateY(-12px) scaleX(-1)}100%{transform:translateX(120cqw) scaleX(-1)}}
.gross .roll{position:absolute;bottom:8%;left:0;width:64px;height:64px;animation:fx-roll 2.6s .3s linear both}
.gross .roll svg{width:100%;height:100%;animation:fx-dreh .7s linear infinite}
@keyframes fx-roll{0%{transform:translateX(-20cqw) translateY(0)}20%{transform:translateX(15cqw) translateY(-20px)}35%{transform:translateX(35cqw) translateY(0)}55%{transform:translateX(60cqw) translateY(-12px)}70%{transform:translateX(78cqw) translateY(0)}100%{transform:translateX(120cqw) translateY(0)}}
@keyframes fx-dreh{to{transform:rotate(360deg)}}
.gross .drei{position:relative;width:120px;height:70px;margin-bottom:6px}
.gross .drei svg{position:absolute;left:50%;top:50%;width:52px;height:52px;margin:-26px 0 0 -26px;transform-origin:5px 5px}
.gross .drei svg:nth-child(1){animation:fx-anflug-1 .5s .05s cubic-bezier(.3,0,.8,.4) both}
.gross .drei svg:nth-child(2){animation:fx-anflug-2 .5s .2s cubic-bezier(.3,0,.8,.4) both}
.gross .drei svg:nth-child(3){animation:fx-anflug-3 .5s .35s cubic-bezier(.3,0,.8,.4) both}
@keyframes fx-anflug-1{0%{transform:translate(-160px,140px) scale(2.5);opacity:0}100%{transform:translate(-12px,4px) rotate(-6deg)}}
@keyframes fx-anflug-2{0%{transform:translate(0,180px) scale(2.5);opacity:0}100%{transform:translate(0,0)}}
@keyframes fx-anflug-3{0%{transform:translate(160px,140px) scale(2.5);opacity:0}100%{transform:translate(12px,4px) rotate(6deg)}}
@media (prefers-reduced-motion:reduce){
 .fxd,.fxs,.kf,.fw,.gross .strahl,.gross .welle,.gross .roll,.gross .schwimmt,.gross .glanz,.gross .riss{display:none}
 .gross .wort,.gross .pokal,.fxc{animation:fx-ein .3s both}ha-card.fx-wackeln,ha-card.fx-stoss,.fx-treffer{animation:none}}`;
  const FX_FARBEN = ['#ff1744', '#ffea00', '#00e676', '#2979ff', '#ff9100', '#d500f9', '#ffffff', '#00e5ff'];
  // a steel-tip dart, tip at (5,5), seen from the thrower: barrel, shaft and flight point back to the viewer
  const dartSvg = farbe => '<svg viewBox="0 0 58 58"><defs><linearGradient id="fxbar" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e0e0e0"/><stop offset=".5" stop-color="#5f6670"/><stop offset="1" stop-color="#2b3036"/></linearGradient></defs>' +
    '<path d="M5 5 L15 14" stroke="#cfd8dc" stroke-width="1.6" stroke-linecap="round"/>' +
    '<path d="M14 13 L29 28" stroke="url(#fxbar)" stroke-width="5" stroke-linecap="round"/>' +
    '<path d="M17 16 l2 2 M20 19 l2 2 M23 22 l2 2 M26 25 l2 2" stroke="#1c1f22" stroke-width="1.2"/>' +
    '<path d="M29 28 L40 39" stroke="#263238" stroke-width="2.6" stroke-linecap="round"/>' +
    '<path d="M38 37 L56 41 L50 46 Z M38 37 L41 55 L46 49 Z" fill="' + farbe + '" stroke="rgba(0,0,0,.45)" stroke-width=".8"/>' +
    '<path d="M38 37 L52 52" stroke="rgba(255,255,255,.55)" stroke-width="1"/></svg>';
  const zufall = (a, b) => a + Math.random() * (b - a);
  const konfetti = (n, verz) => Array.from({ length: n }, () => {
    const w = zufall(0, Math.PI * 2), r = zufall(18, 46);
    return '<i class="kf' + (Math.random() < .3 ? ' rund' : '') + '" style="--c:' + FX_FARBEN[Math.floor(Math.random() * FX_FARBEN.length)] + ';--x:' + (Math.cos(w) * r).toFixed(1) + 'cqw;--y:' + (Math.sin(w) * r * .8 - 18).toFixed(1) + 'cqh;--r:' +
      Math.round(zufall(-720, 720)) + 'deg;--t:' + zufall(2, 3.2).toFixed(2) + 's;--v:' + ((verz || 0) + zufall(0, .25)).toFixed(2) + 's"></i>';
  }).join('');
  const feuerwerk = (n, start) => Array.from({ length: n }, (_, k) => {
    const c = FX_FARBEN[k % 6], v = (start + k * .55).toFixed(2), x = zufall(18, 82).toFixed(0), y = zufall(15, 45).toFixed(0);
    return '<span class="fw" style="left:' + x + '%;top:' + y + '%;--c:' + c + ';--v:' + v + 's"><b></b>' +
      Array.from({ length: 22 }, (_, j) => '<i style="--a:' + (j * 360 / 22) + 'deg;--w:' + zufall(60, 105).toFixed(0) + 'px"></i>').join('') + '</span>';
  }).join('');
  const ROLL_SVG = '<svg viewBox="0 0 64 64"><g fill="none" stroke="#a1887f" stroke-width="2" stroke-linecap="round"><circle cx="32" cy="32" r="26"/><path d="M10 26 C24 10 44 50 56 30 M12 42 C26 20 40 56 54 18 M22 8 C28 30 38 34 46 58 M8 34 C30 34 34 12 52 46"/></g></svg>';
  const RISS_SVG = '<svg class="riss" viewBox="0 0 100 100" preserveAspectRatio="none"><path d="M50 48 L38 40 L30 44 L18 30 M50 48 L62 36 L70 40 L84 24 M50 48 L46 62 L36 70 L30 88 M50 48 L60 60 L74 64 L86 80 M50 48 L52 30 L48 18 L54 6"/></svg>';
  // synthesized sounds (no audio files): thud of a dart, crowd cheer, buzzer
  let fxAudio = null;
  /* caller on this phone/tablet (1.18): while a game card has its speaker button on, Home Assistant sends the
     same announcements as to the speakers (voice, sound packs, walk-on songs) as addresses; played one after another */
  const hoerKarten = new Set();
  let hoerAbo = null, hoerOk = false, hoerKette = Promise.resolve(), hoerQuelle = null, hoerNr = 0;
  const hoerStop = () => { hoerNr++; if (hoerQuelle) try { hoerQuelle.stop(); } catch (e) {} hoerQuelle = null; };
  const hoerSpielen = (h, m) => {
    if (m.stop) { hoerStop(); return; }
    if (!m.url) return;
    const nr = hoerNr, laden = fetch(h.hassUrl(m.url)).then(r => r.arrayBuffer());
    hoerKette = hoerKette.then(() => laden).then(buf => {
      if (nr !== hoerNr) return;
      if (!fxAudio) { const C = window.AudioContext || window.webkitAudioContext; if (!C) return; fxAudio = new C(); }
      return fxAudio.decodeAudioData(buf).then(b => new Promise(fertig => {
        if (nr !== hoerNr) { fertig(); return; }
        if (fxAudio.state === 'suspended') fxAudio.resume();
        const q = fxAudio.createBufferSource(); q.buffer = b; q.connect(fxAudio.destination);
        q.onended = () => { if (hoerQuelle === q) hoerQuelle = null; fertig(); };
        hoerQuelle = q; q.start();
      }));
    }).catch(() => {});
  };
  const hoerPruefen = h => {
    if (hoerKarten.size && !hoerAbo && h && h.connection) {
      hoerAbo = h.connection.subscribeMessage(m => hoerSpielen(h, m), { type: 'autodarts/ansager/hoeren' })
        .then(ab => { hoerOk = true; return ab; }, () => null);  // older integration: the phone voice speaks instead
    } else if (!hoerKarten.size && hoerAbo) { const p = hoerAbo; hoerAbo = null; hoerOk = false; p.then(ab => ab && ab()); hoerStop(); }
  };
  const fxKlang = art => {
    try {
      if (!fxAudio) { const C = window.AudioContext || window.webkitAudioContext; if (!C) return; fxAudio = new C(); }
      const ac = fxAudio; if (ac.state === 'suspended') ac.resume();
      const jetzt = ac.currentTime, aus = ac.createGain(); aus.connect(ac.destination);
      const rauschen = sek => { const b = ac.createBuffer(1, Math.ceil(ac.sampleRate * sek), ac.sampleRate), d = b.getChannelData(0); for (let i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1; const q = ac.createBufferSource(); q.buffer = b; return q; };
      if (art === 'tock') {
        const q = rauschen(.12), f = ac.createBiquadFilter(); f.type = 'lowpass'; f.frequency.value = 1400; q.connect(f); f.connect(aus);
        aus.gain.setValueAtTime(.55, jetzt); aus.gain.exponentialRampToValueAtTime(.001, jetzt + .09);
        const o = ac.createOscillator(), g = ac.createGain(); o.frequency.setValueAtTime(190, jetzt); o.frequency.exponentialRampToValueAtTime(70, jetzt + .12); o.connect(g); g.connect(ac.destination);
        g.gain.setValueAtTime(.35, jetzt); g.gain.exponentialRampToValueAtTime(.001, jetzt + .14); o.start(jetzt); o.stop(jetzt + .15); q.start(jetzt);
      } else if (art === 'jubel' || art === 'gross') {
        const lang = art === 'gross' ? 3.4 : 2.2, q = rauschen(lang), f = ac.createBiquadFilter(); f.type = 'bandpass'; f.frequency.value = 1300; f.Q.value = .6;
        const lfo = ac.createOscillator(), lg = ac.createGain(); lfo.frequency.value = 7; lg.gain.value = .12; lfo.connect(lg); lg.connect(aus.gain);
        q.connect(f); f.connect(aus); aus.gain.setValueAtTime(.001, jetzt); aus.gain.exponentialRampToValueAtTime(.32, jetzt + .35); aus.gain.exponentialRampToValueAtTime(.001, jetzt + lang);
        q.start(jetzt); lfo.start(jetzt); lfo.stop(jetzt + lang);
      } else if (art === 'buzz') {
        const o = ac.createOscillator(); o.type = 'sawtooth'; o.frequency.value = 98; const f = ac.createBiquadFilter(); f.type = 'lowpass'; f.frequency.value = 900; o.connect(f); f.connect(aus);
        aus.gain.setValueAtTime(.22, jetzt); aus.gain.setValueAtTime(.22, jetzt + .45); aus.gain.exponentialRampToValueAtTime(.001, jetzt + .6); o.start(jetzt); o.stop(jetzt + .62);
      } else if (art === 'pfiff') {
        const o = ac.createOscillator(); o.type = 'sine'; o.frequency.setValueAtTime(900, jetzt); o.frequency.exponentialRampToValueAtTime(260, jetzt + .5); o.connect(aus);
        aus.gain.setValueAtTime(.12, jetzt); aus.gain.exponentialRampToValueAtTime(.001, jetzt + .55); o.start(jetzt); o.stop(jetzt + .56);
      }
    } catch (e) {}
  };

  const werferZeile = p => p.werfer ? '<div class="wf">▸ ' + esc(p.werfer) + '</div>' : '';
  const TUR_GRENZEN = { ko: [3, 32], doppel_ko: [3, 16], gruppen: [6, 32], liga: [3, 10] };
  const TUR_ARTEN = [['ko', 'mdi:tournament', 'tour_ko', 's_tko', 'tour_hint'], ['doppel_ko', 'mdi:sitemap-outline', 'tour_dko', 's_tdko', 'dko_hint'],
    ['gruppen', 'mdi:table-large', 'tour_gr', 's_tgr', 'gr_hint'], ['liga', 'mdi:format-list-numbered', 'tour_liga', 's_tliga', 'liga_hint']];
  class AutodartsGameCard extends DartsSeite {
    static get CSS() { return SPIEL_CSS + FX_CSS; }
    get _spiel() { return E(this._h, 'sensor.game'); }
    get _spieler() { return E(this._h, 'sensor.players'); }
    _lobbyStart() {
      const l = att(this._h, this._spieler).letzte || {}, roh = l.spieler || [], teams = roh.some(x => String(x).startsWith('team:'));
      this._lob = {
        spieler: (teams ? roh.flatMap(x => String(x).startsWith('team:') ? String(x).slice(5).split('+') : [x]) : roh).slice(0, 64), teams,
        bull_5050: !!l.bull_5050, max_runden: l.max_runden || 0, handicap: { ...(l.handicap || {}) }, hc: !!Object.keys(l.handicap || {}).length, startwert: l.startwert || 501, legs: l.legs || 1, sets: l.sets || 0,
        einwurf: l.einwurf || 'straight', auswurf: l.auswurf || 'double', bull_off: !!l.bull_off,
        spiel: l.spiel || 'x01', variante: l.variante || '', zahlen: l.zahlen || 'classic', runden: l.runden || 0, leben: l.leben || 3, zielwert: l.zielwert || 0
      };
    }
    _sichtbar() { this._wach(); this._lvStrom(); this._abo(); }
    _abo() { if (this._ansage() && this.isConnected) hoerKarten.add(this); else hoerKarten.delete(this); hoerPruefen(this._h); }
    // view: camera 1–3 (index) or graphic; stored per device
    _ansichtNr() { let v = '1'; try { v = localStorage.getItem('autodarts_view') || v; } catch (e) {} return v; }
    _ansicht() { const n = this._ansichtNr(); return n === 'g' ? 'grafik' : E(this._h, KAMERA_KEYS[(+n || 2) - 1]); }
    _netzAn() { try { return localStorage.getItem('autodarts_grid') === '1'; } catch (e) { return false; } }
    _lvSoll() {
      const id = this._ansicht(), h = this._h;
      return id && id !== 'grafik' && phase(att(h, this._spiel)) === 'running' && boardOnline(h) && an(h, E(h, 'binary_sensor.detection_running')) && !!entzerrung(att(h, id).kalibrierung);
    }
    // switches by itself: board offline = keypad, board online = camera; a manual choice holds until the board state changes
    _tippAn() { const on = boardOnline(this._h); if (this._onAlt !== on) { this._onAlt = on; this._tapHand = null; } return this._tapHand != null ? this._tapHand : !on; }
    _toast(message) { this.dispatchEvent(new CustomEvent('hass-notification', { detail: { message }, bubbles: true, composed: true })); }
    // keypad instead of the drawn board (default while the board is offline): keys like a dart machine, or the total of a visit (X01)
    _tmod(x01) { let v = 'k'; try { v = localStorage.getItem('autodarts_tapmode') || v; } catch (e) {} return v === 's' && !x01 ? 'k' : v; }
    _kseg(m, x01) {
      const w = [['k', 'mdi:dialpad', t('kp_keys')]].concat(x01 ? [['s', 'mdi:numeric', t('kp_sum')]] : [], [['b', 'mdi:bullseye', t('kp_board')]], boardOnline(this._h) ? [['c', 'mdi:cctv', t('kp_cam')]] : []);
      return '<div class="kseg">' + w.map(([v, ic, x]) => '<button class="feld' + (v === m ? ' an' : '') + '" data-act="kmod" data-v="' + v + '"><ha-icon icon="' + ic + '"></ha-icon>' + x + '</button>').join('') + '</div>';
    }
    _tastenfeld(m, n) {
      const voll = n >= 3 ? ' disabled' : '';
      if (m === 's') {
        const z = this._summe || '';
        return '<div class="kp"><div class="ksum feld"><b>' + (z || '0') + '</b><small>' + t('kp_sum_hint') + '</small></div><div class="kgrid k3">' +
          ['1', '2', '3', '4', '5', '6', '7', '8', '9'].map(d => '<button class="k feld" data-act="kzif" data-v="' + d + '">' + d + '</button>').join('') +
          '<button class="k feld" data-act="kzif" data-v="&lt;"><ha-icon icon="mdi:backspace-outline"></ha-icon></button><button class="k feld" data-act="kzif" data-v="0">0</button>' +
          '<button class="k ok" data-act="ksum"' + (z === '' ? ' disabled' : '') + '>OK</button></div></div>';
      }
      const mo = this._mod || '';
      return '<div class="kp"><div class="kgrid k2"><button class="k feld' + (mo === 'D' ? ' an' : '') + '" data-act="kmodi" data-v="D">Double</button><button class="k feld' + (mo === 'T' ? ' an' : '') + '" data-act="kmodi" data-v="T">Triple</button></div>' +
        '<div class="kgrid">' + Array.from({ length: 20 }, (_, i) => '<button class="k feld" data-act="kz" data-v="' + (i + 1) + '"' + voll + '>' + (mo ? '<i>' + mo + '</i>' : '') + (i + 1) + '</button>').join('') + '</div>' +
        '<div class="kgrid k3"><button class="k feld" data-act="kz" data-v="25"' + voll + '>25</button><button class="k feld" data-act="kz" data-v="50"' + voll + '>Bull</button><button class="k feld miss" data-act="kz" data-v="0"' + voll + '>' + t('kp_miss') + '</button></div></div>';
    }
    _brettHtml(darts, ziel, x01) {
      const id = this._ansicht(), nr = this._ansichtNr();
      const tk = '<button class="tipp' + (this._tippAn() ? ' an' : '') + '" data-act="tipp" title="' + t('tap_on') + '"><ha-icon icon="mdi:gesture-tap"></ha-icon>' + t('tap_mode') + '</button>' +
        (this._tb ? '<span class="tasten">' + esc(this._tb) + '</span>' : '');
      if (this._tippAn()) {
        const m = this._tmod(x01);
        return this._kseg(m, x01) + (m === 'b' ? '<div class="brett tippen" data-act="tippen" data-n="' + (darts || []).length + '">' + brett(darts, ziel) + (this._tb ? '<span class="tasten">' + esc(this._tb) + '</span>' : '') + '</div>' : this._tastenfeld(m, (darts || []).length));
      }
      if (!this._lvSoll()) return '<div class="brett grafik" data-act="ansicht" title="' + t('tap_view') + '">' + brett(darts, ziel) + tk + (id !== 'grafik' ? '<div class="bk"><span>' + (boardOnline(this._h) ? t('cams_off') : t('sc_off')) + ' – ' + t('graphic') + '</span></div>' : '') + '</div>';
      const netz = this._netzAn();
      const pf = (darts || []).map((d, i) => { const [x, y] = dartMM(d, i); return '<g transform="translate(' + x.toFixed(1) + ' ' + y.toFixed(1) + ')"><circle r="15" fill="' + ['#ff5252', '#40c4ff', '#ffd740'][i] + '"/><text y="6.5">' + (i + 1) + '</text></g>'; }).join('');
      return '<div class="brett live" data-act="ansicht" title="' + t('tap_view') + '"><div class="lvh"></div>' +
        (netz ? '<svg class="netz" viewBox="-225 -225 450 450"><path d="' + NETZ_MM + '"/></svg>' : '') +
        '<svg class="pf" viewBox="-225 -225 450 450">' + pf + '</svg>' + tk + '<div class="bk"><span>' + t('cam', { n: nr }) + '</span><button class="' + (netz ? 'an' : '') + '" data-act="netz">' + t('grid') + '</button></div></div>';
    }
    _lvStrom() {
      const soll = this._sicht && !document.hidden && this.isConnected && this._lvSoll();
      const halter = soll && this._in && this._in.querySelector('.lvh');
      if (!soll || !halter) {
        if (this._lv) { const img = this._lv.firstChild; if (img.getAttribute('src')) img.removeAttribute('src'); this._lvId = null; }
        return;
      }
      if (!this._lv) {
        this._lv = document.createElement('div'); this._lv.className = 'lv'; this._lv.innerHTML = '<img alt="">';
        this._lv.firstChild.addEventListener('load', () => this._lvForm());
        if ('ResizeObserver' in window) new ResizeObserver(() => this._lvForm()).observe(this._lv);
      }
      if (this._lv.parentNode !== halter) halter.appendChild(this._lv);
      const id = this._ansicht(), img = this._lv.firstChild;
      if (this._lvId !== id || !img.getAttribute('src')) {
        const bild = att(this._h, id).entity_picture || '';
        if (bild) { this._lvId = id; img.src = bild.replace('/api/camera_proxy/', '/api/camera_proxy_stream/'); }
      }
      this._lvForm();
    }
    _lvForm() {
      // map the camera image onto the straight board with matrix3d (only on size or camera change)
      const lv = this._lv, img = lv && lv.firstChild; if (!img || !img.naturalWidth || !this._lvId) return;
      const S = lv.clientWidth, H = entzerrung(att(this._h, this._lvId).kalibrierung); if (!S || !H) return;
      const key = S + '|' + this._lvId + '|' + img.naturalWidth + '|' + JSON.stringify(H); if (this._lvKey === key) return; this._lvKey = key;
      const k = S / 450, M = mul3([[k, 0, S / 2], [0, k, S / 2], [0, 0, 1]], H);
      img.style.width = img.naturalWidth + 'px'; img.style.height = img.naturalHeight + 'px';
      img.style.transform = 'matrix3d(' + [M[0][0], M[1][0], 0, M[2][0], M[0][1], M[1][1], 0, M[2][1], 0, 0, 1, 0, M[0][2], M[1][2], 0, M[2][2]].map(v => +v.toPrecision(9)).join(',') + ')';
    }
    // optional: hide elements of the dashboard (e.g. a fixed bottom bar) while the game card is shown
    connectedCallback() {
      this._ausblenden(true);
      if (!this._tasteFn) this._tasteFn = ev => this._taste(ev);
      window.addEventListener('keydown', this._tasteFn);
      if (this._h) this._abo();
    }
    disconnectedCallback() { this._ausblenden(false); this._lvStrom(); window.removeEventListener('keydown', this._tasteFn); this._abo(); }
    // keyboard input while a game runs: T20, D16, S5, 25, 50/BULL, 0/M + Enter; Enter alone = next, Backspace = undo / delete, Esc = clear
    _taste(ev) {
      if (!this._h || ev.ctrlKey || ev.metaKey || ev.altKey) return;
      const a = att(this._h, this._spiel);
      if (phase(a) !== 'running' || !this._sicht || document.hidden) return;
      if (ev.composedPath().some(x => x.tagName === 'INPUT' || x.tagName === 'TEXTAREA' || x.isContentEditable)) return;
      const m = this._r && this._r.querySelector('.modal'); if (m && !m.hidden) return;
      const k = ev.key, alt = this._tb || '';
      let tb = alt;
      if (/^[0-9]$/.test(k) && alt.replace(/\D/g, '').length < 2) tb = alt + k;
      else if (/^[tdsbm]$/i.test(k) && !alt) tb = k.toUpperCase();
      else if (k === 'Backspace') { if (alt) tb = alt.slice(0, -1); else { this._dienst('rueckgaengig'); ev.preventDefault(); return; } }
      else if (k === 'Escape') tb = '';
      else if (k === 'Enter') {
        ev.preventDefault();
        if (!alt) { this._dienst('weiter'); return; }
        const f = this._tastenFeld(alt), n = ((a.aufnahme || {}).darts || []).length;
        this._tb = ''; this._alt = null; this._zeichnen();
        if (!f) { this._toast(t('tap_on')); return; }
        if (n >= 3) { this._toast(t('tap_full')); return; }
        this._dienst('wurf_aendern', { dart: n, feld: f }); return;
      } else return;
      ev.preventDefault();
      this._tb = tb; this._alt = null; this._zeichnen();
    }
    _tastenFeld(x) {
      if (x === 'M' || x === '0') return 'M';
      if (x === 'B' || x === '50' || x === 'D25') return 'D25';
      if (x === '25' || x === 'S25') return 'S25';
      const m = /^([TDS]?)(\d{1,2})$/.exec(x); if (!m) return null;
      const n = +m[2]; if (n < 1 || n > 20) return null;
      return (m[1] || 'S') + n;
    }
    _ausblenden(weg) {
      if (!weg) { (this._weg || []).forEach(b => { b.style.visibility = ''; b.style.pointerEvents = ''; }); this._weg = null; return; }
      const sel = (this._c && this._c.hide_elements) || []; if (!sel.length) return;
      this._wegZeit = Date.now();
      let n = this, r = null;
      for (let i = 0; i < 40 && n; i++) { const x = n.getRootNode(); if (!x.host) break; if (x.host.tagName === 'HUI-ROOT') { r = x; break; } n = x.host; }
      if (!r) return;
      const liste = []; sel.forEach(s => { try { r.querySelectorAll(s).forEach(b => liste.push(b)); } catch (e) {} });
      liste.forEach(b => { b.style.visibility = 'hidden'; b.style.pointerEvents = 'none'; });
      if (liste.length) this._weg = liste;
    }
    _wach() {
      // keep the screen on during a game (only while visible)
      const soll = this._sicht && !document.hidden && ['running', 'bulloff'].includes(phase(att(this._h, this._spiel)));
      if (soll && !this._lock && navigator.wakeLock) navigator.wakeLock.request('screen').then(l => { this._lock = l; l.addEventListener('release', () => { this._lock = null; }); }).catch(() => {});
      if (!soll && this._lock) { this._lock.release(); this._lock = null; }
    }
    _ansage() { try { return localStorage.getItem('autodarts_caller') === '1'; } catch (e) { return false; } }
    _sagen(text) {
      try { speechSynthesis.cancel(); const u = new SpeechSynthesisUtterance(text); u.lang = SPR === 'de' ? 'de-DE' : 'en-GB'; u.rate = 1.05; speechSynthesis.speak(u); } catch (e) {}
    }
    _sprechen(a) {
      if (!this._ansage() || !window.speechSynthesis || !this._sicht || document.hidden) return;
      const p = a.spieler || [], wer = p[a.am_zug] || {};
      let x = '';
      const neu = a.ansage_id !== this._ansId, zug = a.am_zug + '/' + a.aufnahmen;
      if (neu && a.ansage) {
        const s = String(a.ansage);
        if (s === '180') x = t('say_180');
        else if (s === 'Bust') x = t('say_bust');
        else if (s.startsWith('Spiel ')) x = t('say_game', { n: s.slice(6) });
        else if (s.startsWith('Satz ')) x = t('say_set', { n: s.slice(5) });
        else if (s.startsWith('Leg ')) x = t('say_leg', { n: s.slice(4) });
        else if (s === '0') x = t('say_0');
        else x = s;
      }
      if (this._zugAlt !== undefined && zug !== this._zugAlt && a.gewinner == null && a.leg_gewinner == null && !((a.aufnahme || {}).darts || []).length && wer.rest <= 170 && wer.weg && !wer.bot)
        x += (x ? '. ' : '') + t('say_need', { n: wer.name, r: wer.rest });
      this._ansId = a.ansage_id; this._zugAlt = zug;
      if (x && !hoerOk) this._sagen(x);
    }
    // ---------- effects ----------
    _fxAn() {
      if (this._c.effects === false) return false;
      try { return localStorage.getItem('autodarts_fx') !== '0'; } catch (e) { return true; }
    }
    _fxEbene() {
      const karte = this._r.querySelector('ha-card');
      let e = karte.querySelector(':scope > .fx');
      if (!e) { e = document.createElement('div'); e.className = 'fx'; karte.appendChild(e); }
      return e;
    }
    _fxWeg(el, ms) { setTimeout(() => el.remove(), ms); }
    _fxKarte(klasse) {
      const k = this._r.querySelector('ha-card'); k.classList.remove(klasse); void k.offsetWidth; k.classList.add(klasse);
      clearTimeout(this['_fxk' + klasse]); this['_fxk' + klasse] = setTimeout(() => k.classList.remove(klasse), 700);
    }
    // where a dart sits on the drawn board, as a point inside the effect layer
    _fxPunkt(d, i) {
      const b = this._in.querySelector('.brett.live') || this._in.querySelector('.brett.grafik svg');
      if (!b) return null;
      const r = b.getBoundingClientRect(), k = this._r.querySelector('ha-card').getBoundingClientRect();
      let fx, fy;
      if (b.classList.contains('live')) { const [x, y] = dartMM(d, i); fx = (x + 225) / 450; fy = (y + 225) / 450; }
      else { const [x, y] = brettPos(d, i); fx = x / 120; fy = y / 120; }
      return [r.left - k.left + fx * r.width, r.top - k.top + fy * r.height, b];
    }
    _fxDart(d, i, bot) {
      const p = this._fxPunkt(d, i), f = d.f || 'M', farbe = ['#ff5252', '#40c4ff', '#ffd740'][i] || '#fff';
      if (this._ansage()) setTimeout(() => fxKlang(f === 'M' ? 'pfiff' : 'tock'), 230);
      if (!p) return;
      const [x, y, brettEl] = p, art = f === 'M' ? 'miss' : f === 'D25' ? 'bullseye' : f === 'S25' ? 'bull' : f[0];
      const k = { T: '#ff9100', D: '#2979ff', bullseye: '#ff1744', bull: '#00e676', S: '#ffffff', miss: '#9e9e9e' }[art];
      let s = '<div class="fxd' + (art === 'miss' ? ' miss' : '') + '">' + dartSvg(farbe) + '</div><div class="fxr" style="--k:' + k + '"></div>';
      if (art === 'T' || art === 'D') s += Array.from({ length: art === 'T' ? 12 : 8 }, (_, j) => '<i class="fxs" style="--k:' + k + ';--a:' + (j * 360 / (art === 'T' ? 12 : 8) + zufall(-10, 10)).toFixed(0) + 'deg;--w:' + zufall(22, 44).toFixed(0) + 'px"></i>').join('');
      if (art === 'bullseye' || art === 'bull') s += '<div class="fxb" style="--k:' + k + '"></div>';
      const chip = { T: 'TRIPLE ' + f.slice(1), D: 'DOUBLE ' + f.slice(1), bullseye: 'BULLSEYE', bull: 'BULL 25', miss: 'MISS' }[art];
      if (chip) s += '<span class="fxc" style="--k:' + (art === 'S' ? '#455a64' : k) + '">' + (bot ? '🤖 ' : '') + chip + '</span>';
      const el = document.createElement('div'); el.className = 'fxp'; el.style.transform = 'translate(' + x.toFixed(1) + 'px,' + y.toFixed(1) + 'px)'; el.innerHTML = s;
      this._fxEbene().appendChild(el); this._fxWeg(el, 1900);
      if (brettEl && art !== 'miss') setTimeout(() => { brettEl.classList.remove('fx-treffer'); void brettEl.offsetWidth; brettEl.classList.add('fx-treffer'); }, 230);
    }
    _fxChampion(name) {
      if (!this.isConnected) return;
      this._fxGross('regenbogen', '<div class="strahl l"></div><div class="strahl r"></div>' + feuerwerk(8, .2) + konfetti(80) + '<div class="pokal">🏆</div><div class="wort lang">' + t('fx_champion') + '<span class="glanz"></span></div><div class="unter">' + esc(name) + '</div><div class="unter2">' + esc(t('champion')) + '</div>', 6500, 'fx-stoss', 'gross');
    }
    _fxGross(klasse, inhalt, dauer, karte, klang) {
      const ebene = this._fxEbene();
      ebene.querySelectorAll('.gross').forEach(g => g.remove());
      const el = document.createElement('div'); el.className = 'gross ' + klasse; el.style.setProperty('--ende', ((dauer - 500) / 1000) + 's');
      el.innerHTML = '<div class="bg"></div>' + inhalt; ebene.appendChild(el); this._fxWeg(el, dauer);
      if (karte) this._fxKarte(karte);
      if (klang && this._ansage()) fxKlang(klang);
    }
    _fxAufnahme(z, a) {
      if (a.art && a.art !== 'x01' && (a.art !== 'highscore' || z.c)) return this._fxArt(z, a);
      const sp = a.spieler || [], wer = (sp[z.s] || {}).name || '', p = z.p, d = z.d || [];
      const wort = (x, lang) => '<div class="wort' + (lang ? ' lang' : '') + '">' + esc(x) + '<span class="glanz"></span></div>';
      const unter = (x, y) => '<div class="unter">' + esc(x) + '</div>' + (y ? '<div class="unter2">' + esc(y) + '</div>' : '');
      const strahlen = '<div class="strahl l"></div><div class="strahl r"></div>';
      if (z.c) {
        const ansage = String(a.ansage || ''), match = ansage.startsWith('Spiel '), satz = ansage.startsWith('Satz ');
        const neun = (sp[z.s] || {}).leg_darts === 9;
        if (neun) return this._fxGross('regenbogen', strahlen + feuerwerk(6, .3) + konfetti(70) + wort(t('fx_nine'), true) + unter(wer, t('fx_perfect')), 6000, 'fx-stoss', 'gross');
        if (match) return this._fxGross('gold', feuerwerk(5, .4) + konfetti(50, .2) + '<div class="pokal">🏆</div>' + wort('GAME SHOT', true) + unter(t('fx_match', { n: wer }), p + ' Checkout'), 5200, 'fx-stoss', 'gross');
        if (p === 170) return this._fxGross('gold', strahlen + '<div class="schwimmt">🐟</div>' + konfetti(40) + wort('170') + unter('THE BIG FISH', wer), 4000, 'fx-stoss', 'gross');
        if (p >= 100) return this._fxGross('gold', strahlen + '<div class="welle"></div>' + konfetti(36) + wort(String(p)) + unter('HIGH FINISH', (satz ? t('fx_set', { n: wer }) : t('fx_leg', { n: wer }))), 3800, 'fx-stoss', 'jubel');
        return this._fxGross('gruen', '<div class="welle"></div>' + konfetti(satz ? 40 : 26) + wort('GAME SHOT', true) + unter(satz ? t('fx_set', { n: wer }) : t('fx_leg', { n: wer }), p + ' Checkout'), 3200, 'fx-stoss', 'jubel');
      }
      if (z.b) return this._fxGross('bust', RISS_SVG + wort(t('fx_bust'), t('fx_bust').length > 5) + unter(wer), 2200, 'fx-wackeln', 'buzz');
      if (p === 180) return this._fxGross('gold', strahlen + '<div class="welle"></div>' + konfetti(60, .15) + wort('180') + unter('ONE HUNDRED AND EIGHTY', wer), 4200, 'fx-stoss', 'gross');
      if (d.length === 3 && d[0] === d[1] && d[1] === d[2] && d[0] !== 'M') {
        const drei = '<div class="drei">' + [0, 1, 2].map(i => dartSvg(['#ff5252', '#40c4ff', '#ffd740'][i])).join('') + '</div>';
        return this._fxGross(p >= 100 ? 'gold' : 'silber', drei + wort(String(p)) + unter('THREE IN A BED', wer + ' · ' + d.map(ft).join(' · ')), 3000, 'fx-stoss', 'jubel');
      }
      if (p >= 140) return this._fxGross('silber', '<div class="welle"></div>' + konfetti(18) + wort(String(p)) + unter('TON-FORTY', wer), 2800, 'fx-stoss', 'jubel');
      if (p >= 100) return this._fxGross('silber', wort(String(p)) + unter('TON', wer), 2300);
      if (p === 26 && ['S20', 'S5', 'S1'].every(f => d.includes(f))) return this._fxGross('grau', '<div class="pokal">☕</div>' + wort('26') + unter('BED & BREAKFAST', wer), 2600);
      if (p === 0 && d.length) return this._fxGross('grau', '<div class="roll">' + ROLL_SVG + '</div>' + wort('NO SCORE', true) + unter(wer), 2800);
      return null;
    }
    // compare with the last state: only new darts and newly finished visits trigger effects
    _fxPruefen(a, ph) {
      if (!['running', 'finished'].includes(ph)) { this._fxAlt = null; return; }
      const vl = a.verlauf || [], au = a.aufnahme || { darts: [] }, darts = au.darts || [];
      const offen = [darts.length && vl.length ? vl[vl.length - 1].i : (a.aufnahmen || 0), darts.length];
      const visit = a.ansage_id === '' || a.ansage_id == null ? -1 : +a.ansage_id;
      const alt = this._fxAlt; this._fxAlt = { id: a.id, offen, visit };
      if (!alt || alt.id !== a.id || !this._fxAn() || !this._sicht || document.hidden) return;
      const neu = offen[0] === alt.offen[0] ? darts.slice(alt.offen[1]) : (offen[0] > alt.offen[0] ? darts : []);
      const start = darts.length - neu.length, bot = !!((a.spieler || [])[a.am_zug] || {}).bot;
      neu.forEach((d, k) => setTimeout(() => this._fxDart(d, start + k, bot), k * 170));
      if (visit > alt.visit) {
        const z = vl.find(v => v.i === visit);
        if (z) setTimeout(() => this._fxAufnahme(z, a), neu.length ? 420 + (neu.length - 1) * 170 : 0);
      }
    }
    _zeichnen() {
      if (this._fehlt()) return;
      const h = this._h, a = att(h, this._spiel), ph = phase(a);
      if (!this._weg && this.isConnected && Date.now() - (this._wegZeit || 0) > 3000) this._ausblenden(true);
      const ansage = this._ansage(), vb = !!document.fullscreenElement;
      this._kopf(ph === 'idle' ? t('new_game') : (ph === 'finished' ? t('game_over') : t('darts')), modusText(a.einstellungen) || t('local'),
        (ph === 'running' || ph === 'bulloff' ? '<button class="ik" data-act="xabbr" title="' + t('cancel_game') + '"><ha-icon icon="mdi:close"></ha-icon></button>' : '') +
        (this._c.effects === false ? '' : '<button class="ik' + (this._fxAn() ? ' an' : '') + '" data-act="fx" title="' + t('effects') + '"><ha-icon icon="' + (this._fxAn() ? 'mdi:creation' : 'mdi:creation-outline') + '"></ha-icon></button>') +
        '<button class="ik' + (ansage ? ' an' : '') + '" data-act="ansage" title="' + t('caller') + '"><ha-icon icon="' + (ansage ? 'mdi:volume-high' : 'mdi:volume-off') + '"></ha-icon></button>' +
        ((tvInfo(h).geraete || []).length ? '<button class="ik" data-act="tv" title="' + t('tv_show') + '"><ha-icon icon="mdi:television-play"></ha-icon></button>' +
          '<button class="ik' + (tvInfo(h).brett ? ' an' : '') + '" data-act="tvbrett" title="' + t('tv_board_on') + '"><ha-icon icon="mdi:bullseye-arrow"></ha-icon></button>' : '') +
        (clipsInfo(h).an && ph === 'running' ? '<button class="ik" data-act="clip" title="' + t('clips_save') + '"><ha-icon icon="mdi:movie-open-plus-outline"></ha-icon></button>' : '') +
        '<button class="ik" data-act="vollbild" title="' + t('fullscreen') + '"><ha-icon icon="' + (vb ? 'mdi:fullscreen-exit' : 'mdi:fullscreen') + '"></ha-icon></button>');
      if (ph !== this._phAlt) {
        if (ph === 'idle') this._lobbyStart();
        if (ph === 'finished' && this._phAlt === 'running' && a.turnier && a.turnier.sieger && this._fxAn()) setTimeout(() => this._fxChampion(a.turnier.sieger), 5400);
        this._phAlt = ph; this._wach();
      }
      if (!this._lob) this._lobbyStart();
      if (ph === 'running' || ph === 'finished') this._sprechen(a);
      let html;
      if (ph === 'bulloff') html = this._turBanner(a) + this._bulloff(a);
      else if (ph === 'running') html = this._turBanner(a) + this._match(a);
      else if (ph === 'finished') html = a.turnier ? this._turEnde(a) : this._ende(a);
      else html = this._lobby();
      this._setze(html);
      this._lvStrom();
      this._fxPruefen(a, ph);
    }
    // tournament: round name, banner, bracket
    _rundeName(r, gesamt) {
      const rest = gesamt - r;
      return rest === 1 ? t('t_final') : rest === 2 ? t('t_semi') : rest === 3 ? t('t_quarter') : rest === 4 ? t('t_last16') : rest === 5 ? t('t_last32') : t('t_round', { n: r + 1 });
    }
    _max() { const m = (TUR_GRENZEN[this._turMod] || [1, 8])[1]; return this._lob && this._lob.teams ? m * 2 : m; }
    // what is sent: player ids and bots, or teams "team:a+b" of two players each
    _eintraege(L) {
      if (!L.teams) return L.spieler.slice();
      const out = []; for (let i = 0; i + 1 < L.spieler.length; i += 2) out.push('team:' + L.spieler[i] + '+' + L.spieler[i + 1]); return out;
    }
    _turBanner(a) {
      const tu = a.turnier, n = tu && tu.match_nr; if (!n) return '';
      const ban = (ic, x, klein) => '<div class="tban"><ha-icon icon="' + ic + '"></ha-icon>' + x + (klein ? ' <small>· ' + klein + '</small>' : '') + '</div>';
      const von = n[2] > 1 ? t('match_of', { n: n[1], m: n[2] }) : '';
      if (tu.phase === 'gruppe') return ban('mdi:table-large', t('t_group', { g: tu.gruppe }), t('liga_match', { n: n[1], m: n[2] }));
      if (tu.phase === 'oben') return ban('mdi:sitemap-outline', t('t_winners'), [t('t_round', { n: n[0] + 1 }), von].filter(Boolean).join(' · '));
      if (tu.phase === 'unten') return ban('mdi:sitemap-outline', t('t_losers'), [t('t_round', { n: n[0] + 1 }), von].filter(Boolean).join(' · '));
      if (tu.phase === 'finale') return ban('mdi:trophy-outline', t('t_grand'));
      if (tu.phase === 'entscheidung') return ban('mdi:trophy-outline', t('t_decider'));
      if (tu.modus === 'liga') return '<div class="tban"><ha-icon icon="mdi:format-list-numbered"></ha-icon>' + t('liga') + ' <small>· ' + t('liga_match', { n: n[1], m: n[2] }) + '</small></div>';
      return '<div class="tban"><ha-icon icon="mdi:tournament"></ha-icon>' + this._rundeName(n[0], n[3]) + (n[2] > 1 ? ' <small>· ' + t('match_of', { n: n[1], m: n[2] }) + '</small>' : '') + '</div>';
    }
    _liga(tu) {
      return '<div class="liga"><small>' + t('table') + '</small>' + this._ltab(tu.tabelle, i => i === 0 && tu.sieger) + '<small>' + t('fixtures') + '</small>' + this._lspiele(tu.spiele) + '</div>';
    }
    _ltab(zeilen, sieger) {
      return '<table class="ltab"><tr><th></th><th></th><th>' + t('t_pl') + '</th><th>' + t('t_w') + '</th><th>' + t('t_legs') + '</th><th>' + t('t_pts') + '</th></tr>' +
        zeilen.map((z, i) => '<tr' + (sieger && sieger(i) ? ' class="w"' : '') + '><td>' + (i + 1) + '</td><td>' + esc(z.name) + '</td><td>' + z.spiele + '</td><td>' + z.siege + '</td><td>' + z.legs + ':' + z.gegen + '</td><td><b>' + z.punkte + '</b></td></tr>').join('') + '</table>';
    }
    _lspiele(spiele) {
      return '<div class="lsl">' + spiele.map(m => '<div class="lsp feld' + (m.aktiv ? ' akt' : '') + '"><span class="' + (m.sieger === 0 ? 'w' : m.sieger === 1 ? 'l' : '') + '">' + esc(m.a) + '</span><b>' + (m.legs ? m.legs[0] + ':' + m.legs[1] : m.sieger == null ? '–' : '✓') + '</b><span class="' + (m.sieger === 1 ? 'w' : m.sieger === 0 ? 'l' : '') + '">' + esc(m.b) + '</span></div>').join('') + '</div>';
    }
    _baum(tu) {
      if (tu.modus === 'liga') return this._liga(tu);
      const champ = tu.sieger ? '<div class="brd"><small>' + t('champion') + '</small><div><div class="bm feld akt"><div class="w">🏆 ' + esc(tu.sieger) + '</div></div></div></div>' : '';
      if (tu.modus === 'doppel_ko') {
        const fin = (tu.finale || []).map((m, i) => '<div class="brd"><small>' + t(i ? 't_decider' : 't_grand') + '</small><div>' + this._bm(m) + '</div></div>').join('');
        return '<small class="tsek">' + t('t_winners') + '</small>' + this._klammer(tu.runden, r => t('t_round', { n: r + 1 }), '') +
          '<small class="tsek">' + t('t_losers') + '</small>' + this._klammer(tu.unten || [], r => t('t_round', { n: r + 1 }), '') +
          (fin || champ ? '<div class="baum fin">' + fin + champ + '</div>' : '');
      }
      if (tu.modus === 'gruppen') {
        const n = tu.naechstes, offen = !tu.gruppen_fertig;
        const gr = tu.gruppen.map(g => {
          const hier = offen && n && g.spiele.some(m => m.k === n.k || m.aktiv);
          return '<div class="grp feld' + (hier ? ' akt' : '') + '"><small>' + t('t_group', { g: g.name }) + '</small>' + this._ltab(g.tabelle, i => i < 2 && !offen) +
            (hier ? this._lspiele(g.spiele) : '') + '</div>';
        }).join('');
        return '<small class="tsek">' + t('t_groups') + '</small><div class="grps">' + gr + '</div><small class="tsek">' + t('t_ko_stage') + '</small>' + this._klammer(tu.runden, r => this._rundeName(r, tu.runden.length), champ);
      }
      return this._klammer(tu.runden, r => this._rundeName(r, tu.runden.length), champ);
    }
    _bm(m) {
      const zeile = k => {
        const nm = k ? m.b : m.a;
        if (nm === '') return '<div class="o">' + t('bye') + '</div>';
        if (nm == null) return '<div class="o">' + (m.pa ? esc(k ? m.pb : m.pa) : '–') + '</div>';
        const c = m.sieger == null || m.freilos ? (m.freilos ? ' class="w"' : '') : m.sieger === k ? ' class="w"' : ' class="l"';
        return '<div' + c + '>' + (m.sieger === k && !m.freilos ? '✓ ' : '') + esc(nm) + '</div>';
      };
      return '<div class="bm feld' + (m.aktiv ? ' akt' : '') + '">' + zeile(0) + zeile(1) + '</div>';
    }
    _klammer(runden, titel, ende) {
      return '<div class="baum">' + runden.map((runde, r) => '<div class="brd"><small>' + titel(r) + '</small><div>' + runde.map(m => this._bm(m)).join('') + '</div></div>').join('') + ende + '</div>';
    }
    _turKnoepfe(tu) {
      if (tu.sieger) return '<button class="start" data-act="turende"><ha-icon icon="mdi:flag-checkered"></ha-icon>' + t('end_tour') + '</button>';
      const n = tu.naechstes;
      return (n ? '<button class="start" data-act="turweiter"><ha-icon icon="mdi:sword-cross"></ha-icon>' + t('next_match', { a: esc(n.a), b: esc(n.b) }) + '</button>' : '') +
        '<button class="auf feld" data-act="turabbr" data-lbl="' + t('cancel_tour') + '" style="--sr-f:var(--red-color,#e53935)"><ha-icon icon="mdi:close-circle-outline"></ha-icon><span class="lbl">' + t('cancel_tour') + '</span></button>';
    }
    _turEnde(a) {
      const tu = a.turnier, sp = a.spieler || [], g = sp[a.gewinner] || {};
      let s = tu.sieger ? '<div class="champ"><span class="pk">🏆</span><h2>' + esc(tu.sieger) + '</h2><div>' + t('champion') + ' · ' + esc(modusText(a.einstellungen)) + '</div></div>'
        : '<div class="sieg"><ha-icon icon="mdi:trophy"></ha-icon><h2>' + t('wins', { n: esc(g.name) }) + '</h2><div>' + this._turBanner(a).replace(/<[^>]+>/g, ' ').trim() + '</div></div>';
      s += '<div class="blk feld" style="margin-top:12px"><div class="bt"><ha-icon icon="mdi:tournament"></ha-icon>' + t('bracket') + '</div>' + this._baum(tu) + '</div>';
      return s + this._turKnoepfe(tu) + '<button class="auf feld" data-act="undo"><ha-icon icon="mdi:undo"></ha-icon><span>' + t('undo_last') + '</span></button>';
    }
    _lobby() {
      const tu = att(this._h, this._spiel).turnier;
      if (tu) return '<div class="lobby"><div class="blk feld"><div class="bt"><ha-icon icon="mdi:tournament"></ha-icon>' + (tu.sieger ? t('champion') + ': ' + esc(tu.sieger) : t('tour_running')) + '</div>' + this._baum(tu) + '</div>' + this._turKnoepfe(tu) + '</div>';
      const h = this._h, L = this._lob, alle = att(h, this._spieler).spieler || [], name = id => (alle.find(s => s.id === id) || {}).name;
      L.spieler = L.spieler.filter(x => x.startsWith('bot:') || name(x));
      if (this._wartName) { const n = alle.find(s => s.name.toLowerCase() === this._wartName); if (n) { this._wartName = null; if (!L.spieler.includes(n.id) && L.spieler.length < this._max()) L.spieler.push(n.id); } }
      const x01 = L.spiel === 'x01', hcAn = x01 && L.hc, eintr = this._eintraege(L);
      const hc = e => { const v = L.handicap[e] || L.startwert; return '<span class="hc"><button class="feld" data-act="hc" data-e="' + esc(e) + '" data-d="-1">−</button><b>' + v + '</b><button class="feld" data-act="hc" data-e="' + esc(e) + '" data-d="1">+</button></span>'; };
      const liste = L.spieler.map((x, i) => {
        const bot = x.startsWith('bot:');
        const kopf = L.teams && i % 2 === 0 ? '<div class="tkopf">' + t('team_n', { n: i / 2 + 1 }) + (hcAn && eintr[i / 2] ? hc(eintr[i / 2]) : '') + '</div>' : '';
        return kopf + '<div class="sp feld"><span class="nr">' + (i + 1) + '</span><span class="nm">' + (bot ? t('bot') + ' <small>' + t('average') + ' ' + x.slice(4) + '</small>' : esc(name(x))) + '</span>' +
          (hcAn && !L.teams ? hc(x) : '') +
          (i ? '<button data-act="hoch" data-i="' + i + '" title="' + t('move_up') + '"><ha-icon icon="mdi:arrow-up"></ha-icon></button>' : '') +
          '<button data-act="weg" data-i="' + i + '" title="' + t('remove') + '"><ha-icon icon="mdi:close"></ha-icon></button></div>';
      }).join('') || '<div class="leer">' + t('nobody') + '</div>';
      const frei = alle.filter(s => !L.spieler.includes(s.id));
      const einh = eintr.length, ungerade = L.teams && L.spieler.length % 2 === 1, max = this._max(), voll = L.spieler.length >= max;
      const tur = !!this._turMod && einh >= 3, gz = TUR_GRENZEN[this._turMod] || [3, 32], turFalsch = tur && (einh < gz[0] || einh > gz[1]);
      let s = '<div class="lobby">';
      if (einh >= 3) {
        s += '<div class="seg breit">' + [['', 'mdi:account-multiple', t('single_game')], ['t', 'mdi:tournament', t('tour_mode')]].map(([v, ic, x]) =>
          '<button class="feld' + ((this._turMod ? 't' : '') === v ? ' an' : '') + '" data-act="turmod" data-v="' + v + '"><ha-icon icon="' + ic + '"></ha-icon> ' + x + '</button>').join('') + '</div>';
        if (tur) {
          s += '<div class="atiles tarten">' + TUR_ARTEN.map(([v, ic, nm, kurz]) => {
            const g = TUR_GRENZEN[v], passt = einh >= g[0] && einh <= g[1];
            return '<button class="feld' + (this._turMod === v ? ' an' : '') + (passt ? '' : ' passtnicht') + '" data-act="turart" data-v="' + v + '"><ha-icon icon="' + ic + '"></ha-icon>' +
              '<span class="an1"><b>' + t(nm) + '</b><small>' + t(kurz) + '</small></span><span class="spz">' + g[0] + '–' + g[1] + ' <ha-icon icon="mdi:account"></ha-icon></span></button>';
          }).join('') + '</div><div class="regel" style="margin:0 0 10px"><ha-icon icon="mdi:information-outline"></ha-icon><span>' + t(TUR_ARTEN.find(x => x[0] === this._turMod)[4]) + '</span></div>';
        }
      }
      s += '<div class="blk feld"><div class="bt"><ha-icon icon="mdi:account-group"></ha-icon>' + t('players') + '<span class="rechts">' + (L.teams ? t('n_teams', { n: einh }) : this._turMod ? t('of16', { n: L.spieler.length, m: max }) : L.spieler.length + ' / ' + max) + '</span>' +
        '<button class="ik" data-act="mischen" title="' + t('shuffle') + '"' + (L.spieler.length < 2 ? ' disabled' : '') + '><ha-icon icon="mdi:shuffle-variant"></ha-icon></button></div>' +
        '<div class="sliste">' + liste + '</div><div class="chips">' +
        frei.map(p => '<button class="chip feld" data-act="dazu" data-id="' + p.id + '"' + (voll ? ' disabled' : '') + '><ha-icon icon="mdi:plus"></ha-icon>' + esc(p.name) + '</button>').join('') +
        '<button class="chip feld" data-act="neu"' + (voll ? ' disabled' : '') + '><ha-icon icon="mdi:account-plus"></ha-icon>' + t('new_player') + '</button>' +
        '<button class="chip feld' + (this._auf.bot ? ' an' : '') + '" data-act="tgl" data-x="bot"' + (voll ? ' disabled' : '') + '><ha-icon icon="mdi:robot-outline"></ha-icon>' + t('bot') + '</button>' +
        (L.spieler.length >= 2 || L.teams ? '<button class="chip feld' + (L.teams ? ' an' : '') + '" data-act="teams"><ha-icon icon="mdi:account-multiple-outline"></ha-icon>' + t('teams') + '</button>' : '') + '</div>';
      if (L.teams) s += '<div class="regel" style="margin:12px 0 0"><ha-icon icon="mdi:information-outline"></ha-icon><span>' + t('teams_hint') + '</span></div>';
      if (hcAn) s += '<div class="regel" style="margin:12px 0 0"><ha-icon icon="mdi:scale-balance"></ha-icon><span>' + t('handicap_hint') + '</span></div>';
      if (this._auf.bot && !voll) s += '<div class="reihe" style="padding-top:12px"><span>' + t('bot_level') + '</span><div class="seg">' + BOTS.map(b => '<button class="feld" data-act="bot" data-l="' + b + '">' + b + '</button>').join('') + '</div></div>';
      s += '</div>';
      const seg = (k, opts) => '<div class="seg">' + opts.map(([v, x]) => '<button class="feld' + (String(L[k]) === String(v) ? ' an' : '') + '" data-act="set" data-k="' + k + '" data-v="' + v + '">' + x + '</button>').join('') + '</div>';
      const legs = n => n + ' Leg' + (n > 1 ? 's' : '');
      const mehrText = [L.sets ? t('sets_to', { n: L.sets }) : t('no_sets'), MODUS.find(m => m[0] === L.einwurf)[1] + ' In', t('bulloff_onoff', { v: L.bull_off ? t('on_w') : t('off_w') }),
        L.bull_5050 ? t('bull5050') : '', L.max_runden ? t('rl_short', { n: L.max_runden }) : '', L.hc ? t('handicap') : ''].filter(Boolean).join(' · ');
      s += this._artWahl(L, seg, legs);
      if (L.spiel === 'x01') {
        s += '<div class="blk feld"><div class="bt"><ha-icon icon="mdi:tune-variant"></ha-icon>' + t('game') + '</div>' +
          '<div class="reihe"><span>' + t('start_value') + '</span>' + seg('startwert', STARTWERTE.map(v => [v, v])) + '</div>' +
          '<div class="reihe"><span>' + (L.sets ? t('legs_per_set') : t('first_to')) + '</span><div class="stepper"><button class="feld" data-act="minus" data-k="legs">−</button><b>' + legs(L.legs) + '</b><button class="feld" data-act="plus" data-k="legs">+</button></div></div>' +
          '<div class="reihe"><span>' + t('checkout') + '</span>' + seg('auswurf', MODUS) + '</div>' +
          auf('mehr', this._auf.mehr, 'mdi:cog-outline', t('more'), mehrText);
        if (this._auf.mehr) s += '<div class="aufinhalt">' +
          '<div class="reihe"><span>' + t('sets_first') + '</span><div class="stepper"><button class="feld" data-act="minus" data-k="sets">−</button><b>' + (L.sets ? L.sets + ' Set' + (L.sets > 1 ? 's' : '') : t('no_sets')) + '</b><button class="feld" data-act="plus" data-k="sets">+</button></div></div>' +
          '<div class="reihe"><span>' + t('checkin') + '</span>' + seg('einwurf', MODUS) + '</div>' +
          '<div class="reihe"><span>' + t('bulloff_who') + '</span>' + seg('bull_off', [[false, t('off_w')], [true, t('on_w')]]) + '</div>' +
          '<div class="reihe"><span>' + t('bull5050') + '<small class="rk">' + t('bull5050_hint') + '</small></span>' + seg('bull_5050', [[false, t('off_w')], [true, t('on_w')]]) + '</div>' +
          '<div class="reihe"><span>' + t('round_limit') + '</span>' + seg('max_runden', [[0, t('off_w')], [10, '10'], [15, '15'], [20, '20']]) + '</div>' +
          '<div class="reihe"><span>' + t('handicap') + '</span>' + seg('hc', [[false, t('off_w')], [true, t('on_w')]]) + '</div></div>';
        s += '</div>';
      }
      if (!boardOnline(this._h) && !L.spieler.every(x => x.startsWith('bot:')))
        s += '<div class="warn"><ha-icon icon="mdi:power-plug-off-outline"></ha-icon><span>' + t('board_off_hint') + '</span>' + ((this._c.power_on || stromCfg(this._h).power_on) ? '<button data-act="pcein">' + t('on') + '</button>' : '') + '</div>';
      const gr = !tur && ART_SPIELER[L.spiel], falsch = gr && einh && (einh < gr[0] || einh > gr[1]);
      if (falsch) s += '<div class="warn"><ha-icon icon="mdi:account-alert-outline"></ha-icon><span>' + t(gr[0] === gr[1] ? 'needs_exact' : 'needs_min', { g: t('a_' + L.spiel), n: gr[0] }) + '</span></div>';
      if (ungerade) s += '<div class="warn"><ha-icon icon="mdi:account-alert-outline"></ha-icon><span>' + t('teams_odd') + '</span></div>';
      if (turFalsch) s += '<div class="warn"><ha-icon icon="mdi:account-alert-outline"></ha-icon><span>' + t('needs_tour', { f: t(TUR_ARTEN.find(x => x[0] === this._turMod)[2]), a: gz[0], b: gz[1] }) + '</span></div>';
      s += tur ? '<button class="start" data-act="turstart"' + (turFalsch || ungerade ? ' disabled' : '') + '><ha-icon icon="mdi:tournament"></ha-icon>' + t('start_tour') + '</button></div>'
        : '<button class="start" data-act="start"' + (einh && einh <= 8 && !falsch && !ungerade ? '' : ' disabled') + '><ha-icon icon="mdi:play"></ha-icon>' + t('start_game') + '</button></div>';
      return s;
    }
    _bulloff(a) {
      const bo = a.bulloff || [];
      const z = bo.map((p, i) => '<div class="boz feld' + (i === a.am_zug && !p.dart && !p.raus ? ' aktiv' : '') + '"' + (p.raus ? ' style="opacity:.45"' : '') + '><ha-icon icon="' + (p.bot ? 'mdi:robot-outline' : 'mdi:account') + '"></ha-icon><b>' + esc(p.name) + (p.werfer ? ' <small>▸ ' + esc(p.werfer) + '</small>' : '') + '</b><span>' +
        (p.raus ? t('out') : p.dart ? ft(p.dart.f) + ' · ' + p.abstand + ' mm' : (i === a.am_zug ? t('aims_bull') : t('waits'))) + '</span></div>').join('');
      return '<div class="blk feld"><div class="bt"><ha-icon icon="mdi:bullseye"></ha-icon>' + (a.gleichstand ? t('tie') : t('bulloff_title')) + '<span class="rechts">' + t('one_dart') + '</span></div><div class="bo">' + z + '</div></div>' +
        '<div class="leiste"><button class="lk feld" data-act="undo"><ha-icon icon="mdi:undo"></ha-icon>' + t('undo') + '</button><button class="lk feld" data-act="dart" data-i="' + bo.filter(p => p.dart && !p.raus).length + '"><ha-icon icon="mdi:pencil"></ha-icon>' + t('enter') + '</button>' +
        '<button class="lk weiter" data-act="weiter"><ha-icon icon="mdi:skip-next"></ha-icon>' + t('missed') + '</button></div>' +
        '<button class="auf feld" data-act="abbr" data-lbl="' + t('cancel_game') + '" style="--sr-f:var(--red-color,#e53935)"><ha-icon icon="mdi:close-circle-outline"></ha-icon><span class="lbl">' + t('cancel_game') + '</span></button>';
    }
    _match(a) {
      if (a.art && a.art !== 'x01') return this._matchArt(a);
      const sp = a.spieler || [], am = a.am_zug, e = a.einstellungen || {}, au = a.aufnahme || { darts: [] }, wer = sp[am] || {};
      const tiles = sp.map((p, i) => '<div class="sk feld' + (i === am ? ' aktiv' : '') + '"><div class="sn">' + (p.bot ? '<ha-icon icon="mdi:robot-outline"></ha-icon>' : '') + esc(p.name) +
        '<span class="lg">' + (e.sets ? p.sets + ' S · ' : '') + p.legs + ' L</span></div>' + werferZeile(p) + '<div class="sr">' + p.rest + '</div>' +
        '<div class="sa">Ø ' + z1(p.avg) + ' · ' + t('n_darts', { n: p.leg_darts }) + (p.letzte != null ? ' · ' + t('last') + ' <b>' + p.letzte + '</b>' : '') + '</div>' +
        (i !== am && p.weg ? '<div class="sw">' + p.weg.map(f => '<span>' + ft(f) + '</span>').join('') + '</div>' : '') + '</div>').join('');
      let hinw, cls = '';
      if (a.leg_gewinner != null) { hinw = '<ha-icon icon="mdi:check-decagram"></ha-icon>' + t('leg_won', { n: esc(sp[a.leg_gewinner].name) }); cls = ' check'; }
      else if (au.bust) { hinw = '<ha-icon icon="mdi:close-octagon"></ha-icon>' + t('bust'); cls = ' bust'; }
      else if (au.fertig) hinw = '<ha-icon icon="mdi:hand-back-left-outline"></ha-icon>' + t('remove_darts');
      else if (wer.bot || wer.werfer_bot) hinw = '<ha-icon icon="mdi:robot-outline"></ha-icon>' + t('throws_now', { n: esc(wer.werfer || wer.name) });
      else if (!wer.offen && e.einwurf !== 'straight') hinw = t(e.einwurf === 'double' ? 'to_start_d' : 'to_start_m', { n: esc(wer.werfer || wer.name) });
      else hinw = '<ha-icon icon="mdi:target"></ha-icon>' + t('your_turn', { n: esc(wer.werfer || wer.name) });
      const dz = [0, 1, 2].map(i => { const d = au.darts[i]; return '<button class="dz feld' + (d ? '' : ' leer') + '" data-act="dart" data-i="' + i + '"><b>' + (d ? ft(d.f) : '–') + '</b><small>' + (d ? pkt(d.f) + ' ' + t('pts') : t('dart') + ' ' + (i + 1)) + '</small></button>'; }).join('');
      const weg = a.weg ? '<div class="weg">' + a.weg.map(f => '<span>' + ft(f) + '</span>').join('') + '</div>' : '';
      let s = '<div class="spieler' + (sp.length > 3 ? ' viele' : '') + '">' + tiles + '</div><div class="mitte"><div class="aufn feld' + cls + '"><div class="hinw">' + hinw + '</div><div class="dartsz">' + dz + '</div>' +
        '<div class="summe"><b>' + au.summe + '</b><span>' + t('rest', { n: wer.rest }) + (a.runden ? ' · ' + this._rundeText(a, wer) : '') + '</span></div>' + weg + this._vorige(a) + '</div>' +
        this._brettHtml(au.darts, undefined, true) + '</div>' +
        '<div class="leiste"><button class="lk feld" data-act="undo"><ha-icon icon="mdi:undo"></ha-icon>' + t('undo') + '</button><button class="lk feld" data-act="dart" data-i="' + Math.min(au.darts.length, 2) + '"><ha-icon icon="mdi:pencil"></ha-icon>' + t('enter') + '</button>' +
        '<button class="lk weiter" data-act="weiter"><ha-icon icon="mdi:skip-next"></ha-icon>' + t('next') + '</button></div>';
      s += auf('verlauf', this._auf.verlauf, 'mdi:history', t('visits'), t('leg') + ' ' + a.leg + (e.sets ? ' · ' + t('set') + ' ' + a.set : ''));
      if (this._auf.verlauf) s += '<div class="aufinhalt">' + this._verlauf(a) + '</div>';
      s += auf('stat', this._auf.stat, 'mdi:chart-box-outline', t('statistics'));
      if (this._auf.stat) s += '<div class="aufinhalt">' + this._statTab(sp) + '</div>';
      s += auf('opt', this._auf.opt, 'mdi:dots-horizontal', t('game'));
      if (this._auf.opt) s += '<div class="aufinhalt"><button class="auf feld" style="margin-top:0;--sr-f:var(--red-color,#e53935)" data-act="abbr" data-lbl="' + t('cancel_noscore') + '"><ha-icon icon="mdi:close-circle-outline"></ha-icon><span class="lbl">' + t('cancel_noscore') + '</span></button></div>';
      return s;
    }
    // lobby: game type (X01, Cricket, Training, Party), the game and its options
    _artWahl(L, seg, legs) {
      const g = GRUPPE[L.spiel] || 'x01';
      let s = '<div class="blk feld"><div class="bt"><ha-icon icon="mdi:bullseye-arrow"></ha-icon>' + t('game_type') + '</div><div class="arten">' +
        ['x01', 'cricket', 'training', 'party'].map(x => '<button class="feld' + (g === x ? ' an' : '') + '" data-act="gruppe" data-v="' + x + '"><ha-icon icon="' + ART_ICON[x] + '"></ha-icon>' + t('g_' + x) + '</button>').join('') + '</div>';
      if (g !== 'x01') {
        // tiles: name, one line of what it is, players if limited
        const n = this._eintraege(L).length;
        s += '<div class="atiles">' + Object.keys(GRUPPE).filter(x => GRUPPE[x] === g).map(x => {
          const gr = ART_SPIELER[x], passt = !gr || !n || (n >= gr[0] && n <= gr[1]);
          return '<button class="feld' + (L.spiel === x ? ' an' : '') + (passt ? '' : ' passtnicht') + '" data-act="art" data-v="' + x + '"><ha-icon icon="' + ART_ICON[x] + '"></ha-icon>' +
            '<span class="an1"><b>' + t('a_' + x) + '</b><small>' + t('s_' + x) + '</small></span>' +
            (gr ? '<span class="spz">' + (gr[0] === gr[1] ? gr[0] : gr[0] + '+') + ' <ha-icon icon="mdi:account"></ha-icon></span>' : '') + '</button>';
        }).join('') + '</div>';
        const v = L.spiel === 'cricket' && L.zahlen === 'hidden' ? 'hidden' : L.spiel === 'cricket' && L.variante && L.variante !== 'standard' ? L.variante : L.spiel;
        s += '<div class="regel"><ha-icon icon="mdi:information-outline"></ha-icon><span>' + t('h_' + v) + '</span></div>';
      }
      s += '</div>';
      if (L.spiel === 'x01') return s;
      (ART_OPT[L.spiel] || []).forEach(([k]) => { if (L[k] === '' || L[k] == null || ((k === 'runden' || k === 'zielwert') && !L[k]) || !ART_OPT[L.spiel].find(o => o[0] === k)[1].some(o => String(o[0]) === String(L[k]))) L[k] = (OPT_STANDARD[k] || {})[L.spiel] || (k === 'leben' ? 3 : ART_OPT[L.spiel].find(o => o[0] === k)[1][0][0]); });
      s += '<div class="blk feld"><div class="bt"><ha-icon icon="mdi:tune-variant"></ha-icon>' + t('game') + '</div>';
      (ART_OPT[L.spiel] || []).forEach(([k, opts]) => {
        s += '<div class="reihe"><span>' + t(OPT_TITEL_ART[L.spiel + ':' + k] || OPT_TITEL[k]) + '</span>' + seg(k, opts.map(([w, x]) => [w, TEXTE.en[x] !== undefined ? t(x) : x])) + '</div>';
      });
      s += '<div class="reihe"><span>' + t('first_to') + '</span><div class="stepper"><button class="feld" data-act="minus" data-k="legs">−</button><b>' + legs(L.legs) + '</b><button class="feld" data-act="plus" data-k="legs">+</button></div></div>' +
        '<div class="reihe"><span>' + t('bulloff_who') + '</span>' + seg('bull_off', [[false, t('off_w')], [true, t('on_w')]]) + '</div></div>';
      return s;
    }
    // text of a target: "D7", "18", "any double" …
    _zielText(z) {
      if (!z) return '';
      if (z === 'D') return t('any_double'); if (z === 'T') return t('any_triple'); if (z === 'DB') return 'Bullseye';
      if (z === 'B' || z === 'S25' || z === 'D25' || z === '25') return z === 'S25' ? '25 / Bull' : 'Bull';
      return z[0] === 'S' ? z.slice(1) : z;
    }
    _rundeText(a, p) {
      const m = a.runden || 0; if (!m) return '';
      const n = (p.runde || 0) + 1;
      if (n > m) return t('tie_extra');
      return t(a.art === 'golf' ? 'hole_of' : a.art === 'baseball' ? 'inning_of' : 'round_of', { n, m });
    }
    _matchArt(a) {
      const sp = a.spieler || [], am = a.am_zug, e = a.einstellungen || {}, au = a.aufnahme || { darts: [] }, art = a.art;
      const wer = sp[am] ? { ...sp[am], name: sp[am].werfer || sp[am].name, bot: sp[am].bot || sp[am].werfer_bot } : {};
      const cricket = CRICKETARTIG.includes(art), check = CHECKARTIG.includes(art);
      const herzen = p => '<span class="herz">' + '❤'.repeat(Math.max(0, p.leben || 0)) + '</span> ' + t('lives') + ' <b>' + (p.leben || 0) + '</b>';
      let oben;
      if (cricket) oben = this._cricketTafel(a);
      else {
        // big value of a player tile
        const gross = p => {
          if (art === 'atc') return this._zielText(p.fertig ? 'D25' : (p.ziel || ''));
          if (art === 'killer') return p.nummer;
          if (art === 'nine_lives') return p.fertig ? '✓' : p.raus ? '–' : this._zielText(p.ziel || '');
          if (art === 'football') return p.rest + (p.ball ? ' <small class="ball">⚽</small>' : '');
          return p.rest;
        };
        // small line below it
        const neben = p => {
          if (art === 'killer' || art === 'nine_lives') return herzen(p);
          if (art === 'checkout121' || art === 'checkout') return t('target_n', { n: p.zielwert }) + ' · ' + t('checks') + ' <b>' + (p.geschafft || 0) + '</b>';
          if (art === 'catch40') return (p.zielwert ? t('target_n', { n: p.zielwert }) + ' · ' : '') + t('checks') + ' <b>' + (p.geschafft || 0) + '</b>';
          if (art === 'atc') return t('n_darts', { n: p.leg_darts });
          if (art === 'rtw') return (p.fertig ? t('done_w') : t('target') + ' <b>' + esc(this._zielText(p.ziel)) + '</b>') + ' · ' + t('hits') + ' ' + (p.treffer || 0);
          if (art === 'gotcha') return t('to_go', { n: p.restwert }) + (p.letzte != null ? ' · ' + t('last') + ' <b>' + p.letzte + '</b>' : '');
          if (art === 'football') return p.ball ? t('has_ball_s') : t('needs_bull');
          if (art === 'scram') return '<b>' + t(p.rolle) + '</b>' + (p.letzte != null ? ' · ' + t('last') + ' <b>' + p.letzte + '</b>' : '');
          if (art === 'jdc') return t('part_of', { n: p.teil || 3 }) + (p.letzte != null ? ' · ' + t('last') + ' <b>' + p.letzte + '</b>' : '');
          return this._rundeText(a, p) + (p.letzte != null ? ' · ' + t('last') + ' <b>' + p.letzte + '</b>' : '');
        };
        const zielImTile = ['atc', 'nine_lives', 'rtw', 'football', 'scram'].includes(art) || check;
        oben = '<div class="spieler' + (sp.length > 3 ? ' viele' : '') + '">' + sp.map((p, i) => '<div class="sk feld' + (i === am ? ' aktiv' : '') + (p.raus ? ' raus' : '') + '"><div class="sn">' +
          (p.bot ? '<ha-icon icon="mdi:robot-outline"></ha-icon>' : '') + esc(p.name) + (p.killer ? '<span class="kil">' + t('killer_w') + '</span>' : '') +
          (p.raus || p.fertig || +e.legs > 1 ? '<span class="lg">' + (p.raus ? t('out_w') : p.fertig ? t('done_w') : p.legs + ' L') + '</span>' : '') + '</div>' + werferZeile(p) +
          '<div class="sr">' + gross(p) + '</div><div class="sa">' + neben(p) + '</div>' +
          (i !== am && p.ziel && !p.raus && !zielImTile ? '<span class="zk">' + t('target') + ' ' + esc(this._zielText(p.ziel)) + '</span>' : '') + '</div>').join('') + '</div>';
        if (art === 'scram') oben += this._zahlenLeiste(a.zahlen || [], (sp[0] || {}).marks || []);
      }
      let hinw, cls = '';
      if (a.leg_gewinner != null) { hinw = '<ha-icon icon="mdi:check-decagram"></ha-icon>' + t('leg_won', { n: esc(sp[a.leg_gewinner].name) }); cls = ' check'; }
      else if (au.fertig) hinw = '<ha-icon icon="mdi:hand-back-left-outline"></ha-icon>' + t('remove_darts');
      else if (wer.bot) hinw = '<ha-icon icon="mdi:robot-outline"></ha-icon>' + t('throws_now', { n: esc(wer.name) });
      else if (art === 'killer') hinw = '<ha-icon icon="mdi:skull-outline"></ha-icon>' + (wer.killer ? t('killer_aims', { n: esc(wer.name) }) : t('hit_double', { n: esc(wer.name), z: wer.nummer }));
      else if (art === 'football') hinw = '<ha-icon icon="mdi:soccer"></ha-icon>' + t(wer.ball ? 'has_ball' : 'get_ball', { n: esc(wer.name) });
      else if (art === 'scram') hinw = '<ha-icon icon="' + (wer.rolle === 'stopper' ? 'mdi:lock-outline' : 'mdi:plus-circle-outline') + '"></ha-icon>' + t(wer.rolle === 'stopper' ? 'is_stopper' : 'is_scorer', { n: esc(wer.name) });
      else hinw = '<ha-icon icon="mdi:target"></ha-icon>' + t('your_turn', { n: esc(wer.name) });
      const dz = [0, 1, 2].map(i => { const d = au.darts[i]; return '<button class="dz feld' + (d ? '' : ' leer') + '" data-act="dart" data-i="' + i + '"><b>' + (d ? ft(d.f) : '–') + '</b><small>' + (d ? pkt(d.f) + ' ' + t('pts') : t('dart') + ' ' + (i + 1)) + '</small></button>'; }).join('');
      let rechts = this._rundeText(a, wer);
      if (cricket) rechts = t('mpr') + ' ' + z1(wer.avg);
      if (art === 'checkout121' || art === 'checkout') rechts = t('rest', { n: wer.rest }) + ' · ' + t('attempt', { n: Math.min(3, wer.versuch || 1) });
      if (art === 'catch40') rechts = t('rest', { n: wer.restwert }) + ' · ' + t('attempt2', { n: Math.min(2, wer.versuch || 1) });
      if (art === 'gotcha') rechts = t('to_go', { n: wer.restwert });
      if (art === 'jdc') rechts = t('part_of', { n: wer.teil || 1 });
      if (art === 'atc') rechts = t('n_darts', { n: wer.leg_darts });
      if (['killer', 'nine_lives', 'rtw', 'football', 'scram'].includes(art)) rechts = '';
      const einheit = { golf: t('strokes'), baseball: t('runs'), atc: t('hits'), doppel: t('hits'), nine_lives: t('hits'), football: t('goals'), catch40: t('points') }[art] || (cricket ? t('marks') : '');
      const summe = cricket ? (((a.verlauf || []).slice(-1)[0] || {}).m || 0) * (au.darts.length ? 1 : 0) : au.summe;
      const ziel = a.ziel && !cricket ? '<div class="ziel">' + esc(this._zielText(a.ziel)) + '<small>' + t('target') + '</small></div>' : '';
      const weg = a.weg ? '<div class="weg">' + a.weg.map(f => '<span>' + ft(f) + '</span>').join('') + '</div>' : '';
      const golf = art === 'golf' && au.darts.length && !au.fertig ? '<div class="klein" style="margin:8px 0 0">' + t('golf_hint') + '</div>' : '';
      const brettZiel = cricket || check || art === 'gotcha' || art === 'scram' ? null : a.ziel;
      let s = oben + '<div class="mitte"><div class="aufn feld' + cls + '"><div class="hinw">' + hinw + '</div><div class="dartsz">' + dz + '</div>' +
        '<div class="summe"><b>' + summe + '</b><span>' + (einheit ? einheit + (rechts ? ' · ' : '') : '') + rechts + '</span></div>' + (check || art === 'gotcha' ? weg : '') + ziel + golf + this._vorige(a) + '</div>' +
        this._brettHtml(au.darts, brettZiel) + '</div>' +
        '<div class="leiste"><button class="lk feld" data-act="undo"><ha-icon icon="mdi:undo"></ha-icon>' + t('undo') + '</button><button class="lk feld" data-act="dart" data-i="' + Math.min(au.darts.length, 2) + '"><ha-icon icon="mdi:pencil"></ha-icon>' + t('enter') + '</button>' +
        '<button class="lk weiter" data-act="weiter"><ha-icon icon="mdi:skip-next"></ha-icon>' + t('next') + '</button></div>';
      s += auf('verlauf', this._auf.verlauf, 'mdi:history', t('visits'), +e.legs > 1 ? t('leg') + ' ' + a.leg : '');
      if (this._auf.verlauf) s += '<div class="aufinhalt">' + this._verlauf(a) + '</div>';
      s += auf('regel', this._auf.regel, 'mdi:information-outline', t('a_' + art));
      if (this._auf.regel) s += '<div class="aufinhalt"><div class="regel" style="margin:0">' + t('h_' + this._regelKey(art, e)) + '</div></div>';
      s += auf('opt', this._auf.opt, 'mdi:dots-horizontal', t('game'));
      if (this._auf.opt) s += '<div class="aufinhalt"><button class="auf feld" style="margin-top:0;--sr-f:var(--red-color,#e53935)" data-act="abbr" data-lbl="' + t('cancel_noscore') + '"><ha-icon icon="mdi:close-circle-outline"></ha-icon><span class="lbl">' + t('cancel_noscore') + '</span></button></div>';
      return s;
    }
    _regelKey(art, e) {
      if (art === 'cricket' && e.zahlen === 'hidden') return 'hidden';
      return art === 'cricket' && e.variante && e.variante !== 'standard' ? e.variante : art;
    }
    // Scram: the numbers and how far the stopper has closed them
    _zahlenLeiste(zahlen, marks) {
      return '<div class="zleiste feld">' + zahlen.map((z, k) => { const m = marks[k] || 0; return '<div class="' + (m >= 3 ? 'zu' : '') + '"><b>' + (z === 25 ? 'B' : z) + '</b><span class="m v' + m + '">' + MARK[m] + '</span></div>'; }).join('') + '</div>';
    }
    _cricketTafel(a) {
      const sp = a.spieler || [], zahlen = a.zahlen || [], am = a.am_zug, ohne = (a.einstellungen || {}).variante === 'no_score' || a.art === 'mickey', verdeckt = a.verdeckt || [];
      const spalten = 'minmax(44px,.7fr) repeat(' + sp.length + ',minmax(0,1fr))';
      const zelle = (i, x, cls) => '<div class="' + (cls || '') + (i === am ? ' akt' : '') + '">' + x + '</div>';
      const name = (z, k) => verdeckt[k] ? '?' : z === 25 ? 'B' : typeof z === 'string' ? t('lbl_' + z) : z;
      let s = '<div class="ct feld" style="--sp:' + spalten + '"><div class="r kopf"><div></div>' + sp.map((p, i) => zelle(i, (p.bot ? '🤖 ' : '') + esc(p.name) + (+(a.einstellungen || {}).legs > 1 ? ' · ' + p.legs : ''))).join('') + '</div>';
      zahlen.forEach((z, k) => {
        const zu = sp.every(p => (p.marks || [])[k] >= 3);
        s += '<div class="r' + (zu ? ' zu' : '') + (verdeckt[k] ? ' verd' : '') + '"><div class="z">' + name(z, k) + '</div>' + sp.map((p, i) => { const m = (p.marks || [])[k] || 0; return zelle(i, MARK[m], 'm v' + m); }).join('') + '</div>';
      });
      if (!ohne) s += '<div class="r pk"><div></div>' + sp.map((p, i) => zelle(i, p.rest)).join('') + '</div>';
      s += '<div class="r mp"><div>' + t('mpr') + '</div>' + sp.map((p, i) => zelle(i, z1(p.avg))).join('') + '</div></div>';
      return s;
    }
    _endeArt(a) {
      const sp = a.spieler || [], g = sp[a.gewinner] || {}, e = a.einstellungen || {}, art = a.art;
      const weniger = art === 'golf' || (art === 'cricket' && e.variante === 'cut_throat');
      const wert = p => art === 'checkout121' || art === 'checkout' ? (p.geschafft || 0) : art === 'killer' || art === 'nine_lives' ? (p.leben || 0) : p.rest;
      const reihe = sp.map((p, i) => i).sort((x, y) => (x === a.gewinner ? -1 : y === a.gewinner ? 1 : (+e.legs > 1 ? sp[y].legs - sp[x].legs : 0) || (weniger ? wert(sp[x]) - wert(sp[y]) : wert(sp[y]) - wert(sp[x]))));
      const ohne = (art === 'cricket' && e.variante === 'no_score') || art === 'mickey';
      const einheit = { cricket: ohne ? t('mpr') : t('points'), mickey: t('mpr'), golf: t('strokes'), baseball: t('runs'), checkout121: t('checks'), checkout: t('checks'), killer: t('lives'),
        nine_lives: t('lives'), football: t('goals'), atc: t('n_darts', { n: '' }).trim() }[art] || t('points');
      const zeig = p => art === 'atc' ? p.darts : ohne ? z1(p.avg) : wert(p);
      return '<div class="sieg"><ha-icon icon="mdi:trophy"></ha-icon><h2>' + t('wins', { n: esc(g.name) }) + '</h2><div>' + esc(modusText(e)) + '</div></div>' +
        '<div class="rang">' + reihe.map((i, k) => '<div class="feld' + (i === a.gewinner ? ' g' : '') + '"><span>' + (k + 1) + '.</span><span>' + esc(sp[i].name) + (+e.legs > 1 ? ' · ' + sp[i].legs + ' L' : '') + '</span><b>' + zeig(sp[i]) + ' <small style="font-size:12px;font-weight:600;color:var(--secondary-text-color)">' + einheit + '</small></b></div>').join('') + '</div>' +
        '<div class="zweier"><button class="lk weiter" data-act="revanche"><ha-icon icon="mdi:refresh"></ha-icon>' + t('rematch') + '</button><button class="lk feld" data-act="neues"><ha-icon icon="mdi:account-group"></ha-icon>' + t('new_game') + '</button></div>' +
        '<button class="auf feld" data-act="undo"><ha-icon icon="mdi:undo"></ha-icon><span>' + t('undo_last') + '</span></button>';
    }
    // effects of Cricket, training and party games
    _fxArt(z, a) {
      const sp = a.spieler || [], wer = (sp[z.s] || {}).name || '', x = z.x || [], art = a.art;
      const wort = (w, lang) => '<div class="wort' + (lang ? ' lang' : '') + '">' + esc(w) + '<span class="glanz"></span></div>';
      const unter = (u, v) => '<div class="unter">' + esc(u) + '</div>' + (v ? '<div class="unter2">' + esc(v) + '</div>' : '');
      const strahlen = '<div class="strahl l"></div><div class="strahl r"></div>';
      if (z.c) {
        const match = String(a.ansage || '').startsWith('Spiel ');
        if (x.includes('shanghai')) return this._fxGross('regenbogen', strahlen + feuerwerk(5, .3) + konfetti(60) + wort('SHANGHAI!', true) + unter(wer, match ? t('fx_match', { n: wer }) : t('fx_leg', { n: wer })), 5200, 'fx-stoss', 'gross');
        if (match) return this._fxGross('gold', feuerwerk(5, .4) + konfetti(50, .2) + '<div class="pokal">🏆</div>' + wort(t('fx_win'), true) + unter(wer, modusText(a.einstellungen)), 5200, 'fx-stoss', 'gross');
        return this._fxGross('gruen', '<div class="welle"></div>' + konfetti(30) + wort('LEG', true) + unter(t('fx_leg', { n: wer })), 3200, 'fx-stoss', 'jubel');
      }
      const raus = x.filter(v => v.startsWith('raus')), leben = x.filter(v => v.startsWith('leben:')), gotcha = x.filter(v => v.startsWith('gotcha:'));
      if (gotcha.length) return this._fxGross('bust', '<div class="pokal">🎯</div>' + wort(t('fx_gotcha'), true) + unter(wer, gotcha.map(v => t('back_to_0', { n: (sp[+v.slice(7)] || {}).name || '' })).join(' · ')), 2800, 'fx-stoss', 'buzz');
      if (x.includes('tor')) return this._fxGross('gruen', '<div class="pokal">⚽</div><div class="welle"></div>' + konfetti(26) + wort(t('fx_goal'), true) + unter(wer, String(z.r)), 2800, 'fx-stoss', 'jubel');
      if (x.includes('wechsel')) return this._fxGross('silber', '<div class="pokal">🔄</div>' + wort(t('fx_swap'), true) + unter(t('stopper') + ' ⇄ ' + t('scorer')), 2600, 'fx-stoss', 'jubel');
      if (x.includes('shanghai')) return this._fxGross('regenbogen', strahlen + konfetti(36) + wort('SHANGHAI!', true) + unter(wer, '+100'), 3400, 'fx-stoss', 'jubel');
      if (x.includes('killer')) return this._fxGross('bust', '<div class="pokal">💀</div>' + wort(t('fx_killer'), true) + unter(wer), 2600, 'fx-stoss', 'buzz');
      if (raus.length) {
        const namen = raus.map(v => (sp[v.startsWith('raus:') ? +v.slice(5) : z.s] || {}).name).join(', ');
        return this._fxGross('bust', RISS_SVG + wort(t('fx_out'), t('fx_out').length > 5) + unter(namen), 2600, 'fx-wackeln', 'buzz');
      }
      if (leben.length) {
        const opfer = sp[+leben[0].slice(6)] || {};
        return this._fxGross('bust', '<div class="pokal">💔</div>' + wort(t('fx_life'), true) + unter(opfer.name || '', opfer.leben === 1 ? t('fx_life1') : t('fx_lives', { n: opfer.leben })), 2400, 'fx-wackeln', 'buzz');
      }
      if (x.includes('nine_marks')) return this._fxGross('gold', strahlen + '<div class="welle"></div>' + konfetti(50, .15) + wort(t('fx_marks', { n: z.m || 9 }), true) + unter(wer, (z.d || []).map(ft).join(' · ')), 4200, 'fx-stoss', 'gross');
      if (x.includes('six_marks')) return this._fxGross('silber', '<div class="welle"></div>' + konfetti(16) + wort(t('fx_marks', { n: z.m }), true) + unter(wer), 2600, 'fx-stoss', 'jubel');
      if (x.includes('hole_in_one')) return this._fxGross('gold', strahlen + '<div class="pokal">⛳</div>' + konfetti(36) + wort(t('fx_hio'), true) + unter(wer), 3600, 'fx-stoss', 'jubel');
      if (x.includes('home_run')) return this._fxGross('gold', '<div class="pokal">⚾</div><div class="welle"></div>' + konfetti(30) + wort(t('fx_homerun'), true) + unter(wer, z.p + ' ' + t('runs')), 3400, 'fx-stoss', 'jubel');
      if (x.includes('halbiert')) return this._fxGross('bust', RISS_SVG + wort(t('fx_halved'), true) + unter(wer, String(z.r)), 2400, 'fx-wackeln', 'buzz');
      if (x.includes('check')) return this._fxGross('gruen', '<div class="welle"></div>' + konfetti(24) + wort(t('fx_check'), true) + unter(wer), 2800, 'fx-stoss', 'jubel');
      if (x.includes('verfehlt')) return this._fxGross('grau', wort(t('fx_missed'), true) + unter(wer), 2200);
      if (x.includes('bust')) return this._fxGross('bust', RISS_SVG + wort(t('fx_bust'), t('fx_bust').length > 5) + unter(wer), 2000, 'fx-wackeln', 'buzz');
      if (x.includes('ball')) return this._fxGross('gruen', '<div class="pokal">⚽</div>' + wort(t('fx_ball'), false) + unter(wer), 1800);
      if (x.includes('geschafft')) return this._fxGross('gruen', '<div class="welle"></div>' + konfetti(30) + wort(t('fx_done'), true) + unter(wer), 3000, 'fx-stoss', 'jubel');
      const zu = x.filter(v => v.startsWith('zu:'));
      if (zu.length) return this._fxGross('gruen', wort(zu.map(v => v === 'zu:25' ? 'BULL' : v.slice(3)).join(' · '), zu.length > 1) + unter(t('fx_closed', { z: '' }).trim() + ' · ' + wer), 1800);
      return null;
    }
    // the last finished visits of everybody, newest first
    _vorige(a) {
      const sp = a.spieler || [], au = a.aufnahme || { darts: [] };
      let v = (a.verlauf || []).slice();
      if ((au.darts || []).length && !au.fertig) v = v.slice(0, -1);
      v = v.filter(z => z.d.length || z.p).slice(-5).reverse();
      if (!v.length) return '';
      return '<div class="vor">' + v.map(z => '<span class="' + (z.b ? 'b' : '') + (z.c ? ' c' : '') + '"><i>' + esc(((sp[z.s] || {}).name || '?').slice(0, 10)) + '</i>' +
        (CRICKETARTIG.includes(a.art) ? (z.m || 0) + ' M' : (z.b && (!a.art || a.art === 'x01' || a.art === 'gotcha') ? 'Bust' : z.p)) + '</span>').join('') + '</div>';
    }
    _verlauf(a) {
      const sp = a.spieler || [], v = (a.verlauf || []).slice().reverse();
      if (!v.length) return '<div class="leer">' + t('no_visit') + '</div>';
      return '<div class="vl">' + v.map(z => '<div class="vz' + (z.b ? ' bu' : '') + (z.c ? ' co' : '') + '" data-act="vz" data-i="' + z.i + '"><span>' + esc(z.w || (sp[z.s] || {}).name) + '</span><span>' +
        (z.d.length ? z.d.map(ft).join(' · ') : '–') + '</span><b>' + (CRICKETARTIG.includes(a.art) ? (z.m || 0) + ' M' : (z.b && (!a.art || a.art === 'x01' || a.art === 'gotcha') ? 'Bust' : z.p)) + '</b><span class="r">' + z.r + '</span></div>').join('') + '</div>' +
        '<div class="klein">' + t('tap_fix') + '</div>';
    }
    _statTab(sp) {
      const zeilen = [[t('average'), p => z1(p.avg)], [t('first9'), p => z1(p.f9)], [t('darts'), p => p.darts], ['Checkout', p => (p.versuche ? z1(p.quote) + ' % (' + p.treffer + '/' + p.versuche + ')' : '–')],
        [t('highest'), p => p.hoechste], [t('best_finish'), p => p.finish || '–'], ['180 / 140+ / 100+', p => p.n180 + ' / ' + p.n140 + ' / ' + p.n100], [t('best_leg'), p => (p.bestes_leg ? t('n_darts', { n: p.bestes_leg }) : '–')]];
      return '<div style="overflow-x:auto"><table class="tab"><tr><th></th>' + sp.map(p => '<th>' + esc(p.name) + '</th>').join('') + '</tr>' +
        zeilen.map(([x, f]) => '<tr><td>' + x + '</td>' + sp.map(p => '<td>' + f(p) + '</td>').join('') + '</tr>').join('') + '</table></div>';
    }
    _ende(a) {
      if (a.art && a.art !== 'x01') return this._endeArt(a);
      const sp = a.spieler || [], g = sp[a.gewinner] || {};
      return '<div class="sieg"><ha-icon icon="mdi:trophy"></ha-icon><h2>' + t('wins', { n: esc(g.name) }) + '</h2><div>' + esc(modusText(a.einstellungen)) + ' · ' +
        sp.map(p => esc(p.name) + ' ' + ((a.einstellungen || {}).sets ? p.sets : p.legs)).join(' : ') + '</div></div>' +
        '<div class="blk feld" style="margin-top:12px">' + this._statTab(sp) + '</div>' +
        '<div class="zweier"><button class="lk weiter" data-act="revanche"><ha-icon icon="mdi:refresh"></ha-icon>' + t('rematch') + '</button><button class="lk feld" data-act="neues"><ha-icon icon="mdi:account-group"></ha-icon>' + t('new_game') + '</button></div>' +
        '<button class="auf feld" data-act="undo"><ha-icon icon="mdi:undo"></ha-icon><span>' + t('undo_last') + '</span></button>';
    }
    _waehler(aufnahme, i, titel) { this._pick = { aufnahme, i, m: 'S' }; this._waehlerZeichnen(titel); }
    _waehlerZeichnen(titel) {
      const p = this._pick; if (titel) p.titel = titel;
      const mb = ['S', 'D', 'T'].map(m => '<button class="feld' + (p.m === m ? ' an' : '') + '" data-act="pm" data-m="' + m + '">' + t({ S: 'single', D: 'double', T: 'treble' }[m]) + '</button>').join('');
      this._modal('<h3>' + esc(p.titel) + '</h3><div class="seg" style="justify-content:center">' + mb + '</div><div class="zahlgitter">' +
        Array.from({ length: 20 }, (_, k) => '<button class="feld" data-act="pf" data-f="' + p.m + (k + 1) + '">' + (p.m === 'S' ? '' : p.m) + (k + 1) + '</button>').join('') + '</div>' +
        '<div class="sonder"><button class="feld" data-act="pf" data-f="S25">25</button><button class="feld" data-act="pf" data-f="D25">Bull</button><button class="feld" data-act="pf" data-f="M">Miss</button>' +
        '<button class="feld" data-act="pf" data-f="" style="color:var(--red-color,#e53935)">' + t('clear') + '</button></div><div class="mknoepfe"><button class="feld" data-act="mzu">' + t('cancel') + '</button></div>');
    }
    _klick(act, b, e) {
      if (act === 'tv') { tvZeigen(this, this._h); return; }
      if (act === 'clip') { this._h.callService('autodarts', 'clip_speichern', {}).then(() => meldung(this, t('clips_saved')), e => meldung(this, (e && e.message) || String(e))); return; }
      if (act === 'tvbrett') { const an = !tvInfo(this._h).brett; this._h.callService('autodarts', 'fernseher_setzen', { brett: an }).then(() => meldung(this, t('tv_board_on') + ': ' + t(an ? 'tv_on_state' : 'tv_off')), e => meldung(this, (e && e.message) || String(e))); return; }
      const h = this._h, L = this._lob, a = att(h, this._spiel);
      const neu = () => { this._alt = null; this._zeichnen(); };
      if (this._ansage()) fxKlang('');  // sounds need a tap once to be allowed
      switch (act) {
        case 'fx': { const ein = !this._fxAn(); try { localStorage.setItem('autodarts_fx', ein ? '1' : '0'); } catch (e) {} this._kxAlt = null; this._zeichnen(); break; }
        case 'ansicht': { const f = ['1', '2', '3', 'g'], n = f[(f.indexOf(this._ansichtNr()) + 1) % 4]; try { localStorage.setItem('autodarts_view', n); } catch (e) {} neu(); break; }
        case 'tipp': {
          const ein = !this._tippAn(); this._tapHand = ein;
          if (ein) this._toast(t('tap_on')); neu(); break;
        }
        case 'kmod': {
          const v = b.dataset.v;
          if (v === 'c') this._tapHand = false; else try { localStorage.setItem('autodarts_tapmode', v); } catch (e) {}
          this._mod = ''; this._summe = ''; neu(); break;
        }
        case 'kmodi': this._mod = this._mod === b.dataset.v ? '' : b.dataset.v; neu(); break;
        case 'kz': {
          const z = +b.dataset.v, mo = this._mod || 'S', n = att(h, this._spiel).aufnahme;
          const f = z === 0 ? 'M' : z === 50 ? 'D25' : z === 25 ? (mo === 'D' ? 'D25' : 'S25') : mo + z;
          if (z === 25 && mo === 'T') break;
          const anz = ((n && n.darts) || []).length;
          if (anz >= 3) { this._toast(t('tap_full')); break; }
          this._dienst('wurf_aendern', { dart: anz, feld: f }); this._mod = ''; neu(); break;
        }
        case 'kzif': {
          const z = this._summe || '', v = b.dataset.v;
          this._summe = v === '<' ? z.slice(0, -1) : (+(z + v) <= 180 ? String(+(z + v)) : z); neu(); break;
        }
        case 'ksum': if (this._summe !== '' && this._summe != null) { this._dienst('aufnahme_eintragen', { punkte: +this._summe }); this._summe = ''; neu(); } break;
        case 'tippen': {
          if (+b.dataset.n >= 3) { this._toast(t('tap_full')); break; }
          const svg = b.querySelector('svg'); if (!svg || !e) break;
          const r = svg.getBoundingClientRect(), x = (e.clientX - r.left) / r.width * 120, y = (e.clientY - r.top) / r.height * 120;
          this._dienst('wurf_aendern', { dart: +b.dataset.n, feld: feldAn(x, y) }); break;
        }
        case 'netz': { try { localStorage.setItem('autodarts_grid', this._netzAn() ? '0' : '1'); } catch (e) {} neu(); break; }
        case 'ansage': { const ein = !this._ansage(); try { localStorage.setItem('autodarts_caller', ein ? '1' : '0'); } catch (e) {} this._abo(); if (ein) this._toast(t('caller_on')); this._kxAlt = null; this._zeichnen(); break; }
        case 'vollbild':
          if (document.fullscreenElement) document.exitFullscreen(); else if (this.requestFullscreen) this.requestFullscreen().catch(() => {});
          setTimeout(() => { this._kxAlt = null; this._zeichnen(); }, 300); break;
        case 'dazu': if (L.spieler.length < this._max()) L.spieler.push(b.dataset.id); neu(); break;
        case 'bot': if (L.spieler.length < this._max()) L.spieler.push('bot:' + b.dataset.l); this._auf.bot = false; neu(); break;
        case 'turmod': this._turMod = b.dataset.v ? (this._turMod || 'ko') : false; L.spieler = L.spieler.slice(0, this._max()); neu(); break;
        case 'turart': this._turMod = b.dataset.v; L.spieler = L.spieler.slice(0, this._max()); neu(); break;
        case 'teams': L.teams = !L.teams; L.spieler = L.spieler.slice(0, this._max()); neu(); break;
        case 'hc': {
          const k = b.dataset.e, i = STARTWERTE.indexOf(L.handicap[k] || L.startwert), v = STARTWERTE[Math.max(0, Math.min(STARTWERTE.length - 1, i + +b.dataset.d))];
          if (v === L.startwert) delete L.handicap[k]; else L.handicap[k] = v; neu(); break;
        }
        case 'turweiter': this._dienst('turnier_weiter'); this._auf.verlauf = this._auf.stat = this._auf.opt = false; break;
        case 'turabbr': zweimal(this, b, t('really_tour'), () => this._dienst('turnier_abbrechen')); break;
        case 'turende': this._dienst('turnier_abbrechen'); if (phase(a) === 'finished') this._dienst('spiel_abbrechen'); break;
        case 'weg': L.spieler.splice(+b.dataset.i, 1); neu(); break;
        case 'hoch': { const i = +b.dataset.i; [L.spieler[i - 1], L.spieler[i]] = [L.spieler[i], L.spieler[i - 1]]; neu(); break; }
        case 'mischen': for (let i = L.spieler.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [L.spieler[i], L.spieler[j]] = [L.spieler[j], L.spieler[i]]; } neu(); break;
        case 'set': { const v = b.dataset.v, k = b.dataset.k; L[k] = ['startwert', 'runden', 'leben', 'zielwert', 'max_runden'].includes(k) ? +v : v === 'true' ? true : v === 'false' ? false : v; neu(); break; }
        case 'gruppe': { const g = b.dataset.v; if (g !== GRUPPE[L.spiel]) { L.spiel = g === 'training' ? 'atc' : g === 'party' ? 'shanghai' : g; L.variante = ''; L.runden = 0; L.zielwert = 0; } neu(); break; }
        case 'art': if (L.spiel !== b.dataset.v) { L.spiel = b.dataset.v; L.variante = ''; L.runden = 0; L.zielwert = 0; } neu(); break;
        case 'plus': case 'minus': { const k = b.dataset.k, d = act === 'plus' ? 1 : -1; L[k] = Math.max(k === 'legs' ? 1 : 0, Math.min(k === 'legs' ? 21 : 13, L[k] + d)); neu(); break; }
        case 'neu':
          this._modal('<h3>' + t('new_player') + '</h3><input maxlength="20" placeholder="' + t('name') + '"><div class="mknoepfe"><button class="feld" data-act="mzu">' + t('cancel') + '</button><button class="ja" data-act="neuok">' + t('create') + '</button></div>');
          this._r.querySelector('.modal input').addEventListener('keydown', e => { if (e.key === 'Enter') this._klick('neuok'); });
          break;
        case 'neuok': {
          const name = ((this._r.querySelector('.modal input') || {}).value || '').trim(); if (!name) return;
          this._modal(null); this._wartName = name.toLowerCase();
          this._dienst('spieler_anlegen', { name });
          break;
        }
        case 'pcein': { const ein = this._c.power_on || stromCfg(h).power_on; if (ein) ausloesen(h, ein, false); break; }
        case 'start': case 'turstart': {
          const x01 = L.spiel === 'x01', eintr = this._eintraege(L), hcw = {};
          if (x01 && L.hc) eintr.forEach(e => { if (L.handicap[e] && L.handicap[e] !== L.startwert) hcw[e] = L.handicap[e]; });
          this._dienst(act === 'turstart' ? 'turnier_starten' : 'spiel_starten', { spieler: eintr, handicap: hcw, bull_5050: x01 && L.bull_5050, max_runden: x01 ? L.max_runden || 0 : 0, spiel: L.spiel, startwert: L.startwert, legs: L.legs, sets: L.spiel === 'x01' ? L.sets : 0, einwurf: L.einwurf, auswurf: L.auswurf, bull_off: L.bull_off,
            variante: L.variante || '', zahlen: L.zahlen, runden: L.runden || 0, leben: L.leben, zielwert: L.zielwert || 0, ...(act === 'turstart' ? { turnier_modus: this._turMod || 'ko' } : {}) });
          this._auf.verlauf = this._auf.stat = this._auf.opt = false; break;
        }
        case 'undo': this._dienst('rueckgaengig'); break;
        case 'weiter': this._dienst('weiter'); break;
        case 'abbr': zweimal(this, b, t('really_cancel'), () => this._dienst('spiel_abbrechen')); break;
        case 'xabbr': this._modal('<h3>' + t('cancel_q') + '</h3><div class="klein" style="margin:0">' + t('cancel_text') + '</div><div class="mknoepfe"><button class="feld" data-act="mzu">' + t('keep_playing') + '</button><button class="ja" data-act="abbrja" style="background:var(--red-color,#e53935)">' + t('cancel') + '</button></div>'); break;
        case 'abbrja': this._modal(null); this._dienst('spiel_abbrechen'); break;
        case 'revanche': this._dienst('spiel_starten'); break;
        case 'neues': this._dienst('spiel_abbrechen'); break;
        case 'dart': this._waehler(null, +b.dataset.i, t('enter_dart', { n: +b.dataset.i + 1 })); break;
        case 'vz': {
          const z = (a.verlauf || []).find(v => v.i === +b.dataset.i); if (!z) return;
          const sp = (a.spieler || [])[z.s] || {};
          this._modal('<h3>' + esc(sp.name) + ': ' + (z.d.length ? z.d.map(ft).join(' · ') : '–') + '</h3><div class="klein" style="margin:0 0 10px">' + t('which_dart') + '</div><div class="dartsz">' +
            [0, 1, 2].map(i => '<button class="dz feld' + (z.d[i] ? '' : ' leer') + '" data-act="vzd" data-a="' + z.i + '" data-i="' + i + '"' + (i > z.d.length ? ' disabled' : '') + '><b>' + (z.d[i] ? ft(z.d[i]) : '+') + '</b><small>' + t('dart') + ' ' + (i + 1) + '</small></button>').join('') +
            '</div><div class="mknoepfe"><button class="feld" data-act="mzu">' + t('close') + '</button></div>');
          break;
        }
        case 'vzd': this._waehler(+b.dataset.a, +b.dataset.i, t('visit_dart', { a: +b.dataset.a + 1, d: +b.dataset.i + 1 })); break;
        case 'pm': this._pick.m = b.dataset.m; this._waehlerZeichnen(); break;
        case 'pf': {
          const p = this._pick, d = { dart: p.i, feld: b.dataset.f };
          if (p.aufnahme != null) d.aufnahme = p.aufnahme;
          this._dienst('wurf_aendern', d); this._modal(null); break;
        }
      }
    }
  }
  customElements.define('autodarts-game-card', AutodartsGameCard);

  /* ---------- Board Manager card ---------- */
  const MGR_CSS = `
.ll{max-height:320px;overflow:auto;border-radius:14px;padding:4px}
.ll label{display:flex;align-items:center;gap:10px;margin:0;padding:10px;border-radius:10px;font-size:14px;font-weight:500;color:var(--primary-text-color);cursor:pointer}
.ll label:hover{background:color-mix(in srgb,var(--primary-text-color) 6%,transparent)}
.ll label ha-icon{--mdc-icon-size:20px;color:var(--secondary-text-color)}
.ll small{margin-left:auto;color:var(--secondary-text-color);font-size:11.5px}
.werte{display:grid;grid-template-columns:repeat(auto-fit,minmax(104px,1fr));gap:6px;margin-bottom:10px}
.wt{border-radius:14px;padding:8px 10px;cursor:pointer}
.wt small{display:block;font-size:11.5px;color:var(--secondary-text-color);font-weight:600}
.wt b{font-size:16px;font-weight:700}
.wt.gut b{color:var(--green-color,#43a047)}.wt.schlecht b{color:var(--red-color,#e53935)}
.kams{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin-bottom:10px}
.kam{position:relative;border-radius:16px;overflow:hidden;background:#000;aspect-ratio:4/3;cursor:pointer}
.kam.live{grid-column:1/-1;aspect-ratio:16/9;order:-1}
.dyn .kams{grid-template-columns:repeat(2,1fr)}
@container (max-width:480px){.kam span{font-size:10.5px;left:5px;top:5px;padding:2px 6px}}
.kam img{width:100%;height:100%;object-fit:cover;display:block}
.kam span{position:absolute;left:8px;top:8px;font-size:12px;font-weight:700;color:#fff;padding:3px 8px;border-radius:8px;background:rgba(0,0,0,.55)}
.kam i{position:absolute;right:8px;top:8px;font-style:normal;font-size:11px;font-weight:800;color:#fff;padding:3px 7px;border-radius:8px;background:#e53935;display:none}
.kam.live i{display:block}
.kam .knetz{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;display:none}
.kam .knetz path{fill:none;stroke:#00e5a8;stroke-width:1.3;vector-effect:non-scaling-stroke;opacity:.9}
.netzk{display:flex;align-items:center;justify-content:space-between;gap:8px;margin:0 2px 6px}
.netzk button{border-radius:10px;padding:5px 11px;font-size:12.5px;font-weight:700}
.netzk button.an{background:color-mix(in srgb,#00a37a 30%,transparent);color:var(--primary-text-color)}
.kam .aus{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;color:#888;font-size:13px;text-align:center;padding:4px}
.steuer{display:grid;grid-template-columns:repeat(auto-fit,minmax(110px,1fr));gap:8px}
.sk2{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:5px;min-height:66px;border-radius:16px;padding:8px 4px;font-size:13px;font-weight:600;--sr-f:var(--k)}
.sk2 ha-icon{--mdc-icon-size:24px;color:var(--k)}
.info{display:grid;grid-template-columns:auto 1fr;gap:6px 14px;font-size:13.5px}
.info span{color:var(--secondary-text-color)}
.info button{border-radius:10px;padding:4px 10px;font-weight:700;margin-left:6px}
.zeile2{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-top:10px}
.zeile2 button{border-radius:12px;padding:9px 14px;font-weight:700}`;
  class AutodartsManagerCard extends DartsSeite {
    static get CSS() { return MGR_CSS; }
    _grund() {
      super._grund();
      const i = this._r.querySelector('.inhalt');
      i.innerHTML = '<div class="netzk"><span class="klein" style="margin:0"></span><button class="feld" data-act="knetz"></button></div><div class="werte"></div><div class="kams"></div><div class="dyn"></div>';
      this._werte = i.querySelector('.werte'); this._kams = i.querySelector('.kams'); this._in = i.querySelector('.dyn');
      this._kams.innerHTML = [1, 2, 3].map(n => '<div class="kam" data-key="camera.camera_' + n + '" data-n="' + n + '"><img alt=""><svg class="knetz" preserveAspectRatio="xMidYMid slice"><path/></svg><span></span><i>LIVE</i><div class="aus"></div></div>').join('');
      this._knetz = true; try { this._knetz = localStorage.getItem('autodarts_manager_grid') !== '0'; } catch (e) {}
      this._r.querySelector('.netzk button').classList.toggle('an', !!this._knetz);
      this._r.querySelector('.inhalt').addEventListener('click', e => { if (e.target.closest('.netzk')) return; const k = e.target.closest('.kam'); if (!k) return; this._live = this._live === k.dataset.key ? null : k.dataset.key; this._bilder(true); });
      this._werte.addEventListener('click', e => { const w = e.target.closest('[data-e]'); if (w) mehrInfo(this, w.dataset.e); });
      this._takt = setInterval(() => this._bilder('takt'), 3000);
    }
    disconnectedCallback() { this._live = null; this._bilder(true); }
    connectedCallback() { if (this._r) this._bilder(true); }
    _sichtbar() { this._bilder(true); }
    _bilder(sofort) {
      // still images every 3 s, only while visible and the board is on; one camera as live stream on request
      if (!this._h || !this._kams) return;
      const h = this._h, on = boardOnline(h), lauf = an(h, E(h, 'binary_sensor.detection_running'));
      const zeigen = this._sicht && !document.hidden && this.isConnected && on && lauf;
      const liste = [...this._kams.querySelectorAll('.kam'), ...this._r.querySelectorAll('.dyn .kam')];
      liste.forEach(k => {
        const id = E(h, k.dataset.key), img = k.querySelector('img'), bild = (att(h, id).entity_picture) || '';
        if (!img._netz) { img._netz = true; img.addEventListener('load', () => this._netzMalen(k, E(this._h, k.dataset.key), true)); }
        const live = zeigen && this._live === k.dataset.key;
        k.classList.toggle('live', live);
        const aus = k.querySelector('.aus'), at = on ? t('cams_start') : t('sc_off');
        aus.style.display = zeigen ? 'none' : ''; if (aus.textContent !== at) aus.textContent = at;
        this._netzMalen(k, id, zeigen && bild);
        if (!zeigen || !bild) { if (img.getAttribute('src')) img.removeAttribute('src'); k.dataset.modus = ''; return; }
        if (live) { if (k.dataset.modus !== 'live') { k.dataset.modus = 'live'; img.src = bild.replace('/api/camera_proxy/', '/api/camera_proxy_stream/'); } return; }
        if (k.dataset.modus === 'live' || sofort === true || !img.getAttribute('src') || (sofort === 'takt' && !k.dataset.laedt)) {
          k.dataset.modus = 'bild'; k.dataset.laedt = '1';
          const neu = new Image(); neu.onload = neu.onerror = () => { k.dataset.laedt = ''; if (k.dataset.modus === 'bild' && neu.complete && neu.naturalWidth) img.src = neu.src; };
          neu.src = bild + (bild.includes('?') ? '&' : '?') + '_=' + Date.now();
        }
      });
    }
    _netzMalen(k, id, zeigen) {
      // calibration grid: rings and segment borders projected back into the camera image
      const svg = k.querySelector('.knetz'); if (!svg) return;
      const H = this._knetz && zeigen ? entzerrung(att(this._h, id).kalibrierung) : null;
      svg.style.display = H ? 'block' : 'none'; if (!H) return;
      const img = k.querySelector('img'); if (!img.naturalWidth) { svg.style.display = 'none'; return; }
      const w = img.naturalWidth, hh = img.naturalHeight, key = w + 'x' + hh + JSON.stringify(H);
      if (svg.dataset.k === key) return; svg.dataset.k = key;
      const Hi = inv3(H); svg.setAttribute('viewBox', '0 0 ' + w + ' ' + hh);
      svg.firstChild.setAttribute('d', pfad(netzLinien(), p => proj(Hi, p[0], p[1])));
    }
    _zeichnen() {
      if (this._fehlt()) return;
      const h = this._h, on = boardOnline(h), c = this._c;
      const S = k => E(h, 'sensor.' + k);
      const status = zst(h, S('status')), ver = zst(h, S('software_version'));
      this._kopf(t('manager'), on ? 'Autodarts ' + (ver || '') + ' · ' + (({ throw: t('st_throw'), takeout: t('st_takeout'), takeoutInProgress: t('st_takeout'), calibrating: t('st_calibrating'), starting: t('st_starting'), stopped: t('st_stopped'), standby: t('st_standby') })[status] || status) : t('sc_off'));
      const nk = this._r.querySelector('.netzk');
      if (nk.firstChild.textContent !== t('tap_cam')) { nk.firstChild.textContent = t('tap_cam'); nk.lastChild.textContent = t('calib_grid'); }
      this._kams.querySelectorAll('.kam span').forEach((s, i) => { const x = t('cam', { n: i + 1 }); if (s.textContent !== x) s.textContent = x; });
      const w = (id, x, wert, kl) => '<div class="wt feld ' + (kl || '') + '" data-e="' + id + '"><small>' + x + '</small><b>' + wert + '</b></div>';
      const n = id => { const v = parseFloat(zst(h, id)); return isNaN(v) ? '–' : zahl(v, v % 1 ? 1 : 0); };
      const kalId = E(h, 'binary_sensor.calibrated'), erkId = E(h, 'binary_sensor.detection_running'), kal = zst(h, kalId), erk = zst(h, erkId);
      const werte = on ? w(S('connection'), t('connection'), t('online'), 'gut') + w(erkId, t('detection'), erk === 'on' ? t('running') : status === 'standby' ? t('st_standby') : t('stopped'), erk === 'on' ? 'gut' : status === 'standby' ? '' : 'schlecht') +
        w(S('fps'), t('fps'), n(S('fps')) + ' fps') + w(S('camera_fps'), t('cameras'), n(S('camera_fps')) + ' fps') +
        w(S('cpu_load'), t('cpu'), n(S('cpu_load')) + ' %') + w(S('memory'), t('memory'), n(S('memory')) + ' MB') +
        w(kalId, t('calibrated'), kal === 'on' ? t('yes') + (n(S('calibration_error')) === '–' ? '' : ' · ' + n(S('calibration_error')) + ' px') : t('no'), kal === 'on' ? 'gut' : 'schlecht')
        : w(S('connection'), t('connection'), t('offline'), 'schlecht');
      if (this._werteAlt !== werte) { this._werteAlt = werte; this._werte.innerHTML = werte; }
      const k = (act, x, icon, f, frage) => '<button class="sk2 feld" data-act="' + act + '" data-lbl="' + x + '"' + (frage ? ' data-frage="' + frage + '"' : '') + ' style="--k:' + f + '"' + (on || act === 'pc' ? '' : ' disabled') + '><ha-icon icon="' + icon + '"></ha-icon><span class="lbl">' + x + '</span></button>';
      let s = '<div class="blk feld"><div class="bt"><ha-icon icon="mdi:gamepad-variant-outline"></ha-icon>' + t('controls') + '</div><div class="steuer">' +
        k('start', t('start'), 'mdi:play', G) + k('stop', t('stop'), 'mdi:stop', R) + k('reset', t('reset'), 'mdi:eject', B) +
        k('kalib', t('calibrate'), 'mdi:crosshairs-gps', 'var(--teal-color,#009688)', t('calibrate_q')) + k('neu', t('restart_sw'), 'mdi:restart', A, t('sure')) +
        (c.pc_restart ? k('pc', t('restart_pc'), 'mdi:desktop-classic', A, t('sure')) : '') + '</div></div>';
      s += auf('extra', this._auf.extra, 'mdi:image-filter-center-focus', t('extra_imgs'));
      if (this._auf.extra) s += '<div class="aufinhalt"><div class="kams">' + [['camera.detection_image', t('detection_img')], ['camera.live_image', t('live_img')]].map(([key, x]) => '<div class="kam" data-key="' + key + '"><img alt=""><span>' + x + '</span><i>LIVE</i><div class="aus"></div></div>').join('') + '</div></div>';
      s += auf('kamset', this._auf.kamset, 'mdi:camera-outline', t('cam_settings'));
      if (this._auf.kamset) {
        const sel = (id, x, fmt) => { const a = att(h, id), cur = zst(h, id); return '<div class="reihe"><span>' + x + '</span><div class="seg">' + (a.options || []).map(o => '<button class="feld' + (o === cur ? ' an' : '') + '" data-act="sel" data-e="' + id + '" data-v="' + esc(o) + '"' + (on ? '' : ' disabled') + '>' + esc(fmt ? fmt(o) : o) + '</button>').join('') + '</div></div>'; };
        s += '<div class="aufinhalt">' + sel(E(h, 'select.camera_resolution'), t('resolution')) + sel(E(h, 'select.camera_fps_setting'), t('fps'), o => o + ' fps') +
          sel(E(h, 'select.camera_standby'), t('standby'), o => (/^\d+$/.test(o) ? t('minutes', { n: o }) : o)) + '<div class="klein">' + t('standby_hint') + '</div></div>';
      }
      const strom = att(h, E(h, 'sensor.players')).strom || {}, nm = id => id ? esc((st(h, id) && st(h, id).attributes.friendly_name) || id) : '–';
      s += auf('strom', this._auf.strom, 'mdi:power-plug', t('plug_title'), strom.schalter ? nm(strom.schalter) : t('plug_none'));
      if (this._auf.strom) {
        s += '<div class="aufinhalt"><div class="reihe"><span>' + t('plug_switch') + '</span><div class="seg"><button class="feld" data-act="plugwahl" data-f="schalter">' + (strom.schalter ? nm(strom.schalter) : t('plug_pick')) + '</button></div></div>' +
          (strom.schalter ? ['leistung', 'einschalten', 'ausschalten', 'pc_online'].map(f => '<div class="reihe"><span>' + t('plug_' + f) + '</span><div class="seg"><button class="feld" data-act="plugwahl" data-f="' + f + '">' + (strom[f] ? nm(strom[f]) : t('plug_pick')) + '</button></div></div>').join('') : '') +
          '<div class="klein">' + t('plug_hint') + '</div></div>';
      }
      s += auf('soft', this._auf.soft, 'mdi:information-outline', t('software'));
      if (this._auf.soft) {
        const a = att(h, S('software_version')), ub = st(h, E(h, 'update.board_software')), url = boardUrl(h);
        const zu = (u, x) => u ? '<span>' + x + '</span><b>' + esc(u.attributes.installed_version || '–') + (u.state === 'on' ? ' → ' + esc(u.attributes.latest_version) + ' <button class="feld" data-act="upd" data-e="' + u.entity_id + '">' + t('install') + '</button>' : '') + '</b>' : '';
        s += '<div class="aufinhalt"><div class="info">' + zu(ub, t('board_sw')) +
          '<span>' + t('vision') + '</span><b>' + esc(a.visionVersion || '–') + '</b><span>' + t('host') + '</span><b>' + esc(a.hostname || '–') + '</b><span>' + t('kernel') + '</span><b>' + esc(a.kernelVersion || '–') + '</b></div>' +
          (url ? '<div class="zeile2"><button class="feld" data-act="orig">' + t('open_orig') + '</button></div><div class="klein">' + t('home_only') + '</div>' : '') + '</div>';
      }
      this._setze(s);
      this._bilder();
    }
    _klick(act, b) {
      if (b.dataset.frage) { zweimal(this, b, b.dataset.frage, () => this._los(act, b)); return; }
      this._los(act, b);
    }
    _los(act, b) {
      const h = this._h, knopf = key => { const id = E(h, 'button.' + key); if (id) aktion(h, 'button', 'press', { entity_id: id }); };
      if (act === 'knetz') { this._knetz = !this._knetz; try { localStorage.setItem('autodarts_manager_grid', this._knetz ? '1' : '0'); } catch (e) {} b.classList.toggle('an', this._knetz); this._bilder(); return; }
      if (act === 'start') knopf('start_detection');
      else if (act === 'stop') knopf('stop_detection');
      else if (act === 'reset') knopf('reset_throws');
      else if (act === 'kalib') knopf('calibrate');
      else if (act === 'neu') knopf('restart_software');
      else if (act === 'pc' && this._c.pc_restart) ausloesen(h, this._c.pc_restart, false);
      else if (act === 'sel') aktion(h, 'select', 'select_option', { entity_id: b.dataset.e, option: b.dataset.v });
      else if (act === 'upd') aktion(h, 'update', 'install', { entity_id: b.dataset.e });
      else if (act === 'orig') { const url = boardUrl(h); if (url) window.open(url, '_blank'); }
      else if (act === 'plugwahl') this._plugWahl(b.dataset.f);
      else if (act === 'plugsetz') {
        const strom = Object.assign({ schalter: '', leistung: '', einschalten: '', ausschalten: '', pc_online: '' }, att(h, E(h, 'sensor.players')).strom || {});
        strom[b.dataset.f] = b.dataset.v || '';
        if (!strom.schalter) Object.keys(strom).forEach(k => { strom[k] = ''; });
        this._dienst('strom_setzen', strom); this._modal(null);
      }
    }
    _plugWahl(feld) {
      // pick the plug (switch.*) or its power meter (sensor in W) from a searchable list
      const h = this._h, name = id => (h.states[id].attributes.friendly_name || id);
      const dom = id => id.split('.')[0], a = id => h.states[id].attributes;
      const passt = id => feld === 'schalter' ? dom(id) === 'switch'
        : feld === 'leistung' ? dom(id) === 'sensor' && (a(id).device_class === 'power' || a(id).unit_of_measurement === 'W')
        : feld === 'pc_online' ? dom(id) === 'binary_sensor'
        : ['script', 'button', 'input_button', 'automation'].includes(dom(id));
      const eigen = id => ((h.entities || {})[id] || {}).platform === 'autodarts';
      const alle = Object.keys(h.states).filter(id => passt(id) && !eigen(id) && h.states[id].state !== 'unavailable').sort((a, b) => name(a).localeCompare(name(b)));
      const zeile = id => '<label data-act="plugsetz" data-f="' + feld + '" data-v="' + id + '"><ha-icon icon="' + ({ schalter: 'mdi:power-socket-eu', leistung: 'mdi:flash-outline', pc_online: 'mdi:desktop-classic' }[feld] || 'mdi:script-text-outline') + '"></ha-icon>' + esc(name(id)) + '<small>' + esc(id) + '</small></label>';
      this._modal('<h3>' + t(feld === 'schalter' ? 'plug_switch' : 'plug_' + feld) + '</h3><input type="search" placeholder="' + t('search') + '"><div class="ll feld" style="margin-top:8px">' + alle.map(zeile).join('') +
        '</div><div class="mknoepfe"><button class="feld" data-act="plugsetz" data-f="' + feld + '" data-v="">' + t('plug_none') + '</button><button class="feld" data-act="mzu">' + t('cancel') + '</button></div>');
      const inp = this._r.querySelector('.modal input'), liste = this._r.querySelector('.modal .ll');
      inp.addEventListener('input', () => { const q = inp.value.toLowerCase(); liste.querySelectorAll('label').forEach(l => { l.style.display = l.textContent.toLowerCase().includes(q) ? '' : 'none'; }); });
    }
  }
  customElements.define('autodarts-manager-card', AutodartsManagerCard);

  /* ---------- Players & statistics card ---------- */
  const SPL_CSS = `
.pl{border-radius:18px;margin-bottom:8px;overflow:hidden}
.plk{display:flex;align-items:center;gap:12px;width:100%;padding:12px 14px;background:transparent;text-align:left}
.plk .av{width:38px;height:38px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:16px;color:#fff;background:var(--primary-color);flex:none}
.plk b{display:block;font-size:15.5px}.plk small{color:var(--secondary-text-color);font-size:12.5px}
.plk .gr{margin-left:auto;text-align:right;font-size:22px;font-weight:800;line-height:1}
.plk .gr small{display:block;font-size:11px;font-weight:600}
.pld{padding:0 14px 14px}
.kach{display:grid;grid-template-columns:repeat(auto-fit,minmax(80px,1fr));gap:6px}
.ka{border-radius:12px;padding:8px 10px}
.ka small{display:block;font-size:11.5px;color:var(--secondary-text-color);font-weight:600}.ka b{font-size:16px}
.plknoepfe{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}
.plknoepfe button{display:flex;align-items:center;gap:6px;border-radius:12px;padding:9px 12px;font-size:13px;font-weight:600;--sr-f:var(--red-color,#e53935)}
.plknoepfe ha-icon{--mdc-icon-size:18px}
.sv{border-radius:14px;padding:10px 12px;margin-bottom:6px;font-size:13.5px}
.sv .k{display:flex;justify-content:space-between;color:var(--secondary-text-color);font-size:12px;margin-bottom:4px}
.sv .g{color:var(--amber-color,#ffc107);font-weight:700}
.chipz{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:10px}
.chipz span{display:inline-flex;align-items:center;gap:5px;font-size:12.5px;font-weight:700;padding:4px 10px;border-radius:999px;background:color-mix(in srgb,var(--primary-text-color) 9%,transparent)}
.chipz ha-icon{--mdc-icon-size:16px}
.ab{display:flex;align-items:center;gap:8px;margin:14px 0 8px;font-size:13px;font-weight:700;color:var(--secondary-text-color);letter-spacing:.02em}
.ab ha-icon{--mdc-icon-size:17px}.ab .rechts{margin-left:auto}
.hm{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:12px;align-items:start}
.hm svg{width:100%;height:auto;display:block}.hm text{font-size:5px;font-weight:700;fill:#ddd;text-anchor:middle;font-family:Arial,sans-serif}
.hm .skala{height:6px;border-radius:99px;margin-top:6px;background:linear-gradient(90deg,#1e3a5f,#2a6fb0,#22a7a0,#7cc644,#f2c12e,#f07b22,#e53935)}
.tf{display:grid;gap:6px}
.tf div{display:grid;grid-template-columns:44px 1fr 34px;gap:6px;align-items:center;font-size:12.5px;font-weight:700}
.tf i{display:block;height:7px;border-radius:99px;background:var(--primary-color)}
.tf span:last-child{text-align:right;color:var(--secondary-text-color)}
.seg2{display:inline-flex;gap:4px}
.seg2 button{font-size:12px;font-weight:700;padding:4px 10px;border-radius:999px;background:transparent;color:var(--secondary-text-color)}
.seg2 button.an{background:color-mix(in srgb,var(--primary-color) 22%,transparent);color:var(--primary-color)}
.spark{width:100%;height:60px;display:block;border-radius:12px;background:color-mix(in srgb,var(--primary-text-color) 5%,transparent)}
.abz{display:grid;grid-template-columns:repeat(auto-fill,minmax(132px,1fr));gap:6px}
.abz div{display:flex;gap:8px;align-items:center;border-radius:12px;padding:8px}
.abz .md{width:30px;height:30px;border-radius:50%;flex:none;display:flex;align-items:center;justify-content:center;font-size:15px;box-shadow:inset 0 -3px 0 rgba(0,0,0,.25)}
.abz .md.s0{opacity:.35}
.abz b{display:block;font-size:12.5px;line-height:1.2}.abz small{font-size:11px;color:var(--secondary-text-color)}
.vs div{display:flex;justify-content:space-between;padding:6px 2px;font-size:13.5px;border-top:1px solid color-mix(in srgb,var(--primary-text-color) 8%,transparent)}
.vs div:first-child{border-top:none}
.rl{display:grid;gap:4px}
.rl div{display:grid;grid-template-columns:26px 1fr auto auto;gap:8px;align-items:center;font-size:13.5px;padding:7px 10px;border-radius:12px}
.rl b{font-variant-numeric:tabular-nums}.rl small{color:var(--secondary-text-color)}
.aim{display:grid;gap:6px;font-size:13.5px}.aim .aimf{font-size:30px;line-height:1.1;color:var(--primary-color)}
@container (max-width:420px){.hm{grid-template-columns:1fr}}`;
  const datum = x => { try { const d = new Date(x); return d.toLocaleDateString(LOC, { day: '2-digit', month: '2-digit' }) + ' ' + d.toLocaleTimeString(LOC, { hour: '2-digit', minute: '2-digit' }); } catch (e) { return ''; } };
  class AutodartsPlayersCard extends DartsSeite {
    static get CSS() { return SPL_CSS; }
    // hit map, most hit fields, trend, badges and head to head of one player
    _profil(p, alle) {
      const felder = p.felder || {}, summe = Object.values(felder).reduce((a, b) => a + b, 0), modus = (this._hm || {})[p.id] || 'f', pkt = modus === 'p';
      let s = '<div class="ab"><ha-icon icon="mdi:bullseye"></ha-icon>' + t('heatmap') + '<span class="rechts seg2">' +
        [['f', 't_fields'], ['p', 't_points'], ['a', 't_aim']].map(([v, k]) => '<button class="' + (modus === v ? 'an' : '') + '" data-act="hm" data-id="' + p.id + '" data-v="' + v + '">' + t(k) + '</button>').join('') + '</span></div>';
      if (modus === 'a') {
        if (!(p.avg > 0)) s += '<div class="leer">' + t('aim_no_avg') + '</div>';
        else {
          const k = aimKarte(p.avg), gut = k.best[0] * 3, t20 = k.t20 * 3;
          s += '<div class="hm"><div>' + aimBrett(k) + '<div class="skala"></div></div><div class="aim"><div class="ab" style="margin-top:0">' + t('aim_best') + '</div><b class="aimf">' + ft(k.feld) + '</b>' +
            '<div>' + t('aim_avg', { n: z1(gut) }) + '</div><div class="klein">' + (k.feld !== 'T20' ? t('aim_vs', { n: z1(t20), d: z1(gut - t20) }) : t('aim_t20')) + '</div>' +
            '<div class="klein">' + t('aim_hint', { a: z1(p.avg), s: Math.round(k.sg) }) + '</div></div></div>';
        }
      } else if (!summe) s += '<div class="leer">' + t('no_data') + '</div>';
      else {
        const top = Object.entries(felder).sort((a, b) => b[1] - a[1]).slice(0, 7), max = top[0][1];
        s += '<div class="hm"><div>' + heatBrett(felder, p.xy, pkt) + (pkt ? '<div class="klein">' + t('points_hint') + '</div>' : '<div class="skala"></div>') + '</div><div><div class="ab" style="margin-top:0">' + t('top_fields') + '</div><div class="tf">' +
          top.map(([f, n]) => '<div><span>' + ft(f) + '</span><i style="width:' + Math.max(4, n / max * 100) + '%"></i><span>' + Math.round(n / summe * 100) + ' %</span></div>').join('') + '</div></div></div>';
      }
      const avgs = (p.trend || []).filter(e => e[0] === 'x01').map(e => e[1]);
      if (avgs.length > 1) s += '<div class="ab"><ha-icon icon="mdi:chart-line"></ha-icon>' + t('trend') + '<span class="rechts">' + z1(avgs[0]) + ' → ' + z1(avgs[avgs.length - 1]) + '</span></div>' + linie(avgs, 300, 60);
      const abz = p.abzeichen || [];
      if (abz.length) {
        const n = abz.filter(a => a.stufe > 0).length;
        s += '<div class="ab"><ha-icon icon="mdi:medal-outline"></ha-icon>' + t('badges') + '<span class="rechts">' + t('n_of', { a: n, b: abz.length }) + '</span></div><div class="abz">' +
          abz.slice().sort((a, b) => b.stufe - a.stufe).map(a => '<div class="feld" title="' + (a.ziel != null ? t('next_at', { n: a.ziel }) : t('gold')) + '"><span class="md s' + a.stufe + '" style="background:' + MEDAILLE[a.stufe] + '">' + (a.stufe ? '★' : '☆') + '</span><span><b>' + t('b_' + a.key) + '</b><small>' +
            (a.stufe ? t(['', 'bronze', 'silver', 'gold'][a.stufe]) + ' · ' : '') + zahl(a.wert || 0, Number.isInteger(a.wert || 0) ? 0 : 1) + (a.ziel != null ? ' / ' + zahl(a.ziel) : '') + '</small></span></div>').join('') + '</div>';
      }
      const gegen = Object.entries(p.gegen || {}).filter(([, w]) => w[0] + w[1] > 0);
      if (gegen.length) s += '<div class="ab"><ha-icon icon="mdi:sword-cross"></ha-icon>' + t('vs') + '</div><div class="vs">' + gegen.map(([id, w]) => '<div><span>' + esc((alle.find(x => x.id === id) || {}).name || '?') + '</span><b>' + w[0] + ' : ' + w[1] + '</b></div>').join('') + '</div>';
      return s;
    }
    _export() {
      const a = att(this._h, E(this._h, 'sensor.players')), sp = a.spieler || [];
      const kopf = ['name', 'elo', 'games', 'wins', 'average', 'first9', 'checkout_pct', 'highest', 'best_finish', 'best_leg', 'n180', 'n140', 'n100', 'darts', 'streak', 'best_streak'];
      const zeilen = sp.map(p => [p.name, p.elo, p.spiele, p.siege, p.avg, p.f9, p.quote, p.hoechste, p.finish, p.bestes_leg, p.n180, p.n140, p.n100, p.darts, p.serie, p.beste_serie]);
      Object.keys(sp.reduce((o, p) => Object.assign(o, p.arten || {}), {})).forEach(art => { kopf.push(art + '_games', art + '_wins', art + '_best'); zeilen.forEach((z, i) => { const g = (sp[i].arten || {})[art] || {}; z.push(g.spiele || 0, g.siege || 0, g.best == null ? '' : g.best); }); });
      const csv = [kopf, ...zeilen].map(z => z.map(v => { const x = String(v == null ? '' : v); return /[",;\n]/.test(x) ? '"' + x.replace(/"/g, '""') + '"' : x; }).join(',')).join('\n');
      const url = URL.createObjectURL(new Blob(['﻿' + csv], { type: 'text/csv' })), l = document.createElement('a');
      l.href = url; l.download = 'autodarts-statistik.csv'; document.body.appendChild(l); l.click(); l.remove(); setTimeout(() => URL.revokeObjectURL(url), 2000);
    }
    _zeichnen() {
      if (this._fehlt()) return;
      const a = att(this._h, E(this._h, 'sensor.players')), sp = a.spieler || [], vl = a.verlauf || [];
      this._kopf(t('players_stats'), t('n_players', { p: sp.length, g: vl.length + (vl.length === 20 ? '+' : '') }));
      let s = '<button class="start" style="background:linear-gradient(135deg,var(--primary-color),color-mix(in srgb,var(--primary-color) 70%,#000));min-height:52px;font-size:16px;margin:0 0 12px" data-act="neu"><ha-icon icon="mdi:account-plus"></ha-icon>' + t('new_player') + '</button>';
      if (!sp.length) s += '<div class="leer">' + t('no_players') + '</div>';
      sp.slice().sort((x, y) => y.spiele - x.spiele).forEach(p => {
        const offen = this._auf['p' + p.id];
        s += '<div class="pl feld"><button class="plk" data-act="tgl" data-x="p' + p.id + '"><span class="av">' + esc(p.name[0] || '?').toUpperCase() + '</span><span><b>' + esc(p.name) + '</b><small>' +
          t('games_wins', { g: p.spiele, w: p.siege }) + (p.spiele ? ' (' + Math.round(p.siege / p.spiele * 100) + ' %)' : '') + '</small></span><span class="gr">' + z1(p.avg) + '<small>' + t('average') + '</small></span></button>';
        if (offen) {
          const ka = (x, v) => '<div class="ka feld"><small>' + x + '</small><b>' + v + '</b></div>';
          s += '<div class="pld"><div class="chipz"><span><ha-icon icon="mdi:chart-line-variant"></ha-icon>' + t('elo') + ' ' + (p.elo || 1000) + '</span>' +
            '<span><ha-icon icon="mdi:fire"></ha-icon>' + t('streak') + ' ' + (p.serie === 1 ? t('n_day') : t('n_days', { n: p.serie || 0 })) + '</span>' +
            '<span><ha-icon icon="mdi:trophy-outline"></ha-icon>' + t('best_streak') + ' ' + (p.beste_serie === 1 ? t('n_day') : t('n_days', { n: p.beste_serie || 0 })) + '</span></div><div class="kach">' + ka(t('average'), z1(p.avg)) + ka(t('first9'), z1(p.f9)) + ka(t('best_avg'), z1(p.bester_avg)) + ka('Checkout', z1(p.quote) + ' %') +
            ka(t('highest'), p.hoechste) + ka(t('best_finish'), p.finish || '–') + ka(t('best_leg'), p.bestes_leg ? t('n_darts', { n: p.bestes_leg }) : '–') + ka(t('n180'), p.n180) +
            ka('140+', p.n140) + ka('100+', p.n100) + ka(t('legs'), p.legs) + ka(t('darts'), zahl(p.darts)) + '</div>' +
            this._profil(p, sp) +
            (Object.keys(p.arten || {}).length ? '<div class="kach" style="margin-top:8px">' + Object.entries(p.arten).filter(([, g]) => g.spiele).map(([art, g]) =>
              ka(t('a_' + art), t('games_wins', { g: g.spiele, w: g.siege }) + (g.best != null ? '<br><small>' + t('best') + ' ' + (CRICKETARTIG.includes(art) ? z1(g.best) + ' MPR' : g.best) + '</small>' : ''))).join('') + '</div>' : '') +
            '<div class="plknoepfe"><button class="feld" data-act="umb" data-id="' + p.id + '" data-n="' + esc(p.name) + '"><ha-icon icon="mdi:pencil"></ha-icon><span class="lbl">' + t('rename') + '</span></button>' +
            '<button class="feld" data-act="statweg" data-id="' + p.id + '" data-lbl="' + t('del_stats') + '"><ha-icon icon="mdi:delete-sweep-outline"></ha-icon><span class="lbl">' + t('del_stats') + '</span></button>' +
            '<button class="feld" data-act="spweg" data-id="' + p.id + '" data-lbl="' + t('del_player') + '"><ha-icon icon="mdi:account-remove"></ha-icon><span class="lbl">' + t('del_player') + '</span></button></div></div>';
        }
        s += '</div>';
      });
      if (sp.length > 1) {
        s += auf('rang', this._auf.rang, 'mdi:podium', t('ranking_elo'), t('elo'));
        if (this._auf.rang) s += '<div class="aufinhalt"><div class="rl">' + sp.slice().sort((x, y) => (y.elo || 1000) - (x.elo || 1000)).map((p, i) =>
          '<div class="feld"><b>' + (i + 1) + '.</b><span>' + esc(p.name) + '</span><small>' + t('games_wins', { g: p.spiele + Object.values(p.arten || {}).reduce((a, g) => a + (g.spiele || 0), 0), w: p.siege + Object.values(p.arten || {}).reduce((a, g) => a + (g.siege || 0), 0) }) + '</small><b>' + (p.elo || 1000) + '</b></div>').join('') + '</div></div>';
      }
      s += auf('verlauf', this._auf.verlauf, 'mdi:history', t('recent'), vl.length ? datum(vl[0].zeit) : '');
      if (this._auf.verlauf) s += '<div class="aufinhalt">' + (vl.length ? vl.map(v => '<div class="sv feld"><div class="k"><span>' + datum(v.zeit) + '</span><span></span></div>' +
        (v.art ? '<small>' + esc(t('a_' + v.art)) + '</small> ' : '') + v.spieler.map(p => '<span class="' + (p.sieger ? 'g' : '') + '">' + (p.sieger ? '🏆 ' : '') + esc(p.name) + ' ' + (p.wert != null ? p.wert : (p.sets || p.legs) + ' <small>(Ø ' + z1(p.avg) + ')</small>') + '</span>').join(' · ') + '</div>').join('') : '<div class="leer">' + t('no_game_yet') + '</div>') + '</div>';
      if (sp.length) s += '<button class="auf feld" data-act="export"><ha-icon icon="mdi:file-delimited-outline"></ha-icon><span>' + t('export') + '</span></button>';
      s += auf('gefahr', this._auf.gefahr, 'mdi:delete-outline', t('reset_all'));
      if (this._auf.gefahr) s += '<div class="aufinhalt"><div class="plknoepfe" style="margin-top:0"><button class="feld" data-act="allesweg" data-lbl="' + t('del_all') + '"><ha-icon icon="mdi:delete-forever"></ha-icon><span class="lbl">' + t('del_all') + '</span></button></div>' +
        '<div class="klein">' + t('players_stay') + '</div></div>';
      this._setze(s);
    }
    _klick(act, b) {
      if (act === 'neu' || act === 'umb') {
        const umb = act === 'umb';
        this._m = { id: b.dataset.id };
        this._modal('<h3>' + (umb ? t('rename') : t('new_player')) + '</h3><input maxlength="20" placeholder="' + t('name') + '" value="' + (umb ? b.dataset.n : '') + '"><div class="mknoepfe"><button class="feld" data-act="mzu">' + t('cancel') + '</button><button class="ja" data-act="' + (umb ? 'umbok' : 'neuok') + '">' + (umb ? t('save') : t('create')) + '</button></div>');
        this._r.querySelector('.modal input').addEventListener('keydown', e => { if (e.key === 'Enter') this._klick(umb ? 'umbok' : 'neuok', b); });
        return;
      }
      if (act === 'neuok' || act === 'umbok') {
        const name = ((this._r.querySelector('.modal input') || {}).value || '').trim(); if (!name) return;
        if (act === 'neuok') this._dienst('spieler_anlegen', { name }); else this._dienst('spieler_aendern', { id: this._m.id, name });
        this._modal(null); return;
      }
      if (act === 'hm') { this._hm = this._hm || {}; this._hm[b.dataset.id] = b.dataset.v; this._alt = null; this._zeichnen(); return; }
      if (act === 'export') { this._export(); return; }
      if (act === 'statweg') zweimal(this, b, t('really_del'), () => this._dienst('statistik_loeschen', { id: b.dataset.id }));
      if (act === 'spweg') zweimal(this, b, t('really_del'), () => this._dienst('spieler_aendern', { id: b.dataset.id, loeschen: true }));
      if (act === 'allesweg') zweimal(this, b, t('del_all_q'), () => this._dienst('statistik_loeschen', { verlauf: true }));
    }
  }
  customElements.define('autodarts-players-card', AutodartsPlayersCard);

  /* ---------- Light effects card ---------- */
  const LICHT_CSS = `
.lr{display:flex;align-items:center;gap:10px;border-radius:16px;padding:10px 12px;margin-bottom:8px}
.lr .pk{width:30px;height:30px;border-radius:50%;flex:none;box-shadow:0 0 12px var(--lf,transparent);border:2px solid color-mix(in srgb,var(--primary-text-color) 15%,transparent)}
.lr .pk.rb{background:conic-gradient(red,#ff0,lime,cyan,blue,#f0f,red)}
.lr .tx{flex:1;min-width:0}.lr b{display:block;font-size:14.5px}.lr small{display:block;color:var(--secondary-text-color);font-size:12.5px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.lr.aus{opacity:.5}
.lr button{width:38px;height:38px;border-radius:12px;display:flex;align-items:center;justify-content:center;background:transparent;flex:none;--sr-f:var(--red-color,#e53935)}
.lr button ha-icon{--mdc-icon-size:20px}
.mbox label{display:block;font-size:12.5px;font-weight:700;color:var(--secondary-text-color);margin:12px 2px 6px}
.mbox select{width:100%;font:inherit;font-size:15px;padding:11px 12px;border-radius:14px;color:var(--primary-text-color);background:color-mix(in srgb,var(--primary-text-color) 7%,transparent);border:1px solid color-mix(in srgb,var(--primary-text-color) 18%,transparent)}
.mbox select option{color:#000}
.fz{display:flex;align-items:center;gap:12px}
.fz input[type=color]{width:54px;height:40px;padding:0;border:none;border-radius:12px;background:none;cursor:pointer}
.fz input[type=range]{flex:1;accent-color:var(--primary-color)}
.fz b{min-width:46px;text-align:right}
.ll{max-height:220px;overflow:auto;border-radius:14px;padding:4px}
.ll label{display:flex;align-items:center;gap:10px;margin:0;padding:8px;border-radius:10px;font-size:14px;font-weight:500;color:var(--primary-text-color);cursor:pointer}
.ll label:hover{background:color-mix(in srgb,var(--primary-text-color) 6%,transparent)}
.ll input{width:18px;height:18px;accent-color:var(--primary-color)}
.ll small{margin-left:auto;color:var(--secondary-text-color);font-size:11.5px}
.seg.fxw{display:grid;grid-template-columns:repeat(auto-fill,minmax(130px,1fr))}
.seg.fxw button{display:flex;align-items:center;gap:6px;padding:9px 10px;font-size:13.5px;text-align:left}`;
  const LICHT_FX = { farbe: 'mdi:palette', blinken: 'mdi:alarm-light-outline', blitz: 'mdi:flash', regenbogen: 'mdi:looks', pulsieren: 'mdi:heart-pulse', herzschlag: 'mdi:heart-flash', stroboskop: 'mdi:flash-alert', ausblenden: 'mdi:weather-sunset-down', wechsel: 'mdi:swap-horizontal', welle: 'mdi:waves', konfetti: 'mdi:party-popper', lauflicht: 'mdi:dots-horizontal', funkeln: 'mdi:shimmer', polizei: 'mdi:car-emergency', feuer: 'mdi:fire', gewitter: 'mdi:weather-lightning', lampe: 'mdi:auto-fix', preset: 'mdi:playlist-star' };
  const OHNE_FARBE = ['regenbogen', 'welle', 'konfetti', 'polizei', 'feuer'];
  const hex = c => '#' + (c || [255, 0, 0]).map(x => ('0' + (+x).toString(16)).slice(-2)).join('');
  const rgb = h => [1, 3, 5].map(i => parseInt(h.slice(i, i + 2), 16));
  class AutodartsLightsCard extends DartsSeite {
    static get CSS() { return LICHT_CSS; }
    getCardSize() { return 6; }
    async _laden() {
      try { this._daten = await this._h.callWS({ type: 'autodarts/lichteffekte' }); } catch (e) { this._daten = { regeln: [], ereignisse: [], effekte: [] }; }
      this._alt = null; this._zeichnen();
    }
    _name(id) { const s = st(this._h, id); return (s && s.attributes.friendly_name) || id; }
    _zeichnen() {
      if (this._fehlt()) return;
      if (!this._daten) { if (!this._lade) { this._lade = true; this._laden(); } return; }
      const r = this._daten.regeln || [];
      this._kopf(t('lights_title'), t('n_rules', { n: r.length }));
      let s = '<button class="start" style="background:linear-gradient(135deg,var(--primary-color),color-mix(in srgb,var(--primary-color) 70%,#000));min-height:52px;font-size:16px;margin:0 0 12px" data-act="neu"><ha-icon icon="mdi:lightbulb-auto-outline"></ha-icon>' + t('new_rule') + '</button>';
      if (!r.length) s += '<div class="leer">' + t('no_rules') + '</div>';
      r.forEach((x, i) => {
        const MUSTER = { feuer: '#ff6d00;background:linear-gradient(135deg,#ff1744,#ffab00)', polizei: '#2962ff;background:linear-gradient(90deg,#f00 50%,#0028ff 50%)' };
        const rb = OHNE_FARBE.includes(x.effekt) && !MUSTER[x.effekt], f = MUSTER[x.effekt] || (x.effekt === 'wechsel' ? hex(x.farbe) + ';background:linear-gradient(135deg,' + hex(x.farbe) + ' 50%,' + hex(x.farbe2 || [0, 0, 255]) + ' 50%)' : hex(x.farbe));
        s += '<div class="lr feld' + (x.aktiv ? '' : ' aus') + '"><span class="pk' + (rb ? ' rb' : '') + '" style="' + (rb ? '' : 'background:' + f + ';--lf:' + f) + '"></span><span class="tx"><b>' + esc(t('ev_' + x.ereignis)) + '</b><small><ha-icon icon="' + LICHT_FX[x.effekt] + '" style="--mdc-icon-size:14px"></ha-icon> ' + esc(x.effekt === 'lampe' && x.lampen_effekt ? x.lampen_effekt : x.effekt === 'preset' && x.preset ? x.preset : t('e_' + x.effekt)) + ' · ' + t('seconds', { n: x.dauer }) + ' · ' +
          esc(x.lichter.map(l => this._name(l)).join(', ')) + '</small></span>' +
          '<button data-act="test" data-i="' + i + '" title="' + t('test') + '"><ha-icon icon="mdi:play"></ha-icon></button>' +
          '<button data-act="aktiv" data-i="' + i + '" title="' + (x.aktiv ? t('active') : t('inactive')) + '"><ha-icon icon="' + (x.aktiv ? 'mdi:toggle-switch' : 'mdi:toggle-switch-off-outline') + '"></ha-icon></button>' +
          '<button data-act="bearb" data-i="' + i + '" title="' + t('edit_rule') + '"><ha-icon icon="mdi:pencil"></ha-icon></button></div>';
      });
      s += '<div class="klein">' + t('lights_hint') + '</div>';
      this._setze(s);
    }
    async _speichern(regeln) {
      await this._h.callService('autodarts', 'lichteffekte_setzen', { regeln: regeln.map(r => { const x = Object.assign({}, r); return x; }) });
      await this._laden();
    }
    _editor() {
      const e = this._ed, ev = this._daten.ereignisse || [], fx = this._daten.effekte || [];
      const wled = this._daten.wled || {}, fxl = id => (st(this._h, id) || { attributes: {} }).attributes.effect_list || [];
      const passt = id => e.effekt === 'preset' ? !!wled[id] : e.effekt === 'lampe' ? fxl(id).length > 0 : true;
      const alle = Object.keys(this._h.states).filter(id => id.startsWith('light.') && this._h.states[id].state !== 'unavailable' && (passt(id) || e.lichter.includes(id)))
        .sort((a, b) => (e.lichter.includes(b) - e.lichter.includes(a)) || this._name(a).localeCompare(this._name(b)));
      const such = (this._such || '').toLowerCase();
      const liste = alle.filter(id => !such || e.lichter.includes(id) || this._name(id).toLowerCase().includes(such) || id.includes(such));
      this._modal('<h3>' + (e.i == null ? t('new_rule') : t('edit_rule')) + '</h3>' +
        '<label>' + t('trigger') + '</label><select data-f="ereignis">' + ev.map(x => '<option value="' + x + '"' + (x === e.ereignis ? ' selected' : '') + '>' + esc(t('ev_' + x)) + '</option>').join('') + '</select>' +
        '<label>' + t('effect') + '</label><div class="seg fxw">' + fx.map(x => '<button class="feld' + (x === e.effekt ? ' an' : '') + '" data-act="fx" data-v="' + x + '"><ha-icon icon="' + LICHT_FX[x] + '" style="--mdc-icon-size:18px"></ha-icon> ' + t('e_' + x) + '</button>').join('') + '</div>' +
        this._extra(e, wled, fxl, alle) +
        (e.effekt === 'preset' ? '' : '<label>' + (OHNE_FARBE.includes(e.effekt) ? t('brightness') : t('color') + ' · ' + t('brightness')) + '</label><div class="fz">' + (OHNE_FARBE.includes(e.effekt) ? '' : '<input type="color" data-f="farbe" value="' + hex(e.farbe) + '">') +
        (e.effekt === 'wechsel' ? '<input type="color" data-f="farbe2" title="' + t('color2') + '" value="' + hex(e.farbe2 || [0, 0, 255]) + '">' : '') +
        '<input type="range" min="1" max="100" data-f="helligkeit" value="' + e.helligkeit + '"><b class="hw">' + e.helligkeit + ' %</b></div>') +
        '<label>' + t('duration') + '</label><div class="stepper"><button class="feld" data-act="dauer" data-v="-1">−</button><b>' + t('seconds', { n: e.dauer }) + '</b><button class="feld" data-act="dauer" data-v="1">+</button></div>' +
        '<label>' + t('lights') + ' · ' + t('n_lights', { n: e.lichter.length }) + '</label><input type="search" data-f="such" placeholder="' + t('search') + '" value="' + esc(this._such || '') + '">' +
        (e.effekt === 'lampe' || e.effekt === 'preset' ? '<div class="klein">' + t(e.effekt === 'lampe' ? 'only_fx' : 'only_wled') + '</div>' : '') +
        (['welle', 'lauflicht', 'funkeln', 'polizei'].includes(e.effekt) ? '<div class="klein">' + t('fx_more') + '</div>' : '') +
        '<div class="ll feld" style="margin-top:6px">' + liste.map(id => '<label><input type="checkbox" data-l="' + id + '"' + (e.lichter.includes(id) ? ' checked' : '') + '>' + esc(this._name(id)) + '<small>' + id.slice(6) + '</small></label>').join('') + '</div>' +
        (this._edFehler ? '<div class="klein" style="color:var(--red-color,#e53935)">' + t('no_lights') + '</div>' : '') +
        '<div class="mknoepfe">' + (e.i != null ? '<button class="feld" data-act="weg" data-lbl="' + t('delete') + '" style="margin-right:auto;--sr-f:var(--red-color,#e53935)"><span class="lbl">' + t('delete') + '</span></button>' : '') +
        '<button class="feld" data-act="edtest"><ha-icon icon="mdi:play" style="--mdc-icon-size:18px"></ha-icon> ' + t('test') + '</button><button class="feld" data-act="mzu">' + t('cancel') + '</button><button class="ja" data-act="edok">' + t('save') + '</button></div>');
      const box = this._r.querySelector('.mbox');
      box.querySelectorAll('[data-f]').forEach(f => f.addEventListener('input', () => {
        const k = f.dataset.f;
        if (k === 'farbe') e.farbe = rgb(f.value);
        else if (k === 'farbe2') e.farbe2 = rgb(f.value);
        else if (k === 'helligkeit') { e.helligkeit = +f.value; box.querySelector('.hw').textContent = f.value + ' %'; }
        else if (k === 'ereignis') e.ereignis = f.value;
        else if (k === 'lampen_effekt' || k === 'preset') e[k] = f.value;
        else if (k === 'tempo' || k === 'staerke') { e[k] = +f.value; f.nextElementSibling.textContent = Math.round(f.value / 2.55) + ' %'; }
        else if (k === 'such') { this._such = f.value; clearTimeout(this._sw); this._sw = setTimeout(() => { this._editor(); const i = this._r.querySelector('[data-f=such]'); i.focus(); i.setSelectionRange(i.value.length, i.value.length); }, 250); }
      }));
      box.querySelectorAll('[data-l]').forEach(c => c.addEventListener('change', () => {
        const id = c.dataset.l; e.lichter = c.checked ? e.lichter.concat(id) : e.lichter.filter(x => x !== id);
        if (e.effekt === 'lampe' || e.effekt === 'preset') { const y = this._r.querySelector('.mbox').scrollTop; this._editor(); this._r.querySelector('.mbox').scrollTop = y; return; }
        box.querySelector('.ll').previousElementSibling.previousElementSibling.textContent = t('lights') + ' · ' + t('n_lights', { n: e.lichter.length });
      }));
    }
    _extra(e, wled, fxl, alle) {
      // choices for the light's own effects and WLED presets, taken from the chosen lights (or all fitting ones)
      const basis = e.lichter.length ? e.lichter : alle, sel = (f, liste, wert) => '<select data-f="' + f + '">' + liste.map(x => '<option' + (x === wert ? ' selected' : '') + '>' + esc(x) + '</option>').join('') + '</select>';
      if (e.effekt === 'lampe') {
        const liste = [...new Set(basis.flatMap(fxl))].filter(x => !['None', 'off', 'Solid'].includes(x));
        if (!liste.length) return '<label>' + t('fx_name') + '</label><div class="klein">' + t('no_fx') + '</div>';
        if (!liste.includes(e.lampen_effekt)) e.lampen_effekt = liste[0];
        let s = '<label>' + t('fx_name') + '</label>' + sel('lampen_effekt', liste, e.lampen_effekt);
        if (basis.some(id => wled[id] && wled[id].tempo)) {
          if (e.tempo == null) e.tempo = 128; if (e.staerke == null) e.staerke = 128;
          s += [['tempo', 'speed'], ['staerke', 'intensity']].map(([k, n]) => '<label>' + t(n) + '</label><div class="fz"><input type="range" min="0" max="255" data-f="' + k + '" value="' + e[k] + '"><b>' + Math.round(e[k] / 2.55) + ' %</b></div>').join('');
        } else { e.tempo = null; e.staerke = null; }
        return s;
      }
      if (e.effekt === 'preset') {
        const liste = [...new Set(basis.flatMap(id => (wled[id] && wled[id].presets) || []))];
        if (!Object.keys(wled).length) return '<div class="klein">' + t('no_wled') + '</div>';
        if (!liste.includes(e.preset)) e.preset = liste[0] || '';
        return '<label>' + t('preset_name') + '</label>' + (liste.length ? sel('preset', liste, e.preset) : '<div class="klein">' + t('no_fx') + '</div>');
      }
      return '';
    }
    _regel(e) {
      const r = { id: e.id, ereignis: e.ereignis, lichter: e.lichter, effekt: e.effekt, farbe: e.farbe, farbe2: e.farbe2 || [0, 0, 255], helligkeit: e.helligkeit, dauer: e.dauer, aktiv: e.aktiv !== false };
      if (e.effekt === 'lampe') Object.assign(r, { lampen_effekt: e.lampen_effekt || '', tempo: e.tempo == null ? null : e.tempo, staerke: e.staerke == null ? null : e.staerke });
      if (e.effekt === 'preset') r.preset = e.preset || '';
      return r;
    }
    _klick(act, b) {
      const r = (this._daten && this._daten.regeln) || [];
      if (act === 'neu' || act === 'bearb') {
        const x = act === 'bearb' ? r[+b.dataset.i] : null;
        this._ed = x ? Object.assign({ i: +b.dataset.i }, JSON.parse(JSON.stringify(x))) : { ereignis: 'one_eighty', effekt: 'regenbogen', farbe: [255, 170, 0], helligkeit: 100, dauer: 5, lichter: [], aktiv: true };
        this._such = ''; this._edFehler = false; this._editor(); return;
      }
      if (act === 'test') { this._h.callService('autodarts', 'lichteffekt_testen', { regel: this._regel(r[+b.dataset.i]) }); return; }
      if (act === 'aktiv') { const n = r.map((x, i) => i === +b.dataset.i ? Object.assign({}, x, { aktiv: !x.aktiv }) : x); this._speichern(n); return; }
      const e = this._ed; if (!e) return;
      if (act === 'fx') { e.effekt = b.dataset.v; this._editor(); return; }
      if (act === 'dauer') { e.dauer = Math.max(1, Math.min(30, e.dauer + +b.dataset.v)); this._editor(); return; }
      if (act === 'edtest' || act === 'edok') {
        if (!e.lichter.length) { this._edFehler = true; this._editor(); return; }
        if (act === 'edtest') { this._h.callService('autodarts', 'lichteffekt_testen', { regel: this._regel(e) }); return; }
        const n = r.slice(); if (e.i == null) n.push(this._regel(e)); else n[e.i] = this._regel(e);
        this._ed = null; this._modal(null); this._speichern(n); return;
      }
      if (act === 'weg') zweimal(this, b, t('really_del'), () => { const n = r.filter((x, i) => i !== e.i); this._ed = null; this._modal(null); this._speichern(n); });
    }
  }
  customElements.define('autodarts-lights-card', AutodartsLightsCard);

  /* ---------- Caller card: announcements and walk-on songs on the speakers of Home Assistant ---------- */
  const ANSAGE_ARTEN = ['punkte', 'rest', 'ende', 'besondere', 'game_on', 'walkon'];
  class AutodartsCallerCard extends DartsSeite {
    static get CSS() { return LICHT_CSS + '.schalter{display:flex;align-items:center;gap:12px;border-radius:18px;padding:14px 16px;width:100%;font:inherit;font-size:16px;font-weight:700;color:inherit;cursor:pointer;margin-top:8px}.schalter ha-icon{--mdc-icon-size:28px}.schalter.an{background:color-mix(in srgb,var(--primary-color) 22%,transparent);border-color:var(--primary-color)}.schalter small{margin-left:auto;font-weight:600;color:var(--secondary-text-color)}' +
      '.chips{display:flex;flex-wrap:wrap;gap:6px}.wl{display:flex;align-items:center;gap:10px;margin:6px 0}.wl b{flex:1;min-width:0;font-size:14px}.wl select{width:auto;flex:1.4;min-width:0}' +
      '.schritt{font-size:15px;font-weight:800;margin:22px 2px 4px}.lb{display:block;font-size:12.5px;font-weight:700;color:var(--secondary-text-color);margin:16px 2px 6px}' +
      '.inhalt select{width:100%;font:inherit;font-size:15px;padding:11px 12px;border-radius:14px;color:var(--primary-text-color);background:color-mix(in srgb,var(--primary-text-color) 7%,transparent);border:1px solid color-mix(in srgb,var(--primary-text-color) 18%,transparent)}.inhalt select option{color:#000}' +
      '.wahl{display:flex;align-items:center;gap:12px;width:100%;box-sizing:border-box;border-radius:16px;padding:12px 12px 12px 14px;margin-top:8px;text-align:left;font:inherit;color:inherit}.wahl.an{border-color:var(--primary-color);background:color-mix(in srgb,var(--primary-color) 16%,transparent)}' +
      '.wahl .rad{--mdc-icon-size:24px;color:var(--secondary-text-color)}.wahl.an .rad{color:var(--primary-color)}.wahl span{flex:1;min-width:0}.wahl b{display:block;font-size:15px}.wahl small{display:block;font-size:12.5px;color:var(--secondary-text-color);margin-top:2px}' +
      '.wahl .mehr{border:0;background:none;color:inherit;padding:8px;border-radius:12px;cursor:pointer}.wahl .mehr ha-icon{--mdc-icon-size:22px}.balken{height:6px;border-radius:3px;background:color-mix(in srgb,var(--primary-text-color) 12%,transparent);margin-top:6px;overflow:hidden}.balken i{display:block;height:100%;background:var(--primary-color)}' +
      '.neu{display:flex;align-items:center;justify-content:center;gap:8px;width:100%;border-radius:16px;padding:13px;margin-top:10px;font-weight:700;border-style:dashed}' +
      '.sp{display:flex;align-items:center;gap:10px;width:100%;box-sizing:border-box;border-radius:14px;padding:10px 12px;margin-top:6px;text-align:left;font:inherit;color:inherit}.sp.an{border-color:var(--primary-color);background:color-mix(in srgb,var(--primary-color) 16%,transparent)}.sp span{flex:1}.sp small{color:var(--secondary-text-color);margin-left:6px}.sp .probe{border-radius:999px;padding:6px 12px;font-weight:700}' +
      '.mbox .rot,.rot{color:var(--red-color,#e53935)}.mknoepfe .weg{background:var(--red-color,#e53935);color:#fff}.mknoepfe .links{margin-right:auto}.mbox .text{font-size:14px;line-height:1.45;color:var(--secondary-text-color);margin:0 0 6px}'; }
    getCardSize() { return 8; }
    _ansage() { try { return localStorage.getItem('autodarts_caller') === '1'; } catch (e) { return false; } }
    _abo() { if (this._ansage() && this.isConnected) hoerKarten.add(this); else hoerKarten.delete(this); hoerPruefen(this._h); }
    connectedCallback() { if (this._h) this._abo(); }
    disconnectedCallback() { this._abo(); clearTimeout(this._ezT); }
    async _laden() {
      this._abo();
      try { this._daten = await this._h.callWS({ type: 'autodarts/ansager' }); } catch (e) { this._daten = { einstellungen: {}, stimmen: [], packs: {}, songs: [], info: {} }; }
      this._alt = null; this._zeichnen();
      if (this._dlg) this._dialog(this._dlg);  // keep an open dialog up to date (progress)
    }
    _e() { return Object.assign({ aktiv: false, lautsprecher: [], stimme: '', pack: '', punkte: true, rest: true, ende: true, besondere: true, game_on: true, walkon: true, walkon_sekunden: 15, songs: {} }, (this._daten || {}).einstellungen || {}); }
    _name(id) { const s = st(this._h, id); return (s && s.attributes.friendly_name) || id; }
    _stimme() { const d = this._daten || {}; return this._e().stimme || (d.stimmen || [])[0] || ''; }
    _google() { const ent = this._h.entities && this._h.entities[this._stimme()]; return !!ent && ent.platform === 'google_generative_ai_conversation'; }
    _soll() { const i = (this._daten.info || {}); const m = Object.values(i).find(x => x.fehlen != null); return m ? m.toene + m.fehlen : 182; }
    // status line of a pack: ready, being made, waiting for the daily limit, incomplete, own pack
    _status(k) {
      const d = this._daten, ez = d.erzeugung || {}, inf = (d.info || {})[k] || { toene: (d.packs[k] || []).length, fehlen: null }, auf = (d.auftrag || {}).pack === k;
      const pr = d.pruefung || {}, nur = auf && (d.auftrag || {}).nur;
      if (pr.hoeren && pr.laeuft && pr.pack === k) return { text: t('k_listening', { n: pr.fertig, m: pr.gesamt }), anteil: pr.gesamt ? pr.fertig / pr.gesamt : 0 };
      if (ez.pack === k && ez.laeuft) return { text: t('k_run', { n: ez.fertig, m: ez.gesamt }), anteil: ez.gesamt ? ez.fertig / ez.gesamt : 0 };
      if (nur && nur.length) return { text: t('k_redo', { n: nur.length }) };
      if (inf.fehlen == null) return { text: inf.toene ? t('k_ownp', { n: inf.toene }) : t('k_empty') };
      const m = inf.toene + inf.fehlen;
      if (!inf.fehlen) return { text: t('k_done', { n: inf.toene }) + ((d.gehoert || {})[k] ? ' · ' + t('k_listen_ok') : '') };
      if (auf) return { text: t('k_wait', { f: inf.toene, m }), anteil: inf.toene / m };
      if (ez.pack === k && ez.fehler) return { text: ez.fehler === 'stopped' ? t('k_stopped') : ez.fehler === 'daily limit' ? t('k_wait', { f: inf.toene, m }) : t('k_err', { e: ez.fehler }), anteil: inf.toene / m, rot: ez.fehler !== 'daily limit' && ez.fehler !== 'stopped' };
      return { text: t('k_part', { n: inf.fehlen }), anteil: inf.toene / m };
    }
    _zeichnen() {
      if (this._fehlt()) return;
      if (!this._daten) { if (!this._lade) { this._lade = true; this._laden(); } return; }
      const e = this._e(), d = this._daten, hier = this._ansage(), boxen = e.aktiv;
      const stimmen = d.stimmen || [], packs = d.packs || {}, songs = d.songs || [];
      const spieler = (att(this._h, E(this._h, 'sensor.players')).spieler || []);
      const aus = !hier && !(boxen && e.lautsprecher.length);
      this._kopf(t('caller_title'), aus ? t('caller_off_hint') : [hier ? t('phone_run') : '', boxen && e.lautsprecher.length ? e.lautsprecher.length + ' ' + t('speakers') : ''].filter(Boolean).join(' · '));
      // sample on top
      let s = '<button class="start" style="background:linear-gradient(135deg,var(--primary-color),color-mix(in srgb,var(--primary-color) 70%,#000));min-height:52px;font-size:16px;margin:4px 0 0"' + (aus ? ' disabled' : '') + ' data-act="test"><ha-icon icon="mdi:play-circle-outline"></ha-icon>' + t('k_try') + '</button>' +
        '<div class="klein' + (aus ? ' rot' : '') + '">' + (aus ? t('k_no_out') : t('k_try_hint', { n: esc((spieler[0] || {}).name || 'Alex') })) + '</div>';
      // 1 · where
      s += '<div class="schritt">' + t('k_s1') + '</div>';
      s += '<button class="schalter feld' + (hier ? ' an' : '') + '" data-act="hier"><ha-icon icon="' + (hier ? 'mdi:cellphone-sound' : 'mdi:cellphone-off') + '"></ha-icon>' + t('phone_run') + '<small>' + (hier ? t('caller_on_hint') : t('caller_off_hint')) + '</small></button><div class="klein">' + t('phone_hint') + '</div>';
      s += '<button class="schalter feld' + (boxen ? ' an' : '') + '" data-act="aktiv"><ha-icon icon="' + (boxen ? 'mdi:speaker-wireless' : 'mdi:speaker-off') + '"></ha-icon>' + t('caller_run') + '<small>' + (boxen ? t('caller_on_hint') : t('caller_off_hint')) + '</small></button>';
      if (boxen) {
        const lp = Object.keys(this._h.states).filter(id => id.startsWith('media_player.') && this._h.states[id].state !== 'unavailable')
          .sort((a, b) => (e.lautsprecher.includes(b) - e.lautsprecher.includes(a)) || this._name(a).localeCompare(this._name(b)));
        const offen = this._auf.lp != null ? this._auf.lp : !e.lautsprecher.length;
        s += auf('lp', offen, 'mdi:speaker-multiple', t('k_pick_sp'), t('k_n_sel', { n: e.lautsprecher.length }));
        if (offen) s += '<div class="aufinhalt"><div class="ll feld">' + lp.map(id => '<label><input type="checkbox" data-lp="' + id + '"' + (e.lautsprecher.includes(id) ? ' checked' : '') + '>' + esc(this._name(id)) + '<small>' + id.slice(13) + '</small></label>').join('') + '</div></div>';
        if (!e.lautsprecher.length) s += '<div class="klein rot">' + t('no_speakers') + '</div>';
      }
      // 2 · which voice
      s += '<div class="schritt">' + t('k_s2') + '</div>';
      const zeile = (k, titel, unter, an, anteil, rot) => '<div class="wahl feld' + (an ? ' an' : '') + '" data-act="pack" data-v="' + esc(k) + '" role="button"><ha-icon class="rad" icon="' + (an ? 'mdi:radiobox-marked' : 'mdi:radiobox-blank') + '"></ha-icon><span><b>' + esc(titel) + '</b><small' + (rot ? ' class="rot"' : '') + '>' + esc(unter) + '</small>' +
        (anteil != null ? '<div class="balken"><i style="width:' + Math.round(anteil * 100) + '%"></i></div>' : '') + '</span>' + (k ? '<button class="mehr" data-act="packmenue" data-v="' + esc(k) + '" title="' + esc(titel) + '"><ha-icon icon="mdi:dots-vertical"></ha-icon></button>' : '') + '</div>';
      s += zeile('', t('k_live'), stimmen.length ? t('k_live_sub', { v: this._name(this._stimme()) }) : t('no_voice'), !e.pack);
      Object.keys(packs).forEach(k => { const x = this._status(k); s += zeile(k, k, x.text, e.pack === k, x.anteil, x.rot); });
      if (this._google()) s += '<button class="neu feld" data-act="neu"><ha-icon icon="mdi:trophy-variant-outline"></ha-icon>' + t('k_new') + '</button>';
      else if (stimmen.length) s += '<div class="klein">' + t('k_need_google') + '</div>';
      s += auf('stimme', this._auf.stimme, 'mdi:account-voice', t('k_voice_set'), esc(this._name(this._stimme())));
      if (this._auf.stimme) s += '<div class="aufinhalt">' + (stimmen.length ? '<select data-f="stimme"><option value="">' + esc(this._name(stimmen[0])) + ' (auto)</option>' + stimmen.map(x => '<option value="' + x + '"' + (x === e.stimme ? ' selected' : '') + '>' + esc(this._name(x)) + '</option>').join('') + '</select>' : '<div class="klein">' + t('no_voice') + '</div>') + '</div>';
      s += auf('eigen', this._auf.eigen, 'mdi:folder-music-outline', t('k_own'));
      if (this._auf.eigen) s += '<div class="aufinhalt"><div class="klein" style="margin-top:0">' + t('pack_hint') + '</div></div>';
      const ez = d.erzeugung || {};
      clearTimeout(this._ezT);
      if (ez.laeuft || (d.pruefung || {}).laeuft) this._ezT = setTimeout(() => { if (this.isConnected) this._laden(); }, 4000);
      // 3 · what
      s += '<div class="schritt">' + t('k_s3') + '</div><div class="chips">' + ANSAGE_ARTEN.map(k => '<button class="chip feld' + (e[k] ? ' an' : '') + '" data-act="art" data-v="' + k + '"><ha-icon icon="' + (e[k] ? 'mdi:check' : 'mdi:close') + '" style="--mdc-icon-size:16px"></ha-icon>' + t('c_' + k) + '</button>').join('') + '</div>';
      // walk-on songs
      if (e.walkon) {
        s += auf('walk', this._auf.walk, 'mdi:music-note', t('k_s4'), Object.keys(e.songs).length + ' / ' + spieler.length);
        if (this._auf.walk) {
          s += '<div class="aufinhalt">';
          if (!spieler.length) s += '<div class="klein" style="margin-top:0">' + t('no_players_yet') + '</div>';
          else if (!songs.length) s += '<div class="klein" style="margin-top:0">' + t('no_songs') + '</div>';
          else s += spieler.map(p => '<div class="wl"><b>' + esc(p.name) + '</b><select data-song="' + esc(p.id) + '"><option value="">' + t('no_song') + '</option>' + songs.map(x => '<option' + (e.songs[p.id] === x ? ' selected' : '') + '>' + esc(x) + '</option>').join('') + '</select></div>').join('');
          s += '<label class="lb">' + t('walk_secs') + '</label><div class="stepper"><button class="feld" data-act="sek" data-v="-5">−</button><b>' + t('seconds', { n: e.walkon_sekunden }) + '</b><button class="feld" data-act="sek" data-v="5">+</button></div><div class="klein">' + t('songs_hint') + '</div></div>';
        }
      }
      this._setze(s);
      this._in.querySelectorAll('[data-lp]').forEach(c => c.onchange = () => { const x = this._e(); x.lautsprecher = c.checked ? x.lautsprecher.concat(c.dataset.lp) : x.lautsprecher.filter(y => y !== c.dataset.lp); this._speichern(x); });
      this._in.querySelectorAll('[data-f=stimme]').forEach(c => c.onchange = () => { const x = this._e(); x.stimme = c.value; this._speichern(x); });
      this._in.querySelectorAll('[data-song]').forEach(c => c.onchange = () => { const x = this._e(); x.songs = Object.assign({}, x.songs); if (c.value) x.songs[c.dataset.song] = c.value; else delete x.songs[c.dataset.song]; this._speichern(x); });
    }
    _packName(sp) { return 'Meisterschaft ' + sp.charAt(0).toUpperCase() + sp.slice(1); }
    // dialogs: new pack (choose a speaker), pack menu, delete (asks once more with what is lost)
    _dialog(art) {
      this._dlg = art;
      const d = this._daten, packs = d.packs || {}, e = this._e(), ez = d.erzeugung || {}, laeuft = !!ez.laeuft;
      let h;
      if (art.typ === 'neu') {
        const sp = art.sp, da = sp && (packs[this._packName(sp)] || []).length;
        h = '<h3>' + t('k_new') + '</h3><p class="text">' + t('k_new_text', { m: this._soll() }) + '</p><label>' + t('k_choose') + '</label>' +
          SPRECHER.map(([k, n]) => '<div class="sp feld' + (k === sp ? ' an' : '') + '" data-act="sp" data-v="' + k + '" role="button"><ha-icon icon="' + (k === sp ? 'mdi:radiobox-marked' : 'mdi:radiobox-blank') + '"></ha-icon><span><b>' + n + '</b><small>' + t('sp_' + k) + ((packs[this._packName(k)] || []).length ? ' · ' + t('k_have') : '') + '</small></span>' +
            '<button class="probe feld" data-act="probe" data-v="' + k + '"><ha-icon icon="mdi:play" style="--mdc-icon-size:16px"></ha-icon> ' + t('k_sample') + '</button></div>').join('') +
          (laeuft ? '<p class="text" style="margin-top:10px">' + esc(t('k_busy', { p: ez.pack })) + '</p>' : '') +
          '<div class="mknoepfe"><button class="feld" data-act="dzu">' + t('k_cancel') + '</button><button class="ja" data-act="los"' + (!sp || laeuft ? ' disabled' : '') + '>' + (da ? t('k_make_rest') : t('k_make')) + '</button></div>';
      } else if (art.typ === 'menue') {
        const k = art.pack, x = this._status(k), inf = (d.info || {})[k] || {}, auftrag = (d.auftrag || {}).pack === k, sp = (/^Meisterschaft (\w+)$/.exec(k) || [])[1];
        const weiter = sp && this._google() && inf.fehlen > 0 && !laeuft && !auftrag;
        const pr = d.pruefung || {}, hoeren = sp && d.hoeren && this._google() && !laeuft && !auftrag && !(pr.hoeren && pr.laeuft);
        h = '<h3>' + esc(k) + '</h3><p class="text' + (x.rot ? ' rot' : '') + '">' + esc(x.text) + '</p>' + (x.anteil != null ? '<div class="balken"><i style="width:' + Math.round(x.anteil * 100) + '%"></i></div>' : '') +
          '<div class="mknoepfe" style="flex-wrap:wrap"><button class="feld rot links" data-act="wegfrage" data-v="' + esc(k) + '"><ha-icon icon="mdi:delete-outline" style="--mdc-icon-size:18px"></ha-icon> ' + t('k_del') + '</button>' +
          ((ez.pack === k && laeuft) || auftrag ? '<button class="feld" data-act="halt">' + t('k_stop') + '</button>' : '') +
          (weiter ? '<button class="feld" data-act="weiter" data-v="' + esc(k) + '">' + t('k_go_on') + '</button>' : '') +
          (hoeren ? '<button class="feld" data-act="anhoeren" data-v="' + esc(k) + '" title="' + esc(t('k_listen_hint')) + '"><ha-icon icon="mdi:ear-hearing" style="--mdc-icon-size:18px"></ha-icon> ' + t('k_listen') + '</button>' : '') +
          (e.pack === k ? '<button class="feld" disabled>' + t('k_in_use') + '</button>' : '<button class="ja" data-act="nutzen" data-v="' + esc(k) + '">' + t('k_use') + '</button>') +
          '<button class="feld" data-act="dzu">' + t('k_close') + '</button></div>';
      } else {
        const k = art.pack, n = (packs[k] || []).length;
        h = '<h3>' + esc(t('k_del_q', { p: k })) + '</h3><p class="text">' + t('k_del_text', { n }) + '</p><div class="mknoepfe"><button class="feld" data-act="dzu">' + t('k_cancel') + '</button><button class="weg" data-act="wegja" data-v="' + esc(k) + '">' + t('k_del_ok') + '</button></div>';
      }
      if (this._dlgAlt !== h) { this._dlgAlt = h; this._modal(h); }
    }
    _modal(html) { if (!html) { this._dlg = null; this._dlgAlt = null; } super._modal(html); }
    async _speichern(x) {
      this._daten.einstellungen = x; this._alt = null; this._zeichnen();
      try { await this._h.callService('autodarts', 'ansager_setzen', { einstellungen: x }); } catch (err) { await this._laden(); }
    }
    _klick(act, b) {
      const x = this._e(), v = b.dataset.v;
      if (act === 'aktiv') { x.aktiv = !x.aktiv; this._auf.lp = x.aktiv && !x.lautsprecher.length ? true : this._auf.lp; this._speichern(x); }
      else if (act === 'hier') { try { localStorage.setItem('autodarts_caller', this._ansage() ? '0' : '1'); } catch (e) {} fxKlang(''); this._abo(); this._alt = null; this._zeichnen(); }
      else if (act === 'pack') { if (x.pack !== v) { x.pack = v; this._speichern(x); } }
      else if (act === 'packmenue') this._dialog({ typ: 'menue', pack: v });
      else if (act === 'neu') this._dialog({ typ: 'neu', sp: null });
      else if (act === 'sp') this._dialog({ typ: 'neu', sp: v });
      else if (act === 'probe') { fxKlang(''); this._h.callService('autodarts', 'ansager_testen', { sprecher: v }); }
      else if (act === 'los' || act === 'weiter') {
        const sp = act === 'los' ? this._dlg.sp : ((/^Meisterschaft (\w+)$/.exec(v) || [])[1] || '').toLowerCase();
        this._modal(null);
        this._h.callService('autodarts', 'ansager_pack_erzeugen', { sprecher: sp, name: this._packName(sp) }).then(() => setTimeout(() => this._laden(), 800));
      }
      else if (act === 'anhoeren') { this._modal(null); this._h.callService('autodarts', 'ansager_pack_pruefen', { name: v, anhoeren: true }).then(() => setTimeout(() => this._laden(), 800)); }
      else if (act === 'halt') this._h.callService('autodarts', 'ansager_pack_anhalten', {}).then(() => this._laden());
      else if (act === 'nutzen') { this._modal(null); x.pack = v; this._speichern(x); }
      else if (act === 'wegfrage') this._dialog({ typ: 'weg', pack: v });
      else if (act === 'wegja') { this._modal(null); this._h.callService('autodarts', 'ansager_pack_loeschen', { name: v }).then(() => this._laden()); }
      else if (act === 'dzu') this._modal(null);
      else if (act === 'art') { x[v] = !x[v]; this._speichern(x); }
      else if (act === 'sek') { x.walkon_sekunden = Math.max(5, Math.min(60, x.walkon_sekunden + +v)); this._speichern(x); }
      else if (act === 'test') { fxKlang(''); this._h.callService('autodarts', 'ansager_testen', {}); }
    }
  }
  customElements.define('autodarts-caller-card', AutodartsCallerCard);

  /* ---------- TV card: the scoreboard on Fire TV, Google TV, Chromecast or any browser ---------- */
  Object.assign(TEXTE.en, { tv_title: 'TV', d_tv: 'Shows the game big on the TV, with clock and ranking in between', tv_sub_none: 'No TV chosen yet', tv_show: 'Show on TV', tv_stop: 'Take off TV', tv_pick: 'Which TV?', tv_auto: 'Show by itself when a game starts', tv_auto_s: 'The TV switches on and opens the scoreboard', tv_link: 'Link for any browser', tv_copy: 'Copy', tv_open: 'Open', tv_new: 'New link', tv_new_q: 'Old link stops working – sure?', tv_copied: 'Link copied',
    tv_none: 'No suitable TV found yet. Add it in Home Assistant first:', tv_firetv: 'Fire TV and Android TV: integration "Android Debug Bridge"', tv_gtv: 'Google TV: integration "Android TV Remote"', tv_cc: 'Chromecast: integration "Google Cast" (usually found by itself)',
    tv_hint: 'Between games the TV shows the clock, the ranking and the last games. The link works without login – share it only at home.', tv_sent: 'Sent to the TV', tv_off: 'off', tv_on_state: 'on', tv_preview: 'Preview', settings_title: 'Settings', d_settings: 'All DartNest settings behind clear buttons: board, lights, caller, TV',
    m_board: 'Board', m_board_s: 'Cameras, calibration, power', m_lights_s: 'Lights at 180, checkout …', m_caller_s: 'Speakers, voice, walk-on songs', m_tv_s: 'Scoreboard and clock on the TV', online: 'online', offline: 'offline', n_tv: '{n} TV',
    tv_board: 'Show the dartboard', tv_board_s: 'Next to the score, with the darts of the visit', tv_v_g: 'Drawn', tv_v_c: 'Camera {n}', tv_v_hint: 'The camera image appears while the board detects darts, otherwise the drawn board.', tv_board_on: 'Dartboard on the TV' });
  Object.assign(TEXTE.de, { tv_title: 'Fernseher', d_tv: 'Zeigt das Spiel groß auf dem Fernseher, dazwischen Uhr und Rangliste', tv_sub_none: 'Noch kein Fernseher gewählt', tv_show: 'Auf dem Fernseher zeigen', tv_stop: 'Vom Fernseher nehmen', tv_pick: 'Welcher Fernseher?', tv_auto: 'Von selbst zeigen, wenn ein Spiel startet', tv_auto_s: 'Der Fernseher geht an und öffnet die Anzeige', tv_link: 'Link für jeden Browser', tv_copy: 'Kopieren', tv_open: 'Öffnen', tv_new: 'Neuer Link', tv_new_q: 'Alter Link geht dann nicht mehr – sicher?', tv_copied: 'Link kopiert',
    tv_none: 'Noch kein passender Fernseher gefunden. Zuerst in Home Assistant hinzufügen:', tv_firetv: 'Fire TV und Android TV: Integration „Android Debug Bridge“', tv_gtv: 'Google TV: Integration „Android TV Remote“', tv_cc: 'Chromecast: Integration „Google Cast“ (meist schon von selbst gefunden)',
    tv_hint: 'Zwischen den Spielen zeigt der Fernseher Uhr, Rangliste und die letzten Spiele. Der Link geht ohne Anmeldung – nur zu Hause weitergeben.', tv_sent: 'An den Fernseher geschickt', tv_off: 'aus', tv_on_state: 'an', tv_preview: 'Vorschau', settings_title: 'Einstellungen', d_settings: 'Alle DartNest-Einstellungen hinter klaren Knöpfen: Board, Licht, Ansager, Fernseher',
    m_board: 'Board', m_board_s: 'Kameras, Kalibrierung, Strom', m_lights_s: 'Licht bei 180, Checkout …', m_caller_s: 'Lautsprecher, Stimme, Einlaufmusik', m_tv_s: 'Spielstand und Uhr auf dem Fernseher', online: 'online', offline: 'offline', n_tv: '{n} Fernseher',
    tv_board: 'Dartscheibe zeigen', tv_board_s: 'Neben dem Spielstand, mit den Darts der Aufnahme', tv_v_g: 'Gezeichnet', tv_v_c: 'Kamera {n}', tv_v_hint: 'Das Kamerabild erscheint, solange das Board Darts erkennt, sonst die gezeichnete Scheibe.', tv_board_on: 'Dartscheibe am Fernseher' });
  const TV_ART = { androidtv: 'Fire TV / Android TV', androidtv_remote: 'Google TV', cast: 'Chromecast' };
  const tvInfo = h => att(h, E(h, 'sensor.players')).tv || { geraete: [], auto: false, url: '', brett: false, ansicht: 'camera_1' };
  const meldung = (el, text) => el.dispatchEvent(new CustomEvent('hass-notification', { detail: { message: text }, bubbles: true, composed: true }));
  // starts the page on the chosen TVs; errors (TV off, not reachable) come back as a message
  const tvZeigen = (el, h) => h.callService('autodarts', 'fernseher_zeigen', {}).then(() => meldung(el, t('tv_sent')), e => meldung(el, (e && e.message) || String(e)));
  const TV_CSS = `
.tvbild{position:relative;margin:0 auto 14px;width:min(100%,420px);aspect-ratio:16/9;border-radius:16px;overflow:hidden;background:#0d0f14;border:6px solid #23262d;box-shadow:0 10px 30px rgba(0,0,0,.35);display:block;padding:0;cursor:pointer}
.tvbild iframe{position:absolute;left:0;top:0;width:1280px;height:720px;border:0;transform-origin:0 0;pointer-events:none}
.tvbild:after{content:'';position:absolute;left:50%;bottom:-16px;width:90px;height:8px;margin-left:-45px;border-radius:4px;background:#23262d}
.zwei{display:grid;grid-template-columns:1fr auto;gap:8px}
.zwei .start{margin:0}
.zwei .stop{display:flex;align-items:center;gap:8px;border-radius:20px;padding:0 16px;font-weight:700}
.wahl{display:flex;align-items:center;gap:12px;width:100%;box-sizing:border-box;border-radius:16px;padding:12px 14px;margin-top:8px;text-align:left}
.wahl.an{border-color:var(--primary-color);background:color-mix(in srgb,var(--primary-color) 16%,transparent)}
.wahl>ha-icon{--mdc-icon-size:24px;color:var(--secondary-text-color);flex:none}.wahl.an>ha-icon{color:var(--primary-color)}
.wahl span{flex:1;min-width:0}.wahl b{display:block;font-size:15px}.wahl small{display:block;font-size:12.5px;color:var(--secondary-text-color);margin-top:2px}
.wahl .pk{width:10px;height:10px;border-radius:50%;flex:none;background:var(--disabled-color,#9e9e9e)}.wahl .pk.on{background:var(--green-color,#43a047)}
.link{display:flex;align-items:center;gap:8px;border-radius:16px;padding:8px 8px 8px 14px}
.link code{flex:1;min-width:0;font-size:12.5px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;color:var(--secondary-text-color)}
.link button{display:flex;align-items:center;gap:6px;border-radius:12px;padding:8px 10px;font-size:13px;font-weight:700;flex:none}
.link button ha-icon{--mdc-icon-size:18px}
.neuer{display:inline-flex;align-items:center;gap:6px;border-radius:12px;padding:8px 12px;margin-top:8px;font-size:13px;font-weight:600;--sr-f:var(--red-color,#e53935)}
.ohne{border-radius:16px;padding:12px 14px;font-size:13.5px;line-height:1.5}
.ansicht{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin-top:8px}
.ansicht button{display:flex;flex-direction:column;align-items:center;gap:4px;border-radius:14px;padding:10px 4px;font-size:12.5px;font-weight:700}
.ansicht button ha-icon{--mdc-icon-size:22px;color:var(--secondary-text-color)}
.ansicht button.an{border-color:var(--primary-color);background:color-mix(in srgb,var(--primary-color) 16%,transparent)}.ansicht button.an ha-icon{color:var(--primary-color)}
.ohne ul{margin:6px 0 0;padding-left:18px}`;
  class AutodartsTvCard extends DartsSeite {
    static get CSS() { return TV_CSS + '.schalter{display:flex;align-items:center;gap:12px;border-radius:18px;padding:14px 16px;width:100%;box-sizing:border-box;text-align:left;margin-top:8px}.schalter>ha-icon{--mdc-icon-size:28px;flex:none}.schalter.an{background:color-mix(in srgb,var(--primary-color) 22%,transparent);border-color:var(--primary-color)}.schalter.an>ha-icon{color:var(--primary-color)}.schalter span{flex:1}.schalter b{display:block;font-size:15px}.schalter small{display:block;font-size:12.5px;color:var(--secondary-text-color);font-weight:500;margin-top:2px}'; }
    getCardSize() { return 9; }
    _tvs() {
      const h = this._h;
      return Object.values(h.entities || {}).filter(e => e && e.entity_id.startsWith('media_player.') && TV_ART[e.platform] && !e.hidden && !e.disabled_by)
        .map(e => e.entity_id).sort((a, b) => this._name(a).localeCompare(this._name(b)));
    }
    _name(id) { const s = st(this._h, id); return (s && s.attributes.friendly_name) || id; }
    _zeichnen() {
      if (this._fehlt()) return;
      const h = this._h, tv = tvInfo(h), gew = this._gew || tv.geraete || [], alle = this._tvs();
      if (this._gew && JSON.stringify(this._gew) === JSON.stringify(tv.geraete)) this._gew = null;
      const auto = this._auto != null ? this._auto : tv.auto;
      if (this._auto != null && this._auto === tv.auto) this._auto = null;
      this._kopf(t('tv_title'), gew.length ? gew.map(id => this._name(id)).join(', ') : t('tv_sub_none'));
      let s = '<button class="tvbild" data-act="oeffnen" title="' + t('tv_open') + '"><iframe tabindex="-1" loading="lazy" src="' + esc(tv.url ? new URL(tv.url).pathname : '') + '"></iframe></button>' +
        '<div class="zwei"><button class="start" data-act="zeigen"' + (gew.length ? '' : ' disabled') + '><ha-icon icon="mdi:television-play"></ha-icon>' + t('tv_show') + '</button>' +
        '<button class="stop feld" data-act="stop"' + (gew.length ? '' : ' disabled') + ' title="' + t('tv_stop') + '"><ha-icon icon="mdi:television-off"></ha-icon></button></div>' +
        '<div class="titel"><ha-icon icon="mdi:television"></ha-icon>' + t('tv_pick') + '</div>';
      if (!alle.length) s += '<div class="ohne feld">' + t('tv_none') + '<ul><li>' + t('tv_firetv') + '</li><li>' + t('tv_gtv') + '</li><li>' + t('tv_cc') + '</li></ul></div>';
      alle.forEach(id => {
        const an = gew.includes(id), z = zst(h, id), e = h.entities[id];
        s += '<button class="wahl feld' + (an ? ' an' : '') + '" data-act="geraet" data-id="' + id + '"><ha-icon icon="' + (an ? 'mdi:checkbox-marked-circle' : 'mdi:checkbox-blank-circle-outline') + '"></ha-icon><span><b>' + esc(this._name(id)) + '</b><small>' + TV_ART[e.platform] + '</small></span>' +
          '<i class="pk' + (z && z !== 'off' && z !== 'unavailable' && z !== 'standby' ? ' on' : '') + '"></i></button>';
      });
      const br = this._brett != null ? this._brett : !!tv.brett, an = this._tvAns || tv.ansicht || 'camera_1';
      if (this._brett != null && this._brett === !!tv.brett) this._brett = null;
      if (this._tvAns && this._tvAns === tv.ansicht) this._tvAns = null;
      s += '<button class="schalter feld' + (auto ? ' an' : '') + '" data-act="auto"' + (gew.length ? '' : ' disabled') + '><ha-icon icon="' + (auto ? 'mdi:toggle-switch' : 'mdi:toggle-switch-off-outline') + '"></ha-icon><span><b>' + t('tv_auto') + '</b><small>' + t('tv_auto_s') + '</small></span></button>' +
        '<button class="schalter feld' + (br ? ' an' : '') + '" data-act="brett"><ha-icon icon="' + (br ? 'mdi:toggle-switch' : 'mdi:toggle-switch-off-outline') + '"></ha-icon><span><b>' + t('tv_board') + '</b><small>' + t('tv_board_s') + '</small></span></button>' +
        (br ? '<div class="ansicht">' + [['graphic', 'mdi:bullseye', t('tv_v_g')], ['camera_1', 'mdi:cctv', t('tv_v_c', { n: 1 })], ['camera_2', 'mdi:cctv', t('tv_v_c', { n: 2 })], ['camera_3', 'mdi:cctv', t('tv_v_c', { n: 3 })]]
          .map(([v, ic, x]) => '<button class="feld' + (v === an ? ' an' : '') + '" data-act="ansicht" data-v="' + v + '"><ha-icon icon="' + ic + '"></ha-icon>' + x + '</button>').join('') + '</div><div class="klein">' + t('tv_v_hint') + '</div>' : '') +
        '<div class="titel"><ha-icon icon="mdi:link-variant"></ha-icon>' + t('tv_link') + '</div>' +
        '<div class="link feld"><code>' + esc(tv.url) + '</code><button class="feld" data-act="kopie"><ha-icon icon="mdi:content-copy"></ha-icon>' + t('tv_copy') + '</button></div>' +
        '<button class="neuer feld" data-act="neu" data-lbl="' + t('tv_new') + '"><ha-icon icon="mdi:link-variant-off" style="--mdc-icon-size:16px"></ha-icon><span class="lbl">' + t('tv_new') + '</span></button>' +
        '<div class="klein">' + t('tv_hint') + '</div>' +
        '<div class="titel"><ha-icon icon="mdi:broadcast"></ha-icon>' + t('ov_title') + '</div>' +
        '<div class="link feld"><code>' + esc(tv.url ? tv.url + '/overlay' : '') + '</code><button class="feld" data-act="kopie" data-ov="1"><ha-icon icon="mdi:content-copy"></ha-icon>' + t('tv_copy') + '</button></div>' +
        '<div class="klein">' + t('ov_hint') + '</div>';
      this._setze(s);
      const f = this._r.querySelector('.tvbild iframe'), b = this._r.querySelector('.tvbild');
      if (f && b) { const w = b.clientWidth || 400; f.style.transform = 'scale(' + (w / 1280) + ')'; if (!this._ro && 'ResizeObserver' in window) { this._ro = new ResizeObserver(() => { const i = this._r.querySelector('.tvbild iframe'), bb = this._r.querySelector('.tvbild'); if (i && bb) i.style.transform = 'scale(' + (bb.clientWidth / 1280) + ')'; }); this._ro.observe(b); } }
    }
    _setzen(daten) { return this._h.callService('autodarts', 'fernseher_setzen', daten).catch(e => meldung(this, (e && e.message) || String(e))); }
    _klick(act, b) {
      const h = this._h, tv = tvInfo(h), gew = this._gew || tv.geraete || [];
      if (act === 'zeigen') { tvZeigen(this, h); return; }
      if (act === 'stop') { h.callService('autodarts', 'fernseher_beenden', {}).catch(e => meldung(this, (e && e.message) || String(e))); return; }
      if (act === 'geraet') { const id = b.dataset.id; this._gew = gew.includes(id) ? gew.filter(x => x !== id) : gew.concat(id); this._alt = null; this._zeichnen(); this._setzen({ geraete: this._gew }); return; }
      if (act === 'auto') { this._auto = !(this._auto != null ? this._auto : tv.auto); this._alt = null; this._zeichnen(); this._setzen({ auto: this._auto }); return; }
      if (act === 'brett') { this._brett = !(this._brett != null ? this._brett : !!tv.brett); this._alt = null; this._zeichnen(); this._setzen({ brett: this._brett }); return; }
      if (act === 'ansicht') { this._tvAns = b.dataset.v; this._alt = null; this._zeichnen(); this._setzen({ ansicht: this._tvAns }); return; }
      if (act === 'oeffnen') { if (tv.url) window.open(new URL(tv.url).pathname, '_blank', 'noopener'); return; }
      if (act === 'kopie') {
        const fertig = () => meldung(this, t('tv_copied')), url = tv.url + (b.dataset.ov ? '/overlay' : '');
        if (navigator.clipboard && window.isSecureContext) navigator.clipboard.writeText(url).then(fertig, () => window.prompt('', url));
        else window.prompt('', url);
        return;
      }
      if (act === 'neu') zweimal(this, b, t('tv_new_q'), () => { this._setzen({ neuer_link: true }); });
    }
  }
  customElements.define('autodarts-tv-card', AutodartsTvCard);

  /* ---------- Highlights card: clips of 180, high finish, match dart ---------- */
  Object.assign(TEXTE.en, { clips_title: 'Highlights', d_clips: 'Short videos of your 180s, high finishes and match darts from the board camera', clips_on: 'Record highlights', clips_on_s: 'At a highlight the last seconds of the board camera are saved as a short video',
    clips_cam: 'Camera', clips_when: 'When', clips_replay: 'Replay on the TV and the overlay', clips_replay_s: 'Right after the highlight, once', clips_none: 'No clips yet – throw a 180!', clips_off_s: 'off', n_clips: '{n} clips',
    clips_del: 'Delete', clips_del_q: 'Really delete?', clips_all: 'Delete all clips', clips_all_q: 'Delete all clips – sure?', clips_dl: 'Download', clips_save: 'Save clip', clips_saved: 'Clip is being saved',
    clips_hint: 'Clips are recorded while a game runs and the board detects darts. They are straightened with the calibration and kept in Media → dartnest/clips; the oldest go when there are more than {n}.',
    a_one_eighty: '180', a_high_finish: 'Finish 100+', a_match_won: 'Match dart', a_leg_won: 'Leg won', a_nine_darter: 'Nine-darter', a_ton_forty: '140+', a_checkout: 'Every finish', a_bullseye: 'Bullseye', a_three_in_a_bed: 'Three in a bed', a_manual: 'Saved by hand',
    today: 'today', yesterday: 'yesterday', m_clips_s: '180, high finishes, match darts as video', ov_title: 'Stream overlay (OBS, Streamlabs)', ov_hint: 'In OBS or Streamlabs add a source → Browser, paste the link, size 1920 × 1080. The background is see-through: only the score at the bottom left and the replays show.' });
  Object.assign(TEXTE.de, { clips_title: 'Highlights', d_clips: 'Kurze Videos deiner 180er, hohen Finishes und Matchdarts aus der Board-Kamera', clips_on: 'Highlights aufnehmen', clips_on_s: 'Bei einem Highlight werden die letzten Sekunden der Board-Kamera als kurzes Video gespeichert',
    clips_cam: 'Kamera', clips_when: 'Wann', clips_replay: 'Wiederholung auf Fernseher und Overlay', clips_replay_s: 'Direkt nach dem Highlight, einmal', clips_none: 'Noch keine Clips – wirf eine 180!', clips_off_s: 'aus', n_clips: '{n} Clips',
    clips_del: 'Löschen', clips_del_q: 'Wirklich löschen?', clips_all: 'Alle Clips löschen', clips_all_q: 'Alle Clips löschen – sicher?', clips_dl: 'Herunterladen', clips_save: 'Clip speichern', clips_saved: 'Clip wird gespeichert',
    clips_hint: 'Aufgenommen wird während eines Spiels, solange das Board Darts erkennt. Die Clips sind mit der Kalibrierung gerade gerückt und liegen unter Medien → dartnest/clips; über {n} Stück gehen die ältesten.',
    a_one_eighty: '180', a_high_finish: 'Finish ab 100', a_match_won: 'Matchdart', a_leg_won: 'Leg gewonnen', a_nine_darter: '9-Darter', a_ton_forty: 'Ab 140', a_checkout: 'Jedes Finish', a_bullseye: 'Bullseye', a_three_in_a_bed: 'Drei in einem Feld', a_manual: 'Von Hand gespeichert',
    today: 'heute', yesterday: 'gestern', m_clips_s: '180er, hohe Finishes, Matchdarts als Video', ov_title: 'Stream-Overlay (OBS, Streamlabs)', ov_hint: 'In OBS oder Streamlabs eine Quelle → Browser hinzufügen, Link einfügen, Größe 1920 × 1080. Der Hintergrund ist durchsichtig: zu sehen sind nur der Spielstand unten links und die Wiederholungen.' });
  const CLIP_ANLAESSE = ['one_eighty', 'high_finish', 'match_won', 'leg_won', 'nine_darter', 'ton_forty', 'checkout', 'bullseye', 'three_in_a_bed'];
  const clipsInfo = h => att(h, E(h, 'sensor.players')).clips || { an: false, kamera: 'camera_1', anlaesse: [], anzahl: 30, wiederholung: true, liste: [] };
  // signed links for <img>/<video> (they cannot send the login)
  const signiert = {};
  const signieren = (h, pfad, fertig) => {
    if (signiert[pfad]) return signiert[pfad] === 1 ? '' : signiert[pfad];
    signiert[pfad] = 1;
    h.callWS({ type: 'auth/sign_path', path: pfad, expires: 86400 }).then(r => { signiert[pfad] = r.path; fertig(); }, () => { delete signiert[pfad]; });
    return '';
  };
  const clipZeit = z => {
    const d = new Date(z); if (isNaN(d)) return '';
    const heute = new Date(), gestern = new Date(Date.now() - 864e5), uhr = d.toLocaleTimeString(SPR === 'de' ? 'de-DE' : 'en-GB', { hour: '2-digit', minute: '2-digit' });
    if (d.toDateString() === heute.toDateString()) return t('today') + ' ' + uhr;
    if (d.toDateString() === gestern.toDateString()) return t('yesterday') + ' ' + uhr;
    return d.toLocaleDateString(SPR === 'de' ? 'de-DE' : 'en-GB', { day: 'numeric', month: 'short' }) + ' ' + uhr;
  };
  const clipName = c => t('a_' + c.art) + (c.wert && c.art !== 'one_eighty' ? ' · ' + c.wert : '');
  const CLIPS_CSS = `
.clips{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px;margin-top:4px}
.clip{position:relative;display:block;padding:0;border-radius:16px;overflow:hidden;aspect-ratio:1;background:#111;border:0;cursor:pointer;text-align:left}
.clip img{width:100%;height:100%;object-fit:cover;display:block}
.clip .cl{position:absolute;left:0;right:0;bottom:0;padding:22px 10px 8px;background:linear-gradient(transparent,rgba(0,0,0,.85));color:#fff}
.clip .cl b{display:block;font-size:14px}.clip .cl small{font-size:11.5px;opacity:.8}
.clip .ab{position:absolute;left:8px;top:8px;border-radius:999px;padding:3px 9px;font-size:12px;font-weight:800;background:linear-gradient(90deg,#ff8a3d,#ff4d5e);color:#fff}
.clip .pl{position:absolute;right:8px;top:8px;width:28px;height:28px;border-radius:50%;background:rgba(0,0,0,.55);display:flex;align-items:center;justify-content:center;color:#fff}.clip .pl ha-icon{--mdc-icon-size:18px}
.seg{display:grid;grid-template-columns:repeat(3,1fr);gap:6px}
.seg button{border-radius:14px;padding:10px 4px;font-size:13px;font-weight:700}
.seg button.an,.chips button.an{border-color:var(--primary-color);background:color-mix(in srgb,var(--primary-color) 16%,transparent)}
.chips{display:flex;flex-wrap:wrap;gap:6px}
.chips button{border-radius:999px;padding:8px 13px;font-size:13px;font-weight:700;display:inline-flex;align-items:center;gap:6px}.chips button ha-icon{--mdc-icon-size:16px}
.spieler video{display:block;width:100%;max-height:70vh;aspect-ratio:1;object-fit:contain;background:#000;border-radius:16px}
.spieler .zl{display:flex;gap:8px;margin-top:10px;flex-wrap:wrap}.spieler .zl>*{display:inline-flex;align-items:center;gap:6px;border-radius:12px;padding:9px 13px;font-size:13.5px;font-weight:700;text-decoration:none;color:inherit}
.neuer{display:inline-flex;align-items:center;gap:6px;border-radius:12px;padding:8px 12px;margin-top:12px;font-size:13px;font-weight:600}
.spieler h3{margin:0 0 8px;font-size:17px}.spieler h3 small{display:block;font-size:12.5px;color:var(--secondary-text-color);font-weight:500;margin-top:2px}`;
  class AutodartsClipsCard extends DartsSeite {
    static get CSS() { return CLIPS_CSS + '.schalter{display:flex;align-items:center;gap:12px;border-radius:18px;padding:14px 16px;width:100%;box-sizing:border-box;text-align:left;margin-top:8px}.schalter>ha-icon{--mdc-icon-size:28px;flex:none}.schalter.an{background:color-mix(in srgb,var(--primary-color) 22%,transparent);border-color:var(--primary-color)}.schalter.an>ha-icon{color:var(--primary-color)}.schalter span{flex:1}.schalter b{display:block;font-size:15px}.schalter small{display:block;font-size:12.5px;color:var(--secondary-text-color);font-weight:500;margin-top:2px}'; }
    getCardSize() { return 8; }
    _w() { return Object.assign({}, clipsInfo(this._h), this._neu || {}); }
    _zeichnen() {
      if (this._fehlt()) return;
      const h = this._h, c = this._w(), echt = clipsInfo(h);
      if (this._neu && Object.keys(this._neu).every(k => JSON.stringify(this._neu[k]) === JSON.stringify(echt[k]))) this._neu = null;
      const liste = c.liste || [];
      this._kopf(t('clips_title'), c.an ? t('n_clips', { n: liste.length }) : t('clips_off_s'));
      const neu = () => { this._alt = null; this._zeichnen(); };
      let s = '<button class="schalter feld' + (c.an ? ' an' : '') + '" data-act="an"><ha-icon icon="' + (c.an ? 'mdi:toggle-switch' : 'mdi:toggle-switch-off-outline') + '"></ha-icon><span><b>' + t('clips_on') + '</b><small>' + t('clips_on_s') + '</small></span></button>';
      if (c.an) {
        s += '<div class="titel"><ha-icon icon="mdi:cctv"></ha-icon>' + t('clips_cam') + '</div><div class="seg">' + ['camera_1', 'camera_2', 'camera_3'].map((k, i) => '<button class="feld' + (c.kamera === k ? ' an' : '') + '" data-act="kamera" data-v="' + k + '">' + t('tv_v_c', { n: i + 1 }) + '</button>').join('') + '</div>' +
          '<div class="titel"><ha-icon icon="mdi:star-outline"></ha-icon>' + t('clips_when') + '</div><div class="chips">' + CLIP_ANLAESSE.map(a => { const an = (c.anlaesse || []).includes(a); return '<button class="feld' + (an ? ' an' : '') + '" data-act="anlass" data-v="' + a + '"><ha-icon icon="' + (an ? 'mdi:check' : 'mdi:plus') + '"></ha-icon>' + t('a_' + a) + '</button>'; }).join('') + '</div>' +
          '<button class="schalter feld' + (c.wiederholung ? ' an' : '') + '" data-act="wdh"><ha-icon icon="' + (c.wiederholung ? 'mdi:toggle-switch' : 'mdi:toggle-switch-off-outline') + '"></ha-icon><span><b>' + t('clips_replay') + '</b><small>' + t('clips_replay_s') + '</small></span></button>';
      }
      s += '<div class="titel"><ha-icon icon="mdi:movie-star-outline"></ha-icon>' + t('clips_title') + '</div>';
      if (!liste.length) s += '<div class="leer">' + t('clips_none') + '</div>';
      else s += '<div class="clips">' + liste.map(x => {
        const bild = signieren(h, '/api/autodarts/clip/' + x.id + '.jpg', neu);
        return '<button class="clip" data-act="zeigen" data-id="' + x.id + '">' + (bild ? '<img loading="lazy" alt="" src="' + esc(bild) + '">' : '') +
          '<span class="ab">' + esc(t('a_' + x.art)) + '</span><span class="pl"><ha-icon icon="mdi:play"></ha-icon></span><span class="cl"><b>' + esc(x.spieler || clipName(x)) + '</b><small>' + esc((x.spieler ? clipName(x) + ' · ' : '') + clipZeit(x.zeit)) + '</small></span></button>';
      }).join('') + '</div>' +
        '<button class="neuer feld" data-act="alle" data-lbl="' + t('clips_all') + '" style="--sr-f:var(--red-color,#e53935)"><ha-icon icon="mdi:delete-sweep-outline" style="--mdc-icon-size:16px"></ha-icon><span class="lbl">' + t('clips_all') + '</span></button>';
      s += '<div class="klein">' + t('clips_hint', { n: c.anzahl || 30 }) + '</div>';
      this._setze(s);
    }
    _setzen(daten) {
      this._neu = Object.assign(this._neu || {}, daten); this._alt = null; this._zeichnen();
      this._h.callService('autodarts', 'clips_setzen', daten).catch(e => { this._neu = null; meldung(this, (e && e.message) || String(e)); this._alt = null; this._zeichnen(); });
    }
    _klick(act, b) {
      const h = this._h, c = this._w();
      if (act === 'an') return this._setzen({ an: !c.an });
      if (act === 'wdh') return this._setzen({ wiederholung: !c.wiederholung });
      if (act === 'kamera') return this._setzen({ kamera: b.dataset.v });
      if (act === 'anlass') { const v = b.dataset.v, l = c.anlaesse || []; return this._setzen({ anlaesse: l.includes(v) ? l.filter(x => x !== v) : CLIP_ANLAESSE.filter(x => x === v || l.includes(x)) }); }
      if (act === 'alle') { zweimal(this, b, t('clips_all_q'), () => h.callService('autodarts', 'clip_loeschen', { alle: true })); return; }
      if (act === 'zeigen') {
        const x = (c.liste || []).find(y => y.id === b.dataset.id); if (!x) return;
        h.callWS({ type: 'auth/sign_path', path: '/api/autodarts/clip/' + x.id + '.mp4', expires: 3600 }).then(r => {
          this._modal('<div class="spieler"><h3>' + esc(x.spieler || clipName(x)) + '<small>' + esc((x.spieler ? clipName(x) + ' · ' : '') + clipZeit(x.zeit)) + '</small></h3><video controls autoplay playsinline muted src="' + esc(r.path) + '"></video>' +
            '<div class="zl"><a class="feld" href="' + esc(r.path) + '" download="dartnest-' + x.id + '.mp4"><ha-icon icon="mdi:download"></ha-icon>' + t('clips_dl') + '</a>' +
            '<button class="feld" data-act="weg" data-id="' + x.id + '" data-lbl="' + t('clips_del') + '"><ha-icon icon="mdi:delete-outline"></ha-icon><span class="lbl">' + t('clips_del') + '</span></button>' +
            '<button class="feld" data-act="mzu"><ha-icon icon="mdi:close"></ha-icon>' + t('close') + '</button></div></div>');
        }, e => meldung(this, (e && e.message) || String(e)));
        return;
      }
      if (act === 'weg') { zweimal(this, b, t('clips_del_q'), () => { h.callService('autodarts', 'clip_loeschen', { id: b.dataset.id }); this._modal(null); }); }
    }
  }
  customElements.define('autodarts-clips-card', AutodartsClipsCard);

  /* ---------- Pixel displays (AWTRIX 3, PixelIt): score and effects on a small LED matrix ---------- */
  Object.assign(TEXTE.en, { pixel_title: 'Pixel display', d_pixel: 'Score and effects on AWTRIX 3 and PixelIt LED displays', m_pixel_s: 'AWTRIX 3, PixelIt: score on the LED clock',
    pixel_on: 'Show the score', pixel_on_s: 'Name and rest of the player at the oche, while a game runs', pixel_fx: 'Effects', pixel_fx_s: '180, checkout, bust, leg and the winner flash on the display',
    pixel_devs: 'Displays', pixel_none: 'No display yet. Add one with its IP address.', pixel_add: 'Add display', pixel_addr: 'IP address of the display', pixel_find: 'Find',
    pixel_add_s: 'The address is shown on the display when it starts (AWTRIX: in the menu under Network), or in your router. DartNest finds out by itself whether it is an AWTRIX 3 or a PixelIt.',
    pixel_found: '{name} added – it says DARTNEST now', pixel_test: 'Test', pixel_test_ok: 'Sent – the display says hello', pixel_del: 'Remove', pixel_del_q: 'Tap again to remove',
    pixel_live: 'Preview', pixel_idle: 'No game: the display shows its own apps or the clock', pixel_off_s: 'off', n_pixel: '{n} displays', n_pixel1: '1 display', pixel_online: 'online', pixel_offline: 'not reachable',
    pixel_hint: 'Works with AWTRIX 3 (Ulanzi TC001 and self-built ones) and PixelIt in your home network, no cloud and no extra add-on. While a game runs DartNest shows its own app; afterwards the display goes back to what it showed before.' });
  Object.assign(TEXTE.de, { pixel_title: 'Pixel-Anzeige', d_pixel: 'Spielstand und Effekte auf AWTRIX-3- und PixelIt-LED-Anzeigen', m_pixel_s: 'AWTRIX 3, PixelIt: Spielstand auf der LED-Uhr',
    pixel_on: 'Spielstand zeigen', pixel_on_s: 'Name und Rest des Spielers am Oche, während ein Spiel läuft', pixel_fx: 'Effekte', pixel_fx_s: '180, Checkout, Bust, Leg und der Sieger blinken auf der Anzeige',
    pixel_devs: 'Anzeigen', pixel_none: 'Noch keine Anzeige. Füge eine mit ihrer IP-Adresse hinzu.', pixel_add: 'Anzeige hinzufügen', pixel_addr: 'IP-Adresse der Anzeige', pixel_find: 'Suchen',
    pixel_add_s: 'Die Adresse zeigt die Anzeige beim Start (AWTRIX: im Menü unter Network) oder dein Router. DartNest erkennt selbst, ob es eine AWTRIX 3 oder eine PixelIt ist.',
    pixel_found: '{name} hinzugefügt – sie zeigt jetzt DARTNEST', pixel_test: 'Test', pixel_test_ok: 'Gesendet – die Anzeige grüßt', pixel_del: 'Entfernen', pixel_del_q: 'Zum Entfernen nochmal tippen',
    pixel_live: 'Vorschau', pixel_idle: 'Kein Spiel: die Anzeige zeigt ihre eigenen Apps oder die Uhr', pixel_off_s: 'aus', n_pixel: '{n} Anzeigen', n_pixel1: '1 Anzeige', pixel_online: 'online', pixel_offline: 'nicht erreichbar',
    pixel_hint: 'Geht mit AWTRIX 3 (Ulanzi TC001 und Eigenbau) und PixelIt im Heimnetz, ohne Cloud und ohne Zusatz-App. Während eines Spiels zeigt DartNest seine eigene App; danach zeigt die Anzeige wieder, was sie vorher zeigte.' });
  const pixelInfo = h => att(h, E(h, 'sensor.players')).pixel || { an: true, effekte: true, geraete: [], vorschau: null };
  // 3×5 pixel font like the small LED clocks
  const PIXEL_FONT = { A: '111101111101101', B: '110101110101110', C: '011100100100011', D: '110101101101110', E: '111100110100111', F: '111100110100100', G: '011100101101011',
    H: '101101111101101', I: '111010010010111', J: '001001001101010', K: '101101110101101', L: '100100100100111', M: '101111111101101', N: '110101101101101', O: '010101101101010',
    P: '110101110100100', Q: '010101101110011', R: '110101110101101', S: '011100010001110', T: '111010010010010', U: '101101101101111', V: '101101101101010', W: '101101111111101',
    X: '101101010101101', Y: '101101010010010', Z: '111001010100111', 0: '111101101101111', 1: '010110010010111', 2: '110001010100111', 3: '110001010001110', 4: '101101111001001',
    5: '111100110001110', 6: '011100111101111', 7: '111001010010010', 8: '111101111101111', 9: '111101111001110', '-': '000000111000000', '!': '010010010000010', '.': '000000000000010',
    ':': '000010000010000', "'": '010010000000000', '/': '001001010100100', '?': '110001010000010', '+': '000010111010000' };
  function pixelSvg(teile) {
    // the text as lit dots on a 32 × 8 matrix; longer texts scroll like on the display
    const an = [];
    let x = 0;
    (teile || []).forEach(p => {
      for (const roh of String(p.t || '').toUpperCase()) {
        const z = ({ 'Ä': 'A', 'Ö': 'O', 'Ü': 'U' })[roh] || roh;
        if (z === ' ') { x += 2; continue; }
        const g = PIXEL_FONT[z] || PIXEL_FONT['?'];
        for (let i = 0; i < 15; i++) if (g[i] === '1') an.push([x + i % 3, 1 + Math.floor(i / 3), p.c || '#fff']);
        x += 4;
      }
    });
    const breite = Math.max(0, x - 1), lauf = breite > 32, w = lauf ? breite + 34 : 32, dx = lauf ? 32 : Math.floor((32 - breite) / 2);
    let punkte = '';
    for (let yy = 0; yy < 8; yy++) for (let xx = 0; xx < 32; xx++) punkte += '<circle cx="' + (xx + .5) + '" cy="' + (yy + .5) + '" r=".36" fill="#1d1f24"/>';
    const leuchten = an.map(([px, py, c]) => '<circle cx="' + (px + dx + .5) + '" cy="' + (py + .5) + '" r=".4" fill="' + c + '"/>').join('');
    return '<svg class="mx" viewBox="0 0 32 8" preserveAspectRatio="xMidYMid meet" aria-hidden="true">' + punkte +
      '<g class="lt"' + (lauf ? ' style="--w:' + w + ';animation-duration:' + (w * 0.09).toFixed(1) + 's"' : '') + '>' + leuchten + '</g></svg>';
  }
  const PIXEL_CSS = `
.matrix{border-radius:18px;background:#0b0c0f;padding:14px 14px 10px;box-shadow:inset 0 0 0 1px rgba(255,255,255,.06)}
.mx{display:block;width:100%;height:auto;overflow:hidden}
.mx .lt{filter:drop-shadow(0 0 .35px currentColor)}
.mx .lt[style]{animation:pxlauf linear infinite}
@keyframes pxlauf{from{transform:translateX(0)}to{transform:translateX(calc(var(--w) * -1px))}}
.matrix small{display:block;color:#9a9ea7;font-size:12px;margin-top:8px;text-align:center}
.pg{display:flex;flex-wrap:wrap;align-items:center;gap:8px 12px;border-radius:16px;padding:12px;margin-top:8px}
.pg .pk{flex:1 0 100%;display:flex;gap:8px;justify-content:flex-end}
.pg>ha-icon{--mdc-icon-size:26px;color:#29b6f6;flex:none}
.pg>span:not(.pk){flex:1;min-width:0}.pg b{display:block;font-size:14.5px}.pg small{display:block;font-size:12px;color:var(--secondary-text-color);margin-top:2px}
.pg i{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:5px;background:var(--disabled-color,#9e9e9e)}
.pg i.ok{background:var(--green-color,#43a047)}.pg i.weg{background:var(--red-color,#e53935)}
.pg button{display:inline-flex;align-items:center;gap:5px;border-radius:12px;padding:7px 10px;font-size:12.5px;font-weight:600;flex:none}
.pg button ha-icon{--mdc-icon-size:16px}
.mbox p{font-size:13px;color:var(--secondary-text-color);line-height:1.45;margin:8px 0 0}
.mbox p.fehler{color:var(--error-color,#db4437);font-weight:600}.mbox p.fehler:empty{display:none}`;
  class AutodartsPixelCard extends DartsSeite {
    static get CSS() { return PIXEL_CSS + '.schalter{display:flex;align-items:center;gap:12px;border-radius:18px;padding:14px 16px;width:100%;box-sizing:border-box;text-align:left;margin-top:8px}.schalter>ha-icon{--mdc-icon-size:28px;flex:none}.schalter.an{background:color-mix(in srgb,var(--primary-color) 22%,transparent);border-color:var(--primary-color)}.schalter.an>ha-icon{color:var(--primary-color)}.schalter span{flex:1}.schalter b{display:block;font-size:15px}.schalter small{display:block;font-size:12.5px;color:var(--secondary-text-color);font-weight:500;margin-top:2px}.neuer{display:inline-flex;align-items:center;gap:6px;border-radius:12px;padding:8px 12px;margin-top:10px;font-size:13px;font-weight:600}'; }
    getCardSize() { return 6; }
    _w() { return Object.assign({}, pixelInfo(this._h), this._neu || {}); }
    _zeichnen() {
      if (this._fehlt()) return;
      const p = this._w(), echt = pixelInfo(this._h), g = p.geraete || [];
      if (this._neu && Object.keys(this._neu).every(k => this._neu[k] === echt[k])) this._neu = null;
      this._kopf(t('pixel_title'), !g.length ? t('pixel_add') : p.an ? (g.length === 1 ? t('n_pixel1') : t('n_pixel', { n: g.length })) : t('pixel_off_s'));
      const jetzt = p.an && p.vorschau;
      let s = '<div class="titel"><ha-icon icon="mdi:dots-grid"></ha-icon>' + t('pixel_live') + '</div><div class="matrix">' +
        pixelSvg(jetzt ? p.vorschau : [{ t: new Date().toTimeString().slice(0, 5), c: '#8e8e93' }]) + (jetzt ? '' : '<small>' + t('pixel_idle') + '</small>') + '</div>';
      s += '<button class="schalter feld' + (p.an ? ' an' : '') + '" data-act="an"><ha-icon icon="' + (p.an ? 'mdi:toggle-switch' : 'mdi:toggle-switch-off-outline') + '"></ha-icon><span><b>' + t('pixel_on') + '</b><small>' + t('pixel_on_s') + '</small></span></button>' +
        '<button class="schalter feld' + (p.effekte ? ' an' : '') + '" data-act="fx"><ha-icon icon="' + (p.effekte ? 'mdi:toggle-switch' : 'mdi:toggle-switch-off-outline') + '"></ha-icon><span><b>' + t('pixel_fx') + '</b><small>' + t('pixel_fx_s') + '</small></span></button>';
      s += '<div class="titel"><ha-icon icon="mdi:led-strip-variant"></ha-icon>' + t('pixel_devs') + '</div>';
      if (!g.length) s += '<div class="leer">' + t('pixel_none') + '</div>';
      s += g.map(d => '<div class="pg feld"><ha-icon icon="mdi:dots-grid"></ha-icon><span><b>' + esc(d.name || d.host) + '</b><small><i class="' + (d.online === true ? 'ok' : d.online === false ? 'weg' : '') + '"></i>' + esc(d.host) +
        (d.online === false ? ' · ' + t('pixel_offline') : d.online ? ' · ' + t('pixel_online') : '') + (d.version ? ' · v' + esc(d.version) : '') + '</small></span>' +
        '<span class="pk"><button class="feld" data-act="test" data-h="' + esc(d.host) + '"><ha-icon icon="mdi:message-flash-outline"></ha-icon>' + t('pixel_test') + '</button>' +
        '<button class="feld" data-act="weg" data-h="' + esc(d.host) + '" data-lbl="' + t('pixel_del') + '" style="--sr-f:var(--red-color,#e53935)"><ha-icon icon="mdi:delete-outline"></ha-icon><span class="lbl">' + t('pixel_del') + '</span></button></span></div>').join('');
      s += '<button class="neuer feld" data-act="neu"><ha-icon icon="mdi:plus" style="--mdc-icon-size:16px"></ha-icon>' + t('pixel_add') + '</button>';
      s += '<div class="klein">' + t('pixel_hint') + '</div>';
      this._setze(s);
    }
    _setzen(daten) {
      this._neu = Object.assign(this._neu || {}, daten); this._alt = null; this._zeichnen();
      this._h.callService('autodarts', 'pixel_setzen', daten).catch(e => { this._neu = null; meldung(this, (e && e.message) || String(e)); this._alt = null; this._zeichnen(); });
    }
    _klick(act, b) {
      const h = this._h, p = this._w();
      if (act === 'an') return this._setzen({ an: !p.an });
      if (act === 'fx') return this._setzen({ effekte: !p.effekte });
      if (act === 'test') { h.callService('autodarts', 'pixel_testen', { adresse: b.dataset.h }).then(() => meldung(this, t('pixel_test_ok')), e => meldung(this, (e && e.message) || String(e))); return; }
      if (act === 'weg') { zweimal(this, b, t('pixel_del_q'), () => h.callService('autodarts', 'pixel_entfernen', { adresse: b.dataset.h })); return; }
      if (act === 'neu') {
        this._modal('<h3>' + t('pixel_add') + '</h3><input inputmode="decimal" autocomplete="off" placeholder="' + t('pixel_addr') + ' · 192.168.178.50"><p class="fehler"></p><p>' + t('pixel_add_s') + '</p><div class="mknoepfe"><button class="feld" data-act="mzu">' + t('cancel') + '</button><button class="ja" data-act="neuok">' + t('pixel_find') + '</button></div>');
        this._r.querySelector('.modal input').addEventListener('keydown', e => { if (e.key === 'Enter') this._klick('neuok', {}); });
        return;
      }
      if (act === 'neuok') {
        const feld = this._r.querySelector('.modal input'), knopf = this._r.querySelector('.modal .ja'), adresse = ((feld || {}).value || '').trim();
        if (!adresse || (knopf && knopf.disabled)) return;
        if (knopf) { knopf.disabled = true; knopf.textContent = '…'; }
        const fz = this._r.querySelector('.modal .fehler'); if (fz) fz.textContent = '';
        h.callWS({ type: 'call_service', domain: 'autodarts', service: 'pixel_hinzufuegen', service_data: { adresse }, return_response: true })
          .then(r => { this._modal(null); meldung(this, t('pixel_found', { name: ((r && r.response) || {}).name || adresse })); },
            e => {
              if (knopf) { knopf.disabled = false; knopf.textContent = t('pixel_find'); }
              const f = this._r.querySelector('.modal .fehler'); if (f) f.textContent = ((e && e.message) || String(e)).replace(/^Validation error:\s*/, ''); else meldung(this, (e && e.message) || String(e));
            });
      }
    }
  }
  customElements.define('autodarts-pixel-card', AutodartsPixelCard);

  /* ---------- Settings card: one menu with big buttons, each opens the matching card ---------- */
  const MENUE = [
    ['board', 'autodarts-manager-card', 'mdi:camera-iris', 'm_board', 'm_board_s', '#26a69a'],
    ['licht', 'autodarts-lights-card', 'mdi:lightbulb-auto-outline', 'lights_title', 'm_lights_s', '#ffb300'],
    ['ansager', 'autodarts-caller-card', 'mdi:account-voice', 'caller_title', 'm_caller_s', '#7e57c2'],
    ['tv', 'autodarts-tv-card', 'mdi:television-play', 'tv_title', 'm_tv_s', '#ef5350'],
    ['clips', 'autodarts-clips-card', 'mdi:movie-star-outline', 'clips_title', 'm_clips_s', '#ec407a'],
    ['pixel', 'autodarts-pixel-card', 'mdi:dots-grid', 'pixel_title', 'm_pixel_s', '#29b6f6']
  ];
  const MENUE_CSS = `
.menue{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:10px}
.mk{display:flex;align-items:center;gap:14px;border-radius:20px;padding:16px;text-align:left;min-height:84px;box-sizing:border-box}
.mk .ic{width:48px;height:48px;border-radius:16px;display:flex;align-items:center;justify-content:center;flex:none;background:color-mix(in srgb,var(--mf) 20%,transparent);color:var(--mf)}
.mk .ic ha-icon{--mdc-icon-size:28px}
.mk span{flex:1;min-width:0}.mk b{display:block;font-size:16px}.mk small{display:block;font-size:12.5px;color:var(--secondary-text-color);margin-top:3px;line-height:1.35}
.mk .st{display:inline-block;font-style:normal;margin-top:5px;font-size:11.5px;font-weight:700;border-radius:999px;padding:2px 8px;background:color-mix(in srgb,var(--primary-text-color) 8%,transparent);color:var(--secondary-text-color)}
.mk .st.gut{background:color-mix(in srgb,var(--green-color,#43a047) 18%,transparent);color:var(--green-color,#43a047)}
.mk>ha-icon{--mdc-icon-size:22px;color:var(--secondary-text-color)}`;
  class AutodartsSettingsCard extends DartsSeite {
    static get CSS() { return MENUE_CSS; }
    getCardSize() { return 4; }
    setConfig(c) { super.setConfig(c); if (this._kind) { this._kind = null; this._wahl = null; } }
    _status(k) {
      const h = this._h;
      if (k === 'board') { const on = boardOnline(h); return ['<i class="st' + (on ? ' gut' : '') + '">' + t(on ? 'online' : 'offline') + '</i>', on]; }
      if (k === 'tv') { const n = (tvInfo(h).geraete || []).length; return n ? ['<i class="st gut">' + t('n_tv', { n }) + '</i>', true] : ['', false]; }
      if (k === 'pixel') { const p = pixelInfo(h), n = (p.geraete || []).length; return n ? ['<i class="st' + (p.an ? ' gut' : '') + '">' + (p.an ? (n === 1 ? t('n_pixel1') : t('n_pixel', { n })) : t('pixel_off_s')) + '</i>', p.an] : ['', false]; }
      if (k === 'clips') { const c = clipsInfo(h); return c.an ? ['<i class="st gut">' + t('n_clips', { n: (c.liste || []).length }) + '</i>', true] : ['<i class="st">' + t('clips_off_s') + '</i>', false]; }
      return ['', false];
    }
    _zeichnen() {
      if (this._kind) { this._kind.hass = this._h; return; }
      if (this._fehlt()) return;
      this._kopf(t('settings_title'), 'DartNest');
      this._setze('<div class="menue">' + MENUE.map(([k, , icon, ti, sub, f]) => '<button class="mk feld" data-act="menue" data-k="' + k + '" style="--mf:' + f + '"><span class="ic"><ha-icon icon="' + icon + '"></ha-icon></span><span><b>' + t(ti) + '</b><small>' + t(sub) + '</small>' + this._status(k)[0] + '</span><ha-icon icon="mdi:chevron-right"></ha-icon></button>').join('') + '</div>');
    }
    _klick(act, b) {
      if (act !== 'menue') return;
      const def = MENUE.find(x => x[0] === b.dataset.k);
      const k = document.createElement(def[1]);
      k.setConfig(Object.assign({}, this._c[def[0]] || {}, { back_button: true }));
      k._zurueck = () => this._menue();
      this._kind = k;
      this._r.querySelector('ha-card').style.display = 'none';
      this._r.appendChild(k);
      k.hass = this._h;
      try { k.scrollIntoView({ block: 'nearest' }); } catch (e) {}
    }
    _menue() {
      if (this._kind) { this._kind.remove(); this._kind = null; }
      this._r.querySelector('ha-card').style.display = '';
      this._alt = null; this._zeichnen();
    }
  }
  customElements.define('autodarts-settings-card', AutodartsSettingsCard);

  /* ---------- Sidebar panel "DartNest": all cards as tabs, no setup needed ---------- */
  const PANEL_TABS = [
    ['board', 'autodarts-overview-card', 'mdi:bullseye', 'tab_board'],
    ['spiel', 'autodarts-game-card', 'mdi:bullseye-arrow', 'play'],
    ['spieler', 'autodarts-players-card', 'mdi:account-group', 'players'],
    ['licht', 'autodarts-lights-card', 'mdi:lightbulb-auto-outline', 'lights_title'],
    ['ansager', 'autodarts-caller-card', 'mdi:account-voice', 'caller_title'],
    ['fernseher', 'autodarts-tv-card', 'mdi:television-play', 'tv_title'],
    ['highlights', 'autodarts-clips-card', 'mdi:movie-star-outline', 'clips_title'],
    ['pixel', 'autodarts-pixel-card', 'mdi:dots-grid', 'pixel_title'],
    ['manager', 'autodarts-manager-card', 'mdi:camera-iris', 'manager']
  ];
  const PANEL_CSS = `
:host{display:block;min-height:100vh;background:var(--primary-background-color);color:var(--primary-text-color)}
.leiste{position:sticky;top:0;z-index:4;display:flex;align-items:center;gap:4px;height:56px;padding:0 8px;box-sizing:border-box;
  background:var(--app-header-background-color,var(--primary-background-color));color:var(--app-header-text-color,var(--primary-text-color));border-bottom:1px solid var(--divider-color,rgba(127,127,127,.2))}
.leiste .name{font-size:20px;font-weight:500;margin:0 12px 0 4px;white-space:nowrap}
.tabs{display:flex;gap:4px;overflow-x:auto;scrollbar-width:none;flex:1;height:100%;align-items:stretch}
.tabs::-webkit-scrollbar{display:none}
.tabs button{font:inherit;color:inherit;background:none;border:none;cursor:pointer;display:flex;align-items:center;gap:8px;padding:0 14px;font-size:14px;font-weight:600;opacity:.72;border-bottom:3px solid transparent;white-space:nowrap;-webkit-tap-highlight-color:transparent}
.tabs button.an{opacity:1;border-bottom-color:var(--primary-color);color:var(--primary-color)}
.tabs ha-icon{--mdc-icon-size:20px}
.inhalt{max-width:1100px;margin:0 auto;padding:16px;box-sizing:border-box}
@media (max-width:640px){.leiste .name{display:none}.tabs button{padding:0 10px}.tabs button span{display:none}.tabs button.an span{display:inline}.inhalt{padding:8px}}`;
  class AutodartsPanel extends HTMLElement {
    set hass(h) { this._h = h; sprachePruefen(h); this._zeigen(); }
    set narrow(n) { this._narrow = n; if (this._menu) this._menu.narrow = n; }
    set route(r) { this._zeigen(); }
    set panel(p) {}
    connectedCallback() {
      if (!this._r) {
        this._r = this.attachShadow({ mode: 'open' });
        this._r.innerHTML = '<style>' + PANEL_CSS + '</style><div class="leiste"><ha-menu-button></ha-menu-button><span class="name">DartNest</span><div class="tabs"></div></div><div class="inhalt"></div>';
        this._menu = this._r.querySelector('ha-menu-button');
        this._r.querySelector('.tabs').addEventListener('click', e => { const b = e.target.closest('[data-tab]'); if (b) gehe('/' + this._basis() + '/' + b.dataset.tab); });
        this._ort = () => this._zeigen();
        this._karten = {};
      }
      window.addEventListener('location-changed', this._ort);
      window.addEventListener('popstate', this._ort);
      this._zeigen();
    }
    disconnectedCallback() { window.removeEventListener('location-changed', this._ort); window.removeEventListener('popstate', this._ort); }
    _basis() { return location.pathname.split('/')[1] || 'autodarts'; }
    _tab() { const t2 = location.pathname.split('/')[2]; return PANEL_TABS.some(x => x[0] === t2) ? t2 : 'board'; }
    _zeigen() {
      if (!this._r || !this._h) return;
      if (this._menu) { this._menu.hass = this._h; this._menu.narrow = this._narrow; }
      const tab = this._tab(), basis = '/' + this._basis() + '/';
      const tabs = PANEL_TABS.map(([k, , icon, txt]) => '<button data-tab="' + k + '" class="' + (k === tab ? 'an' : '') + '"><ha-icon icon="' + icon + '"></ha-icon><span>' + t(txt) + '</span></button>').join('');
      if (this._tabsAlt !== tabs) { this._tabsAlt = tabs; this._r.querySelector('.tabs').innerHTML = tabs; }
      let k = this._karten[tab];
      if (!k) {
        const def = PANEL_TABS.find(x => x[0] === tab);
        k = document.createElement(def[1]);
        k.setConfig(tab === 'board' ? { game_path: basis + 'spiel', manager_path: basis + 'manager', players_path: basis + 'spieler' } : { back_button: false });
        this._karten[tab] = k;
      }
      const box = this._r.querySelector('.inhalt');
      if (box.firstChild !== k) { box.innerHTML = ''; box.appendChild(k); }
      k.hass = this._h;  // only the visible card gets updates
    }
  }
  customElements.define('autodarts-panel', AutodartsPanel);

  SPR = sprache(document.querySelector('home-assistant') && document.querySelector('home-assistant').hass);
  window.customCards = window.customCards || [];
  window.customCards.push(
    { type: 'autodarts-overview-card', name: 'DartNest Overview', description: t('d_overview'), preview: true },
    { type: 'autodarts-tile-card', name: 'DartNest Tile', description: t('d_tile'), preview: true },
    { type: 'autodarts-game-card', name: 'DartNest Game', description: t('d_game') },
    { type: 'autodarts-manager-card', name: 'DartNest Board Manager', description: t('d_manager') },
    { type: 'autodarts-players-card', name: 'DartNest Players', description: t('d_players') },
    { type: 'autodarts-lights-card', name: 'DartNest Light effects', description: t('d_lights') },
    { type: 'autodarts-caller-card', name: 'DartNest Caller', description: t('d_caller') },
    { type: 'autodarts-tv-card', name: 'DartNest TV', description: t('d_tv') },
    { type: 'autodarts-settings-card', name: 'DartNest Settings', description: t('d_settings') },
    { type: 'autodarts-clips-card', name: 'DartNest Highlights', description: t('d_clips') },
    { type: 'autodarts-pixel-card', name: 'DartNest Pixel display', description: t('d_pixel') }
  );
  console.info('%c AUTODARTS CARDS %c loaded ', 'color:#fff;background:#00a37a;font-weight:700', 'color:#00a37a');
})();
