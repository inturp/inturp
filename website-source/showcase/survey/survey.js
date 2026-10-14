/* Clinic survey — one question at a time. No dependencies.
   Reads the questions from #sv-data (already in the page language) and the destination from window.SURVEY_CONFIG. */
(() => {
  'use strict';
  const $ = (s, r = document) => r.querySelector(s);
  const root = document.documentElement;
  const DATA = JSON.parse($('#sv-data').textContent);
  const CFG = Object.assign({ endpoint: '', transport: 'json', email: 'info@inturp.com' }, window.SURVEY_CONFIG || {});
  const UI = DATA.ui;
  const card = $('#svCard'), nav = $('#svNav'), bar = $('#svBar'), top = $('.sv-top');
  const backBtn = $('#svBack'), nextBtn = $('#svNext');
  const store = {
    get: k => { try { return localStorage.getItem(k); } catch (_) { return null; } },
    set: (k, v) => { try { localStorage.setItem(k, v); } catch (_) {} },
    del: k => { try { localStorage.removeItem(k); } catch (_) {} },
  };
  const DRAFT = 'inturp-survey-draft-' + DATA.id;
  const answers = {};
  let idx = -1, busy = false, sent = false, startedAt = Date.now();
  try { Object.assign(answers, JSON.parse(store.get(DRAFT) || '{}').answers || {}); } catch (_) {}
  // A saved draft from an older version of the questions may hold options that no longer exist: drop those values.
  DATA.questions.forEach(q => {
    if (!q.options || answers[q.id] == null) return;
    const ok = new Set(q.options.map(o => o.v)), v = answers[q.id];
    if (Array.isArray(v)) { const f = v.filter(x => ok.has(x)); if (f.length) answers[q.id] = f; else delete answers[q.id]; }
    else if (!ok.has(v)) delete answers[q.id];
  });

  /* theme + language buttons (same behaviour as the other pages) */
  document.querySelectorAll('[data-theme-toggle]').forEach(b => b.addEventListener('click', () => {
    const dark = !root.classList.contains('dark');
    root.classList.toggle('dark', dark); root.style.colorScheme = dark ? 'dark' : 'light';
    store.set('inturp-theme', dark ? 'dark' : 'light');
  }));
  document.querySelectorAll('[data-lang-toggle]').forEach(b => b.addEventListener('click', () => {
    const other = root.lang === 'ar' ? 'en' : 'ar';
    const twin = $(`link[rel="alternate"][hreflang="${other}"]`);
    store.set('inturp-lang', other);
    if (twin) location.assign(new URL(twin.href).pathname + location.hash);
  }));
  const pm = $('#pm-btn'), pmMenu = $('#product-links');
  if (pm && pmMenu) {
    const set = o => { pm.setAttribute('aria-expanded', String(o)); pmMenu.hidden = !o; };
    pm.addEventListener('click', () => set(pm.getAttribute('aria-expanded') !== 'true'));
    document.addEventListener('pointerdown', e => { if (!e.target.closest('.product-menu')) set(false); });
  }
  const mb = $('.mobile-toggle'), mp = $('#mnav');
  if (mb && mp) {
    mb.addEventListener('click', () => { const o = mb.getAttribute('aria-expanded') !== 'true'; mb.setAttribute('aria-expanded', String(o)); mp.hidden = !o; });
  }

  /* helpers */
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const visible = () => DATA.questions.filter(q => !q.showIf || (q.showIf.in || []).includes(answers[q.showIf.id]));
  const empty = v => v == null || v === '' || (Array.isArray(v) && !v.length);
  const letter = i => String.fromCharCode(65 + i);
  const CHECK = '<svg class="ck" viewBox="0 0 24 24" aria-hidden="true"><path d="m5 12.5 4.5 4.5L19 7"/></svg>';
  const saveDraft = () => { store.set(DRAFT, JSON.stringify({ answers })); if (typeof syncNext === 'function' && idx >= 0 && !nav.hidden) syncNext(); };

  function setProgress() {
    const vis = visible();
    const pos = idx < 0 ? 0 : Math.min(idx + 1, vis.length);
    bar.style.width = (idx < 0 ? 0 : idx >= vis.length ? 100 : (pos - 1) / vis.length * 100 + 100 / vis.length * 0.35) + '%';
    top.classList.toggle('on', idx >= 0);
  }
  function swap(html, dir) {
    card.classList.remove('swap', 'back');
    if (idx >= 0) card.classList.remove('wide');
    void card.offsetWidth;
    card.innerHTML = html;
    if (dir < 0) card.classList.add('back');
    card.classList.add('swap');
    scrollTo({ top: 0, behavior: 'instant' });
  }
  function setNav(show, last) {
    nav.hidden = !show;
    backBtn.disabled = idx <= 0;
    nav.dataset.last = last ? '1' : '';
    syncNext();
  }
  function syncNext() {
    const q = visible()[idx];
    const last = nav.dataset.last === '1';
    const answered = q && !empty(answers[q.id]) && !(q.type === 'contact' && !Object.values(answers[q.id]).some(x => x && x !== true));
    nextBtn.querySelector('.lbl').textContent = last ? UI.send : (answered ? UI.next : UI.skip);
    nextBtn.classList.toggle('is-skip', !last && !answered);
  }


  /* ── session tracking ────────────────────────────────────────────────────────────────────────────────
     Every answer and click is sent as it happens, so a visitor who stops after one question is still kept.
     Contact details are the exception: they are sent only with the final "send". */
  const TRACK = Boolean(CFG.endpoint) && CFG.transport !== 'script';
  const SESS_KEY = 'inturp-survey-session';
  const newSid = () => { const b = new Uint8Array(16); (window.crypto || {}).getRandomValues ? crypto.getRandomValues(b) : b.forEach((_, i) => { b[i] = Math.random() * 256; }); return [...b].map(x => x.toString(16).padStart(2, '0')).join(''); };
  let sess = null;
  try { sess = JSON.parse(store.get(SESS_KEY) || 'null'); } catch (_) {}
  if (!sess || !sess.sid || Date.now() - sess.t0 > 12 * 3600e3) sess = { sid: newSid(), t0: Date.now(), n: 0, deviceSent: false };
  const persist = () => store.set(SESS_KEY, JSON.stringify(sess));
  let queue = [], timer = null, inflight = false, trackingOn = TRACK, qStart = Date.now();

  function deviceInfo() {
    const ua = navigator.userAgent || '';
    const m = (re) => { const r = ua.match(re); return r ? r : null; };
    let os = 'Other', osVersion = '', t;
    if ((t = m(/Windows NT ([\d.]+)/))) { os = 'Windows'; osVersion = t[1]; }
    else if ((t = m(/(?:iPhone|iPad|iPod).*? OS ([\d_]+)/))) { os = 'iOS'; osVersion = t[1].replace(/_/g, '.'); }
    else if ((t = m(/Android ([\d.]+)/))) { os = 'Android'; osVersion = t[1]; }
    else if ((t = m(/Mac OS X ([\d_]+)/))) { os = (navigator.maxTouchPoints > 1) ? 'iPadOS' : 'macOS'; osVersion = t[1].replace(/_/g, '.'); }
    else if (/CrOS/.test(ua)) os = 'ChromeOS';
    else if (/Linux/.test(ua)) os = 'Linux';
    let browser = 'Other', bv = '';
    if ((t = m(/EdgA?\/([\d.]+)/))) { browser = 'Edge'; bv = t[1]; }
    else if ((t = m(/OPR\/([\d.]+)/))) { browser = 'Opera'; bv = t[1]; }
    else if ((t = m(/SamsungBrowser\/([\d.]+)/))) { browser = 'Samsung Internet'; bv = t[1]; }
    else if ((t = m(/(?:Firefox|FxiOS)\/([\d.]+)/))) { browser = 'Firefox'; bv = t[1]; }
    else if ((t = m(/(?:Chrome|CriOS)\/([\d.]+)/))) { browser = 'Chrome'; bv = t[1]; }
    else if ((t = m(/Version\/([\d.]+).*Safari/))) { browser = 'Safari'; bv = t[1]; }
    const tablet = /iPad|Tablet/i.test(ua) || os === 'iPadOS' || (os === 'Android' && !/Mobile/i.test(ua));
    const mobile = /Mobi|iPhone|iPod|Android.*Mobile/i.test(ua);
    const model = (m(/Android [\d.]+; ([^;)]+)/) || [])[1];
    let ref = '';
    try { ref = document.referrer ? new URL(document.referrer).host : ''; } catch (_) {}
    const conn = navigator.connection && navigator.connection.effectiveType;
    return {
      type: tablet ? 'tablet' : mobile ? 'mobile' : 'desktop', os, osVersion, browser, browserVersion: bv.split('.')[0], model,
      screenW: screen.width, screenH: screen.height, viewW: innerWidth, viewH: innerHeight, dpr: window.devicePixelRatio || 1,
      touch: (navigator.maxTouchPoints || 0) > 0, langs: (navigator.languages || [navigator.language || '']).join(',').slice(0, 48),
      tz: (Intl.DateTimeFormat().resolvedOptions().timeZone || '').slice(0, 48), net: conn || '', ref,
      theme: root.classList.contains('dark') ? 'dark' : 'light',
    };
  }
  const curQid = () => (idx < 0 ? 'intro' : (visible()[idx] ? visible()[idx].id : 'done'));
  const dwell = () => { const ms = Math.min(Date.now() - qStart, 3600e3); qStart = Date.now(); return ms; };
  function snapshot(final) {
    const a = {};
    Object.keys(answers).forEach(k => { if (k === 'contact' && !final) return; if (!empty(answers[k])) a[k] = answers[k]; });
    return a;
  }
  function track(type, extra) {
    if (!trackingOn) return;
    queue.push(Object.assign({ n: sess.n++, t: Date.now() - sess.t0, type }, extra || {}));
    persist(); clearTimeout(timer); timer = setTimeout(() => flush(), 1200);
  }
  function buildBody(final, events) {
    const hp = $('#svHp');
    const body = {
      survey: DATA.id, lang: root.lang, sid: sess.sid, status: final ? 'completed' : 'in_progress', page: location.pathname,
      elapsed_ms: final ? Date.now() - startedAt : Date.now() - sess.t0, hp: hp ? hp.value : '',
      current: { qid: curQid(), idx: idx >= 0 ? idx : undefined }, answers: snapshot(final), events,
    };
    if (!sess.deviceSent) body.device = deviceInfo();
    return body;
  }

  /* A finished survey is never lost: if the final send cannot get through, the answers wait in this browser and are sent again
     quietly (when the page is opened again, when the connection returns, and every half minute) while the visitor sees "done". */
  const OUTBOX = 'inturp-survey-outbox';
  async function retryOutbox() {
    const raw = store.get(OUTBOX); if (!raw || !CFG.endpoint || CFG.transport === 'script') return;
    try {
      const res = await fetch(CFG.endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: raw, credentials: 'omit', keepalive: raw.length < 60000 });
      if (res.ok || (res.status >= 400 && res.status < 500 && res.status !== 429)) store.del(OUTBOX);
    } catch (_) {}
  }
  window.addEventListener('online', retryOutbox);
  setInterval(retryOutbox, 30000);
  setTimeout(retryOutbox, 1500);

  async function flush(opts) {
    const final = !!(opts && opts.final), keepalive = !!(opts && opts.keepalive);
    if (!trackingOn && !final) return true;
    if (inflight && !final) { clearTimeout(timer); timer = setTimeout(() => flush(), 800); return true; }
    clearTimeout(timer);
    const events = queue.slice(0, 40);
    const body = buildBody(final, events);
    inflight = true;
    try {
      const res = await fetch(CFG.endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body), credentials: 'omit', keepalive });
      if (res.status === 429) { trackingOn = false; return !final ? true : false; }
      if (!res.ok) return false;
      queue.splice(0, events.length); sess.deviceSent = true; persist();
      if (queue.length && !final) { timer = setTimeout(() => flush(), 300); }
      return true;
    } catch (_) {
      return false;
    } finally { inflight = false; }
  }
  document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'hidden') {
      if (idx < 0 || idx < visible().length) track('leave', { qid: curQid() === 'intro' ? undefined : curQid(), idx: idx >= 0 ? idx : undefined, ms: dwell() });
      flush({ keepalive: true });
    } else qStart = Date.now();
  });
  addEventListener('pagehide', () => { if (queue.length) flush({ keepalive: true }); });

  /* screens */
  function renderIntro() {
    idx = -1; setProgress(); setNav(false);
    const I = DATA.intro;
    swap(`<section class="sv-intro"><div class="sv-intro-copy">
      <span class="eyebrow"><i class="status-dot"></i>${esc(I.eyebrow)}</span>
      <h1>${esc(I.title)}</h1>
      <p class="lead">${esc(I.lead)}</p>
      <div class="sv-chips">
        <span class="sv-chip"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>${esc(UI.minutes)}</span>
        <span class="sv-chip"><svg viewBox="0 0 24 24"><rect x="5" y="10.5" width="14" height="9.5" rx="2"/><path d="M8 10.5V8a4 4 0 0 1 8 0v2.5"/></svg>${esc(UI.private)}</span>
      </div>
      <div class="sv-start"><button type="button" class="btn btn-solid" id="svGo">${esc(I.start)}</button><p class="sv-note">${esc(I.note)}</p></div>
    </div></section>`, 1);
    $('#svGo').addEventListener('click', () => { startedAt = Date.now(); track('start'); go(0, 1); });
  }

  function optionsHtml(q) {
    const two = '';
    const sel = answers[q.id];
    return `<div class="sv-opts${two}" role="${q.type === 'multi' ? 'group' : 'radiogroup'}" aria-label="${esc(q.q)}">` + q.options.map((o, i) => {
      const on = q.type === 'multi' ? (sel || []).includes(o.v) : sel === o.v;
      return `<button type="button" class="sv-opt" role="${q.type === 'multi' ? 'checkbox' : 'radio'}" aria-checked="${on}" data-v="${esc(o.v)}"><span class="ind" aria-hidden="true">${CHECK}</span><span class="t">${esc(o.label)}</span></button>`;
    }).join('') + '</div>' + (q.type === 'multi' && q.max ? `<p class="sv-count" id="svCount"></p>` : '');
  }

  function bodyHtml(q) {
    const v = answers[q.id];
    switch (q.type) {
      case 'single': case 'multi': return optionsHtml(q);
      case 'scale': return `<div class="sv-scale" role="radiogroup" aria-label="${esc(q.q)}">${[1, 2, 3, 4, 5].map(n => `<button type="button" role="radio" aria-checked="${v === n}" data-v="${n}">${n}</button>`).join('')}</div>
        <div class="sv-scale-labels"><span>${esc(q.min_label)}</span><span>${esc(q.max_label)}</span></div>`;
      case 'short': return `<input class="sv-input" id="svIn" type="text" maxlength="160" placeholder="${esc(q.placeholder || '')}" value="${esc(v || '')}" autocomplete="off">`;
      case 'long': return `<textarea class="sv-text" id="svIn" maxlength="2000" placeholder="${esc(q.placeholder || '')}">${esc(v || '')}</textarea>`;
      case 'contact': {
        const c = v || {};
        return `<div class="sv-fields">${q.fields.map(f => `<label>${esc(f.label)}<input class="sv-input" type="${f.type}" data-f="${f.id}" autocomplete="${f.autocomplete || 'off'}" maxlength="120"${f.type === 'tel' ? ' inputmode="tel"' : ''} value="${esc(c[f.id] || '')}"></label>`).join('')}</div>
        ${q.consent ? `<label class="sv-consent"><input type="checkbox" id="svConsent" ${c.consent ? 'checked' : ''}><span>${esc(q.consent)}</span></label>` : ''}
        <input class="sv-hp" type="text" name="website" id="svHp" tabindex="-1" autocomplete="off" aria-hidden="true">`;
      }
    }
    return '';
  }

  function renderQuestion(dir) {
    const vis = visible(), q = vis[idx];
    setProgress(); setNav(true, idx === vis.length - 1);
    const num = String(idx + 1).padStart(2, '0'), tot = String(vis.length).padStart(2, '0');
    swap(`<section aria-labelledby="svQ">
      <div class="sv-meta"><b>${num} / ${tot}</b><i></i><span>${esc(q.section)}</span></div>
      <h2 class="sv-q" id="svQ">${esc(q.q)}</h2>
      ${q.hint ? `<p class="sv-hint">${esc(q.hint)}</p>` : ''}
      <div class="sv-body">${bodyHtml(q)}</div>
      <p class="sv-err" id="svErr" role="alert"></p>
    </section>`, dir);
    qStart = Date.now(); track('view', { qid: q.id, idx });
    bind(q);
    const f = card.querySelector('#svIn, [data-f="name"]');
    if (f) setTimeout(() => f.focus({ preventScroll: true }), 120);
  }

  function updateCount(q) {
    const el = $('#svCount'); if (!el) return;
    const n = (answers[q.id] || []).length;
    el.textContent = UI.upto.replace('{n}', q.max) + ' · ' + UI.selected.replace('{n}', n);
    card.querySelectorAll('.sv-opt').forEach(b => {
      const on = b.getAttribute('aria-checked') === 'true';
      const ex = q.options.find(o => o.v === b.dataset.v);
      b.setAttribute('aria-disabled', String(!on && n >= q.max && !(ex && ex.exclusive)));
    });
  }

  function bind(q) {
    const err = $('#svErr');
    if (q.type === 'single') {
      card.querySelectorAll('.sv-opt').forEach(b => b.addEventListener('click', () => {
        answers[q.id] = b.dataset.v; saveDraft(); track('answer', { qid: q.id, v: answers[q.id] });
        card.querySelectorAll('.sv-opt').forEach(x => x.setAttribute('aria-checked', String(x === b)));
        err.textContent = '';
        clearTimeout(bind.t); bind.t = setTimeout(() => next(), 380);
      }));
    } else if (q.type === 'multi') {
      card.querySelectorAll('.sv-opt').forEach(b => b.addEventListener('click', () => {
        if (b.getAttribute('aria-disabled') === 'true') return;
        const cur = new Set(answers[q.id] || []);
        const excl = new Set(q.options.filter(o => o.exclusive).map(o => o.v));
        if (cur.has(b.dataset.v)) cur.delete(b.dataset.v);
        else if (excl.has(b.dataset.v)) { cur.clear(); cur.add(b.dataset.v); } // "none of these" stands alone
        else { excl.forEach(x => cur.delete(x)); cur.add(b.dataset.v); }
        answers[q.id] = [...cur]; saveDraft(); track('answer', { qid: q.id, v: answers[q.id] });
        card.querySelectorAll('.sv-opt').forEach(x => x.setAttribute('aria-checked', String(cur.has(x.dataset.v))));
        err.textContent = ''; updateCount(q);
      }));
      updateCount(q);
    } else if (q.type === 'scale') {
      card.querySelectorAll('[data-v]').forEach(b => b.addEventListener('click', () => {
        answers[q.id] = Number(b.dataset.v); saveDraft(); track('answer', { qid: q.id, v: answers[q.id] });
        card.querySelectorAll('[data-v]').forEach(x => x.setAttribute('aria-checked', String(x === b)));
        err.textContent = '';
        clearTimeout(bind.t); bind.t = setTimeout(() => next(), 380);
      }));
    } else if (q.type === 'short' || q.type === 'long') {
      $('#svIn').addEventListener('input', e => { answers[q.id] = e.target.value; saveDraft(); err.textContent = ''; });
      $('#svIn').addEventListener('change', e => track('answer', { qid: q.id, v: String(e.target.value || '').slice(0, 2000) }));
    } else if (q.type === 'contact') {
      card.querySelectorAll('[data-f]').forEach(i => i.addEventListener('input', () => {
        const c = Object.assign({}, answers[q.id]); c[i.dataset.f] = i.value; answers[q.id] = c; saveDraft();
      }));
      const cb = $('#svConsent'); if (cb) cb.addEventListener('change', e => { answers[q.id] = Object.assign({}, answers[q.id], { consent: e.target.checked }); saveDraft(); });
    }
  }

  function validate(q) {
    const v = answers[q.id];
    const required = q.required !== false;
    if (q.type === 'short' || q.type === 'long') { if (required && !String(v || '').trim()) return UI.needText; }
    else if (q.type === 'contact') {
      const c = v || {};
      if (c.email && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(c.email)) return UI.badEmail;
      if (q.consent && (c.name || c.clinic || c.phone || c.email || c.address) && !c.consent) return UI.needConsent;
    } else if (required && empty(v)) return UI.needChoice;
    return '';
  }
  function fail(msg) {
    const e = $('#svErr'); e.textContent = msg; e.classList.remove('shake'); void e.offsetWidth; e.classList.add('shake');
  }

  /* navigation */
  function go(i, dir) {
    idx = i; renderQuestion(dir);
  }
  function next() {
    if (busy || idx < 0) return;
    const vis = visible(), q = vis[idx];
    const msg = validate(q);
    if (msg) return fail(msg);
    const answered = !empty(answers[q.id]) && !(q.type === 'contact' && !Object.values(answers[q.id]).some(x => x && x !== true));
    track(answered ? 'next' : 'skip', { qid: q.id, idx, ms: dwell() });
    if (idx >= vis.length - 1) return submit();
    go(idx + 1, 1);
  }
  function prev() { if (idx > 0) { const q = visible()[idx]; track('back', { qid: q.id, idx, ms: dwell() }); go(idx - 1, -1); } }
  nextBtn.addEventListener('click', next);
  backBtn.addEventListener('click', prev);

  /* keyboard: letters pick options, numbers pick scale values, Enter continues */
  document.addEventListener('keydown', e => {
    if (idx < 0 || e.metaKey || e.ctrlKey || e.altKey) return;
    const q = visible()[idx]; if (!q) return;
    const tag = (e.target.tagName || '').toLowerCase();
    if (e.key === 'Enter') {
      if (tag === 'textarea' && !e.shiftKey) { /* long answers: Enter makes a new line */ return; }
      if (tag === 'button' && e.target.closest('.sv-opts,.sv-scale')) return;
      e.preventDefault(); next(); return;
    }
    if (tag === 'input' || tag === 'textarea') return;
    if (q.type === 'single' || q.type === 'multi') {
      const i = e.key.length === 1 ? e.key.toUpperCase().charCodeAt(0) - 65 : -1;
      const b = card.querySelectorAll('.sv-opt')[i]; if (b) { e.preventDefault(); b.click(); }
    } else if (q.type === 'scale' && /^[1-5]$/.test(e.key)) {
      const b = card.querySelector(`[data-v="${e.key}"]`); if (b) b.click();
    }
  });

  /* result */
  function labelOf(q, v) {
    const o = (q.options || []).find(x => x.v === v);
    return o ? o.label : v;
  }
  function summary() {
    const lines = [];
    DATA.questions.forEach(q => {
      const v = answers[q.id]; if (empty(v)) return;
      let t;
      if (q.type === 'multi') t = v.map(x => labelOf(q, x)).join(', ');
      else if (q.type === 'single') t = labelOf(q, v);
      else if (q.type === 'contact') t = Object.entries(v).filter(([, x]) => x && x !== true).map(([k, x]) => k + ': ' + x).join(' | ') + (v.consent ? ' (OK to contact)' : '');
      else t = String(v);
      lines.push(q.q + '\n  → ' + t);
    });
    return lines.join('\n');
  }
  function payload() {
    const hp = $('#svHp');
    return { survey: DATA.id, lang: root.lang, submitted_at: new Date().toISOString(), page: location.pathname,
      elapsed_ms: Date.now() - startedAt, hp: hp ? hp.value : '', answers };
  }

  async function submit() {
    const any = Object.values(answers).some(v => !empty(v) && !(typeof v === 'object' && !Array.isArray(v) && !Object.values(v).some(x => x && x !== true)));
    if (!any) return fail(UI.needAny);
    const hp = $('#svHp'); if (hp && hp.value) return renderDone(); // bots fill the hidden field
    if (!CFG.endpoint) return renderFallback();
    busy = true; nextBtn.disabled = true;
    nextBtn.querySelector('.lbl').insertAdjacentHTML('beforebegin', '<span class="sv-spin"></span>');
    try {
      let ok;
      if (CFG.transport === 'script') { // Google Apps Script web app: opaque no-cors request
        await fetch(CFG.endpoint, { method: 'POST', mode: 'no-cors', headers: { 'Content-Type': 'text/plain;charset=utf-8' }, body: JSON.stringify(payload()) });
        ok = true;
      } else {
        track('submit', { qid: curQid(), idx });
        for (let i = 0; i < 6 && queue.length > 40; i++) await flush();
        ok = await flush({ final: true });
        // The answers matter more than the click log: if the send was refused, try once more without the queued clicks.
        if (!ok) { queue.length = 0; ok = await flush({ final: true }); }
      }
      if (!ok) { // keep the answers safe in this browser and finish normally; they are sent again in the background
        const b = buildBody(true, []); store.set(OUTBOX, JSON.stringify(b)); setTimeout(retryOutbox, 4000);
      }
      sent = true; store.del(DRAFT); store.del(SESS_KEY); trackingOn = false;
      renderDone();
    } catch (_) {
      try { store.set(OUTBOX, JSON.stringify(buildBody(true, []))); setTimeout(retryOutbox, 4000); } catch (_) {}
      sent = true; store.del(DRAFT); store.del(SESS_KEY); trackingOn = false;
      renderDone();
    } finally {
      busy = false; nextBtn.disabled = false; const s = nav.querySelector('.sv-spin'); if (s) s.remove();
    }
  }

  function doneHtml(extra) {
    const D = DATA.done;
    return `<section class="sv-done">
      <div class="sv-badge"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m5 12.5 4.5 4.5L19 7"/></svg></div>
      <h2>${esc(D.title)}</h2><p class="lead">${esc(D.lead)}</p>
      ${extra || ''}
      <div class="sv-next"><h3>${esc(D.next_title)}</h3><ul>${D.next.map(t => `<li>${esc(t)}</li>`).join('')}</ul></div>
      <div class="sv-actions"><button type="button" class="btn btn-outline" id="svShare">${esc(D.share)}</button><a class="btn btn-solid" href="${esc(D.home_href)}">${esc(D.home)}</a></div>
    </section>`;
  }
  function bindShare() {
    const b = $('#svShare'); if (!b) return;
    b.addEventListener('click', async () => {
      const url = location.origin + location.pathname;
      try { if (navigator.share) { await navigator.share({ title: document.title, url }); return; } } catch (_) { return; }
      try { await navigator.clipboard.writeText(url); b.textContent = UI.copied; } catch (_) {}
    });
  }
  function renderDone() {
    idx = visible().length; setProgress(); setNav(false);
    swap(doneHtml(''), 1); bindShare();
  }
  function renderFallback(failed) {
    idx = visible().length; setProgress(); setNav(false);
    const text = summary();
    const subject = UI.mailSubject, body = UI.mailIntro + '\n\n' + text;
    swap(`<section class="sv-done">
      <div class="sv-badge"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m5 12.5 4.5 4.5L19 7"/></svg></div>
      <h2>${esc(UI.lastTitle)}</h2><p class="lead">${esc(failed ? UI.failLead : UI.lastLead)}</p>
      <div class="sv-fallback"><p>${esc(UI.lastHow)}</p>
        <div class="row"><a class="btn btn-solid" id="svMail" href="mailto:${esc(CFG.email)}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body.slice(0, 1700))}">${esc(UI.openMail)}</a>
        <button type="button" class="btn btn-outline" id="svCopy">${esc(UI.copy)}</button></div></div>
    </section>`, 1);
    $('#svCopy').addEventListener('click', async e => {
      try { await navigator.clipboard.writeText(subject + '\n\n' + text); e.target.textContent = UI.copied; store.del(DRAFT); } catch (_) {}
    });
    $('#svMail').addEventListener('click', () => store.del(DRAFT));
  }

  renderIntro();
  if (!sess.n) track('intro');
  const y = $('#year'); if (y) y.textContent = new Date().getFullYear();
})();
