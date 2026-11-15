"""Generate responsive profile covers. No scripts, remote fonts, or motion required.

    python scripts/build_profile_art.py

Archived artwork in assets/svg is preserved for existing repository backlinks.
"""
from __future__ import annotations

import math
from pathlib import Path

from design import THEMES, data_uri, esc, svg, write
from profile_data import PROJECTS

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "profile"


def lattice(t, cx, cy, radius):
    """A molecular sketch, drawn as decoration rather than simulation output."""
    points = [(cx + radius * math.cos(i * math.pi / 3),
               cy + radius * math.sin(i * math.pi / 3)) for i in range(6)]
    lines = []
    for i, (x, y) in enumerate(points):
        nx, ny = points[(i + 1) % 6]
        lines.append(f'<path d="M{x:.1f},{y:.1f} L{nx:.1f},{ny:.1f}" stroke="{t["cyan"]}" stroke-opacity=".4" stroke-width="1.4"/>')
        if i % 2 == 0:
            lines.append(f'<path d="M{x:.1f},{y:.1f} L{cx},{cy}" stroke="{t["cyan"]}" stroke-opacity=".18" stroke-width="1"/>')
        lines.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.5" fill="{t["bg"]}" stroke="{t["cyan"]}" stroke-width="1.5"/>')
    return "".join(lines)


def hero(t, mobile=False):
    w, h = (480, 430) if mobile else (960, 344)
    cx, cy, r = (366, 318, 73) if mobile else (776, 174, 107)
    photo = data_uri(str(ROOT / "assets" / "photos" / "portrait-hero.jpg"))
    x, label_y, first_y, second_y = (28, 43, 112, 172) if mobile else (42, 45, 132, 211)
    fs = 57 if mobile else 75
    body = f"""
<defs>
  <clipPath id="rounded"><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="22"/></clipPath>
  <clipPath id="portrait"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>
  <radialGradient id="wash" cx=".9" cy=".6" r=".9">
    <stop stop-color="{t['cyan']}" stop-opacity=".13"/>
    <stop offset="1" stop-color="{t['cyan']}" stop-opacity="0"/>
  </radialGradient>
</defs>
<g clip-path="url(#rounded)">
  <rect width="{w}" height="{h}" fill="{t['bg']}"/>
  <rect width="{w}" height="{h}" fill="url(#wash)"/>
  <path d="M0,{h-46} H{w}" stroke="{t['line']}"/>
  {lattice(t, cx, cy, r+42)}
  <circle cx="{cx}" cy="{cy}" r="{r+11}" fill="none" stroke="{t['amber']}" stroke-opacity=".5" stroke-dasharray="2 7"/>
  <image href="{photo}" x="{cx-r}" y="{cy-r}" width="{2*r}" height="{2*r}" clip-path="url(#portrait)" preserveAspectRatio="xMidYMid slice"/>
  <circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{t['line2']}" stroke-width="2"/>
</g>
<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="22" fill="none" stroke="{t['line']}"/>
<circle cx="{x+4}" cy="{label_y-5}" r="3.5" fill="{t['cyan']}"/>
<text class="mono" x="{x+18}" y="{label_y}" font-size="12" letter-spacing="2" fill="{t['muted']}">THE RESEARCH / SOFTWARE NOTEBOOK</text>
<text class="serif" x="{x-2}" y="{first_y}" font-size="{fs}" fill="{t['text']}">A little chemistry.</text>
<text class="serif i" x="{x-2}" y="{second_y}" font-size="{fs}" fill="{t['amber']}">A lot of curiosity.</text>
"""
    if mobile:
        body += f"""
<text class="sans" x="{x}" y="222" font-size="18" fill="{t['muted']}">Energy materials.</text>
<text class="sans" x="{x}" y="250" font-size="18" fill="{t['muted']}">Thoughtful software.</text>
<text class="mono" x="{x}" y="299" font-size="12" fill="{t['cyan']}" letter-spacing="2">ASK. BUILD.</text>
<text class="mono" x="{x}" y="319" font-size="12" fill="{t['cyan']}" letter-spacing="2">REFINE. REPEAT.</text>
<text class="mono" x="{x}" y="412" font-size="12" fill="{t['muted']}">KAMRAN ASHRAF / ISLAMABAD, PK</text>
"""
    else:
        body += f"""
<text class="sans" x="{x}" y="258" font-size="18" fill="{t['muted']}">Energy materials. Thoughtful software. Useful experiments.</text>
<text class="mono" x="{x}" y="326" font-size="12" fill="{t['muted']}" letter-spacing="1">KAMRAN ASHRAF / ISLAMABAD, PK</text>
<text class="mono" x="{w-40}" y="326" font-size="12" fill="{t['cyan']}" text-anchor="end" letter-spacing="1">ASK. BUILD. REFINE. REPEAT.</text>
"""
    return svg(w, h, body, "A little chemistry. A lot of curiosity. — Kamran Ashraf")


def illustration(t, kind, color):
    """Local coordinates: a small abstract sketch with no essential text."""
    if kind == "papers":
        s = []
        for i in range(3):
            x, y = 35 + 26*i, 16 - 8*i
            s.append(f'<rect x="{x}" y="{y}" width="72" height="94" rx="7" fill="{t["panel"]}" stroke="{color}" stroke-opacity="{.3+i*.3}"/>')
            for j in range(4):
                s.append(f'<path d="M{x+15},{y+25+j*14} h{36 if j%2 else 43}" stroke="{color}" stroke-opacity=".5" stroke-width="2" stroke-linecap="round"/>')
        return "".join(s)
    if kind == "agent":
        return f"""
<path d="M25,60 H170" stroke="{color}" stroke-opacity=".4" stroke-width="2"/>
<rect x="12" y="37" width="46" height="46" rx="12" fill="{t['panel']}" stroke="{color}"/>
<path d="M24,52 l8,8 -8,8 M38,68 h8" fill="none" stroke="{color}" stroke-width="2"/>
<path d="M100,34 L126,60 100,86 74,60 Z" fill="{t['panel']}" stroke="{color}"/>
<path d="M90,60 l7,7 13,-15" fill="none" stroke="{color}" stroke-width="2"/>
<circle cx="165" cy="60" r="17" fill="{t['panel']}" stroke="{color}"/>
<circle cx="165" cy="60" r="5" fill="{color}"/>
"""
    s = [f'<path d="M12,88 H184" stroke="{color}" stroke-width="1.5"/>',
         f'<path d="M54,88 a44,44 0 0,1 88,0" fill="{color}" fill-opacity=".14" stroke="{color}" stroke-width="2"/>']
    for angle in range(-160, 0, 30):
        a = math.radians(angle)
        s.append(f'<path d="M{98+56*math.cos(a):.1f},{88+56*math.sin(a):.1f} L{98+66*math.cos(a):.1f},{88+66*math.sin(a):.1f}" stroke="{color}" stroke-width="2" stroke-linecap="round"/>')
    return "".join(s)


def cover(t, project, index, mobile=False):
    w, h = (480, 158) if mobile else (960, 174)
    x = 26 if mobile else 38
    c = t[project["color"]]
    fs = 36 if mobile else 53
    body = f"""
<defs><clipPath id="cover"><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="16"/></clipPath></defs>
<g clip-path="url(#cover)">
  <rect width="{w}" height="{h}" fill="{t['bg']}"/>
  <rect width="4" height="{h}" fill="{c}"/>
  <circle cx="{w-36}" cy="{h/2}" r="122" fill="{c}" fill-opacity=".04"/>
</g>
<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="16" fill="none" stroke="{t['line']}"/>
<text class="mono" x="{x}" y="{37 if mobile else 44}" font-size="{12 if mobile else 13}" letter-spacing="1.8" fill="{c}">0{index} / {esc(project['category'])}</text>
<text class="serif" x="{x-1}" y="{91 if mobile else 110}" font-size="{fs}" fill="{t['text']}">{esc(project['name'])}</text>
<text class="mono" x="{x}" y="{133 if mobile else 148}" font-size="{12 if mobile else 13}" fill="{t['muted']}">{esc(project['symbol'])} · A KAMRAN ASHRAF PROJECT</text>
"""
    if not mobile:
        body += f'<g transform="translate(694,28)">{illustration(t, project["art"], c)}</g>'
    return svg(w, h, body, project["name"] + " — " + project["category"].lower())


def main():
    for theme, t in THEMES.items():
        for mobile in (False, True):
            suffix = f"{'mobile-' if mobile else ''}{theme}"
            write(str(OUT / f"hero-{suffix}.svg"), hero(t, mobile))
            for index, project in enumerate(PROJECTS, 1):
                write(str(OUT / f"{project['repo'].lower()}-{suffix}.svg"), cover(t, project, index, mobile))
    print(f"Wrote 16 responsive covers to {OUT}")


if __name__ == "__main__":
    main()
