/* Case-study pages (Al Ameer, CheckBook) — theme, language, header menus, tour, reveal. No dependencies.
   Each language has its own URL; the language button goes to the page's hreflang twin and remembers the choice.
   Theme uses the same storage key and `.dark` class as inturp.com. */
(() => {
  'use strict';
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const root = document.documentElement;
  const store = {
    get: k => { try { return localStorage.getItem(k); } catch (_) { return null; } },
    set: (k, v) => { try { localStorage.setItem(k, v); } catch (_) {} },
  };

  /* language: go to the twin page */
  $$('[data-lang-toggle]').forEach(b => b.addEventListener('click', () => {
    const other = root.lang === 'ar' ? 'en' : 'ar';
    const twin = $(`link[rel="alternate"][hreflang="${other}"]`);
    store.set('inturp-lang', other);
    if (twin) location.assign(new URL(twin.href).pathname + location.hash);
  }));

  /* theme */
  $$('[data-theme-toggle]').forEach(b => b.addEventListener('click', () => {
    const dark = !root.classList.contains('dark');
    root.classList.toggle('dark', dark);
    root.style.colorScheme = dark ? 'dark' : 'light';
    store.set('inturp-theme', dark ? 'dark' : 'light');
  }));

  /* products dropdown */
  const pmBtn = $('#pm-btn'), pmMenu = $('#product-links');
  if (pmBtn && pmMenu) {
    const set = o => { pmBtn.setAttribute('aria-expanded', String(o)); pmMenu.hidden = !o; };
    pmBtn.addEventListener('click', () => set(pmBtn.getAttribute('aria-expanded') !== 'true'));
    document.addEventListener('pointerdown', e => { if (!e.target.closest('.product-menu')) set(false); });
    addEventListener('keydown', e => { if (e.key === 'Escape') { set(false); pmBtn.focus(); } });
  }

  /* mobile panel */
  const mBtn = $('.mobile-toggle'), mPanel = $('#mnav');
  if (mBtn && mPanel) {
    const set = o => { mBtn.setAttribute('aria-expanded', String(o)); mPanel.hidden = !o; };
    mBtn.addEventListener('click', () => set(mBtn.getAttribute('aria-expanded') !== 'true'));
    mPanel.addEventListener('click', e => { if (e.target.closest('a')) set(false); });
    addEventListener('keydown', e => { if (e.key === 'Escape') set(false); });
    matchMedia('(min-width: 900px)').addEventListener('change', () => set(false));
  }

  /* legal table of contents */
  const items = $$('.toc a').map(a => ({ a, t: $(a.getAttribute('href')) })).filter(x => x.t);
  if (items.length) {
    const run = () => {
      let cur = 0;
      items.forEach((x, i) => { if (x.t.getBoundingClientRect().top < innerHeight * .35) cur = i; });
      items.forEach((x, i) => x.a.classList.toggle('on', i === cur));
    };
    addEventListener('scroll', run, { passive: true });
    run();
  }

  /* reveal */
  const reveal = $$('[data-reveal]');
  if ('IntersectionObserver' in window && !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }), { rootMargin: '0px 0px -6% 0px' });
    reveal.forEach(el => io.observe(el));
  } else reveal.forEach(el => el.classList.add('in'));

  /* app tour */
  const steps = $$('.step'), shots = $$('.tour-phone .scr img'), dots = $$('.tour-dots button');
  if (steps.length) {
    let cur = 0, timer = null, touched = false;
    const go = i => {
      cur = i;
      steps.forEach((s, k) => { s.classList.toggle('on', k === i); s.setAttribute('aria-expanded', String(k === i)); });
      shots.forEach((im, k) => im.classList.toggle('on', k === i));
      dots.forEach((d, k) => d.classList.toggle('on', k === i));
    };
    const auto = () => {
      clearInterval(timer);
      if (!touched && !matchMedia('(prefers-reduced-motion: reduce)').matches) timer = setInterval(() => go((cur + 1) % steps.length), 5200);
    };
    const pick = i => { touched = true; clearInterval(timer); go(i); };
    steps.forEach((s, i) => s.addEventListener('click', () => pick(i)));
    dots.forEach((d, i) => d.addEventListener('click', () => pick(i)));
    const tour = $('.tour');
    if ('IntersectionObserver' in window && tour) {
      new IntersectionObserver(es => es.forEach(e => (e.isIntersecting ? auto() : clearInterval(timer))), { threshold: .3 }).observe(tour);
    }
    go(0);
  }

  const y = $('#year');
  if (y) y.textContent = new Date().getFullYear();
})();
