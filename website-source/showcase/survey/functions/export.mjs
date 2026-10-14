// Exports every survey response to a CSV file next to this script.
//   gcloud auth application-default login     (once)
//   npm install && node export.mjs
import { initializeApp, applicationDefault } from 'firebase-admin/app';
import { getFirestore } from 'firebase-admin/firestore';
import { writeFileSync } from 'node:fs';

initializeApp({ credential: applicationDefault(), projectId: 'vet-charted' });
const db = getFirestore('survey');
const snap = await db.collection('survey_responses').orderBy('createdAt').get();
const rows = snap.docs.map(d => ({ id: d.id, ...d.data() }));
const keys = [...new Set(rows.flatMap(r => Object.keys(r.answers || {})))];
const contactKeys = ['name', 'phone', 'clinic', 'address'];
const head = ['id', 'created_at', 'lang', 'seconds', ...keys.filter(k => k !== 'contact'), ...contactKeys.map(k => 'contact_' + k)];
const cell = v => '"' + String(v ?? '').replace(/"/g, '""') + '"';
const lines = [head.map(cell).join(',')];
for (const r of rows) {
  const a = r.answers || {}, c = a.contact || {};
  lines.push([r.id, r.createdAt?.toDate().toISOString(), r.lang, Math.round((r.elapsedMs || 0) / 1000),
    ...keys.filter(k => k !== 'contact').map(k => Array.isArray(a[k]) ? a[k].join('; ') : a[k]),
    ...contactKeys.map(k => c[k])].map(cell).join(','));
}
writeFileSync('survey-responses.csv', '﻿' + lines.join('\n'));
console.log(`${rows.length} responses written to survey-responses.csv`);
