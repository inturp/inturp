"""Check deployed static artifacts, language metadata and local assets (stdlib only)."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json
import xml.etree.ElementTree as ET

root = Path(__file__).resolve().parents[2]
class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]; self.assets=[]; self.meta=[]; self.h1=0; self.lang=None; self.ld=False; self.schemas=[]
    def handle_starttag(self, tag, attrs):
        d=dict(attrs)
        if tag=='html': self.lang=d.get('lang')
        if tag=='h1': self.h1+=1
        if tag=='link': self.links.append(d)
        if tag=='meta': self.meta.append(d)
        if tag in ['img','script'] and d.get('src'): self.assets.append(d['src'])
        if tag=='link' and d.get('rel') in ['stylesheet','icon']: self.assets.append(d['href'])
        if tag=='script': self.ld=d.get('type')=='application/ld+json'
    def handle_data(self, text):
        if self.ld: self.schemas.append(json.loads(text))
    def handle_endtag(self, tag):
        if tag=='script': self.ld=False

urls=ET.parse(root/'sitemap.xml').findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url')
for entry in urls:
    url=entry.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text
    rel=urlsplit(url).path.lstrip('/')
    file=root/(rel+'index.html' if not rel or rel.endswith('/') else rel)
    assert file.exists(), url
    page=Page(); page.feed(file.read_text())
    canonical=[link['href'] for link in page.links if link.get('rel')=='canonical']
    assert canonical==[url], (url, canonical)
    assert page.h1==1, (url, page.h1)
    assert any(meta.get('name')=='description' and meta.get('content') for meta in page.meta), url
    if '/ar/' in url: assert page.lang=='ar', url
    if url.endswith('en.html'): assert page.lang=='en', url
    for asset in page.assets:
        parsed=urlsplit(asset)
        if parsed.scheme or parsed.netloc: continue
        local=(root/parsed.path.lstrip('/')) if parsed.path.startswith('/') else file.parent/parsed.path
        assert local.exists(), (url, asset)
print(f'PASS: {len(urls)} sitemap pages, canonical URLs, headings, descriptions, JSON-LD and local assets.')
