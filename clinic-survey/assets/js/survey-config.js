/* Where the survey answers go.
 *
 * endpoint:  our Firebase function (project vet-charted, region europe-west1). It validates every answer, applies
 *            rate limits and stores the result in a Firestore database that no browser can read or write.
 * transport: 'json' for that function. Use 'script' only with a Google Apps Script web app (survey-apps-script.gs).
 * email:     the address used for the email fallback if the endpoint is empty or unreachable.
 */
window.SURVEY_CONFIG = {
  endpoint: 'https://europe-west1-vet-charted.cloudfunctions.net/submitSurvey',
  transport: 'json',
  email: 'info@inturp.com',
};
