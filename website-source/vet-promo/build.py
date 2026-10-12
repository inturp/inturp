#!/usr/bin/env python3
"""Builds the static pages from src/ (Python standard library only).

  python3 build.py

Source markup uses two tiny tokens so each sentence is written once per language:
  [[عربي||English]]   -> <span class="ar">..</span><span class="en">..</span>
  attr="{{عربي||English}}" -> Arabic value + data-ar-attr / data-en-attr (swapped by js/site.js)
Partials: <!--HEADER--> and <!--FOOTER-->.
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).parent
SRC = ROOT / "src"

TEXT = re.compile(r"\[\[(.+?)\|\|(.+?)\]\]", re.S)
ATTR = re.compile(r'([\w:-]+)="\{\{(.+?)\|\|(.+?)\}\}"', re.S)
TAG = re.compile(r"<[a-zA-Z][^<>]*\{\{[^<>]*>", re.S)


def expand_attrs(html: str) -> str:
    def per_tag(m: re.Match) -> str:
        tag = m.group(0)
        names = []

        def attr(am: re.Match) -> str:
            name, ar, en = am.group(1), am.group(2).strip(), am.group(3).strip()
            names.append(name)
            return f'{name}="{ar}" data-ar-{name}="{ar}" data-en-{name}="{en}"'

        tag = ATTR.sub(attr, tag)
        # inject data-attrs just before the closing bracket
        tag = re.sub(r"\s*(/?)>$", lambda x: f' data-attrs="{" ".join(names)}"{x.group(1)}>', tag)
        return tag

    return TAG.sub(per_tag, html)


def expand_text(html: str) -> str:
    return TEXT.sub(lambda m: f'<span class="ar">{m.group(1).strip()}</span><span class="en">{m.group(2).strip()}</span>', html)


def render(name: str) -> str:
    """Expands one source page into its bilingual (two-language) markup."""
    page = (SRC / name).read_text(encoding="utf-8")
    page = page.replace("<!--HEADER-->", (SRC / "_header.html").read_text(encoding="utf-8"))
    page = page.replace("<!--FOOTER-->", (SRC / "_footer.html").read_text(encoding="utf-8"))
    page = expand_text(expand_attrs(page))
    left = re.findall(r"\[\[|\]\]|\{\{|\}\}", page)
    if left:
        sys.exit(f"{name}: unexpanded tokens remain ({len(left)})")
    ids = re.findall(r'\sid="([^"]+)"', page)
    dup = {i for i in ids if ids.count(i) > 1}
    if dup:
        sys.exit(f"{name}: duplicate ids {sorted(dup)}")
    return page


# Shared single-language tooling (also used by the Al Ameer / CheckBook builders)
sys.path.insert(0, str(ROOT.parent / "showcase"))
import shared  # noqa: E402

ORIGIN = "https://inturp.com"
# page -> (Arabic path, English path, Arabic description, English description)
PAGES = {
    "index.src.html": ("/vet-charted/", "/vet-charted/en/", None, None),
    "privacy.src.html": ("/vet-charted/privacy/", "/vet-charted/en/privacy/",
                         "سياسة خصوصية Vet Charted: البيانات التي نجمعها وكيف نستخدمها وحقوقك.",
                         "Vet Charted privacy policy: what data we collect, how we use it and your rights."),
    "delete.src.html": ("/vet-charted/delete-account/", "/vet-charted/en/delete-account/",
                        "كيف تحذف حسابك في Vet Charted: من داخل التطبيق أو بطلب، وما الذي يُحذف وما الذي يبقى.",
                        "How to delete your Vet Charted account: inside the app or by request, what is deleted and what stays."),
}
HEAD_LINES = re.compile(r'<link rel="(?:canonical|alternate)"[^>]*>\n?|<meta property="og:(?:url|locale|locale:alternate)"[^>]*>\n?')
THEME_SCRIPT = re.compile(r"<script>\(function\(\)\{try\{var d=document\.documentElement.*?\}catch\(e\)\{\} ?\}\)\(\)</script>", re.S)


def emit(page: str, lang: str, ar_path: str, en_path: str, out: str, desc=None) -> None:
    other = "en" if lang == "ar" else "ar"
    path = ar_path if lang == "ar" else en_path
    # title text follows the language before the language-only markup is stripped
    page = re.sub(r'(<title data-ar="([^"]*)" data-en="([^"]*)">)[^<]*(</title>)',
                  lambda m: m.group(1) + (m.group(2) if lang == "ar" else m.group(3)) + m.group(4), page, count=1)
    html = shared.single(page, lang)
    html = re.sub(r'<html lang="[^"]*" dir="[^"]*">', f'<html lang="{lang}" dir="{"rtl" if lang == "ar" else "ltr"}">', html, count=1)
    html = THEME_SCRIPT.sub(lambda m: shared.prepaint(lang, ar_path), html, count=1)
    html = HEAD_LINES.sub("", html)
    if desc:
        html = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc}">', html, count=1)
    title = re.search(r"<title>([^<]*)</title>", html).group(1)
    dm = re.search(r'<meta name="description" content="([^"]*)">', html)
    locale, alt = ("ar_AR", "en_US") if lang == "ar" else ("en_US", "ar_AR")
    block = (f'<link rel="canonical" href="{ORIGIN}{path}">\n'
             f'<link rel="alternate" hreflang="en" href="{ORIGIN}{en_path}">\n<link rel="alternate" hreflang="ar" href="{ORIGIN}{ar_path}">\n'
             f'<link rel="alternate" hreflang="x-default" href="{ORIGIN}{en_path}">\n'
             f'<meta property="og:url" content="{ORIGIN}{path}">\n<meta property="og:locale" content="{locale}">\n<meta property="og:locale:alternate" content="{alt}">\n')
    if 'property="og:title"' not in html:
        img = f"{ORIGIN}/vet-charted/assets/img/dashboard.webp"
        block += (f'<meta property="og:type" content="website">\n<meta property="og:site_name" content="Inturp">\n<meta property="og:title" content="{title}">\n'
                  f'<meta property="og:description" content="{dm.group(1) if dm else ""}">\n<meta property="og:image" content="{img}">\n<meta name="twitter:card" content="summary_large_image">\n')
    html = html.replace("</head>", block + "</head>", 1)
    if lang == "en":  # English pages link to the English twins of the shared pages
        for ar_href, en_href in (("/vet-charted/privacy/", "/vet-charted/en/privacy/"), ("/vet-charted/delete-account/", "/vet-charted/en/delete-account/")):
            html = html.replace(f'href="{ar_href}"', f'href="{en_href}"')
    target = ROOT / out
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(html, encoding="utf-8")
    print(f"built {out} ({len(html) // 1024} KB)")


if __name__ == "__main__":
    ar_pages = {"index.src.html": "index.html", "privacy.src.html": "privacy/index.html", "delete.src.html": "delete-account/index.html"}
    en_pages = {"en.src.html": "en/index.html", "privacy.src.html": "en/privacy/index.html", "delete.src.html": "en/delete-account/index.html"}
    for name, out in ar_pages.items():
        ar_path, en_path, d_ar, _ = PAGES[name]
        emit(render(name), "ar", ar_path, en_path, out, d_ar)
    for name, out in en_pages.items():
        key = "index.src.html" if name == "en.src.html" else name
        ar_path, en_path, _, d_en = PAGES[key]
        emit(render(name), "en", ar_path, en_path, out, d_en)
    # Old .html addresses keep working (store listings may still point at them).
    for old, new in [("en.html", "en/"), ("privacy.html", "privacy/"), ("delete-account.html", "delete-account/")]:
        target = f"{ORIGIN}/vet-charted/{new}"
        (ROOT / old).write_text(
            '<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Redirecting…</title>'
            f'<link rel="canonical" href="{target}"><meta name="robots" content="noindex">'
            f'<meta http-equiv="refresh" content="0; url=/vet-charted/{new}">'
            f'<script>location.replace("/vet-charted/{new}"+location.search+location.hash)</script></head>'
            f'<body><a href="/vet-charted/{new}">{target}</a></body></html>', encoding="utf-8")
