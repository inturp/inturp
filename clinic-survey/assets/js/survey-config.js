/* Where the answers go.
 *
 * endpoint: the URL that receives each submission as JSON (see survey-apps-script.gs: Google Apps Script web app
 *           that writes a row per answer into a Google Sheet). Leave it empty and the last step offers to send
 *           the answers by email instead.
 * email:    the address used for that email fallback.
 */
window.SURVEY_CONFIG = {
  endpoint: '',
  email: 'info@inturp.com',
};
