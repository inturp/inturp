# Survey backend (Firebase project `vet-charted`)

The survey page streams everything to the Cloud Function `submitSurvey` (europe-west1) as the visitor goes, so a
visitor who stops after one question is still kept.

## What is stored (named Firestore database `survey`; the project's `(default)` database is untouched)
- `survey_sessions/{sid}`: one document per visit. `status` (`in_progress` / `completed`), the latest `answers`, how many
  were answered, the last question reached, `elapsedMs`, language, a short device summary (device type, OS, browser,
  screen and viewport size, pixel ratio, touch, languages, time zone, connection type, referrer host, theme) and the
  raw user-agent string (200 characters).
- `survey_sessions/{sid}/events/{n}`: every view, answer, next, skip, back, start, leave and submit, with the time since
  the visit started and the milliseconds spent on the question. This is what shows where people drop off.
- `survey_rate`, `survey_meta`: counters for the limits below (salted IP hash only).
- Contact details (name, phone, clinic, address) are accepted only together with the final "send", never earlier.

## Security
- `firestore.rules` denies every client read and write; only the function (Admin SDK) writes.
- Allowed web origins only, JSON only, 32 KB limit, strict schema (`survey-schema.json`, generated from
  `questions.json`), device info limited to a closed list of short values, at most 40 events per call and 500 per session.
- Spam: honeypot field, minimum time before the final send, 10 new sessions per hour and 30 per day per visitor,
  600 syncs per hour, 3000 sessions per day overall, at most 3 function instances.
- The IP address is never stored; only a salted hash used for the limits.

## Reading the data
- Firebase console: Firestore > database `survey` > `survey_sessions`.
- CSV: `gcloud auth application-default login` once, then `npm install && node export.mjs` writes
  `survey-sessions.csv` (one row per visit) and `survey-events.csv` (one row per click).

## Deploy (after changing questions.json or index.js)
    python3 ../../build_survey.py            # regenerates survey-schema.json
    npm install
    firebase deploy --only functions:survey,firestore:survey --project vet-charted

`IP_PEPPER` (a random secret) lives in `.env`, which is git-ignored. Create it once: `IP_PEPPER=<64 random hex chars>`.
Changing it only resets the rate-limit counters.
