"""
Design system shared by every generated SVG on the profile.

- Two themes ("dark" = night lab, "light" = lab paper) served through <picture>.
- Real typefaces (Instrument Serif, Inter, JetBrains Mono — all SIL OFL) are
  subset per-SVG to only the glyphs used and embedded as base64 WOFF2, so the
  artwork renders identically everywhere without any external requests.
- Motion respects prefers-reduced-motion.
"""
from __future__ import annotations

import base64
import html
import io
import os
import re
from functools import lru_cache

from fontTools import subset
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "fonts")

THEMES = {
    "dark": dict(
        bg="#0A0D17", bg2="#0E1322", panel="#111829", line="#1E2840", line2="#2A3654",
        text="#ECF1FA", muted="#93A0BD", dim="#5A6683",
        cyan="#3BE3F0", amber="#FFB547", violet="#A994FF", green="#4ADE80", rose="#FF7A90",
        glow=0.22, grid=0.10, photo_ring="#0A0D17",
    ),
    "light": dict(
        bg="#FBFAF6", bg2="#F4F1EA", panel="#FFFFFF", line="#E4DFD3", line2="#D3CCBC",
        text="#14171F", muted="#596173", dim="#9AA0AE",
        cyan="#0A8FA8", amber="#C26E00", violet="#6D4AE0", green="#16823F", rose="#D6264A",
        glow=0.12, grid=0.16, photo_ring="#FBFAF6",
    ),
}

# family -> list of (file, style, weight)
FONTS = {
    "KSerif": [("InstrumentSerif-Regular.ttf", "normal", 400), ("InstrumentSerif-Italic.ttf", "italic", 400)],
    "KSans": [("Inter-Regular.ttf", "normal", 400), ("Inter-SemiBold.ttf", "normal", 600)],
    "KMono": [("JetBrainsMono-Regular.ttf", "normal", 400), ("JetBrainsMono-Bold.ttf", "normal", 700)],
}

BASE_CSS = """
.serif{font-family:KSerif,'Iowan Old Style',Georgia,serif}
.sans{font-family:KSans,'Segoe UI',Helvetica,Arial,sans-serif}
.mono{font-family:KMono,ui-monospace,Consolas,Menlo,monospace}
text{white-space:pre}.i{font-style:italic}.b{font-weight:600}.mb{font-weight:700}
@media (prefers-reduced-motion:reduce){*{animation:none!important}}
"""


@lru_cache(maxsize=None)
def _load(path: str) -> bytes:
    with open(path, "rb") as fh:
        return fh.read()


def _subset_b64(fname: str, chars: str) -> str:
    font = TTFont(io.BytesIO(_load(os.path.join(FONT_DIR, fname))))
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = ["kern", "liga", "calt", "tnum"]
    opts.name_IDs = []
    opts.hinting = False
    opts.desubroutinize = True
    opts.notdef_outline = True
    sub = subset.Subsetter(opts)
    sub.populate(text=chars + " ")
    sub.subset(font)
    buf = io.BytesIO()
    font.flavor = "woff2"
    font.save(buf)
    return base64.b64encode(buf.getvalue()).decode()


def visible_text(svg_body: str) -> str:
    # text nodes only (drop <style>, tags and attribute values)
    body = re.sub(r"<style.*?</style>", "", svg_body, flags=re.S)
    body = re.sub(r"<title>.*?</title>", "", body, flags=re.S)
    txt = re.sub(r"<[^>]+>", "", body)
    return "".join(sorted(set(html.unescape(txt))))


def font_css(svg_body: str) -> str:
    chars = visible_text(svg_body)
    tokens = set()
    for cl in re.findall(r'class="([^"]+)"', svg_body):
        tokens.update(cl.split())
    out = []
    for fam, faces in FONTS.items():
        cls = {"KSerif": "serif", "KSans": "sans", "KMono": "mono"}[fam]
        if cls not in tokens:
            continue
        for fname, style, weight in faces:
            if style == "italic" and "i" not in tokens:
                continue
            if weight >= 600 and not ({"b", "mb"} & tokens):
                continue
            b64 = _subset_b64(fname, chars)
            out.append(
                f"@font-face{{font-family:{fam};font-style:{style};font-weight:{weight};"
                f"src:url(data:font/woff2;base64,{b64}) format('woff2')}}"
            )
    return "".join(out)


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def svg(w: int, h: int, body: str, title: str, css: str = "") -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        f'width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(title)}" xml:space="preserve">'
        f"<title>{esc(title)}</title>"
        f"<style>{font_css(body)}{BASE_CSS}{css}</style>"
        f"{body}</svg>"
    )


def data_uri(path: str, mime: str = "image/jpeg") -> str:
    return f"data:{mime};base64,{base64.b64encode(_load(path)).decode()}"


def mono_w(text: str, size: float, spacing: float = 0.0) -> float:
    """JetBrains Mono advance = 0.6em."""
    return len(text) * (size * 0.6 + spacing)


def card(w: int, h: int, t: dict, r: int = 20) -> str:
    return (
        f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="{r}" fill="{t["bg"]}" stroke="{t["line"]}"/>'
    )


def write(path: str, content: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(content)
