/* Vet Charted site — language, navigation, "a day in the clinic", forms. No dependencies. */
(() => {
  'use strict';
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const root = document.documentElement;
  const cfg = Object.assign({ contactEmail: '', operatorName: 'inturp', updated: '', responseDays: 30 }, window.VC_CONFIG || {});
  const cap = s => s[0].toUpperCase() + s.slice(1);
  const lang = () => (root.lang === 'en' ? 'en' : 'ar');
  const isDesktop = () => matchMedia('(min-width:1021px)').matches;
  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
  const validMail = /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(cfg.contactEmail);

  /* ───────── language ───────── */
  function fillConfig() {
    const fmt = new Intl.DateTimeFormat(lang(), { year: 'numeric', month: 'long', day: 'numeric' });
    $$('[data-updated]').forEach(e => { try { e.textContent = fmt.format(new Date(cfg.updated)); } catch (_) { e.textContent = cfg.updated; } });
    $$('[data-operator]').forEach(e => (e.textContent = cfg.operatorName));
    $$('[data-days]').forEach(e => (e.textContent = cfg.responseDays));
    $$('[data-contact]').forEach(e => (e.textContent = cfg.contactEmail));
    $$('[data-contact-link]').forEach(e => (e.href = 'mailto:' + cfg.contactEmail));
  }
  function applyLang(l) {
    root.lang = l;
    root.dir = l === 'ar' ? 'rtl' : 'ltr';
    $$('[data-attrs]').forEach(el => el.dataset.attrs.split(' ').forEach(a => {
      const v = el.getAttribute(`data-${l}-${a}`);
      if (v != null) el.setAttribute(a, v);
    }));
    $$('option[data-ar]').forEach(o => (o.textContent = o.dataset[l]));
    const t = $('title');
    if (t && t.dataset[l]) document.title = t.dataset[l];
    fillConfig();
    try { localStorage.setItem('vc-lang', l); } catch (_) {}
  }
  (function initLang() {
    const q = new URLSearchParams(location.search).get('lang');
    const defaultLang = location.pathname.endsWith('/en.html') ? 'en' : root.lang;
    if (document.body.dataset.page === 'home' && (q === 'en' || q === 'ar')) {
      location.replace((q === 'en' ? 'en.html' : './') + location.hash);
      return;
    }
    applyLang(defaultLang);
  })();
  /* legal pages keep one article per language, so section ids differ (a3 / e3) */
  const docSectionNo = () => {
    let cur = null;
    $$('.doc section').forEach(s => { if (s.offsetParent && s.getBoundingClientRect().top < 160) cur = s.id; });
    return cur && cur.slice(1);
  };
  const jumpToSection = n => {
    const t = $('#' + (lang() === 'ar' ? 'a' : 'e') + n);
    if (t) t.scrollIntoView({ behavior: 'instant', block: 'start' });
  };
  $$('[data-lang-toggle]').forEach(b => b.addEventListener('click', () => {
    if (document.body.dataset.page === 'home') { location.assign((lang() === 'ar' ? 'en.html' : './') + location.hash); return; }
    const n = docSectionNo();
    applyLang(lang() === 'ar' ? 'en' : 'ar');
    if (n) jumpToSection(n);
  }));
  (function initHash() {
    const m = /^#[ae](\d+)$/.exec(location.hash);
    if (m) setTimeout(() => jumpToSection(m[1]), 0);
  })();

  /* ───────── header & mobile menu ───────── */
  const menuBtn = $('.menu-btn'), mnav = $('#mnav');
  function setMenu(open) {
    if (!menuBtn) return;
    menuBtn.setAttribute('aria-expanded', String(open));
    mnav.hidden = !open;
    document.body.classList.toggle('menu-open', open);
  }
  if (menuBtn) {
    menuBtn.addEventListener('click', () => setMenu(menuBtn.getAttribute('aria-expanded') !== 'true'));
    mnav.addEventListener('click', e => { if (e.target.closest('a')) setMenu(false); });
    addEventListener('keydown', e => { if (e.key === 'Escape' && !mnav.hidden) { setMenu(false); menuBtn.focus(); } });
    document.addEventListener('click', e => { if (!mnav.hidden && !e.target.closest('.site-header')) setMenu(false); });
    addEventListener('resize', () => { if (isDesktop()) setMenu(false); });
  }

  /* scroll-spy for the header links (home page) */
  const spyLinks = $$('[data-spy]');
  if (spyLinks.length) {
    const ids = [...spyLinks.map(a => a.dataset.spy), 'contact'];
    const targets = ids.map(id => $('#' + id));
    const spy = () => {
      let cur = -1;
      targets.forEach((t, i) => { if (t && t.getBoundingClientRect().top < innerHeight * .4) cur = i; });
      spyLinks.forEach((a, i) => (i === cur ? a.setAttribute('aria-current', 'true') : a.removeAttribute('aria-current')));
    };
    addEventListener('scroll', spy, { passive: true });
    spy();
  }

  /* ───────── reveal on scroll ───────── */
  const revealItems = $$('[data-reveal]');
  if ('IntersectionObserver' in window && !reducedMotion.matches) {
    const revealObserver = new IntersectionObserver(entries => {
      entries.forEach(({ target, isIntersecting }) => {
        if (isIntersecting) { target.classList.add('in'); revealObserver.unobserve(target); }
      });
    }, { rootMargin: '0px 0px -6% 0px' });
    revealItems.forEach(el => revealObserver.observe(el));
  } else revealItems.forEach(el => el.classList.add('in'));

  /* ───────── a day in the clinic ───────── */
  const steps = $$('#daySteps .step');
  if (steps.length) {
    const imgs = $$('#dayApp img'), phone = $('#dayPhone'), count = $('#dayCount');
    const prev = $('#dayPrev'), next = $('#dayNext');
    let cur = 0, lock = false, unlockTimer;
    const setStep = i => {
      cur = i;
      steps.forEach((s, k) => { s.classList.toggle('is-active', k === i); if (isDesktop()) s.setAttribute('aria-pressed', String(k === i)); });
      imgs.forEach(im => im.classList.toggle('on', im.dataset.k === steps[i].dataset.img));
      phone.classList.toggle('on', steps[i].hasAttribute('data-phone'));
      count.textContent = `0${i + 1} / 0${steps.length}`;
      prev.disabled = i === 0;
      next.disabled = i === steps.length - 1;
    };
    const go = i => {
      i = Math.max(0, Math.min(steps.length - 1, i));
      lock = true; setStep(i);
      steps[i].scrollIntoView({ behavior: reducedMotion.matches ? 'instant' : 'smooth', block: 'center' });
      clearTimeout(unlockTimer);
      unlockTimer = setTimeout(() => (lock = false), reducedMotion.matches ? 0 : 900);
    };
    const so = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting && !lock) setStep(steps.indexOf(e.target)); }), { rootMargin: '-42% 0px -42% 0px' });
    steps.forEach((s, i) => {
      so.observe(s);
      s.addEventListener('click', () => { if (isDesktop()) go(i); });
      s.addEventListener('keydown', e => {
        if (!isDesktop()) return;
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); go(i); }
        if (['ArrowDown', 'ArrowUp', 'Home', 'End'].includes(e.key)) {
          e.preventDefault();
          const target = e.key === 'Home' ? 0 : e.key === 'End' ? steps.length - 1 : Math.max(0, Math.min(steps.length - 1, i + (e.key === 'ArrowDown' ? 1 : -1)));
          steps[target].focus({ preventScroll: true }); go(target);
        }
      });
    });
    prev.addEventListener('click', () => go(cur - 1));
    next.addEventListener('click', () => go(cur + 1));
    const syncStepControls = () => steps.forEach(s => {
      if (isDesktop()) { s.setAttribute('role', 'button'); s.tabIndex = 0; }
      else { s.removeAttribute('role'); s.removeAttribute('tabindex'); s.removeAttribute('aria-pressed'); }
    });
    addEventListener('resize', syncStepControls);
    syncStepControls();
    setStep(0);
  }

  /* ───────── QR drawing (decorative) ───────── */
  $$('svg[data-qr]').forEach(svg => {
    const n = 29; let s = 42;
    const rnd = () => { s |= 0; s = (s + 0x6D2B79F5) | 0; let t = Math.imul(s ^ (s >>> 15), 1 | s); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
    const finder = (x, y) => (x < 8 && y < 8) || (x >= n - 8 && y < 8) || (x < 8 && y >= n - 8);
    let out = '';
    for (let y = 0; y < n; y++) for (let x = 0; x < n; x++) if (!finder(x, y) && rnd() < .5) out += `<rect x="${x + .06}" y="${y + .06}" width=".88" height=".88" rx=".18" fill="#1E3A5F"/>`;
    const eye = (ox, oy) => `<rect x="${ox}" y="${oy}" width="7" height="7" rx="1.4" fill="#1E3A5F"/><rect x="${ox + 1}" y="${oy + 1}" width="5" height="5" rx="1" fill="#fff"/><rect x="${ox + 2}" y="${oy + 2}" width="3" height="3" rx=".7" fill="#1E3A5F"/>`;
    svg.innerHTML = out + eye(0, 0) + eye(n - 7, 0) + eye(0, n - 7);
  });

  /* ───────── legal table of contents ───────── */
  const tocs = $$('.toc').map(toc => {
    const links = $$('a', toc);
    return { links, targets: links.map(a => $(a.getAttribute('href'))) };
  });
  if (tocs.length) {
    const upd = () => tocs.forEach(({ links, targets }) => {
      if (!links[0].offsetParent) return;
      let cur = 0;
      targets.forEach((t, i) => { if (t && t.getBoundingClientRect().top < 150) cur = i; });
      links.forEach((a, i) => a.classList.toggle('on', i === cur));
    });
    addEventListener('scroll', upd, { passive: true });
    upd();
  }

  /* ───────── forms that prepare an email ───────── */
  const MSG = {
    ready: { ar: 'فتحنا لك رسالة بريد جاهزة. اضغط «إرسال» في تطبيق البريد لإتمام الطلب. إن لم يفتح شيء فاستخدم «نسخ النص».', en: 'We opened a ready-to-send email. Press Send in your mail app to finish. If nothing opened, use “Copy text”.' },
    copied: { ar: 'تم نسخ النص. الصقه في رسالة إلى ', en: 'Text copied. Paste it into an email to ' },
    copyFail: { ar: 'تعذّر النسخ تلقائياً. انسخ النص التالي يدوياً:', en: 'Could not copy automatically. Copy this text manually:' },
    noMail: { ar: 'لم يُضبط بريد الاستلام بعد في js/site-config.js.', en: 'The receiving email is not set yet in js/site-config.js.' },
  };
  $$('form[data-mail]').forEach(form => {
    const msg = $('.form-msg', form);
    const show = (text, err) => { msg.textContent = text; msg.className = 'form-msg show' + (err ? ' err' : ''); };
    const compose = () => {
      const l = lang();
      const d = k => form.dataset[k + cap(l)] || '';
      const lines = [d('intro'), ''];
      let long = '';
      [...form.elements].forEach(el => {
        if (!el.name || el.type === 'checkbox' || el.type === 'submit' || el.type === 'button') return;
        const label = el.dataset['l' + cap(l)] || el.name;
        let val = (el.value || '').trim();
        if (el.tagName === 'SELECT') val = el.selectedOptions[0].dataset[l] || el.selectedOptions[0].textContent;
        if (el.tagName === 'TEXTAREA') { if (val) long += `\n${label}:\n${val}\n`; return; }
        lines.push(`${label}: ${val || '—'}`);
      });
      if (long) lines.push(long);
      if (d('outro')) lines.push('', d('outro'));
      return { subject: d('subject'), body: lines.join('\n') };
    };
    form.addEventListener('submit', e => {
      e.preventDefault();
      if (!form.reportValidity()) return;
      if (!validMail) return show(MSG.noMail[lang()], true);
      const { subject, body } = compose();
      show(MSG.ready[lang()]);
      location.href = `mailto:${cfg.contactEmail}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    });
    const copyBtn = $('[data-copy]', form);
    if (copyBtn) copyBtn.addEventListener('click', async () => {
      if (!form.reportValidity()) return;
      const { subject, body } = compose(), text = `${subject}\n\n${body}`;
      try {
        await navigator.clipboard.writeText(text);
        show(MSG.copied[lang()] + cfg.contactEmail);
      } catch (_) {
        const t = document.createElement('textarea');
        t.value = text; t.style.position = 'fixed'; t.style.opacity = '0'; document.body.appendChild(t); t.select();
        let ok = false; try { ok = document.execCommand('copy'); } catch (__) {}
        t.remove();
        show(ok ? MSG.copied[lang()] + cfg.contactEmail : `${MSG.copyFail[lang()]}\n\n${text}`, !ok);
        if (!ok) msg.style.whiteSpace = 'pre-wrap';
      }
    });
  });
})();
