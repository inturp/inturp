"""Shared Inturp chrome (header, mobile menu, footer) for the static product pages.

Used by the Al Ameer and CheckBook case studies and by the Vet Charted pages, so the Products menu stays
identical everywhere. All links are root-absolute. Language-dependent links use data-ar-*/data-en-* attributes
that the page scripts swap when the language changes.
"""

ARROW = '<svg class="arr" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 7h10v10"/><path d="M7 17 17 7"/></svg>'
INSTAGRAM = ('<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/>'
             '<circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r=".6"/></svg>')

# key, href (en), href (ar), icon, mono (icon is a black mark that must invert in dark mode), names, descriptions
PRODUCTS = [
    dict(key='vet', en_href='/vet-charted/en/', ar_href='/vet-charted/', icon='/vetcharted-logo.png', mono=True,
         name_en='VetCharted', name_ar='VetCharted',
         sub_en='Veterinary clinic management', sub_ar='إدارة العيادات البيطرية'),
    dict(key='alameer', en_href='/alameer/', ar_href='/ar/alameer/', icon='/alameer/assets/img/app-icon.png', mono=False,
         name_en='Al Ameer Hydraulics', name_ar='شركة الأمير',
         sub_en='Heavy-equipment parts app', sub_ar='تطبيق قطع الغيار والمعدات الثقيلة'),
    dict(key='checkbook', en_href='/checkbook/', ar_href='/ar/checkbook/', icon='/checkbook/assets/img/app-icon.png', mono=False,
         name_en='CheckBook', name_ar='CheckBook',
         sub_en='Cheque tracking and reminders', sub_ar='متابعة الشيكات والتذكيرات'),
]


def _bi(ar, en):
    return f'<span class="ar">{ar}</span><span class="en">{en}</span>'


def _href(p):
    return f'href="{p["en_href"]}" data-ar-href="{p["ar_href"]}" data-en-href="{p["en_href"]}" data-attrs="href"'


def header(active, skip_class='skip-link'):
    items = []
    mobile = []
    for p in PRODUCTS:
        on = p['key'] == active
        cls = ' class="active" aria-current="page"' if on else ''
        img_cls = ' class="mono"' if p['mono'] else ''
        items.append(
            '<a' + cls + ' ' + _href(p) + '>'
            '<img' + img_cls + ' src="' + p['icon'] + '" alt="" width="32" height="32">'
            '<span>' + _bi(p['name_ar'], p['name_en']) + '<small>' + _bi(p['sub_ar'], p['sub_en']) + '</small></span>' + ARROW + '</a>')
        mobile.append('<a ' + _href(p) + (' aria-current="page"' if on else '') + '><span>' + _bi(p['name_ar'], p['name_en']) + '</span>' + ARROW + '</a>')
    return f'''<a class="{skip_class}" href="#main"><span class="ar">تخطّي إلى المحتوى</span><span class="en">Skip to content</span></a>
<header class="site-header" id="top" dir="ltr">
  <nav class="site-nav" aria-label="Navigation menu" data-ar-aria-label="قائمة التنقل" data-en-aria-label="Navigation menu" data-attrs="aria-label">
    <a class="brand-link" href="/" data-ar-href="/ar/" data-en-href="/" data-attrs="href"><img src="/inturp-logo.png" alt="Inturp" width="58" height="58"><span>inturp<span class="brand-dot">.</span></span></a>
    <div class="desktop-nav">
      <div class="product-menu">
        <button type="button" class="nav-link active" id="pm-btn" aria-expanded="false" aria-controls="product-links"><span class="ar">المنتجات</span><span class="en">Products</span><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg></button>
        <div class="product-dropdown" id="product-links" hidden>
          {"".join(items)}
        </div>
      </div>
      <a class="nav-link" href="/about/" data-ar-href="/ar/about/" data-en-href="/about/" data-attrs="href"><span class="ar">من نحن</span><span class="en">About us</span></a>
      <a class="nav-contact" href="/#contact" data-ar-href="/ar/#contact" data-en-href="/#contact" data-attrs="href"><span class="ar">لنتحدث</span><span class="en">Let’s talk</span>{ARROW}</a>
    </div>
    <div class="nav-end">
      <div class="nav-preferences">
        <button type="button" class="language-control" data-lang-toggle aria-label="Switch language / تبديل اللغة"><span class="ar">EN</span><span class="en">عربي</span></button>
        <button type="button" class="icon-control" data-theme-toggle aria-label="Toggle theme" data-ar-aria-label="تبديل المظهر" data-en-aria-label="Toggle theme" data-attrs="aria-label"><svg class="sun" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2m-7.07-2.93 1.41-1.41m11.32-11.32 1.41-1.41M2 12h2m16 0h2M4.93 4.93l1.41 1.41m11.32 11.32 1.41 1.41"/></svg><svg class="moon" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg></button>
      </div>
      <button type="button" class="icon-control mobile-toggle menu-btn" aria-expanded="false" aria-controls="mnav" aria-label="Navigation menu" data-ar-aria-label="قائمة التنقل" data-en-aria-label="Navigation menu" data-attrs="aria-label"><svg class="bars" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 6h16M4 12h16M4 18h16"/></svg><svg class="x" viewBox="0 0 24 24" aria-hidden="true"><path d="M18 6 6 18M6 6l12 12"/></svg></button>
    </div>
  </nav>
  <nav class="mobile-panel mnav" id="mnav" hidden aria-label="Navigation menu" data-ar-aria-label="قائمة التنقل" data-en-aria-label="Navigation menu" data-attrs="aria-label">
    {"".join(mobile)}
    <a href="/about/" data-ar-href="/ar/about/" data-en-href="/about/" data-attrs="href"><span class="ar">من نحن</span><span class="en">About us</span>{ARROW}</a>
    <a href="/#contact" data-ar-href="/ar/#contact" data-en-href="/#contact" data-attrs="href"><span class="ar">لنتحدث</span><span class="en">Let’s talk</span>{ARROW}</a>
  </nav>
</header>
'''


def footer(active, privacy, delete, privacy_ar, privacy_en, privacy_settings=False):
    """privacy / delete are (en_href, ar_href) pairs."""
    settings = ('\n      <a href="/privacy/" data-ar-href="/ar/privacy/" data-en-href="/privacy/" data-attrs="href"><span class="ar">الخصوصية</span><span class="en">Privacy</span></a>'
                '\n      <button type="button" data-privacy-settings><span class="ar">إعدادات الخصوصية</span><span class="en">Privacy settings</span></button>') if privacy_settings else ''
    def pair(p):
        return f'href="{p[0]}" data-ar-href="{p[1]}" data-en-href="{p[0]}" data-attrs="href"'
    return f'''<footer class="site-footer{" section-padding" if active != "vet" else ""}">
  <div class="footer-inner">
    <a class="brand-link" href="/" data-ar-href="/ar/" data-en-href="/" data-attrs="href" aria-label="Inturp"><img src="/inturp-logo.png" alt="" width="44" height="44"><span>inturp.</span></a>
    <div class="footer-links">
      <a href="/about/" data-ar-href="/ar/about/" data-en-href="/about/" data-attrs="href"><span class="ar">من نحن</span><span class="en">About us</span></a>
      <a href="/vet-charted/en/" data-ar-href="/vet-charted/" data-en-href="/vet-charted/en/" data-attrs="href">VetCharted</a>
      <a href="/alameer/" data-ar-href="/ar/alameer/" data-en-href="/alameer/" data-attrs="href"><span class="ar">شركة الأمير</span><span class="en">Al Ameer</span></a>
      <a href="/checkbook/" data-ar-href="/ar/checkbook/" data-en-href="/checkbook/" data-attrs="href">CheckBook</a>
      <a href="mailto:info@inturp.com">info@inturp.com</a>
      <a href="https://www.instagram.com/inturp_/" target="_blank" rel="noopener noreferrer" dir="ltr" aria-label="Inturp on Instagram: @inturp_">{INSTAGRAM}<span>@inturp_</span></a>
      <a {pair(privacy)}><span class="ar">{privacy_ar}</span><span class="en">{privacy_en}</span></a>
      <a {pair(delete)}><span class="ar">حذف الحساب</span><span class="en">Delete account</span></a>{settings}
    </div>
    <p>© <span id="year">2026</span> Inturp. <span class="ar">جميع الحقوق محفوظة.</span><span class="en">All rights reserved.</span></p>
  </div>
</footer>'''


# ───────────────────────────────────────────────────────── single-language output
import re as _re
from html.parser import HTMLParser as _HTMLParser

_VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}
_PAIR = _re.compile(r'\sdata-(ar|en)-([\w:-]+)="([^"]*)"')
_TITLE_ATTR = _re.compile(r'\sdata-(?:ar|en)="[^"]*"')
_ATTRS = _re.compile(r'\sdata-attrs="[^"]*"')


class _Single(_HTMLParser):
    """Keeps one language of a bilingual page: drops elements marked class="ar"/"en" of the other language
    and resolves data-ar-*/data-en-* attributes (href, aria-label, alt, ...) into plain attributes."""

    def __init__(self, lang):
        super().__init__(convert_charrefs=False)
        self.lang = lang
        self.other = 'en' if lang == 'ar' else 'ar'
        self.out = []
        self.skip = None

    def _resolve(self, raw):
        pairs = _PAIR.findall(raw)
        for lg, name, val in pairs:
            if lg != self.lang:
                continue
            if _re.search(r'\s' + _re.escape(name) + r'="[^"]*"', raw):
                raw = _re.sub(r'(\s' + _re.escape(name) + r'=")[^"]*(")', lambda m: m.group(1) + val + m.group(2), raw, count=1)
            else:
                raw = _re.sub(r'(/?>)$', lambda m: ' ' + name + '="' + val + '"' + m.group(1), raw)
        raw = _PAIR.sub('', raw)
        raw = _TITLE_ATTR.sub('', raw)
        raw = _ATTRS.sub('', raw)
        return raw

    def handle_starttag(self, tag, attrs):
        if self.skip:
            if tag == self.skip[0] and tag not in _VOID:
                self.skip[1] += 1
            return
        cls = (dict(attrs).get('class') or '').split()
        if self.other in cls and self.lang not in cls:
            if tag not in _VOID:
                self.skip = [tag, 1]
            return
        self.out.append(self._resolve(self.get_starttag_text()))

    def handle_startendtag(self, tag, attrs):
        if self.skip:
            return
        cls = (dict(attrs).get('class') or '').split()
        if self.other in cls and self.lang not in cls:
            return
        self.out.append(self._resolve(self.get_starttag_text()))

    def handle_endtag(self, tag):
        if self.skip:
            if tag == self.skip[0]:
                self.skip[1] -= 1
                if self.skip[1] == 0:
                    self.skip = None
            return
        self.out.append('</' + tag + '>')

    def handle_data(self, data):
        if not self.skip:
            self.out.append(data)

    def handle_entityref(self, name):
        if not self.skip:
            self.out.append('&' + name + ';')

    def handle_charref(self, name):
        if not self.skip:
            self.out.append('&#' + name + ';')

    def handle_comment(self, data):
        if not self.skip:
            self.out.append('<!--' + data + '-->')

    def handle_decl(self, decl):
        self.out.append('<!' + decl + '>')


def single(html, lang):
    p = _Single(lang)
    p.feed(html)
    p.close()
    return ''.join(p.out)


# ───────────────────────────────────────────────────────── page head / frame
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=IBM+Plex+Sans+Arabic:wght@300;400;500;600;700&display=swap">')


def prepaint(lang, ar_path):
    """Runs before first paint: theme, and the language rule (an Arabic URL stores 'ar'; an English URL goes to
    its Arabic twin when the visitor chose Arabic before)."""
    theme = ("var d=document.documentElement,t=localStorage.getItem('inturp-theme'),"
             "dk=t==='dark'||(t!=='light'&&matchMedia('(prefers-color-scheme: dark)').matches);"
             "d.classList.toggle('dark',dk);d.style.colorScheme=dk?'dark':'light';")
    if lang == 'ar':
        rule = "localStorage.setItem('inturp-lang','ar');"
    else:
        rule = f"if(localStorage.getItem('inturp-lang')==='ar'){{location.replace('{ar_path}'+location.search+location.hash)}}"
    return f'<script>(function(){{try{{{theme}{rule}}}catch(e){{}} }})()</script>'


def head(*, lang, title, desc, en_path, ar_path, css, og_image, og_alt, extra='', icon='/inturp-tab-icon.png', robots='index, follow, max-image-preview:large'):
    origin = 'https://inturp.com'
    url = origin + (ar_path if lang == 'ar' else en_path)
    locale, alt_locale = ('ar_AR', 'en_US') if lang == 'ar' else ('en_US', 'ar_AR')
    return f'''<!doctype html>
<html lang="{lang}" dir="{'rtl' if lang == 'ar' else 'ltr'}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{prepaint(lang, ar_path)}
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="en" href="{origin}{en_path}">
<link rel="alternate" hreflang="ar" href="{origin}{ar_path}">
<link rel="alternate" hreflang="x-default" href="{origin}{en_path}">
<meta name="robots" content="{robots}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Inturp">
<meta property="og:locale" content="{locale}">
<meta property="og:locale:alternate" content="{alt_locale}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{origin}{og_image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{og_alt}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{origin}{og_image}">
<meta name="theme-color" content="#0a0a0a">
<link rel="icon" href="{icon}">
{FONTS}
<link rel="stylesheet" href="{css}">
{extra}</head>
<body>
'''
