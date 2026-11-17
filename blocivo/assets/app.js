/* Language handling: ?lang=ar|en  >  saved choice  >  browser language. */
(function () {
  var d = document.documentElement;
  function pick() {
    try {
      var q = new URLSearchParams(location.search).get('lang');
      if (q === 'ar' || q === 'en') { localStorage.setItem('blocivo-lang', q); return q; }
      var s = localStorage.getItem('blocivo-lang');
      if (s === 'ar' || s === 'en') return s;
    } catch (e) {}
    return (navigator.language || 'en').toLowerCase().indexOf('ar') === 0 ? 'ar' : 'en';
  }
  function apply(l) {
    d.lang = l;
    d.dir = l === 'ar' ? 'rtl' : 'ltr';
    var t = document.documentElement.getAttribute('data-title-' + l);
    if (t) document.title = t;
    var b = document.querySelector('[data-lang-toggle]');
    if (b) b.textContent = l === 'ar' ? 'English' : 'العربية';
  }
  apply(pick());
  document.addEventListener('DOMContentLoaded', function () {
    apply(d.lang);
    var b = document.querySelector('[data-lang-toggle]');
    if (b) b.addEventListener('click', function () {
      var n = d.lang === 'ar' ? 'en' : 'ar';
      try { localStorage.setItem('blocivo-lang', n); } catch (e) {}
      apply(n);
    });
    var y = document.querySelectorAll('[data-year]');
    for (var i = 0; i < y.length; i++) y[i].textContent = new Date().getFullYear();
  });
})();
