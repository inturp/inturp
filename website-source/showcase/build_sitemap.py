#!/usr/bin/env python3
"""Writes sitemap.xml (root and website-source/public) with hreflang alternates and lastmod.

  python3 website-source/showcase/build_sitemap.py

Every entry is an (English path, Arabic path) pair; each URL lists both as alternates, x-default is the English one.
"""
import pathlib

SITE = pathlib.Path(__file__).resolve().parents[2]
ORIGIN = 'https://inturp.com'
LASTMOD = '2026-10-12'
PAIRS = [
    ('/', '/ar/'),
    ('/about/', '/ar/about/'),
    ('/vetcharted/', '/ar/vetcharted/'),
    ('/privacy/', '/ar/privacy/'),
    ('/vet-charted/en/', '/vet-charted/'),
    ('/vet-charted/en/privacy/', '/vet-charted/privacy/'),
    ('/vet-charted/en/delete-account/', '/vet-charted/delete-account/'),
    ('/alameer/', '/ar/alameer/'),
    ('/alameer/privacy/', '/ar/alameer/privacy/'),
    ('/alameer/delete-account/', '/ar/alameer/delete-account/'),
    ('/checkbook/', '/ar/checkbook/'),
    ('/checkbook/privacy/', '/ar/checkbook/privacy/'),
    ('/checkbook/delete-account/', '/ar/checkbook/delete-account/'),
]


def entry(loc, en, ar):
    alts = (f'<xhtml:link rel="alternate" hreflang="en" href="{ORIGIN}{en}" />'
            f'<xhtml:link rel="alternate" hreflang="ar" href="{ORIGIN}{ar}" />'
            f'<xhtml:link rel="alternate" hreflang="x-default" href="{ORIGIN}{en}" />')
    return f'<url><loc>{ORIGIN}{loc}</loc><lastmod>{LASTMOD}</lastmod>{alts}</url>'


def main():
    urls = []
    for en, ar in PAIRS:
        urls += [entry(en, en, ar), entry(ar, en, ar)]
    xml = ("<?xml version='1.0' encoding='utf-8'?>\n"
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">'
           + ''.join(urls) + '</urlset>')
    for f in (SITE / 'sitemap.xml', SITE / 'website-source' / 'public' / 'sitemap.xml'):
        f.write_text(xml, encoding='utf-8')
    print(f'sitemap: {len(urls)} URLs')


if __name__ == '__main__':
    main()
