/*
 * desk-loader.js — feedback for a server-rendered app.
 *
 * The problem: every click here is a full page navigation. Flask may spend
 * several seconds scoring 4,530 banks or re-reading workbooks before it emits a
 * single byte, and during that window the browser shows nothing but a tab
 * spinner. The user cannot tell a slow query from a dead click.
 *
 * The fix has to live in the page being left behind, because that is the only
 * code still running. Three layers, cheapest first:
 *
 *   1. Progress bar — every navigation. Appears instantly.
 *   2. Pending marks — the specific link or button that was activated, so it is
 *      obvious WHAT is loading, not just that something is.
 *   3. Work overlay — only for destinations known to be slow. Shows the
 *      destination's own skeleton at the real column geometry, names the actual
 *      work being done, and starts an elapsed clock.
 *
 * Honesty rules, deliberately: the bar never claims to reach 100% (it cannot
 * know), the copy describes work the server genuinely performs, and the overlay
 * waits 260ms so a fast page never flashes a loading state at all.
 *
 * Opt in per element with data-loading="ledger|qc|settings|refresh|analyze".
 * A link or form without it still gets the bar and a pending mark.
 */
(function () {
  'use strict';

  var HOLD = 92;      // bar parks here; the server decides when we are done
  var OVERLAY_IN = 260; // ms before an overlay appears — below this, no flash
  var CLOCK_IN = 1800; // ms before the elapsed clock appears
  var NOTE_IN = 7000; // ms before the "still working" reassurance

  var COPY = {
    ledger: {
      t: 'Screening the universe',
      d: 'Scoring every depository on liquidity, bond book and earnings, then ranking percentiles.',
      sk: 'ledger',
      note: 'First load of a quarter scores all five quarters of composite history. Later loads read the cache and are immediate.'
    },
    qc: {
      t: 'Checking the workbooks',
      d: 'Reading every quarterly file and comparing its columns against the known schema.',
      sk: 'qc',
      note: 'Each workbook is opened and its full column set compared — this scales with how many quarters are in the data folder.'
    },
    refresh: {
      t: 'Re-reading the data folder',
      d: 'Dropping the cached workbooks and scores, then loading the share again.',
      sk: 'ledger',
      note: 'Everything is being rebuilt from the files on disk, so this is the slowest action in the app.'
    },
    analyze: {
      t: 'Building the call-prep set',
      d: 'Scoring the selected cohort against the full universe for the quarters you picked.',
      sk: 'ledger'
    },
    settings: {
      t: 'Applying settings',
      d: 'Saving, then clearing the cached screen so the next ranking reflects the new weights.',
      sk: 'form'
    }
  };

  var bar, timer, val = 0, started = 0, overlayTimer, clockTimer, noteTimer, active = false;

  // Mount inside .desk, not <body>: the theme custom properties are declared on
  // .desk, so anything parented to body renders with them unresolved — which
  // silently washed the toast out in light theme.
  function host() {
    return document.getElementById('desk') || document.querySelector('.desk') || document.body;
  }

  // A target=_blank action (the PDF hand-off) cannot be covered by an overlay —
  // this page is staying put. A toast is the honest equivalent.
  function toast(msg) {
    var t = document.createElement('div');
    t.className = 'desk-toast';
    t.setAttribute('role', 'status');
    t.innerHTML = '<span class="sp"></span><span>' + msg + '</span>';
    host().appendChild(t);
    setTimeout(function () { t.classList.add('out'); }, 5200);
    setTimeout(function () { if (t.parentNode) t.parentNode.removeChild(t); }, 5700);
  }

  function ensureBar() {
    if (bar) return bar;
    bar = document.createElement('div');
    bar.className = 'desk-bar';
    bar.setAttribute('role', 'progressbar');
    bar.setAttribute('aria-label', 'Loading');
    host().appendChild(bar);
    return bar;
  }

  function startBar() {
    ensureBar();
    val = 8;
    bar.classList.add('on');
    bar.style.width = val + '%';
    clearInterval(timer);
    // Asymptotic: fast at first, never arrives. Mirrors a request whose
    // duration we genuinely cannot predict.
    timer = setInterval(function () {
      val += (HOLD - val) * 0.08;
      bar.style.width = val.toFixed(1) + '%';
    }, 110);
  }

  function stopBar() {
    if (!bar) return;
    clearInterval(timer);
    bar.classList.remove('on');
    bar.style.width = '0';
  }

  function skeleton(kind) {
    var h = '';
    var i;
    if (kind === 'ledger') {
      h += '<div class="desk-sk-band"><div class="sk sm" style="width:150px"></div>' +
        '<div class="desk-sk-cards">';
      for (i = 0; i < 5; i++) {
        h += '<div class="desk-sk-card"><div class="sk sm" style="width:80%"></div>' +
          '<div class="sk tall" style="width:52%"></div>' +
          '<div class="sk sm" style="width:92%"></div></div>';
      }
      h += '</div></div><div class="desk-sk-hd"></div><div class="desk-sk-rows">';
      for (i = 0; i < 11; i++) {
        h += '<div class="desk-sk-row ledger">' +
          '<div class="sk" style="width:38px"></div>' +
          '<div class="sk" style="width:' + (58 + (i * 7) % 34) + '%"></div>' +
          '<div class="sk sm" style="width:70%"></div>' +
          '<div class="sk sm"></div><div class="sk sm"></div><div class="sk sm"></div>' +
          '<div class="sk sm" style="width:60%"></div>' +
          '<div class="sk tall" style="width:80%"></div></div>';
      }
      h += '</div>';
    } else if (kind === 'qc') {
      h += '<div class="desk-sk-hd"></div><div class="desk-sk-rows">';
      for (i = 0; i < 7; i++) {
        h += '<div class="desk-sk-row qc">' +
          '<div class="sk" style="width:' + (64 + (i * 11) % 30) + '%"></div>' +
          '<div class="sk sm" style="width:80%"></div>' +
          '<div class="sk sm"></div><div class="sk sm"></div>' +
          '<div class="sk sm" style="width:56%"></div></div>';
      }
      h += '</div>';
    } else {
      h += '<div class="desk-sk-rows">';
      for (i = 0; i < 5; i++) {
        h += '<div class="desk-sk-row" style="grid-template-columns:minmax(0,260px) minmax(0,1fr);height:64px">' +
          '<div><div class="sk" style="width:70%"></div></div>' +
          '<div><div class="sk sm" style="width:88%"></div></div></div>';
      }
      h += '</div>';
    }
    return h;
  }

  function showOverlay(kind) {
    var main = document.querySelector('.desk-main');
    if (!main || main.querySelector('.desk-work')) return;
    var c = COPY[kind] || COPY.ledger;

    var el = document.createElement('div');
    el.className = 'desk-work';
    el.setAttribute('aria-live', 'polite');
    el.innerHTML =
      '<div class="desk-work-head">' +
      '<div class="desk-work-pulse"><i></i><i></i><i></i><b></b></div>' +
      '<div><div class="desk-work-t">' + c.t + '</div>' +
      '<div class="desk-work-d">' + c.d + '</div></div>' +
      '<div class="desk-work-clock" data-clock>0s</div>' +
      '</div>' +
      (c.note ? '<div class="desk-work-note" data-note>' + c.note + '</div>' : '') +
      '<div style="flex:1;overflow:hidden">' + skeleton(c.sk) + '</div>';
    main.appendChild(el);

    var clock = el.querySelector('[data-clock]');
    var note = el.querySelector('[data-note]');

    clockTimer = setInterval(function () {
      var s = Math.round((Date.now() - started) / 1000);
      if (clock) {
        clock.textContent = s + 's';
        if (s >= Math.round(CLOCK_IN / 1000)) clock.classList.add('on');
      }
    }, 250);
    if (note) noteTimer = setTimeout(function () { note.classList.add('on'); }, NOTE_IN);
  }

  function clearAll() {
    active = false;
    clearTimeout(overlayTimer);
    clearInterval(clockTimer);
    clearTimeout(noteTimer);
    stopBar();
    var w = document.querySelector('.desk-work');
    if (w) w.parentNode.removeChild(w);
    document.querySelectorAll('.desk-nav a.pending').forEach(function (a) {
      a.classList.remove('pending');
    });
    document.querySelectorAll('[data-busy]').forEach(function (b) {
      b.removeAttribute('data-busy');
      b.disabled = false;
      if (b.dataset.label) { b.textContent = b.dataset.label; delete b.dataset.label; }
    });
  }

  function start(kind, trigger) {
    if (active) return;
    active = true;
    started = Date.now();
    startBar();

    if (trigger) {
      var navItem = trigger.closest ? trigger.closest('.desk-nav a') : null;
      if (navItem) navItem.classList.add('pending');
      if (trigger.tagName === 'BUTTON' || trigger.tagName === 'INPUT') {
        trigger.dataset.busy = '1';
        if (trigger.tagName === 'BUTTON' && trigger.dataset.busyLabel) {
          trigger.dataset.label = trigger.textContent;
          trigger.textContent = trigger.dataset.busyLabel;
        }
        // Disable AFTER submit so the button's value still posts.
        setTimeout(function () { trigger.disabled = true; }, 0);
      }
    }

    if (kind) overlayTimer = setTimeout(function () { showOverlay(kind); }, OVERLAY_IN);
  }

  // ---- links ----
  document.addEventListener('click', function (e) {
    if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    var a = e.target.closest('a[href]');
    if (!a) return;
    var href = a.getAttribute('href');
    if (!href || href.charAt(0) === '#' || a.hasAttribute('download') ||
      /^(mailto|tel|javascript):/i.test(href)) return;
    if (a.host && a.host !== window.location.host) return;
    if (a.target === '_blank') {
      if (a.dataset.toast) toast(a.dataset.toast);
      return;
    }
    start(a.dataset.loading || null, a);
  }, true);

  // ---- forms ----
  document.addEventListener('submit', function (e) {
    var f = e.target;
    if (!f || f.tagName !== 'FORM' || e.defaultPrevented) return;
    var btn = f.querySelector('button[type=submit]:focus, input[type=submit]:focus') ||
      (document.activeElement && f.contains(document.activeElement) &&
        /^(BUTTON|INPUT)$/.test(document.activeElement.tagName) ? document.activeElement : null);
    start((btn && btn.dataset.loading) || f.dataset.loading || null, btn);
  }, true);

  // The prompt editor submits via form.submit(), which fires no submit event.
  var nativeSubmit = HTMLFormElement.prototype.submit;
  HTMLFormElement.prototype.submit = function () {
    start(this.dataset.loading || null, null);
    return nativeSubmit.apply(this, arguments);
  };

  // Restored from the back/forward cache: the page is live again, drop everything.
  window.addEventListener('pageshow', function (e) { if (e.persisted) clearAll(); });
  window.addEventListener('popstate', clearAll);
  window.addEventListener('pagehide', function () { clearInterval(clockTimer); });

  // toast() is public so other code can announce work that does not navigate.
  window.deskLoader = { start: start, clear: clearAll, toast: toast };
})();
