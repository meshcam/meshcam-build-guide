#!/usr/bin/env python3
"""Build the MeshCam build guide into static HTML.

    python3 build.py            # writes site/
    python3 build.py --out DIR

One dependency: Python-Markdown (requirements.txt), whose only built-in
extensions are used here. Everything else is this file, template.html and
style.css. No JavaScript reaches the reader.

The chapter order is CHAPTERS below. Each chapter is docs/<slug>.md and is
published at /build/<slug>/ (the first one at /build/). Its title is its first
`# heading`.

The build is strict: a link to a chapter that does not exist, an anchor that
is not a heading in that chapter, or an image that is not in docs/ stops the
build with an error instead of shipping a 404.
"""

import argparse
import html
import re
import shutil
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import urlsplit

import markdown
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor

# The path the site is served under. The meshcam app proxies exactly this
# prefix to the guide pod, and every link the build emits starts with it.
BASE = "/build/"
SITE_NAME = "MeshCam build guide"

# (source file stem, nav label). The first entry is the landing page.
CHAPTERS = [
    ("index", "Start here"),
    ("parts", "Parts list"),
    ("battery-and-solar", "Battery and solar"),
    ("first-boot", "First boot"),
    ("deploying", "Deploying"),
    ("troubleshooting", "Troubleshooting"),
]

COMMENT = re.compile(r"<!--.*?-->\n?", re.DOTALL)

ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"


def page_url(stem: str) -> str:
    return BASE if stem == "index" else f"{BASE}{stem}/"


class LinkRewriter(Treeprocessor):
    """Turn `parts.md#x` into `/build/parts/#x` and `img/a.jpg` into
    `/build/img/a.jpg`, and record what each link points at so the build can
    check it once every chapter's headings are known."""

    def __init__(self, md, stem, refs):
        super().__init__(md)
        self.stem = stem
        self.refs = refs

    def run(self, root):
        for el in root.iter():
            if el.tag == "a" and el.get("href"):
                el.set("href", self._rewrite(el.get("href"), "link"))
            elif el.tag == "img" and el.get("src"):
                el.set("src", self._rewrite(el.get("src"), "image"))
                el.set("loading", "lazy")

    def _rewrite(self, url: str, kind: str) -> str:
        parts = urlsplit(url)
        if parts.scheme or parts.netloc or url.startswith("/"):
            return url  # external or already absolute
        if not parts.path:  # "#anchor" within this page
            self.refs.append((self.stem, "anchor", self.stem, parts.fragment))
            return url
        if parts.path.endswith(".md"):
            target = parts.path[:-3]
            self.refs.append((self.stem, "chapter", target, parts.fragment))
            return page_url(target) + (f"#{parts.fragment}" if parts.fragment else "")
        self.refs.append((self.stem, kind, parts.path, ""))
        return BASE + parts.path


class Rewrite(Extension):
    def __init__(self, stem, refs):
        super().__init__()
        self.stem, self.refs = stem, refs

    def extendMarkdown(self, md):
        md.treeprocessors.register(LinkRewriter(md, self.stem, self.refs), "meshcam_links", 0)


def render_nav(current: str) -> str:
    items = []
    for stem, label in CHAPTERS:
        here = ' aria-current="page"' if stem == current else ""
        items.append(f'<li><a href="{page_url(stem)}"{here}>{html.escape(label)}</a></li>')
    return "\n".join(items)


def render_pager(i: int) -> str:
    out = []
    if i > 0:
        stem, label = CHAPTERS[i - 1]
        out.append(
            f'<a class="prev" href="{page_url(stem)}" rel="prev">'
            f"<span>Previous</span>{html.escape(label)}</a>"
        )
    if i < len(CHAPTERS) - 1:
        stem, label = CHAPTERS[i + 1]
        out.append(
            f'<a class="next" href="{page_url(stem)}" rel="next">'
            f"<span>Next</span>{html.escape(label)}</a>"
        )
    return "\n".join(out)


def fill(template: str, **values: str) -> str:
    for key, value in values.items():
        template = template.replace("{{" + key + "}}", value)
    return template


def build(out: Path) -> int:
    template = (ROOT / "template.html").read_text()
    refs: list[tuple[str, str, str, str]] = []
    anchors: dict[str, set[str]] = {}
    pages: dict[str, tuple[str, str]] = {}

    for stem, _label in CHAPTERS:
        # HTML comments are notes to editors (photo plans, open questions).
        # They stay in the Markdown and never reach the published page.
        source = COMMENT.sub("", (DOCS / f"{stem}.md").read_text())
        md = markdown.Markdown(
            extensions=[
                "tables",
                "admonition",
                "fenced_code",
                "attr_list",
                "toc",
                Rewrite(stem, refs),
            ],
            extension_configs={"toc": {"permalink": "#", "permalink_title": "Link to this section"}},
            output_format="html",
        )
        body = md.convert(source)
        tokens = md.toc_tokens
        if not tokens or tokens[0]["level"] != 1:
            sys.exit(f"docs/{stem}.md: must start with a '# Title' heading")
        anchors[stem] = set()

        def walk(ts):
            for t in ts:
                anchors[stem].add(t["id"])
                walk(t["children"])

        walk(tokens)
        pages[stem] = (html.unescape(tokens[0]["name"]), body)

    errors = []
    stems = {s for s, _ in CHAPTERS}
    for src, kind, target, frag in refs:
        where = f"docs/{src}.md"
        if kind in ("chapter", "anchor"):
            if target not in stems:
                errors.append(f"{where}: link to {target}.md, which is not a chapter")
            elif frag and frag not in anchors[target]:
                errors.append(f"{where}: link to {target}.md#{frag}, no such heading")
        elif not (DOCS / target).is_file():
            errors.append(f"{where}: {kind} {target} does not exist under docs/")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    shutil.copytree(DOCS / "img", out / "img")
    shutil.copy2(ROOT / "style.css", out / "style.css")

    for i, (stem, _label) in enumerate(CHAPTERS):
        title, body = pages[stem]
        page_title = SITE_NAME if stem == "index" else f"{title} · {SITE_NAME}"
        dest = out / ("index.html" if stem == "index" else f"{stem}/index.html")
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(
            fill(
                template,
                title=html.escape(page_title),
                canonical=f"https://docs.getmeshcam.com{page_url(stem)}",
                base=BASE,
                nav=render_nav(stem),
                content=body,
                pager=render_pager(i),
            )
        )

    dest = out / "404.html"
    dest.write_text(
        fill(
            template,
            title=html.escape(f"Page not found · {SITE_NAME}"),
            canonical=f"https://docs.getmeshcam.com{BASE}",
            base=BASE,
            nav=render_nav(""),
            content=(
                "<h1>Page not found</h1>\n<p>That page is not part of the build "
                f'guide. Start from <a href="{BASE}">the first chapter</a>.</p>'
            ),
            pager="",
        )
    )
    print(f"built {len(CHAPTERS)} chapters into {out}")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--out", type=Path, default=ROOT / "site")
    sys.exit(build(ap.parse_args().out))
