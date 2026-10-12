#!/usr/bin/env python3
"""Builds the static pages from src/ (no dependencies).

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


def render(name: str, out: str) -> None:
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
    (ROOT / out).write_text(page, encoding="utf-8")
    print(f"built {out} ({len(page) // 1024} KB)")


if __name__ == "__main__":
    render("index.src.html", "index.html")
    render("en.src.html", "en.html")
    render("privacy.src.html", "privacy.html")
    render("delete.src.html", "delete-account.html")
