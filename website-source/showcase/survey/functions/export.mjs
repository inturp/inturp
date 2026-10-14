// Exports the survey to two CSV files next to this script:
//   survey-sessions.csv  one row per visitor session: status, device, how far they got, every answer, contact details
//   survey-events.csv    one row per click/view/answer, with the time spent on each question
//
//   gcloud auth application-default login     (once)
//   npm install && node export.mjs
import { initializeApp, applicationDefault } from 'firebase-admin/app';
import { getFirestore } from 'firebase-admin/firestore';
import { writeFileSync } from 'node:fs';

initializeApp({ credential: applicationDefault(), projectId: 'vet-charted' });
const db = getFirestore('survey');
const cell = v => '"' + String(v ?? '').replace(/"/g, '""') + '"';
const csv = (head, rows) => '﻿' + [head.map(cell).join(','), ...rows.map(r => r.map(cell).join(','))].join('\n');
const iso = t => (t && t.toDate ? t.toDate().toISOString() : '');

const snap = await db.collection('survey_sessions').orderBy('createdAt').get();
const sessions = snap.docs.map(d => ({ id: d.id, ...d.data() }));
const qids = [...new Set(sessions.flatMap(s => Object.keys(s.answers || {})))].filter(k => k !== 'contact');
const contactKeys = ['name', 'phone', 'clinic', 'address'];
const devKeys = ['type', 'os', 'osVersion', 'browser', 'browserVersion', 'model', 'screenW', 'screenH', 'viewW', 'viewH', 'dpr', 'touch', 'langs', 'tz', 'net', 'ref', 'theme'];
const head = ['session', 'created_at', 'updated_at', 'completed_at', 'status', 'lang', 'answered', 'last_question', 'events', 'seconds',
  ...devKeys.map(k => 'device_' + k), ...qids, ...contactKeys.map(k => 'contact_' + k)];
const rows = sessions.map(s => {
  const a = s.answers || {}, c = a.contact || {}, d = s.device || {};
  return [s.id, iso(s.createdAt), iso(s.updatedAt), iso(s.completedAt), s.status, s.lang, s.answeredCount, s.lastQuestion, s.eventsCount, Math.round((s.elapsedMs || 0) / 1000),
    ...devKeys.map(k => d[k]), ...qids.map(k => (Array.isArray(a[k]) ? a[k].join('; ') : a[k])), ...contactKeys.map(k => c[k])];
});
writeFileSync('survey-sessions.csv', csv(head, rows));

const evRows = [];
for (const s of sessions) {
  const es = await db.collection('survey_sessions').doc(s.id).collection('events').orderBy('n').get();
  es.forEach(e => { const x = e.data(); evRows.push([s.id, x.n, Math.round(x.t / 1000), x.type, x.qid, x.idx, x.ms != null ? Math.round(x.ms / 1000) : '', Array.isArray(x.v) ? x.v.join('; ') : x.v]); });
}
writeFileSync('survey-events.csv', csv(['session', 'n', 'seconds_from_start', 'type', 'question', 'index', 'seconds_on_question', 'value'], evRows));
const done = sessions.filter(s => s.status === 'completed').length;
console.log(`${sessions.length} sessions (${done} completed), ${evRows.length} events -> survey-sessions.csv, survey-events.csv`);
