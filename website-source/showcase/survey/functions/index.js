'use strict';
/**
 * submitSurvey: the only way survey data reaches the database.
 *
 * The page streams every answer and click to this function while the visitor works through the survey, so a
 * session that is abandoned after one question is still kept. One Firestore document per session
 * (survey_sessions/{sid}) holds the latest answers, device summary and timings; every click is also stored as an
 * event (survey_sessions/{sid}/events/{n}) so drop-off and time per question can be analysed.
 *
 * Security model
 *  - Firestore rules deny every client read and write. Only this function (Admin SDK) writes.
 *  - Only POST from the allowed web origins, JSON only, small body.
 *  - Every field is checked against survey-schema.json (generated from questions.json): unknown questions, unknown
 *    option codes, wrong types and oversize text are rejected. Device information is a closed list of short values.
 *  - Contact details are accepted only together with the final "send", never while the visitor is still answering.
 *  - Spam: honeypot, minimum time on the final send, per-IP limits (new sessions and sync calls), a global daily cap,
 *    and a cap on events per session.
 *  - The IP address is never stored, only a salted hash used for the limits.
 */
const crypto = require('node:crypto');
const { onRequest } = require('firebase-functions/v2/https');
const logger = require('firebase-functions/logger');
const { initializeApp } = require('firebase-admin/app');
const { getFirestore, FieldValue, Timestamp } = require('firebase-admin/firestore');
const schema = require('./survey-schema.json');

initializeApp();
// A dedicated native-mode database named "survey"; the project's (default) database is left untouched.
const db = getFirestore('survey');

const ORIGINS = new Set(['https://inturp.com', 'https://www.inturp.com']);
if (process.env.ALLOW_LOCALHOST === 'true') ORIGINS.add('http://localhost:8765');
const MAX_BODY = 32 * 1024;
const MIN_FINAL_MS = Number(process.env.MIN_FILL_MS || 4000);
const LIMITS = { newSessionsPerHour: 60, newSessionsPerDay: 300, syncsPerHour: 600, globalSessionsPerDay: 3000, eventsPerSession: 500, eventsPerCall: 40 };
const EMAIL = /^[^@\s]{1,64}@[^@\s]{1,190}\.[^@\s]{2,}$/;
const PHONE = /^[0-9+\-\s().]{5,40}$/;
const SID = /^[a-f0-9]{32}$/;
const CONTROL = /[\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F]/g;
const EVENT_TYPES = new Set(['intro', 'start', 'view', 'answer', 'next', 'skip', 'back', 'submit', 'leave']);
const QIDS = new Set(schema.questions.map(q => q.id));

const fail = (res, code, error) => { logger.warn('survey rejected', { code, error }); res.status(code).json({ ok: false, error }); };
const clean = (s, max) => String(s).replace(CONTROL, '').trim().slice(0, max);
const isStr = v => typeof v === 'string';
const int = (v, min, max) => Number.isInteger(v) && v >= min && v <= max;
const visible = (q, answers) => !q.showIf || (q.showIf.in || []).includes(answers[q.showIf.id]);

const TOKEN = /^[a-z0-9_]{1,40}$/;
const ARABIC_DIGITS = { '٠': '0', '١': '1', '٢': '2', '٣': '3', '٤': '4', '٥': '5', '٦': '6', '٧': '7', '٨': '8', '٩': '9', '۰': '0', '۱': '1', '۲': '2', '۳': '3', '۴': '4', '۵': '5', '۶': '6', '۷': '7', '۸': '8', '۹': '9' };
const latinDigits = s => String(s).replace(/[٠-٩۰-۹]/g, d => ARABIC_DIGITS[d]);

/** Validates one answer. Never rejects a whole submission because of one odd value: a malformed answer is dropped, and an option that is no
 *  longer in the list (a visitor who opened an older version of the page) is kept as its plain code. Returns { value } (undefined = store nothing). */
function validateOne(q, v, { allowContact }) {
  if (v === undefined || v === null || v === '' || (Array.isArray(v) && !v.length)) return { value: undefined };
  switch (q.type) {
    case 'single':
      return isStr(v) && (q.options.includes(v) || TOKEN.test(v)) ? { value: v } : { value: undefined };
    case 'multi': {
      if (!Array.isArray(v)) return { value: undefined };
      let set = [...new Set(v.filter(x => isStr(x) && (q.options.includes(x) || TOKEN.test(x))))];
      const excl = set.filter(x => (q.exclusive || []).includes(x));
      if (set.length > 1 && excl.length) set = [excl[0]];
      if (q.max && set.length > q.max) set = set.slice(0, q.max);
      return { value: set.length ? set : undefined };
    }
    case 'scale':
      return int(v, 1, 5) ? { value: v } : { value: undefined };
    case 'short':
      return isStr(v) ? { value: clean(v, 160) } : { value: undefined };
    case 'long':
      return isStr(v) ? { value: clean(v, 2000) } : { value: undefined };
    case 'contact': {
      if (!allowContact || typeof v !== 'object' || Array.isArray(v)) return { value: undefined };
      const c = {};
      for (const f of q.fields) if (isStr(v[f]) && v[f].trim()) c[f] = clean(f === 'phone' ? latinDigits(v[f]) : v[f], 120);
      if (c.email && !EMAIL.test(c.email)) delete c.email;
      return { value: Object.keys(c).length ? c : undefined };
    }
    default:
      return { value: undefined };
  }
}

function validateAnswers(input, { allowContact }) {
  if (input === undefined) return { answers: {} };
  if (!input || typeof input !== 'object' || Array.isArray(input)) return { answers: {} };
  const byId = new Map(schema.questions.map(q => [q.id, q]));
  const out = {};
  for (const q of schema.questions) {
    const r = validateOne(q, input[q.id], { allowContact });
    if (r.error) return { error: r.error };
    if (r.value !== undefined) out[q.id] = r.value;
  }
  for (const q of schema.questions) {
    if (!visible(q, out)) { delete out[q.id]; continue; }
    if (q.required && out[q.id] === undefined) return { error: 'missing_' + q.id };
  }
  return { answers: out };
}

/** Everything the User-Agent header tells us, read on the server so a session is described even when the page could not send its own details
 *  (an in-app browser, a blocked script, a first request that failed). */
const IN_APP = [[/Snapchat\/([\d.]+)/, 'Snapchat'], [/Instagram ([\d.]+)/, 'Instagram'], [/FBAN|FBAV|FB_IAB/, 'Facebook'], [/Messenger(?:Lite)?ForiOS|FB_IAB\/MESSENGER/, 'Messenger'],
  [/TikTok|musical_ly|BytedanceWebview/, 'TikTok'], [/Line\/([\d.]+)/, 'LINE'], [/Twitter|TwitterAndroid/, 'X (Twitter)'], [/LinkedInApp/, 'LinkedIn'], [/Telegram/, 'Telegram'], [/GSA\//, 'Google app']];
function parseUa(ua) {
  ua = String(ua || '');
  const m = re => ua.match(re);
  const out = {};
  let t, os = 'Other', osVersion = '';
  if ((t = m(/Windows NT ([\d.]+)/))) { os = 'Windows'; osVersion = t[1]; }
  else if ((t = m(/(?:iPhone|iPad|iPod).*? OS ([\d_]+)/))) { os = /iPad/.test(ua) ? 'iPadOS' : 'iOS'; osVersion = t[1].replace(/_/g, '.'); }
  else if ((t = m(/Android ([\d.]+)/))) { os = 'Android'; osVersion = t[1]; }
  else if ((t = m(/Mac OS X ([\d_]+)/))) { os = 'macOS'; osVersion = t[1].replace(/_/g, '.'); }
  else if (/CrOS/.test(ua)) os = 'ChromeOS';
  else if (/Linux/.test(ua)) os = 'Linux';
  let browser = '', bv = '';
  if ((t = m(/EdgA?\/([\d.]+)/))) { browser = 'Edge'; bv = t[1]; }
  else if ((t = m(/OPR\/([\d.]+)/))) { browser = 'Opera'; bv = t[1]; }
  else if ((t = m(/SamsungBrowser\/([\d.]+)/))) { browser = 'Samsung Internet'; bv = t[1]; }
  else if ((t = m(/(?:Firefox|FxiOS)\/([\d.]+)/))) { browser = 'Firefox'; bv = t[1]; }
  else if ((t = m(/(?:Chrome|CriOS)\/([\d.]+)/))) { browser = 'Chrome'; bv = t[1]; }
  else if ((t = m(/Version\/([\d.]+).*Safari/))) { browser = 'Safari'; bv = t[1]; }
  let app = '';
  for (const [re, name] of IN_APP) if (re.test(ua)) { app = name; break; }
  if (!app && /iPhone|iPad|iPod/.test(ua) && !/Safari\//.test(ua) && /AppleWebKit/.test(ua)) app = 'In-app browser';
  else if (!app && /; wv\)/.test(ua)) app = 'In-app browser (WebView)';
  const tablet = /iPad|Tablet/i.test(ua) || (os === 'Android' && !/Mobile/i.test(ua));
  out.type = tablet ? 'tablet' : /Mobi|iPhone|iPod|Android.*Mobile/i.test(ua) ? 'mobile' : 'desktop';
  if (os !== 'Other') out.os = os;
  if (osVersion) out.osVersion = osVersion.slice(0, 14);
  if (browser) { out.browser = browser; out.browserVersion = bv.split('.')[0]; }
  if (app) out.app = app;
  const model = (m(/Android [\d.]+; ([^;)]+)/) || [])[1];
  if (model && model !== 'K') out.model = model.trim().slice(0, 40);
  else if (/iPhone/.test(ua)) out.model = 'iPhone';
  else if (/iPad/.test(ua)) out.model = 'iPad';
  return out;
}

const DEVICE_TYPES = new Set(['mobile', 'tablet', 'desktop']);
const short = (v, n) => (isStr(v) ? clean(v, n) : undefined);
/** A closed list of short, harmless values. Anything else is ignored. */
function validateDevice(d) {
  if (!d || typeof d !== 'object' || Array.isArray(d)) return undefined;
  const out = {};
  if (DEVICE_TYPES.has(d.type)) out.type = d.type;
  for (const [k, n] of [['os', 24], ['osVersion', 14], ['browser', 24], ['browserVersion', 14], ['langs', 48], ['tz', 48], ['net', 10], ['ref', 80], ['model', 40], ['app', 24]]) {
    const s = short(d[k], n); if (s) out[k] = s;
  }
  for (const k of ['screenW', 'screenH', 'viewW', 'viewH']) if (int(d[k], 0, 20000)) out[k] = d[k];
  if (typeof d.dpr === 'number' && d.dpr > 0 && d.dpr <= 8) out.dpr = Math.round(d.dpr * 100) / 100;
  if (typeof d.touch === 'boolean') out.touch = d.touch;
  if (d.theme === 'dark' || d.theme === 'light') out.theme = d.theme;
  return Object.keys(out).length ? out : undefined;
}

function validateEvents(list) {
  if (!Array.isArray(list)) return { events: [] };
  const out = [];
  for (const e of list.slice(0, LIMITS.eventsPerCall)) {
    // Tracking is secondary: a malformed or out-of-range click is skipped, it never blocks the answers.
    if (!e || typeof e !== 'object' || !int(e.n, 0, 100000) || !EVENT_TYPES.has(e.type)) continue;
    const ev = { n: e.n, t: Math.min(Math.max(Number(e.t) || 0, 0), 24 * 3600e3), type: e.type };
    if (Number.isFinite(ev.t)) ev.t = Math.round(ev.t);
    if (e.qid !== undefined) { if (!QIDS.has(e.qid) || (e.qid === 'contact' && e.type === 'answer')) continue; ev.qid = e.qid; }
    if (e.idx !== undefined && int(e.idx, 0, 100)) ev.idx = e.idx;
    if (e.ms !== undefined && Number.isFinite(e.ms)) ev.ms = Math.min(Math.max(Math.round(e.ms), 0), 6 * 3600e3);
    if (e.type === 'answer') {
      const q = e.qid && schema.questions.find(x => x.id === e.qid);
      if (!q) continue;
      const r = validateOne(q, e.v, { allowContact: false });
      if (r.value !== undefined) ev.v = r.value;
    }
    out.push(ev);
  }
  return { events: out };
}

function hashIp(ip) {
  return crypto.createHmac('sha256', process.env.IP_PEPPER || 'unset').update(String(ip || 'unknown')).digest('hex').slice(0, 40);
}

exports.submitSurvey = onRequest(
  { region: 'europe-west1', cors: false, invoker: 'public', maxInstances: 3, memory: '256MiB', timeoutSeconds: 20, concurrency: 20 },
  async (req, res) => {
    const origin = req.get('origin') || '';
    const allowed = ORIGINS.has(origin);
    if (allowed) { res.set('Access-Control-Allow-Origin', origin); res.set('Vary', 'Origin'); }
    res.set('X-Content-Type-Options', 'nosniff');
    res.set('Cache-Control', 'no-store');
    if (req.method === 'OPTIONS') {
      if (!allowed) return fail(res, 403, 'origin');
      res.set('Access-Control-Allow-Methods', 'POST, OPTIONS');
      res.set('Access-Control-Allow-Headers', 'Content-Type');
      res.set('Access-Control-Max-Age', '600');
      return res.status(204).end();
    }
    if (req.method !== 'POST') return fail(res, 405, 'method');
    if (!allowed) return fail(res, 403, 'origin');
    if (!(req.get('content-type') || '').toLowerCase().startsWith('application/json')) return fail(res, 415, 'type');
    const raw = req.rawBody ? req.rawBody.length : 0;
    if (!raw || raw > MAX_BODY) return fail(res, 413, 'size');

    const body = req.body;
    if (!body || typeof body !== 'object') return fail(res, 400, 'body');
    if (body.survey !== schema.id) return fail(res, 400, 'survey');
    if (body.lang !== 'ar' && body.lang !== 'en') return fail(res, 400, 'lang');
    if (!isStr(body.sid) || !SID.test(body.sid)) return fail(res, 400, 'sid');
    const completed = body.status === 'completed';
    if (body.status !== 'in_progress' && !completed) return fail(res, 400, 'status');

    // Bots fill the hidden field or "finish" instantly: answer "ok", store nothing.
    if ((body.hp && String(body.hp).length) || (completed && !(Number(body.elapsed_ms) >= MIN_FINAL_MS))) {
      logger.info('survey dropped', { reason: body.hp ? 'honeypot' : 'too_fast' });
      return res.status(200).json({ ok: true });
    }
    const a = validateAnswers(body.answers, { allowContact: completed });
    if (a.error) return fail(res, 400, a.error);
    const ev = validateEvents(body.events);
    if (ev.error) return fail(res, 400, ev.error);
    const device = validateDevice(body.device);
    let current;
    if (body.current && typeof body.current === 'object') {
      const qid = isStr(body.current.qid) && (QIDS.has(body.current.qid) || ['intro', 'done'].includes(body.current.qid)) ? body.current.qid : undefined;
      current = { qid, idx: int(body.current.idx, 0, 100) ? body.current.idx : undefined };
    }
    const now = Date.now();
    const day = new Date(now).toISOString().slice(0, 10);
    const ipHash = hashIp(req.get('x-forwarded-for')?.split(',')[0].trim() || req.ip);
    const ref = db.collection('survey_sessions').doc(body.sid);
    const ipRef = db.collection('survey_rate').doc(ipHash);
    const dayRef = db.collection('survey_meta').doc('day-' + day);

    try {
      const result = await db.runTransaction(async tx => {
        const [snap, ipSnap, daySnap] = await Promise.all([tx.get(ref), tx.get(ipRef), tx.get(dayRef)]);
        const r = ipSnap.exists ? ipSnap.data() : {};
        const hourStart = r.hourStart && now - r.hourStart < 3600e3 ? r.hourStart : now;
        const same = hourStart === r.hourStart;
        const dayStart = r.dayStart && now - r.dayStart < 86400e3 ? r.dayStart : now;
        const sameDay = dayStart === r.dayStart;
        const rate = {
          hourStart, dayStart,
          syncsHour: (same ? r.syncsHour || 0 : 0) + 1,
          sessHour: same ? r.sessHour || 0 : 0,
          sessDay: sameDay ? r.sessDay || 0 : 0,
        };
        if (rate.syncsHour > LIMITS.syncsPerHour) throw new Error('rate');
        const total = daySnap.exists ? daySnap.data().n || 0 : 0;
        const cur = snap.exists ? snap.data() : null;
        if (cur && cur.survey !== schema.id) throw new Error('survey');
        if (cur && cur.status === 'completed') return { ignored: true };

        if (!cur) {
          if (rate.sessHour >= LIMITS.newSessionsPerHour || rate.sessDay >= LIMITS.newSessionsPerDay || total >= LIMITS.globalSessionsPerDay) throw new Error('rate');
          rate.sessHour += 1; rate.sessDay += 1;
          tx.set(dayRef, { n: total + 1 }, { merge: true });
        }
        const lastN = cur ? cur.lastN ?? -1 : -1;
        const fresh = ev.events.filter(e => e.n > lastN && e.n < LIMITS.eventsPerSession);
        const maxN = fresh.length ? Math.max(...fresh.map(e => e.n)) : lastN;
        

        const update = {
          survey: schema.id,
          lang: body.lang,
          status: completed ? 'completed' : 'in_progress',
          answers: a.answers,
          answeredCount: Object.keys(a.answers).filter(k => k !== 'contact').length,
          hasContact: Boolean(a.answers.contact),
          lastN: maxN,
          eventsCount: (cur?.eventsCount || 0) + fresh.length,
          elapsedMs: Math.min(Math.round(Number(body.elapsed_ms) || 0), 24 * 3600e3),
          updatedAt: FieldValue.serverTimestamp(),
          ipHash,
        };
        if (body.page) update.page = clean(body.page, 80);
        if (current) { if (current.qid) update.lastQuestion = current.qid; if (current.idx !== undefined) update.lastIndex = current.idx; }
        // Client details win; the User-Agent fills whatever is missing, but only the first time a session is stored.
        if (!cur || !cur.device) update.device = { ...parseUa(req.get('user-agent')), ...(device || {}) };
        else if (device) update.device = device;
        if (!cur) { update.createdAt = FieldValue.serverTimestamp(); update.ua = clean(req.get('user-agent') || '', 200); }
        if (completed) update.completedAt = FieldValue.serverTimestamp();
        tx.set(ref, update, { merge: true });
        tx.set(ipRef, { ...rate, updatedAt: FieldValue.serverTimestamp() });
        return { fresh };
      });

      if (result.fresh && result.fresh.length) {
        const batch = db.batch();
        for (const e of result.fresh) {
          const doc = { ...e, at: Timestamp.fromMillis(now) };
          batch.set(ref.collection('events').doc(String(e.n).padStart(5, '0')), doc);
        }
        await batch.commit();
      }
      return res.status(200).json({ ok: true });
    } catch (e) {
      if (e.message === 'rate') return fail(res, 429, 'rate');
      if (e.message === 'survey') return fail(res, 400, 'survey');
      logger.error('sync failed', e);
      return fail(res, 500, 'server');
    }
  }
);

if (process.env.SURVEY_TEST) Object.assign(exports, { _validateAnswers: validateAnswers, _validateEvents: validateEvents, _validateDevice: validateDevice, _parseUa: parseUa });
