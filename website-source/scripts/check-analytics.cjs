const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const path = require('node:path');
const code = fs.readFileSync(path.join(__dirname, '../public/js/analytics.js'), 'utf8');
function run(consent, hostname = 'inturp.com') {
  const scripts = [], listeners = {};
  class Element { closest() { return null; } }
  const document = {
    documentElement: {lang: 'en'}, cookie: '', title: 'Inturp',
    head: {append: item => scripts.push(item)},
    createElement: tag => ({tag}),
    addEventListener: (name, handler) => {listeners[name] = handler;},
    getElementById: () => null,
  };
  const location = {hostname, origin: 'https://' + hostname, pathname: '/', search: '?email=private@example.com'};
  const window = {};
  const context = {document, location, window, Element, localStorage: {getItem: () => consent}, MutationObserver: class {observe() {}}};
  vm.runInNewContext(code, context);
  return {scripts, listeners, location, window, rerun: () => vm.runInNewContext(code, context)};
}
assert.equal(run('denied').scripts.length, 0, 'Refused analytics must never load Google scripts');
assert.equal(run('granted', 'localhost').scripts.length, 0, 'Local previews must not contaminate production analytics');
const allowed = run('granted');
assert.equal(allowed.scripts.length, 1, 'Granted production consent loads exactly one script');
allowed.rerun();
assert.equal(allowed.scripts.length, 1, 'Re-executing shared head scripts must not load Google twice');
const events = () => allowed.window.dataLayer.map(args => Array.from(args)).filter(args => args[0] === 'event');
assert.equal(events().filter(args => args[1] === 'page_view').length, 1);
allowed.listeners['inturp:pageview']();
assert.equal(events().filter(args => args[1] === 'page_view').length, 1, 'Same-path notifications must not duplicate a page view');
allowed.location.pathname = '/about/';
allowed.listeners['inturp:pageview']();
assert.equal(events().filter(args => args[1] === 'page_view').length, 2);
assert.equal(events()[1][2].page_location, 'https://inturp.com/about/');
assert(!JSON.stringify(events()).includes('private@example.com'), 'Query strings containing personal details must not be included in custom events');
console.log('PASS: consent gating, production host, duplicate page views, route changes and sanitized event URLs.');
