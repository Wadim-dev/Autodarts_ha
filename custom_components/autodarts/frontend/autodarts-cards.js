/* Autodarts cards for Home Assistant (shipped with the Autodarts integration, loaded automatically).
   custom:autodarts-overview-card  Board scene with live darts, optional power on/off, shortcuts
   custom:autodarts-game-card      Local X01 game: lobby, bull-off, match, result, corrections, caller
   custom:autodarts-manager-card   Board Manager: cameras with calibration grid, controls, system values, settings
   custom:autodarts-players-card   Players, overall statistics, recent games
   Entities are found automatically (platform "autodarts"), texts follow the HA language (English/German).
   Animations are CSS only and pause when the card is not visible; camera images load only while visible. */
(() => {
  if (customElements.get('autodarts-game-card')) return;

  /* ---------- texts ---------- */
  const TEXTE = {
    en: {
      dart: 'Dart', visit: 'Visit', on: 'Turn on', off: 'Turn off', off_q: 'Really turn off?', play: 'Play', manager: 'Board Manager', players: 'Players',
      sc_off: 'Board off', sc_starting: 'Starting …', sc_stopping: 'Shutting down …', sc_ready: 'Ready – throw!', sc_takeout: 'Remove darts', sc_calib: 'Calibrating …', sc_stopped: 'Detection stopped', sc_lost: 'Connection lost',
      dart_of: 'Dart {n} of 3 · {s} so far', visit_pts: 'Visit {s} points', pc_running: 'PC is running, Autodarts is starting', about_minute: 'Takes about a minute', plug_after: 'The plug switches off afterwards',
      plug_on: 'Plug on', ready_hint: 'Throw a dart to start', game_running: 'Game running', back: 'Back', missing: 'Autodarts integration not found',
      new_game: 'New game', game_over: 'Game over', darts: 'Darts', local: 'X01 – local in Home Assistant', cancel_game: 'Cancel game', caller: 'Caller', fullscreen: 'Full screen',
      nobody: 'Nobody yet – tap below.', of6: '{n} of 6', shuffle: 'Shuffle order', new_player: 'New player', bot: 'Bot', bot_level: 'Bot level (average)', average: 'Average',
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
      cam: 'Camera {n}', cams_off: 'Cameras off', graphic: 'graphic', tap_view: 'Tap: next camera / graphic', grid: 'Grid',
      first_leg: 'First to {n} leg', first_legs: 'First to {n} legs', sets_legs: 'First to {s} sets of {l} legs', din: 'Double In', min: 'Master In', sout: 'Straight Out', dout: 'Double Out', mout: 'Master Out',
      say_180: 'One hundred and eighty!', say_bust: 'Bust', say_game: 'Game shot, and the match, {n}!', say_set: 'Game shot, and the set, {n}!', say_leg: 'Game shot, {n}!', say_0: 'No score',
      say_need: '{n}, you require {r}', caller_on: 'Caller on',
      online: 'Online', offline: 'Offline', connection: 'Connection', detection: 'Detection', running: 'running', stopped: 'stopped', fps: 'Frame rate', cameras: 'Cameras', cpu: 'CPU', memory: 'Memory',
      calibrated: 'Calibrated', yes: 'yes', no: 'no', controls: 'Controls', start: 'Start', stop: 'Stop', reset: 'Reset', calibrate: 'Calibrate', calibrate_q: 'Calibrate now?',
      restart_sw: 'Restart software', restart_pc: 'Restart PC', sure: 'Sure?', extra_imgs: 'Detection & live image', detection_img: 'Detection', live_img: 'Live image', cam_settings: 'Camera settings',
      resolution: 'Resolution', standby: 'Standby after', minutes: '{n} min', standby_hint: 'Cameras sleep after the standby time without motion and wake up with the next throw.',
      software: 'Software & updates', board_sw: 'Board software', vision: 'Detection (vision)', host: 'Computer', kernel: 'Kernel', install: 'Install', open_orig: 'Open original Board Manager', home_only: 'Only in your home network.',
      tap_cam: 'Tap a camera = large and live', calib_grid: 'Calibration grid', cams_start: 'Cameras off – start detection',
      st_throw: 'ready', st_takeout: 'remove darts', st_calibrating: 'calibrating', st_starting: 'starting', st_stopped: 'stopped',
      players_stats: 'Players & statistics', n_players: '{p} players · {g} games saved', no_players: 'No players yet. Add yourself and your opponents – every game then counts towards the statistics.',
      games_wins: '{g} games · {w} wins', best_avg: 'Best avg', n180: '180s', legs: 'Legs', rename: 'Rename', del_stats: 'Delete statistics', del_player: 'Delete player', really_del: 'Really delete?',
      recent: 'Recent games', no_game_yet: 'No finished game yet.', reset_all: 'Reset everything', del_all: 'Delete statistics of all players and game history', del_all_q: 'Sure? This cannot be undone',
      players_stay: 'The players themselves are kept.', save: 'Save',
      d_overview: 'Dartboard scene with live darts, optional power on/off and shortcuts', d_game: 'Local X01 game: lobby, bull-off, match, result', d_manager: 'Cameras, controls, system values, settings', d_players: 'Players, overall statistics, recent games'
    },
    de: {
      dart: 'Dart', visit: 'Aufnahme', on: 'Einschalten', off: 'Ausschalten', off_q: 'Wirklich aus?', play: 'Spielen', manager: 'Board Manager', players: 'Spieler',
      sc_off: 'Board aus', sc_starting: 'Startet …', sc_stopping: 'Fährt herunter …', sc_ready: 'Bereit – wirf!', sc_takeout: 'Darts ziehen', sc_calib: 'Kalibriert …', sc_stopped: 'Erkennung gestoppt', sc_lost: 'Verbindung kurz weg',
      dart_of: 'Dart {n} von 3 · bisher {s}', visit_pts: 'Aufnahme {s} Punkte', pc_running: 'PC läuft, Autodarts startet', about_minute: 'Dauert etwa eine Minute', plug_after: 'Steckdose geht danach aus',
      plug_on: 'Steckdose an', ready_hint: 'Wirf einen Dart zum Start', game_running: 'Spiel läuft', back: 'Zurück', missing: 'Integration „Autodarts“ nicht gefunden',
      new_game: 'Neues Spiel', game_over: 'Spielende', darts: 'Darts', local: 'X01 – lokal in Home Assistant', cancel_game: 'Spiel abbrechen', caller: 'Ansage', fullscreen: 'Vollbild',
      nobody: 'Noch niemand dabei – unten antippen.', of6: '{n} von 6', shuffle: 'Reihenfolge mischen', new_player: 'Neuer Spieler', bot: 'Bot', bot_level: 'Bot-Stärke (Average)', average: 'Average',
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
      cam: 'Kamera {n}', cams_off: 'Kameras aus', graphic: 'Grafik', tap_view: 'Antippen: nächste Kamera / Grafik', grid: 'Netz',
      first_leg: 'Erster bis {n} Leg', first_legs: 'Erster bis {n} Legs', sets_legs: 'Erster bis {s} Sets à {l} Legs', din: 'Double In', min: 'Master In', sout: 'Straight Out', dout: 'Double Out', mout: 'Master Out',
      say_180: 'Einhundertachtzig!', say_bust: 'Überworfen', say_game: 'Game shot! Spiel für {n}', say_set: 'Game shot! Satz für {n}', say_leg: 'Game shot! Leg für {n}', say_0: 'No score',
      say_need: '{n}, du brauchst {r}', caller_on: 'Ansage an',
      online: 'Online', offline: 'Offline', connection: 'Verbindung', detection: 'Erkennung', running: 'läuft', stopped: 'gestoppt', fps: 'Bildrate', cameras: 'Kameras', cpu: 'CPU', memory: 'Speicher',
      calibrated: 'Kalibriert', yes: 'ja', no: 'nein', controls: 'Steuerung', start: 'Start', stop: 'Stop', reset: 'Reset', calibrate: 'Kalibrieren', calibrate_q: 'Jetzt kalibrieren?',
      restart_sw: 'Software neu starten', restart_pc: 'PC neu starten', sure: 'Sicher?', extra_imgs: 'Erkennungsbild & Live-Bild', detection_img: 'Erkennung', live_img: 'Live-Bild', cam_settings: 'Kamera-Einstellungen',
      resolution: 'Auflösung', standby: 'Standby nach', minutes: '{n} Minuten', standby_hint: 'Kameras gehen nach der Standby-Zeit ohne Bewegung schlafen und wachen beim nächsten Wurf auf.',
      software: 'Software & Updates', board_sw: 'Board-Software', vision: 'Erkennung (Vision)', host: 'Rechner', kernel: 'Kernel', install: 'Installieren', open_orig: 'Original Board Manager öffnen', home_only: 'Nur im Heimnetz.',
      tap_cam: 'Kamera antippen = groß und live', calib_grid: 'Kalibriernetz', cams_start: 'Kameras aus – Erkennung starten',
      st_throw: 'bereit', st_takeout: 'Darts ziehen', st_calibrating: 'kalibriert', st_starting: 'startet', st_stopped: 'gestoppt',
      players_stats: 'Spieler & Statistik', n_players: '{p} Spieler · {g} Spiele gespeichert', no_players: 'Noch keine Spieler. Lege dich und deine Mitspieler an – danach zählt jedes Spiel in die Statistik.',
      games_wins: '{g} Spiele · {w} Siege', best_avg: 'Bester Avg', n180: '180er', legs: 'Legs', rename: 'Umbenennen', del_stats: 'Statistik löschen', del_player: 'Spieler löschen', really_del: 'Wirklich löschen?',
      recent: 'Letzte Spiele', no_game_yet: 'Noch kein Spiel beendet.', reset_all: 'Alles zurücksetzen', del_all: 'Statistik aller Spieler und Spielverlauf löschen', del_all_q: 'Sicher? Lässt sich nicht rückgängig machen',
      players_stay: 'Die Spieler selbst bleiben.', save: 'Speichern',
      d_overview: 'Dartscheibe mit Live-Würfen, optional Ein/Aus und Abkürzungen', d_game: 'Lokales X01-Spiel: Lobby, Bull-Off, Spiel, Ergebnis', d_manager: 'Kameras, Steuerung, Systemwerte, Einstellungen', d_players: 'Spieler, Gesamtstatistik, letzte Spiele'
    }
  };
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
    ziehen: ['sc_takeout', 'mdi:hand-back-left-outline'], kalib: ['sc_calib', 'mdi:crosshairs-gps'], gestoppt: ['sc_stopped', 'mdi:stop-circle-outline'], weg: ['sc_lost', 'mdi:wifi-alert']
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
:host([sz=gestoppt]) .szene{--ring:#64b5f6}
:host([sz=gestoppt]) .schein{opacity:.35}
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
    setConfig(c) { this._c = Object.assign({}, c || {}); if (this._r) { this._r = null; this.shadowRoot.innerHTML = ''; } }
    getCardSize() { return 5; }
    getGridOptions() { return { columns: 12, min_columns: 6 }; }
    set hass(h) { this._h = h; sprachePruefen(h); if (!this._r || this._spr !== SPR) this._bauen(); this._zeichnen(); }
    _bauen() {
      this._spr = SPR;
      this._r = this.shadowRoot || this.attachShadow({ mode: 'open' });
      const c = this._c;
      const k = (cls, id, lbl, icon, f) => '<button class="k ' + cls + '" data-id="' + id + '" data-lbl="' + lbl + '" style="--k:' + f + '"><ha-icon icon="' + icon + '"></ha-icon><span class="lbl">' + lbl + '</span></button>';
      const kn = [];
      if (c.power_on) kn.push(k('haupt', 'ein', t('on'), 'mdi:power', G));
      if (c.game_path) kn.push(k('feld', 'spielen', t('play'), 'mdi:bullseye-arrow', R));
      if (c.manager_path) kn.push(k('feld', 'mgr', t('manager'), 'mdi:camera-iris', 'var(--purple-color,#9c27b0)'));
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
      const online = ['bereit', 'ziehen', 'kalib', 'gestoppt', 'weg'].includes(sz) || (sz === 'startet' && zst(h, E(h, 'sensor.status')) === 'starting');
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
        if (a === 'zurueck') { if (document.fullscreenElement) document.exitFullscreen(); if (this._c.back_path) gehe(this._c.back_path); else history.back(); return; }
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
      this._kopf('Autodarts', t('missing')); this._setze('<div class="leer">' + t('missing') + '</div>'); return true;
    }
  }

  /* ---------- Game card (lobby, bull-off, X01, result) ---------- */
  const STARTWERTE = [101, 170, 301, 501, 701, 901];
  const MODUS = [['straight', 'Straight'], ['double', 'Double'], ['master', 'Master']];
  const BOTS = [20, 30, 40, 50, 60, 70, 80, 90, 100];
  const BRETT_CX = 60, BRETT_K = 52;
  const brett = darts => {
    const P = (r, w) => { const a = (w - 90) * Math.PI / 180; return [BRETT_CX + r * Math.cos(a), BRETT_CX + r * Math.sin(a)]; };
    const sek = (r1, r2, w1, w2, f) => { const [a, b] = P(r2, w1), [c, d] = P(r2, w2), [e, g] = P(r1, w2), [i, j] = P(r1, w1); return '<path d="M' + f1(a) + ' ' + f1(b) + 'A' + r2 + ' ' + r2 + ' 0 0 1 ' + f1(c) + ' ' + f1(d) + 'L' + f1(e) + ' ' + f1(g) + 'A' + r1 + ' ' + r1 + ' 0 0 0 ' + f1(i) + ' ' + f1(j) + 'Z" fill="' + f + '"/>'; };
    const k = BRETT_K / 170;
    let s = '<svg viewBox="0 0 120 120"><circle cx="60" cy="60" r="60" fill="#111"/>';
    ORDER.forEach((n, i) => {
      const w1 = i * 18 - 9, w2 = w1 + 18, d = i % 2 === 0, e = d ? '#1c1c1c' : '#e9dfc4', f = d ? '#c62828' : '#2e7d32';
      s += sek(15.9 * k, 99 * k, w1, w2, e) + sek(99 * k, 107 * k, w1, w2, f) + sek(107 * k, 162 * k, w1, w2, e) + sek(162 * k, 170 * k, w1, w2, f);
      const [x, y] = P(56.5, i * 18); s += '<text x="' + f1(x) + '" y="' + f1(y + 1.8) + '">' + n + '</text>';
    });
    s += '<circle cx="60" cy="60" r="' + f1(15.9 * k) + '" fill="#2e7d32"/><circle cx="60" cy="60" r="' + f1(6.35 * k) + '" fill="#c62828"/>';
    (darts || []).forEach((d, i) => {
      let p = null;
      if (typeof d.x === 'number' && typeof d.y === 'number') { const r = Math.hypot(d.x, d.y), f = r > 1.12 ? 1.12 / r : 1; p = [60 + d.x * f * BRETT_K, 60 - d.y * f * BRETT_K]; }
      else {
        const x = d.f || '';
        if (x === 'D25') p = P(1, i * 120); else if (x === 'S25') p = P(3.5, i * 120); else if (x === 'M' || !x) p = P(57, 200 + i * 30);
        else { const n = parseInt(x.slice(1), 10), w = ORDER.indexOf(n) * 18 + [-4, 3, 0][i]; p = P(x[0] === 'T' ? 103 * k : x[0] === 'D' ? 166 * k : (x[0] === 'S' ? 135 * k : 50), w); }
      }
      s += '<g transform="translate(' + f1(p[0]) + ' ' + f1(p[1]) + ')"><circle r="3.6" fill="' + ['#ff5252', '#40c4ff', '#ffd740'][i] + '" stroke="#000" stroke-width="1"/><text y="1.6" font-size="4.4" fill="#000">' + (i + 1) + '</text></g>';
    });
    return s + '</svg>';
  };
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
@container (max-width:420px){.sk .sr{font-size:44px}.spieler{grid-template-columns:repeat(auto-fit,minmax(130px,1fr))}.dz b{font-size:22px}}`;
  const KAMERA_KEYS = ['camera.camera_1', 'camera.camera_2', 'camera.camera_3'];
  class AutodartsGameCard extends DartsSeite {
    static get CSS() { return SPIEL_CSS; }
    get _spiel() { return E(this._h, 'sensor.game'); }
    get _spieler() { return E(this._h, 'sensor.players'); }
    _lobbyStart() {
      const l = att(this._h, this._spieler).letzte || {};
      this._lob = {
        spieler: (l.spieler || []).slice(0, 6), startwert: l.startwert || 501, legs: l.legs || 1, sets: l.sets || 0,
        einwurf: l.einwurf || 'straight', auswurf: l.auswurf || 'double', bull_off: !!l.bull_off
      };
    }
    _sichtbar() { this._wach(); this._lvStrom(); }
    // view: camera 1–3 (index) or graphic; stored per device
    _ansichtNr() { let v = '1'; try { v = localStorage.getItem('autodarts_view') || v; } catch (e) {} return v; }
    _ansicht() { const n = this._ansichtNr(); return n === 'g' ? 'grafik' : E(this._h, KAMERA_KEYS[(+n || 2) - 1]); }
    _netzAn() { try { return localStorage.getItem('autodarts_grid') === '1'; } catch (e) { return false; } }
    _lvSoll() {
      const id = this._ansicht(), h = this._h;
      return id && id !== 'grafik' && phase(att(h, this._spiel)) === 'running' && boardOnline(h) && an(h, E(h, 'binary_sensor.detection_running')) && !!entzerrung(att(h, id).kalibrierung);
    }
    _brettHtml(darts) {
      const id = this._ansicht(), nr = this._ansichtNr();
      if (!this._lvSoll()) return '<div class="brett grafik" data-act="ansicht" title="' + t('tap_view') + '">' + brett(darts) + (id !== 'grafik' ? '<div class="bk"><span>' + (boardOnline(this._h) ? t('cams_off') : t('sc_off')) + ' – ' + t('graphic') + '</span></div>' : '') + '</div>';
      const netz = this._netzAn();
      const pf = (darts || []).map((d, i) => { const [x, y] = dartMM(d, i); return '<g transform="translate(' + x.toFixed(1) + ' ' + y.toFixed(1) + ')"><circle r="15" fill="' + ['#ff5252', '#40c4ff', '#ffd740'][i] + '"/><text y="6.5">' + (i + 1) + '</text></g>'; }).join('');
      return '<div class="brett live" data-act="ansicht" title="' + t('tap_view') + '"><div class="lvh"></div>' +
        (netz ? '<svg class="netz" viewBox="-225 -225 450 450"><path d="' + NETZ_MM + '"/></svg>' : '') +
        '<svg class="pf" viewBox="-225 -225 450 450">' + pf + '</svg><div class="bk"><span>' + t('cam', { n: nr }) + '</span><button class="' + (netz ? 'an' : '') + '" data-act="netz">' + t('grid') + '</button></div></div>';
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
    connectedCallback() { this._ausblenden(true); }
    disconnectedCallback() { this._ausblenden(false); this._lvStrom(); }
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
      if (x) this._sagen(x);
    }
    _zeichnen() {
      if (this._fehlt()) return;
      const h = this._h, a = att(h, this._spiel), ph = phase(a);
      if (!this._weg && this.isConnected && Date.now() - (this._wegZeit || 0) > 3000) this._ausblenden(true);
      const ansage = this._ansage(), vb = !!document.fullscreenElement;
      this._kopf(ph === 'idle' ? t('new_game') : (ph === 'finished' ? t('game_over') : t('darts')), modusText(a.einstellungen) || t('local'),
        (ph === 'running' || ph === 'bulloff' ? '<button class="ik" data-act="xabbr" title="' + t('cancel_game') + '"><ha-icon icon="mdi:close"></ha-icon></button>' : '') +
        '<button class="ik' + (ansage ? ' an' : '') + '" data-act="ansage" title="' + t('caller') + '"><ha-icon icon="' + (ansage ? 'mdi:volume-high' : 'mdi:volume-off') + '"></ha-icon></button>' +
        '<button class="ik" data-act="vollbild" title="' + t('fullscreen') + '"><ha-icon icon="' + (vb ? 'mdi:fullscreen-exit' : 'mdi:fullscreen') + '"></ha-icon></button>');
      if (ph !== this._phAlt) { if (ph === 'idle') this._lobbyStart(); this._phAlt = ph; this._wach(); }
      if (!this._lob) this._lobbyStart();
      if (ph === 'running' || ph === 'finished') this._sprechen(a);
      let html;
      if (ph === 'bulloff') html = this._bulloff(a);
      else if (ph === 'running') html = this._match(a);
      else if (ph === 'finished') html = this._ende(a);
      else html = this._lobby();
      this._setze(html);
      this._lvStrom();
    }
    _lobby() {
      const h = this._h, L = this._lob, alle = att(h, this._spieler).spieler || [], name = id => (alle.find(s => s.id === id) || {}).name;
      L.spieler = L.spieler.filter(x => x.startsWith('bot:') || name(x));
      if (this._wartName) { const n = alle.find(s => s.name.toLowerCase() === this._wartName); if (n) { this._wartName = null; if (!L.spieler.includes(n.id) && L.spieler.length < 6) L.spieler.push(n.id); } }
      const liste = L.spieler.map((x, i) => {
        const bot = x.startsWith('bot:');
        return '<div class="sp feld"><span class="nr">' + (i + 1) + '</span><span class="nm">' + (bot ? t('bot') + ' <small>' + t('average') + ' ' + x.slice(4) + '</small>' : esc(name(x))) + '</span>' +
          (i ? '<button data-act="hoch" data-i="' + i + '" title="' + t('move_up') + '"><ha-icon icon="mdi:arrow-up"></ha-icon></button>' : '') +
          '<button data-act="weg" data-i="' + i + '" title="' + t('remove') + '"><ha-icon icon="mdi:close"></ha-icon></button></div>';
      }).join('') || '<div class="leer">' + t('nobody') + '</div>';
      const frei = alle.filter(s => !L.spieler.includes(s.id));
      const voll = L.spieler.length >= 6;
      let s = '<div class="lobby"><div class="blk feld"><div class="bt"><ha-icon icon="mdi:account-group"></ha-icon>' + t('players') + '<span class="rechts">' + t('of6', { n: L.spieler.length }) + '</span>' +
        '<button class="ik" data-act="mischen" title="' + t('shuffle') + '"' + (L.spieler.length < 2 ? ' disabled' : '') + '><ha-icon icon="mdi:shuffle-variant"></ha-icon></button></div>' +
        '<div class="sliste">' + liste + '</div><div class="chips">' +
        frei.map(p => '<button class="chip feld" data-act="dazu" data-id="' + p.id + '"' + (voll ? ' disabled' : '') + '><ha-icon icon="mdi:plus"></ha-icon>' + esc(p.name) + '</button>').join('') +
        '<button class="chip feld" data-act="neu"' + (voll ? ' disabled' : '') + '><ha-icon icon="mdi:account-plus"></ha-icon>' + t('new_player') + '</button>' +
        '<button class="chip feld' + (this._auf.bot ? ' an' : '') + '" data-act="tgl" data-x="bot"' + (voll ? ' disabled' : '') + '><ha-icon icon="mdi:robot-outline"></ha-icon>' + t('bot') + '</button></div>';
      if (this._auf.bot && !voll) s += '<div class="reihe" style="padding-top:12px"><span>' + t('bot_level') + '</span><div class="seg">' + BOTS.map(b => '<button class="feld" data-act="bot" data-l="' + b + '">' + b + '</button>').join('') + '</div></div>';
      s += '</div>';
      const seg = (k, opts) => '<div class="seg">' + opts.map(([v, x]) => '<button class="feld' + (String(L[k]) === String(v) ? ' an' : '') + '" data-act="set" data-k="' + k + '" data-v="' + v + '">' + x + '</button>').join('') + '</div>';
      const legs = n => n + ' Leg' + (n > 1 ? 's' : '');
      const mehrText = (L.sets ? t('sets_to', { n: L.sets }) : t('no_sets')) + ' · ' + MODUS.find(m => m[0] === L.einwurf)[1] + ' In · ' + t('bulloff_onoff', { v: L.bull_off ? t('on_w') : t('off_w') });
      s += '<div class="blk feld"><div class="bt"><ha-icon icon="mdi:tune-variant"></ha-icon>' + t('game') + '</div>' +
        '<div class="reihe"><span>' + t('start_value') + '</span>' + seg('startwert', STARTWERTE.map(v => [v, v])) + '</div>' +
        '<div class="reihe"><span>' + (L.sets ? t('legs_per_set') : t('first_to')) + '</span><div class="stepper"><button class="feld" data-act="minus" data-k="legs">−</button><b>' + legs(L.legs) + '</b><button class="feld" data-act="plus" data-k="legs">+</button></div></div>' +
        '<div class="reihe"><span>' + t('checkout') + '</span>' + seg('auswurf', MODUS) + '</div>' +
        auf('mehr', this._auf.mehr, 'mdi:cog-outline', t('more'), mehrText);
      if (this._auf.mehr) s += '<div class="aufinhalt">' +
        '<div class="reihe"><span>' + t('sets_first') + '</span><div class="stepper"><button class="feld" data-act="minus" data-k="sets">−</button><b>' + (L.sets ? L.sets + ' Set' + (L.sets > 1 ? 's' : '') : t('no_sets')) + '</b><button class="feld" data-act="plus" data-k="sets">+</button></div></div>' +
        '<div class="reihe"><span>' + t('checkin') + '</span>' + seg('einwurf', MODUS) + '</div>' +
        '<div class="reihe"><span>' + t('bulloff_who') + '</span>' + seg('bull_off', [[false, t('off_w')], [true, t('on_w')]]) + '</div></div>';
      s += '</div>';
      if (!boardOnline(this._h) && !L.spieler.every(x => x.startsWith('bot:')))
        s += '<div class="warn"><ha-icon icon="mdi:power-plug-off-outline"></ha-icon><span>' + t('board_off_hint') + '</span>' + (this._c.power_on ? '<button data-act="pcein">' + t('on') + '</button>' : '') + '</div>';
      s += '<button class="start" data-act="start"' + (L.spieler.length ? '' : ' disabled') + '><ha-icon icon="mdi:play"></ha-icon>' + t('start_game') + '</button></div>';
      return s;
    }
    _bulloff(a) {
      const bo = a.bulloff || [];
      const z = bo.map((p, i) => '<div class="boz feld' + (i === a.am_zug && !p.dart && !p.raus ? ' aktiv' : '') + '"' + (p.raus ? ' style="opacity:.45"' : '') + '><ha-icon icon="' + (p.bot ? 'mdi:robot-outline' : 'mdi:account') + '"></ha-icon><b>' + esc(p.name) + '</b><span>' +
        (p.raus ? t('out') : p.dart ? ft(p.dart.f) + ' · ' + p.abstand + ' mm' : (i === a.am_zug ? t('aims_bull') : t('waits'))) + '</span></div>').join('');
      return '<div class="blk feld"><div class="bt"><ha-icon icon="mdi:bullseye"></ha-icon>' + (a.gleichstand ? t('tie') : t('bulloff_title')) + '<span class="rechts">' + t('one_dart') + '</span></div><div class="bo">' + z + '</div></div>' +
        '<div class="leiste"><button class="lk feld" data-act="undo"><ha-icon icon="mdi:undo"></ha-icon>' + t('undo') + '</button><button class="lk feld" data-act="dart" data-i="' + bo.filter(p => p.dart && !p.raus).length + '"><ha-icon icon="mdi:pencil"></ha-icon>' + t('enter') + '</button>' +
        '<button class="lk weiter" data-act="weiter"><ha-icon icon="mdi:skip-next"></ha-icon>' + t('missed') + '</button></div>' +
        '<button class="auf feld" data-act="abbr" data-lbl="' + t('cancel_game') + '" style="--sr-f:var(--red-color,#e53935)"><ha-icon icon="mdi:close-circle-outline"></ha-icon><span class="lbl">' + t('cancel_game') + '</span></button>';
    }
    _match(a) {
      const sp = a.spieler || [], am = a.am_zug, e = a.einstellungen || {}, au = a.aufnahme || { darts: [] }, wer = sp[am] || {};
      const tiles = sp.map((p, i) => '<div class="sk feld' + (i === am ? ' aktiv' : '') + '"><div class="sn">' + (p.bot ? '<ha-icon icon="mdi:robot-outline"></ha-icon>' : '') + esc(p.name) +
        '<span class="lg">' + (e.sets ? p.sets + ' S · ' : '') + p.legs + ' L</span></div><div class="sr">' + p.rest + '</div>' +
        '<div class="sa">Ø ' + z1(p.avg) + ' · ' + t('n_darts', { n: p.leg_darts }) + (p.letzte != null ? ' · ' + t('last') + ' <b>' + p.letzte + '</b>' : '') + '</div>' +
        (i !== am && p.weg ? '<div class="sw">' + p.weg.map(f => '<span>' + ft(f) + '</span>').join('') + '</div>' : '') + '</div>').join('');
      let hinw, cls = '';
      if (a.leg_gewinner != null) { hinw = '<ha-icon icon="mdi:check-decagram"></ha-icon>' + t('leg_won', { n: esc(sp[a.leg_gewinner].name) }); cls = ' check'; }
      else if (au.bust) { hinw = '<ha-icon icon="mdi:close-octagon"></ha-icon>' + t('bust'); cls = ' bust'; }
      else if (au.fertig) hinw = '<ha-icon icon="mdi:hand-back-left-outline"></ha-icon>' + t('remove_darts');
      else if (wer.bot) hinw = '<ha-icon icon="mdi:robot-outline"></ha-icon>' + t('throws_now', { n: esc(wer.name) });
      else if (!wer.offen && e.einwurf !== 'straight') hinw = t(e.einwurf === 'double' ? 'to_start_d' : 'to_start_m', { n: esc(wer.name) });
      else hinw = '<ha-icon icon="mdi:target"></ha-icon>' + t('your_turn', { n: esc(wer.name) });
      const dz = [0, 1, 2].map(i => { const d = au.darts[i]; return '<button class="dz feld' + (d ? '' : ' leer') + '" data-act="dart" data-i="' + i + '"><b>' + (d ? ft(d.f) : '–') + '</b><small>' + (d ? pkt(d.f) + ' ' + t('pts') : t('dart') + ' ' + (i + 1)) + '</small></button>'; }).join('');
      const weg = a.weg ? '<div class="weg">' + a.weg.map(f => '<span>' + ft(f) + '</span>').join('') + '</div>' : '';
      let s = '<div class="spieler' + (sp.length > 3 ? ' viele' : '') + '">' + tiles + '</div><div class="mitte"><div class="aufn feld' + cls + '"><div class="hinw">' + hinw + '</div><div class="dartsz">' + dz + '</div>' +
        '<div class="summe"><b>' + au.summe + '</b><span>' + t('rest', { n: wer.rest }) + '</span></div>' + weg + '</div>' +
        this._brettHtml(au.darts) + '</div>' +
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
    _verlauf(a) {
      const sp = a.spieler || [], v = (a.verlauf || []).slice().reverse();
      if (!v.length) return '<div class="leer">' + t('no_visit') + '</div>';
      return '<div class="vl">' + v.map(z => '<div class="vz' + (z.b ? ' bu' : '') + (z.c ? ' co' : '') + '" data-act="vz" data-i="' + z.i + '"><span>' + esc((sp[z.s] || {}).name) + '</span><span>' +
        (z.d.length ? z.d.map(ft).join(' · ') : '–') + '</span><b>' + (z.b ? 'Bust' : z.p) + '</b><span class="r">' + z.r + '</span></div>').join('') + '</div>' +
        '<div class="klein">' + t('tap_fix') + '</div>';
    }
    _statTab(sp) {
      const zeilen = [[t('average'), p => z1(p.avg)], [t('first9'), p => z1(p.f9)], [t('darts'), p => p.darts], ['Checkout', p => (p.versuche ? z1(p.quote) + ' % (' + p.treffer + '/' + p.versuche + ')' : '–')],
        [t('highest'), p => p.hoechste], [t('best_finish'), p => p.finish || '–'], ['180 / 140+ / 100+', p => p.n180 + ' / ' + p.n140 + ' / ' + p.n100], [t('best_leg'), p => (p.bestes_leg ? t('n_darts', { n: p.bestes_leg }) : '–')]];
      return '<div style="overflow-x:auto"><table class="tab"><tr><th></th>' + sp.map(p => '<th>' + esc(p.name) + '</th>').join('') + '</tr>' +
        zeilen.map(([x, f]) => '<tr><td>' + x + '</td>' + sp.map(p => '<td>' + f(p) + '</td>').join('') + '</tr>').join('') + '</table></div>';
    }
    _ende(a) {
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
    _klick(act, b) {
      const h = this._h, L = this._lob, a = att(h, this._spiel);
      const neu = () => { this._alt = null; this._zeichnen(); };
      switch (act) {
        case 'ansicht': { const f = ['1', '2', '3', 'g'], n = f[(f.indexOf(this._ansichtNr()) + 1) % 4]; try { localStorage.setItem('autodarts_view', n); } catch (e) {} neu(); break; }
        case 'netz': { try { localStorage.setItem('autodarts_grid', this._netzAn() ? '0' : '1'); } catch (e) {} neu(); break; }
        case 'ansage': { const ein = !this._ansage(); try { localStorage.setItem('autodarts_caller', ein ? '1' : '0'); } catch (e) {} if (ein && window.speechSynthesis) this._sagen(t('caller_on')); this._kxAlt = null; this._zeichnen(); break; }
        case 'vollbild':
          if (document.fullscreenElement) document.exitFullscreen(); else if (this.requestFullscreen) this.requestFullscreen().catch(() => {});
          setTimeout(() => { this._kxAlt = null; this._zeichnen(); }, 300); break;
        case 'dazu': if (L.spieler.length < 6) L.spieler.push(b.dataset.id); neu(); break;
        case 'bot': if (L.spieler.length < 6) L.spieler.push('bot:' + b.dataset.l); this._auf.bot = false; neu(); break;
        case 'weg': L.spieler.splice(+b.dataset.i, 1); neu(); break;
        case 'hoch': { const i = +b.dataset.i; [L.spieler[i - 1], L.spieler[i]] = [L.spieler[i], L.spieler[i - 1]]; neu(); break; }
        case 'mischen': for (let i = L.spieler.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [L.spieler[i], L.spieler[j]] = [L.spieler[j], L.spieler[i]]; } neu(); break;
        case 'set': { const v = b.dataset.v; L[b.dataset.k] = b.dataset.k === 'startwert' ? +v : v === 'true' ? true : v === 'false' ? false : v; neu(); break; }
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
        case 'pcein': if (this._c.power_on) ausloesen(h, this._c.power_on, false); break;
        case 'start':
          this._dienst('spiel_starten', { spieler: L.spieler, startwert: L.startwert, legs: L.legs, sets: L.sets, einwurf: L.einwurf, auswurf: L.auswurf, bull_off: L.bull_off });
          this._auf.verlauf = this._auf.stat = this._auf.opt = false; break;
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
      this._kopf(t('manager'), on ? 'Autodarts ' + (ver || '') + ' · ' + (({ throw: t('st_throw'), takeout: t('st_takeout'), takeoutInProgress: t('st_takeout'), calibrating: t('st_calibrating'), starting: t('st_starting'), stopped: t('st_stopped') })[status] || status) : t('sc_off'));
      const nk = this._r.querySelector('.netzk');
      if (nk.firstChild.textContent !== t('tap_cam')) { nk.firstChild.textContent = t('tap_cam'); nk.lastChild.textContent = t('calib_grid'); }
      this._kams.querySelectorAll('.kam span').forEach((s, i) => { const x = t('cam', { n: i + 1 }); if (s.textContent !== x) s.textContent = x; });
      const w = (id, x, wert, kl) => '<div class="wt feld ' + (kl || '') + '" data-e="' + id + '"><small>' + x + '</small><b>' + wert + '</b></div>';
      const n = id => { const v = parseFloat(zst(h, id)); return isNaN(v) ? '–' : zahl(v, v % 1 ? 1 : 0); };
      const kalId = E(h, 'binary_sensor.calibrated'), erkId = E(h, 'binary_sensor.detection_running'), kal = zst(h, kalId), erk = zst(h, erkId);
      const werte = on ? w(S('connection'), t('connection'), t('online'), 'gut') + w(erkId, t('detection'), erk === 'on' ? t('running') : t('stopped'), erk === 'on' ? 'gut' : 'schlecht') +
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
.kach{display:grid;grid-template-columns:repeat(auto-fit,minmax(96px,1fr));gap:6px}
.ka{border-radius:12px;padding:8px 10px}
.ka small{display:block;font-size:11.5px;color:var(--secondary-text-color);font-weight:600}.ka b{font-size:16px}
.plknoepfe{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}
.plknoepfe button{display:flex;align-items:center;gap:6px;border-radius:12px;padding:9px 12px;font-size:13px;font-weight:600;--sr-f:var(--red-color,#e53935)}
.plknoepfe ha-icon{--mdc-icon-size:18px}
.sv{border-radius:14px;padding:10px 12px;margin-bottom:6px;font-size:13.5px}
.sv .k{display:flex;justify-content:space-between;color:var(--secondary-text-color);font-size:12px;margin-bottom:4px}
.sv .g{color:var(--amber-color,#ffc107);font-weight:700}`;
  const datum = x => { try { const d = new Date(x); return d.toLocaleDateString(LOC, { day: '2-digit', month: '2-digit' }) + ' ' + d.toLocaleTimeString(LOC, { hour: '2-digit', minute: '2-digit' }); } catch (e) { return ''; } };
  class AutodartsPlayersCard extends DartsSeite {
    static get CSS() { return SPL_CSS; }
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
          s += '<div class="pld"><div class="kach">' + ka(t('average'), z1(p.avg)) + ka(t('first9'), z1(p.f9)) + ka(t('best_avg'), z1(p.bester_avg)) + ka('Checkout', z1(p.quote) + ' %') +
            ka(t('highest'), p.hoechste) + ka(t('best_finish'), p.finish || '–') + ka(t('best_leg'), p.bestes_leg ? t('n_darts', { n: p.bestes_leg }) : '–') + ka(t('n180'), p.n180) +
            ka('140+', p.n140) + ka('100+', p.n100) + ka(t('legs'), p.legs) + ka(t('darts'), zahl(p.darts)) + '</div>' +
            '<div class="plknoepfe"><button class="feld" data-act="umb" data-id="' + p.id + '" data-n="' + esc(p.name) + '"><ha-icon icon="mdi:pencil"></ha-icon><span class="lbl">' + t('rename') + '</span></button>' +
            '<button class="feld" data-act="statweg" data-id="' + p.id + '" data-lbl="' + t('del_stats') + '"><ha-icon icon="mdi:delete-sweep-outline"></ha-icon><span class="lbl">' + t('del_stats') + '</span></button>' +
            '<button class="feld" data-act="spweg" data-id="' + p.id + '" data-lbl="' + t('del_player') + '"><ha-icon icon="mdi:account-remove"></ha-icon><span class="lbl">' + t('del_player') + '</span></button></div></div>';
        }
        s += '</div>';
      });
      s += auf('verlauf', this._auf.verlauf, 'mdi:history', t('recent'), vl.length ? datum(vl[0].zeit) : '');
      if (this._auf.verlauf) s += '<div class="aufinhalt">' + (vl.length ? vl.map(v => '<div class="sv feld"><div class="k"><span>' + datum(v.zeit) + '</span><span></span></div>' +
        v.spieler.map(p => '<span class="' + (p.sieger ? 'g' : '') + '">' + (p.sieger ? '🏆 ' : '') + esc(p.name) + ' ' + (p.sets || p.legs) + ' <small>(Ø ' + z1(p.avg) + ')</small></span>').join(' · ') + '</div>').join('') : '<div class="leer">' + t('no_game_yet') + '</div>') + '</div>';
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
      if (act === 'statweg') zweimal(this, b, t('really_del'), () => this._dienst('statistik_loeschen', { id: b.dataset.id }));
      if (act === 'spweg') zweimal(this, b, t('really_del'), () => this._dienst('spieler_aendern', { id: b.dataset.id, loeschen: true }));
      if (act === 'allesweg') zweimal(this, b, t('del_all_q'), () => this._dienst('statistik_loeschen', { verlauf: true }));
    }
  }
  customElements.define('autodarts-players-card', AutodartsPlayersCard);

  SPR = sprache(document.querySelector('home-assistant') && document.querySelector('home-assistant').hass);
  window.customCards = window.customCards || [];
  window.customCards.push(
    { type: 'autodarts-overview-card', name: 'Autodarts Overview', description: t('d_overview'), preview: true },
    { type: 'autodarts-game-card', name: 'Autodarts Game', description: t('d_game') },
    { type: 'autodarts-manager-card', name: 'Autodarts Board Manager', description: t('d_manager') },
    { type: 'autodarts-players-card', name: 'Autodarts Players', description: t('d_players') }
  );
  console.info('%c AUTODARTS CARDS %c loaded ', 'color:#fff;background:#00a37a;font-weight:700', 'color:#00a37a');
})();
