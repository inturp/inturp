/**
 * Receives survey submissions and writes one row per submission into the Google Sheet this script is attached to.
 *
 * Setup (about 3 minutes):
 *  1. Create a Google Sheet, then Extensions > Apps Script, and paste this file in.
 *  2. Deploy > New deployment > type "Web app". Execute as: Me. Who has access: Anyone.
 *  3. Copy the web app URL and put it in clinic-survey/assets/js/survey-config.js as `endpoint`.
 *  4. Rebuild/publish. New answers appear as rows; columns are created for each question automatically.
 */
const SHEET_NAME = 'Responses';
const META = ['submitted_at', 'lang', 'page'];

function doPost(e) {
  const lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try {
    const data = JSON.parse(e.postData.contents);
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const sheet = ss.getSheetByName(SHEET_NAME) || ss.insertSheet(SHEET_NAME);
    if (sheet.getLastRow() === 0) sheet.appendRow(META);
    const header = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
    const answers = data.answers || {};
    Object.keys(answers).forEach(function (id) {
      if (header.indexOf(id) === -1) { header.push(id); sheet.getRange(1, header.length).setValue(id); }
    });
    const row = header.map(function (col) {
      if (col === 'submitted_at') return data.submitted_at || new Date().toISOString();
      if (col === 'lang') return data.lang || '';
      if (col === 'page') return data.page || '';
      const v = answers[col];
      if (v === undefined || v === null) return '';
      if (Array.isArray(v)) return v.join('; ');
      if (typeof v === 'object') return JSON.stringify(v);
      return v;
    });
    sheet.appendRow(row);
    return ContentService.createTextOutput('ok');
  } finally {
    lock.releaseLock();
  }
}

function doGet() { return ContentService.createTextOutput('survey endpoint is running'); }
