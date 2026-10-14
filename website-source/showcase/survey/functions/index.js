'use strict';
/**
 * submitSurvey: the only way answers reach the database.
 *
 * Security model
 *  - Firestore rules deny every client read and write. Only this function (Admin SDK) writes.
 *  - Only POST from the allowed web origins, JSON only, small body.
 *  - Every field is checked against survey-schema.json (generated from questions.json): unknown questions,
 *    unknown option codes, wrong types and oversize text are rejected; required visible questions must be answered.
 *  - Spam: hidden honeypot field, minimum time spent, per-IP limits (hour and day) and a global daily cap.
 *  - The IP address is never stored, only a salted hash used for the limits.
 */
const crypto = require('node:crypto');
const { onRequest } = require('firebase-functions/v2/https');
const logger = require('firebase-functions/logger');
const { initializeApp } = require('firebase-admin/app');
const { getFirestore, FieldValue } = require('firebase-admin/firestore');
const schema = require('./survey-schema.json');

initializeApp();
// A dedicated native-mode database named "survey"; the project's (default) database is left untouched.
const db = getFirestore('survey');

const ORIGINS = new Set(['https://inturp.com', 'https://www.inturp.com']);
if (process.env.ALLOW_LOCALHOST === 'true') ORIGINS.add('http://localhost:8765');
const MAX_BODY = 24 * 1024;
const MIN_MS = Number(process.env.MIN_FILL_MS || 12000);
const LIMITS = { perHour: 4, perDay: 12, globalPerDay: 3000 };
const EMAIL = /^[^@\s]{1,64}@[^@\s]{1,190}\.[^@\s]{2,}$/;
const CONTROL = /[\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F]/g;

const fail = (res, code, error) => { res.status(code).json({ ok: false, error }); };
const clean = (s, max) => String(s).replace(CONTROL, '').trim().slice(0, max);
const isStr = v => typeof v === 'string';

function visible(q, answers) {
  return !q.showIf || (q.showIf.in || []).includes(answers[q.showIf.id]);
}

/** Returns { answers } with sanitized values, or { error } */
function validate(input) {
  if (!input || typeof input !== 'object' || Array.isArray(input)) return { error: 'answers' };
  const byId = new Map(schema.questions.map(q => [q.id, q]));
  for (const k of Object.keys(input)) if (!byId.has(k)) return { error: 'unknown_question' };
  const out = {};
  for (const q of schema.questions) {
    const v = input[q.id];
    if (v === undefined || v === null || v === '' || (Array.isArray(v) && !v.length)) continue;
    switch (q.type) {
      case 'single':
        if (!isStr(v) || !q.options.includes(v)) return { error: 'bad_option' };
        out[q.id] = v; break;
      case 'multi': {
        if (!Array.isArray(v) || v.length > q.options.length) return { error: 'bad_multi' };
        const set = [...new Set(v)];
        if (set.some(x => !isStr(x) || !q.options.includes(x))) return { error: 'bad_option' };
        if (q.max && set.length > q.max) return { error: 'too_many' };
        if (set.length > 1 && set.some(x => (q.exclusive || []).includes(x))) return { error: 'exclusive' };
        out[q.id] = set; break;
      }
      case 'scale':
        if (!Number.isInteger(v) || v < 1 || v > 5) return { error: 'bad_scale' };
        out[q.id] = v; break;
      case 'short':
        if (!isStr(v)) return { error: 'bad_text' };
        out[q.id] = clean(v, 160); break;
      case 'long':
        if (!isStr(v)) return { error: 'bad_text' };
        out[q.id] = clean(v, 2000); break;
      case 'contact': {
        if (typeof v !== 'object' || Array.isArray(v)) return { error: 'bad_contact' };
        const allowed = new Set([...q.fields, 'consent']);
        for (const k of Object.keys(v)) if (!allowed.has(k)) return { error: 'bad_contact' };
        const c = {};
        for (const f of q.fields) if (isStr(v[f]) && v[f].trim()) c[f] = clean(v[f], 120);
        if (c.email && !EMAIL.test(c.email)) return { error: 'bad_email' };
        if (Object.keys(c).length) {
          if (v.consent !== true) return { error: 'no_consent' };
          c.consent = true;
        }
        if (Object.keys(c).length) out[q.id] = c;
        break;
      }
      default: return { error: 'schema' };
    }
  }
  for (const q of schema.questions) {
    if (!visible(q, out)) { delete out[q.id]; continue; }
    if (q.required && out[q.id] === undefined) return { error: 'missing_' + q.id };
  }
  return { answers: out };
}

function hashIp(ip) {
  return crypto.createHmac('sha256', process.env.IP_PEPPER || 'unset').update(String(ip || 'unknown')).digest('hex').slice(0, 40);
}

/** Per-IP and global limits, atomically. Throws 'rate' when exceeded. */
async function checkLimits(ipHash) {
  const now = Date.now();
  const day = new Date(now).toISOString().slice(0, 10);
  const ipRef = db.collection('survey_rate').doc(ipHash);
  const dayRef = db.collection('survey_meta').doc('day-' + day);
  await db.runTransaction(async tx => {
    const [ipSnap, daySnap] = await Promise.all([tx.get(ipRef), tx.get(dayRef)]);
    const r = ipSnap.exists ? ipSnap.data() : {};
    const hourStart = r.hourStart && now - r.hourStart < 3600e3 ? r.hourStart : now;
    const hourN = hourStart === r.hourStart ? (r.hourN || 0) : 0;
    const dayStart = r.dayStart && now - r.dayStart < 86400e3 ? r.dayStart : now;
    const dayN = dayStart === r.dayStart ? (r.dayN || 0) : 0;
    const total = daySnap.exists ? (daySnap.data().n || 0) : 0;
    if (hourN >= LIMITS.perHour || dayN >= LIMITS.perDay || total >= LIMITS.globalPerDay) throw new Error('rate');
    tx.set(ipRef, { hourStart, hourN: hourN + 1, dayStart, dayN: dayN + 1, updatedAt: FieldValue.serverTimestamp() });
    tx.set(dayRef, { n: total + 1 }, { merge: true });
  });
}

if (process.env.SURVEY_TEST) exports._validate = validate;

exports.submitSurvey = onRequest(
  { region: 'europe-west1', cors: false, invoker: 'public', maxInstances: 3, memory: '256MiB', timeoutSeconds: 15, concurrency: 20 },
  async (req, res) => {
    const origin = req.get('origin') || '';
    const allowed = ORIGINS.has(origin);
    if (allowed) {
      res.set('Access-Control-Allow-Origin', origin);
      res.set('Vary', 'Origin');
    }
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
    // Bots fill the hidden field or finish too fast: answer "ok" and store nothing.
    if ((body.hp && String(body.hp).length) || !(Number(body.elapsed_ms) >= MIN_MS)) {
      logger.info('survey dropped', { reason: body.hp ? 'honeypot' : 'too_fast' });
      return res.status(200).json({ ok: true });
    }
    const v = validate(body.answers);
    if (v.error) return fail(res, 400, v.error);
    if (!Object.keys(v.answers).length) return fail(res, 400, 'empty');

    const ipHash = hashIp(req.get('x-forwarded-for')?.split(',')[0].trim() || req.ip);
    try {
      await checkLimits(ipHash);
    } catch (e) {
      if (e.message === 'rate') return fail(res, 429, 'rate');
      logger.error('limit check failed', e);
      return fail(res, 500, 'server');
    }
    try {
      await db.collection('survey_responses').add({
        survey: schema.id,
        lang: body.lang,
        answers: v.answers,
        page: clean(body.page || '', 80),
        elapsedMs: Math.min(Math.round(Number(body.elapsed_ms)), 6 * 3600e3),
        ipHash,
        createdAt: FieldValue.serverTimestamp(),
      });
      return res.status(200).json({ ok: true });
    } catch (e) {
      logger.error('write failed', e);
      return fail(res, 500, 'server');
    }
  }
);
