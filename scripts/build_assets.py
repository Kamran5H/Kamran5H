"""
Render every static SVG used by the profile README, in dark + light themes.

    python scripts/build_assets.py

Output: assets/svg/<name>-<theme>.svg
"""
from __future__ import annotations

import math
import os
import random

from design import THEMES, card, data_uri, esc, mono_w, svg, write

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "svg")
PHOTOS = os.path.join(ROOT, "assets", "photos")


# ───────────────────────────── helpers ──────────────────────────────
def hex_pts(cx, cy, r, rot=-90.0):
    return [
        (cx + r * math.cos(math.radians(rot + 60 * k)), cy + r * math.sin(math.radians(rot + 60 * k)))
        for k in range(6)
    ]


def pts(p):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in p)


def corner_marks(w, h, t, inset=14, ln=12):
    c = t["dim"]
    s = []
    for x, y, dx, dy in ((inset, inset, 1, 1), (w - inset, inset, -1, 1), (inset, h - inset, 1, -1), (w - inset, h - inset, -1, -1)):
        s.append(f'<path d="M{x},{y + dy * ln} L{x},{y} L{x + dx * ln},{y}" fill="none" stroke="{c}" stroke-width="1" opacity=".7"/>')
    return "".join(s)


def check_icon(x, y, color, s=1.0):
    return (
        f'<path d="M{x},{y} l{4*s:.1f},{4*s:.1f} l{8*s:.1f},{-9*s:.1f}" fill="none" stroke="{color}" '
        f'stroke-width="{2*s:.1f}" stroke-linecap="round" stroke-linejoin="round"/>'
    )


def arrow(x1, y, x2, color, w=1.6, head=7):
    return (
        f'<path class="draw" pathLength="1" d="M{x1},{y} L{x2},{y}" stroke="{color}" stroke-width="{w}" fill="none"/>'
        f'<path d="M{x2 - head},{y - head * .65} L{x2},{y} L{x2 - head},{y + head * .65}" stroke="{color}" '
        f'stroke-width="{w}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
    )


def ne_arrow(x, y, color, s=7, w=1.4):
    """small ↗ glyph drawn as a path (bottom-left anchor)."""
    return (
        f'<path d="M{x},{y} L{x + s},{y - s} M{x + 2},{y - s} L{x + s},{y - s} L{x + s},{y - 2}" '
        f'stroke="{color}" stroke-width="{w}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
    )


DRAW_CSS = """
.draw{stroke-dasharray:1;stroke-dashoffset:0;animation:draw 2.4s cubic-bezier(.6,0,.2,1) .3s both}
@keyframes draw{from{stroke-dashoffset:1}to{stroke-dashoffset:0}}
.fade{animation:fade .7s ease both}
@keyframes fade{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
"""


def save(name, theme, content):
    path = os.path.join(OUT, f"{name}-{theme}.svg")
    write(path, content)
    return path


# ───────────────────────────── 1. HERO ──────────────────────────────
TAGLINES = [
    "building local-first autonomous AI agents",
    "simulating molecules with DFT / Quantum ESPRESSO",
    "engineering resilient scrapers & Chrome MV3 tools",
    "studying Ce-doped NiCo-MOF electrocatalysts",
]


def hero(t):
    W, H = 1200, 460
    cx, cy, R = 250, 230, 148
    s = 17
    hw = s * math.sqrt(3)
    photo = data_uri(os.path.join(PHOTOS, "portrait-hero.jpg"))
    X = 532

    defs = f"""
<defs>
  <clipPath id="cardclip"><rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="22"/></clipPath>
  <clipPath id="hexclip"><polygon points="{pts(hex_pts(cx, cy, R))}"/></clipPath>
  <pattern id="lat" width="{hw:.3f}" height="{3*s}" patternUnits="userSpaceOnUse">
    <path d="M{hw/2:.3f},0 L{hw:.3f},{s/2} L{hw:.3f},{1.5*s} L{hw/2:.3f},{2*s} L0,{1.5*s} L0,{s/2} Z M{hw/2:.3f},{2*s} L{hw/2:.3f},{3*s}" fill="none" stroke="{t['muted']}" stroke-width=".6"/>
  </pattern>
  <radialGradient id="fadeR" cx="{cx}" cy="{cy}" r="560" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="#fff" stop-opacity="1"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
  </radialGradient>
  <mask id="latmask"><rect width="{W}" height="{H}" fill="url(#fadeR)"/></mask>
  <radialGradient id="g1" cx="{cx}" cy="{cy}" r="330" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="{t['cyan']}" stop-opacity="{t['glow']}"/><stop offset="1" stop-color="{t['cyan']}" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="g2" cx="1180" cy="10" r="460" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="{t['amber']}" stop-opacity="{t['glow']*0.8}"/><stop offset="1" stop-color="{t['amber']}" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="ring" x1="{cx-R}" y1="{cy-R}" x2="{cx+R}" y2="{cy+R}" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="{t['cyan']}"/><stop offset="1" stop-color="{t['amber']}"/>
  </linearGradient>
  <linearGradient id="nameg" x1="{X}" y1="0" x2="{X+300}" y2="0" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="{t['amber']}"/><stop offset="1" stop-color="{t['rose']}"/>
  </linearGradient>
  <linearGradient id="shade" x1="0" y1="0" x2="0" y2="1">
    <stop offset=".55" stop-color="{t['bg']}" stop-opacity="0"/><stop offset="1" stop-color="{t['bg']}" stop-opacity=".55"/>
  </linearGradient>
"""
    # tagline clip-wipes + carets (SMIL so they are deterministic everywhere)
    tl_defs, tl_body = [], []
    n = len(TAGLINES)
    for i, line in enumerate(TAGLINES):
        wpx = mono_w(line, 16.5) + 30
        st, en = i / n, (i + 1) / n
        ks = [0.0]
        vs = [0.0]
        if st > 0:
            ks.append(st); vs.append(0)
        ks += [st + 0.07, en - 0.012, en]
        vs += [wpx, wpx, 0]
        if en < 1:
            ks.append(1.0); vs.append(0)
        kt = ";".join(f"{k:.4f}" for k in ks)
        v = ";".join(f"{x:.1f}" for x in vs)
        vx = ";".join(f"{X + x:.1f}" for x in vs)
        op = ";".join("1" if (x > 0 or (j + 1 < len(vs) and vs[j + 1] > 0)) else "0" for j, x in enumerate(vs))
        tl_defs.append(
            f'<clipPath id="tl{i}"><rect x="{X}" y="322" width="0" height="30">'
            f'<animate attributeName="width" values="{v}" keyTimes="{kt}" dur="18s" repeatCount="indefinite"/></rect></clipPath>'
        )
        tl_body.append(
            f'<g clip-path="url(#tl{i})"><text class="mono" x="{X}" y="343" font-size="16.5" fill="{t["text"]}">'
            f'<tspan fill="{t["cyan"]}">&gt; </tspan>{esc(line[0:])}</text></g>'
            f'<g class="blink"><rect x="{X}" y="327" width="9" height="20" fill="{t["cyan"]}" opacity="0">'
            f'<animate attributeName="x" values="{vx}" keyTimes="{kt}" dur="18s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="{op}" keyTimes="{kt}" dur="18s" repeatCount="indefinite" calcMode="discrete"/></rect></g>'
        )
    defs += "".join(tl_defs) + "</defs>"

    # benzene / orbit system
    R2 = R + 30
    outer = hex_pts(cx, cy, R2)
    inner = hex_pts(cx, cy, R2 - 9)
    dbl = []
    for k in (0, 2, 4):
        (x1, y1), (x2, y2) = inner[k], inner[(k + 1) % 6]
        ax, ay = x1 + (x2 - x1) * .2, y1 + (y2 - y1) * .2
        bx, by = x1 + (x2 - x1) * .8, y1 + (y2 - y1) * .8
        dbl.append(f'<line x1="{ax:.1f}" y1="{ay:.1f}" x2="{bx:.1f}" y2="{by:.1f}" stroke="{t["line2"]}" stroke-width="1.4"/>')
    atoms = "".join(
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5.5" fill="{t["bg"]}" stroke="{t["cyan"] if k % 2 == 0 else t["amber"]}" stroke-width="2"/>'
        for k, (x, y) in enumerate(outer)
    )
    benzene = (
        f'<g><animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="90s" repeatCount="indefinite"/>'
        f'<polygon points="{pts(outer)}" fill="none" stroke="{t["line2"]}" stroke-width="1.4"/>{"".join(dbl)}{atoms}</g>'
    )

    def orbit(rot, rx, ry, color, dur, rev=False):
        d = f"M{cx - rx},{cy} a{rx},{ry} 0 1,{0 if rev else 1} {2*rx},0 a{rx},{ry} 0 1,{0 if rev else 1} {-2*rx},0"
        return (
            f'<g transform="rotate({rot} {cx} {cy})">'
            f'<path d="{d}" fill="none" stroke="{color}" stroke-opacity=".35" stroke-width="1" stroke-dasharray="2 6"/>'
            f'<g><animateMotion dur="{dur}s" repeatCount="indefinite" path="{d}"/>'
            f'<circle r="10" fill="{color}" opacity=".18"/><circle r="4" fill="{color}"/></g></g>'
        )

    portrait = (
        f'<polygon points="{pts(hex_pts(cx, cy, R + 7))}" fill="{t["photo_ring"]}"/>'
        f'<g clip-path="url(#hexclip)"><image href="{photo}" x="{cx-R}" y="{cy-R}" width="{2*R}" height="{2*R}" preserveAspectRatio="xMidYMid slice"/>'
        f'<rect x="{cx-R}" y="{cy-R}" width="{2*R}" height="{2*R}" fill="url(#shade)"/></g>'
        f'<polygon class="flow" points="{pts(hex_pts(cx, cy, R + 7))}" fill="none" stroke="url(#ring)" stroke-width="2.2" stroke-dasharray="14 8"/>'
    )

    # meta row
    mx = X
    meta = []
    meta.append(f'<circle cx="{mx+4}" cy="414" r="3.5" fill="none" stroke="{t["cyan"]}" stroke-width="1.6"/>')
    lab = "Islamabad, PK"
    meta.append(f'<text class="mono" x="{mx+16}" y="418.5" font-size="12.5" fill="{t["muted"]}">{lab}</text>')
    mx += 16 + mono_w(lab, 12.5) + 18
    meta.append(f'<text class="mono" x="{mx}" y="418.5" font-size="12.5" fill="{t["dim"]}">/</text>')
    mx += 22
    lab = "MPhil Chemistry · QAU"
    meta.append(f'<text class="mono" x="{mx}" y="418.5" font-size="12.5" fill="{t["muted"]}">{lab}</text>')
    mx += mono_w(lab, 12.5) + 18
    meta.append(f'<text class="mono" x="{mx}" y="418.5" font-size="12.5" fill="{t["dim"]}">/</text>')
    mx += 22
    meta.append(f'<circle class="pulse" cx="{mx+4}" cy="414" r="4" fill="{t["green"]}"/><circle cx="{mx+4}" cy="414" r="4" fill="{t["green"]}"/>')
    meta.append(f'<text class="mono" x="{mx+16}" y="418.5" font-size="12.5" fill="{t["text"]}">open to collaboration</text>')

    prompt = "kamran@qau:~$ whoami --verbose"
    body = f"""{defs}
<g clip-path="url(#cardclip)">
  <rect width="{W}" height="{H}" fill="{t['bg']}"/>
  <rect width="{W}" height="{H}" fill="url(#lat)" mask="url(#latmask)" opacity="{t['grid']}"/>
  <rect width="{W}" height="{H}" fill="url(#g1)"/><rect width="{W}" height="{H}" fill="url(#g2)"/>
</g>
<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="22" fill="none" stroke="{t['line']}"/>
{corner_marks(W, H, t)}
{orbit(-28, 232, 64, t['amber'], 11, True)}
{benzene}
{portrait}
{orbit(28, 232, 64, t['cyan'], 7)}
<text class="mono" x="1166" y="44" font-size="11" fill="{t['dim']}" text-anchor="end" letter-spacing="2">PROFILE / v3 / 2026</text>
<text class="mono" x="{X}" y="74" font-size="13" fill="{t['muted']}"><tspan fill="{t['green']}">kamran@qau</tspan>:<tspan fill="{t['cyan']}">~</tspan>$ whoami --verbose</text>
<rect class="blink" x="{X + mono_w(prompt, 13) + 6:.1f}" y="62" width="8" height="15" fill="{t['cyan']}"/>
<text class="mono fade" style="animation-delay:.1s" x="{X}" y="126" font-size="12.5" fill="{t['cyan']}" letter-spacing="3.2">AI SYSTEMS ARCHITECT  ×  COMPUTATIONAL CHEMIST</text>
<text class="serif fade" style="animation-delay:.25s" x="{X-3}" y="210" font-size="84" fill="{t['text']}" letter-spacing="-1">Muhammad Kamran</text>
<text class="serif i fade" style="animation-delay:.4s" x="{X-3}" y="292" font-size="84" fill="url(#nameg)" letter-spacing="-1">Ashraf<tspan fill="{t['cyan']}">.</tspan></text>
{''.join(tl_body)}
<line x1="{X}" y1="382" x2="1160" y2="382" stroke="{t['line']}"/>
{''.join(meta)}
"""
    css = DRAW_CSS + """
.blink{animation:blink 1.1s steps(1) infinite}@keyframes blink{50%{opacity:0}}
.flow{animation:flow 14s linear infinite}@keyframes flow{to{stroke-dashoffset:-220}}
.pulse{transform-box:fill-box;transform-origin:center;animation:pulse 2.2s ease-out infinite}
@keyframes pulse{0%{transform:scale(1);opacity:.7}100%{transform:scale(3.2);opacity:0}}
"""
    return svg(W, H, body, "Muhammad Kamran Ashraf — AI systems architect and computational chemist", css)


# ─────────────────────────── 2. NAV PILLS ───────────────────────────
NAV = [("01", "About"), ("02", "Work"), ("03", "Builds"), ("04", "Stack"), ("05", "Research"), ("06", "Contact")]


def nav_pill(t, num, label):
    W, H = 190, 52
    body = (
        f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="{(H-1)/2}" fill="{t["panel"]}" stroke="{t["line"]}"/>'
        f'<text class="mono" x="24" y="31" font-size="11.5" fill="{t["cyan"]}">{num}</text>'
        f'<text class="sans" x="52" y="31.5" font-size="15" fill="{t["text"]}">{label}</text>'
        + ne_arrow(W - 34, 31, t["dim"], 6, 1.3)
    )
    return svg(W, H, body, f"{label}")


# ───────────────────────── 3. SECTION HEADERS ───────────────────────
def header(t, num, title, sub):
    W, H = 1200, 128
    body = (
        f'<text class="serif i" x="0" y="104" font-size="118" fill="none" stroke="{t["dim"]}" stroke-opacity=".75" stroke-width="1.1">{num}</text>'
        f'<text class="serif" x="150" y="70" font-size="48" fill="{t["text"]}" letter-spacing="-.5">{esc(title)}</text>'
        f'<text class="mono" x="153" y="100" font-size="12.5" fill="{t["muted"]}" letter-spacing="1">{esc(sub)}</text>'
        f'<circle cx="153" cy="120" r="3" fill="{t["cyan"]}"/>'
        f'<path class="draw" pathLength="1" d="M160,120 L1200,120" stroke="{t["line"]}" stroke-width="1"/>'
    )
    return svg(W, H, body, f"{num} — {title}", DRAW_CSS)


SECTIONS = [
    ("01", "about", "The short version", "who / what / why"),
    ("02", "work", "Selected work", "four flagships, each shipped and tested"),
    ("03", "builds", "A periodic table of builds", "every public repository, grouped like elements"),
    ("04", "stack", "Spectrum of a toolchain", "what i reach for, read like an FTIR trace"),
    ("05", "research", "In the lab", "where the chemistry happens"),
    ("06", "telemetry", "Live telemetry", "regenerated twice a day by a GitHub Action"),
    ("07", "contact", "Let's build something", "research collabs, agents, automation"),
]


# ──────────────────────────── 4. ABOUT ──────────────────────────────
def element_tile(t, x, y, num, mass, sym, name, group, color, w=170, h=196, pulse_delay=None):
    pd = f' style="animation-delay:{pulse_delay:.2f}s"' if pulse_delay is not None else ""
    fs_name = 12.5 if len(name) <= 17 else 11
    return f"""<g transform="translate({x},{y})">
<clipPath id="tc{num}{x:.0f}"><rect width="{w}" height="{h}" rx="14"/></clipPath>
<g clip-path="url(#tc{num}{x:.0f})">
<rect width="{w}" height="{h}" fill="{t['panel']}"/>
<rect class="tpulse"{pd} width="{w}" height="{h}" fill="{color}" opacity="0"/>
<rect width="{w}" height="3.5" fill="{color}"/>
</g>
<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="14" fill="none" stroke="{color}" stroke-opacity=".45"/>
<text class="mono" x="16" y="30" font-size="13" fill="{t['text']}">{num}</text>
<text class="mono" x="{w-16}" y="30" font-size="11" fill="{color}" text-anchor="end">{esc(mass)}</text>
<text class="serif" x="{w/2}" y="{h*0.6:.0f}" font-size="68" fill="{t['text']}" text-anchor="middle">{esc(sym)}</text>
<text class="sans" x="{w/2}" y="{h*0.775:.0f}" font-size="{fs_name}" fill="{t['muted']}" text-anchor="middle">{esc(name)}</text>
<text class="mono" x="{w/2}" y="{h*0.9:.0f}" font-size="9.5" fill="{color}" text-anchor="middle" letter-spacing="1.8">{esc(group)}</text>
</g>"""


TILE_CSS = """
.tpulse{animation:tp 7s ease-in-out infinite}
@keyframes tp{0%{opacity:0}7%{opacity:.16}28%{opacity:0}100%{opacity:0}}
"""


def about(t):
    W, H = 1200, 520
    photo = data_uri(os.path.join(PHOTOS, "portrait-studio.jpg"))
    px, py, pw, ph = 60, 56, 320, 400
    X = 450
    kv = [
        ("role", "AI systems architect · computational chemist"),
        ("base", "Quaid-i-Azam University, Islamabad"),
        ("research", "Ce-doped NiCo-MOF electrocatalysis · DFT"),
        ("ships", "agents · scrapers · extensions · desktop apps"),
        ("stack", "Python · TypeScript · FastAPI · Playwright"),
    ]
    rows = []
    for i, (k, v) in enumerate(kv):
        y = 330 + i * 30
        rows.append(
            f'<text class="mono fade" style="animation-delay:{0.9 + i*0.12:.2f}s" x="{X}" y="{y}" font-size="14">'
            f'<tspan fill="{t["dim"]}">{k:<10}</tspan><tspan fill="{t["text"]}">{esc(v)}</tspan></text>'
        )
    pm = []
    for (x, y, dx, dy) in ((px - 10, py - 10, 1, 1), (px + pw + 10, py - 10, -1, 1), (px - 10, py + ph + 10, 1, -1), (px + pw + 10, py + ph + 10, -1, -1)):
        pm.append(f'<path d="M{x},{y + dy*16} L{x},{y} L{x + dx*16},{y}" fill="none" stroke="{t["cyan"]}" stroke-width="1.4"/>')
    body = f"""
<defs><clipPath id="pc"><rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="6"/></clipPath></defs>
{card(W, H, t, 22)}
{corner_marks(W, H, t)}
<image href="{photo}" x="{px}" y="{py}" width="{pw}" height="{ph}" clip-path="url(#pc)" preserveAspectRatio="xMidYMid slice"/>
<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="6" fill="none" stroke="{t['line2']}"/>
{''.join(pm)}
<text class="mono" x="{px}" y="{py+ph+40}" font-size="11.5" fill="{t['dim']}" letter-spacing=".5">FIG. 1 — The author. Islamabad, 2026.</text>
<text class="mono" x="{X}" y="88" font-size="12" fill="{t['cyan']}" letter-spacing="3">IN ONE EQUATION</text>
<text class="serif fade" style="animation-delay:.1s" x="{X-2}" y="152" font-size="54" fill="{t['text']}">Atoms <tspan fill="{t['dim']}">+</tspan> Algorithms</text>
<text class="mono" x="{X+190}" y="190" font-size="12" fill="{t['amber']}" text-anchor="middle">Δ curiosity · rigor</text>
{arrow(X, 202, X + 380, t['amber'])}
<text class="serif i fade" style="animation-delay:.6s" x="{X-2}" y="266" font-size="54" fill="{t['amber']}">Autonomous Systems</text>
{''.join(rows)}
{element_tile(t, 968, 56, "05", "QAU", "Ka", "Kamran Ashraf", "AI × CHEMISTRY", t['cyan'], pulse_delay=0)}
<text class="mono" x="1053" y="282" font-size="10.5" fill="{t['dim']}" text-anchor="middle" letter-spacing="1">element of surprise</text>
"""
    return svg(W, H, body, "About Muhammad Kamran Ashraf", DRAW_CSS + TILE_CSS)


# ─────────────────────────── 5. FLAGSHIPS ───────────────────────────
FLAGSHIPS = [
    dict(repo="AI-Coding", title="AI-Coding", kind="AGENT", color="cyan",
         tag=["A local autonomous coding agent with a", "human-in-the-loop safety gate."],
         bullets=["Reads, writes & refactors a codebase on its own", "Every shell command waits for your approval"],
         chips=["Node.js", "Express", "SSE", "OpenRouter"], metric="HITL-gated", illo="terminal"),
    dict(repo="Quidian-MediaDownloader", title="Quidian", kind="MEDIA ENGINE", color="green",
         tag=["4K & playlist downloader with aria2c turbo", "segments and a live web dashboard."],
         bullets=["SQLite job store resumes across restarts", "Smart playlist resume skips finished files"],
         chips=["Python", "Flask", "yt-dlp", "aria2c", "FFmpeg"], metric="152 tests", check=True, illo="bars"),
    dict(repo="Subah-TaskBook", title="Subah", kind="PRODUCTIVITY", color="amber",
         tag=["A daily focus book: unfinished tasks roll", "over to the next dawn, rewards surprise you."],
         bullets=["Continuous rollover + per-day schedule view", "Life diary & mood log — 100% offline"],
         chips=["Electron", "JavaScript", "localStorage"], metric="offline-first", illo="sunrise"),
    dict(repo="ArticlesDownloader", title="Articles Downloader", kind="RESEARCH", color="violet",
         tag=["Scholarly discovery across nine academic", "APIs, ranked by journal quartile."],
         bullets=["Parallel Crossref · arXiv · PubMed · OpenAlex", "Exports BibTeX, RIS and APA 7 citations"],
         chips=["Python", "Flask", "SSE", "SQLite"], metric="9 APIs", illo="converge"),
]


def illo_terminal(t, c):
    x, y, w, h = 372, 44, 200, 182
    lines = [
        ("$ agent run fix-tests", t["text"]),
        ("> read   src/app.js", t["muted"]),
        ("> patch  src/app.js", t["muted"]),
        ("? run npm test [y/N]", t["amber"]),
        ("y", t["text"]),
        ("● 12 passed", t["green"]),
    ]
    s = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{t["bg2"]}" stroke="{t["line"]}"/>']
    for i, col in enumerate((t["rose"], t["amber"], t["green"])):
        s.append(f'<circle cx="{x + 16 + i*13}" cy="{y + 15}" r="4" fill="{col}" opacity=".85"/>')
    s.append(f'<line x1="{x}" y1="{y+29}" x2="{x+w}" y2="{y+29}" stroke="{t["line"]}"/>')
    for i, (ln, col) in enumerate(lines):
        s.append(f'<text class="mono seq" style="animation-delay:{i*0.85:.2f}s" x="{x+12}" y="{y + 52 + i*21}" font-size="10.5" fill="{col}">{esc(ln)}</text>')
    css = ".seq{animation:seq 8s ease infinite both}@keyframes seq{0%{opacity:0}5%{opacity:1}86%{opacity:1}94%{opacity:0}100%{opacity:0}}"
    return "".join(s), css


def illo_bars(t, c):
    x0, y0 = 380, 58
    s = [f'<text class="mono" x="{x0}" y="{y0}" font-size="10.5" fill="{t["muted"]}">4 × aria2c segments</text>']
    durs = (2.6, 3.4, 2.9, 3.8)
    for i, d in enumerate(durs):
        y = y0 + 26 + i * 30
        s.append(f'<text class="mono" x="{x0}" y="{y+4}" font-size="9.5" fill="{t["dim"]}">conn{i+1}</text>')
        s.append(f'<rect x="{x0+42}" y="{y-4}" width="140" height="8" rx="4" fill="{t["line"]}"/>')
        s.append(f'<rect class="grow" style="animation-duration:{d}s" x="{x0+42}" y="{y-4}" width="140" height="8" rx="4" fill="{c}"/>')
    s.append(f'<text class="mono" x="{x0}" y="{y0+150}" font-size="10" fill="{t["muted"]}">mux <tspan fill="{c}">→</tspan> 2160p.mkv</text>')
    css = ".grow{transform-box:fill-box;transform-origin:left center;animation:grow 3s cubic-bezier(.4,0,.2,1) infinite alternate}@keyframes grow{from{transform:scaleX(.04)}to{transform:scaleX(1)}}"
    return "".join(s), css


def illo_sunrise(t, c):
    cx, hy = 472, 150
    s = [f'<defs><clipPath id="sky"><rect x="372" y="40" width="200" height="{hy-40}"/></clipPath></defs>']
    rays = "".join(
        f'<line x1="{cx + 34*math.cos(math.radians(a)):.1f}" y1="{hy + 34*math.sin(math.radians(a)):.1f}" '
        f'x2="{cx + 48*math.cos(math.radians(a)):.1f}" y2="{hy + 48*math.sin(math.radians(a)):.1f}" stroke="{c}" stroke-width="2" stroke-linecap="round"/>'
        for a in range(-170, -9, 20)
    )
    s.append(f'<g clip-path="url(#sky)"><g class="rise">{rays}<circle cx="{cx}" cy="{hy}" r="24" fill="{c}"/></g></g>')
    s.append(f'<line x1="382" y1="{hy}" x2="562" y2="{hy}" stroke="{t["muted"]}" stroke-width="1.4"/>')
    items = ["read 20 pages", "deep work 2h", "call home"]
    for i, it in enumerate(items):
        y = hy + 24 + i * 22
        s.append(f'<rect x="396" y="{y-10}" width="12" height="12" rx="3" fill="none" stroke="{t["line2"]}"/>')
        s.append(f'<g class="tick" style="animation-delay:{1.2 + i*0.9:.1f}s">{check_icon(398.5, y-4, t["green"], .7)}</g>')
        s.append(f'<text class="mono" x="418" y="{y}" font-size="10.5" fill="{t["muted"]}">{it}</text>')
    css = (".rise{animation:rise 6s ease-in-out infinite alternate}@keyframes rise{from{transform:translateY(46px)}to{transform:translateY(0)}}"
           ".tick{animation:tick 6s ease infinite both}@keyframes tick{0%{opacity:0}8%{opacity:1}85%{opacity:1}95%{opacity:0}100%{opacity:0}}")
    return "".join(s), css


def illo_converge(t, c):
    tx, ty = 528, 132
    s = []
    for i in range(9):
        a = math.radians(-64 + i * 16)
        nx, ny = 476 - 92 * math.cos(a), ty + 92 * math.sin(a)
        d = f"M{nx:.1f},{ny:.1f} Q{(nx+tx)/2:.1f},{ty:.1f} {tx-24},{ty}"
        s.append(f'<path d="{d}" fill="none" stroke="{t["line2"]}" stroke-width="1"/>')
        s.append(f'<circle cx="{nx:.1f}" cy="{ny:.1f}" r="5" fill="{t["panel"]}" stroke="{c}" stroke-width="1.6"/>')
        s.append(f'<circle r="2.6" fill="{c}"><animateMotion dur="2.4s" begin="{i*0.27:.2f}s" repeatCount="indefinite" path="{d}"/></circle>')
    s.append(f'<rect x="{tx-24}" y="{ty-32}" width="48" height="62" rx="5" fill="{t["panel"]}" stroke="{c}" stroke-width="1.6"/>')
    for k in range(5):
        s.append(f'<line x1="{tx-14}" y1="{ty-18+k*10}" x2="{tx+(14 if k%2==0 else 6)}" y2="{ty-18+k*10}" stroke="{t["muted"]}" stroke-width="1.6" stroke-linecap="round"/>')
    s.append(f'<text class="mono" x="{tx}" y="{ty+52}" font-size="9.5" fill="{t["muted"]}" text-anchor="middle">.bib .ris</text>')
    return "".join(s), ""


ILLOS = dict(terminal=illo_terminal, bars=illo_bars, sunrise=illo_sunrise, converge=illo_converge)


def flagship(t, idx, d):
    W, H = 600, 336
    c = t[d["color"]]
    illo, icss = ILLOS[d["illo"]](t, c)
    s = [f"""<defs><radialGradient id="fg" cx="560" cy="20" r="320" gradientUnits="userSpaceOnUse">
<stop offset="0" stop-color="{c}" stop-opacity="{t['glow']*0.7}"/><stop offset="1" stop-color="{c}" stop-opacity="0"/></radialGradient></defs>""",
         card(W, H, t, 20), f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="19" fill="url(#fg)"/>']
    s.append(f'<text class="mono" x="32" y="48" font-size="11.5" fill="{c}" letter-spacing="2.5">F/0{idx} · {d["kind"]}</text>')
    s.append(f'<text class="serif" x="30" y="100" font-size="{42 if len(d["title"]) < 14 else 36}" fill="{t["text"]}" letter-spacing="-.3">{esc(d["title"])}</text>')
    for i, ln in enumerate(d["tag"]):
        s.append(f'<text class="sans" x="32" y="{132 + i*21}" font-size="14.5" fill="{t["muted"]}">{esc(ln)}</text>')
    for i, b in enumerate(d["bullets"]):
        y = 196 + i * 25
        s.append(f'<rect x="32" y="{y-5}" width="10" height="2" fill="{c}"/>')
        s.append(f'<text class="sans" x="52" y="{y}" font-size="13.5" fill="{t["text"]}">{esc(b)}</text>')
    x = 32
    for ch in d["chips"]:
        w = mono_w(ch, 11.5) + 22
        s.append(f'<rect x="{x}" y="250" width="{w:.1f}" height="26" rx="13" fill="none" stroke="{t["line2"]}"/>')
        s.append(f'<text class="mono" x="{x + w/2:.1f}" y="267" font-size="11.5" fill="{t["muted"]}" text-anchor="middle">{esc(ch)}</text>')
        x += w + 8
    s.append(f'<line x1="32" y1="294" x2="{W-32}" y2="294" stroke="{t["line"]}"/>')
    link = f"github.com/Kamran5H/{d['repo']}"
    s.append(f'<text class="mono" x="32" y="318" font-size="11" fill="{t["dim"]}">{esc(link)}</text>')
    s.append(ne_arrow(32 + mono_w(link, 11) + 6, 318, t["dim"], 6, 1.2))
    mx = W - 32
    s.append(f'<text class="mono mb" x="{mx}" y="318" font-size="11.5" fill="{c}" text-anchor="end">{esc(d["metric"])}</text>')
    if d.get("check"):
        s.append(check_icon(mx - mono_w(d["metric"], 11.5) - 18, 313, c, .75))
    s.append(illo)
    return svg(W, H, "".join(s), f'{d["title"]} — {" ".join(d["tag"])}', icss)


# ───────────────────────── 6. PERIODIC TABLE ────────────────────────
GROUPS = {
    "ai": ("AI · GENERATIVE", "cyan"),
    "sci": ("RESEARCH", "amber"),
    "data": ("DATA · SCRAPING", "violet"),
    "auto": ("AUTOMATION", "green"),
    "app": ("APPS · WEB", "rose"),
}
ELEMENTS = [
    # repo, symbol, display, lang, group
    ("AI-Coding", "Ac", "AI-Coding", "JS", "ai"),
    ("Humanizer", "Hu", "Humanizer", "Py", "ai"),
    ("VideoStudio", "Vs", "VideoStudio", "Py", "ai"),
    ("Urdu-Poetry-Studio", "Ur", "Urdu Poetry Studio", "JS", "ai"),
    ("ArticlesDownloader", "Ad", "ArticlesDownloader", "Py", "sci"),
    ("ReviewForge", "Rf", "ReviewForge", "Py", "sci"),
    ("ResearchDaybook", "Rd", "Research Daybook", "HTML", "sci"),
    ("Early-Coding-Archive", "Ea", "Early Coding Archive", "Py", "sci"),
    ("SourceGenius", "Sg", "SourceGenius", "JS", "data"),
    ("SourceGenius-Share", "Ss", "SourceGenius Share", "JS", "data"),
    ("BrandScrapers", "Bs", "BrandScrapers", "Py", "data"),
    ("TikTokProductHunter", "Tk", "TikTok Product Hunter", "Py", "data"),
    ("Quidian-MediaDownloader", "Qd", "Quidian", "Py", "auto"),
    ("GmailZenith", "Gz", "GmailZenith", "Py", "auto"),
    ("FacebookCleaner", "Fc", "FacebookCleaner", "Py", "auto"),
    ("DiskOptimizerPro", "Do", "DiskOptimizerPro", "Py", "auto"),
    ("ChromeMonitor", "Cm", "ChromeMonitor", "Py", "auto"),
    ("AutoClearExtension", "Ax", "AutoClear Extension", "JS", "auto"),
    ("Subah-TaskBook", "Sb", "Subah TaskBook", "JS", "app"),
    ("Portfolio", "Pf", "Portfolio", "TS", "app"),
]


def tile(t, i, el):
    repo, sym, name, lang, g = el
    label, ck = GROUPS[g]
    body = element_tile(t, 0, 0, f"{i+1:02d}", lang, sym, name, label, t[ck], pulse_delay=i * 0.22)
    return svg(170, 196, body, f"{name} — {label.title()}", TILE_CSS)


def legend(t):
    W, H = 1200, 44
    s, x = [], 2
    for key, (label, ck) in GROUPS.items():
        s.append(f'<rect x="{x}" y="15" width="14" height="14" rx="3" fill="{t[ck]}" opacity=".9"/>')
        s.append(f'<text class="mono" x="{x+22}" y="26.5" font-size="12" fill="{t["muted"]}" letter-spacing="1">{label}</text>')
        x += 22 + mono_w(label, 12, 1) + 28
    note = "tap any element to open it"
    s.append(f'<text class="mono" x="{W-24}" y="26.5" font-size="11.5" fill="{t["dim"]}" text-anchor="end">{note}</text>')
    s.append(ne_arrow(W - 12, 27, t["dim"], 6, 1.2))
    return svg(W, H, "".join(s), "Legend: AI, research, data, automation, apps")


# ──────────────────────────── 7. SPECTRUM ───────────────────────────
PEAKS = [
    # label, x(px), depth, region
    ("Gemini", 128, .48, "ai"), ("LangGraph", 196, .80, "ai"), ("OpenRouter", 266, .44, "ai"),
    ("Python", 340, .96, "be"), ("FastAPI", 404, .52, "be"), ("Node · Express", 470, .84, "be"), ("Flask", 536, .44, "be"),
    ("Playwright", 604, .90, "br"), ("Chrome MV3", 670, .50, "br"), ("TypeScript", 736, .80, "br"), ("Next.js", 798, .42, "br"),
    ("SQLite", 860, .74, "ops"), ("GitHub Actions", 920, .44, "ops"),
    ("Quantum ESPRESSO", 1000, .90, "sci"), ("DFT", 1062, .48, "sci"), ("OriginLab", 1104, .74, "sci"),
]
REGIONS = [("AI · LLM", 90, 300, "cyan"), ("BACKEND", 300, 570, "green"), ("BROWSER · WEB", 570, 830, "violet"),
           ("DATA · OPS", 830, 955, "rose"), ("SCIENCE", 955, 1140, "amber")]
RKEY = {"ai": "cyan", "be": "green", "br": "violet", "ops": "rose", "sci": "amber"}


def spectrum(t):
    W, H = 1200, 420
    X0, X1, Y0, D = 90, 1140, 104, 182
    rnd = random.Random(5)
    minor = [(rnd.uniform(X0 + 10, X1 - 10), rnd.uniform(.03, .12), rnd.uniform(4, 10)) for _ in range(34)]

    def y_at(x):
        v = 0.0
        for _, px, dep, _ in PEAKS:
            v += dep * math.exp(-((x - px) ** 2) / (2 * 8.5 ** 2))
        for px, dep, sg in minor:
            v += dep * math.exp(-((x - px) ** 2) / (2 * sg ** 2))
        v += 0.012 * math.sin(x * 0.21) + 0.008 * math.sin(x * 0.53)
        return Y0 + min(v, 1.0) * D

    xs = [X0 + k * 1.5 for k in range(int((X1 - X0) / 1.5) + 1)]
    curve = " ".join(f"{'M' if k == 0 else 'L'}{x:.1f},{y_at(x):.1f}" for k, x in enumerate(xs))
    area = f"M{X0},{Y0} " + curve[1:].replace("M", "L", 1) + f" L{X1},{Y0} Z"
    area = f"M{X0},{Y0} L" + curve[1:] + f" L{X1},{Y0} Z"

    s = [f"""<defs>
<linearGradient id="sf" x1="0" y1="{Y0}" x2="0" y2="{Y0+D}" gradientUnits="userSpaceOnUse">
<stop offset="0" stop-color="{t['cyan']}" stop-opacity="0"/><stop offset="1" stop-color="{t['cyan']}" stop-opacity="{.30 if t is THEMES['dark'] else .20}"/></linearGradient>
<linearGradient id="ss" x1="{X0}" y1="0" x2="{X1}" y2="0" gradientUnits="userSpaceOnUse">
<stop offset="0" stop-color="{t['cyan']}"/><stop offset=".5" stop-color="{t['violet']}"/><stop offset="1" stop-color="{t['amber']}"/></linearGradient>
<clipPath id="plot"><rect x="{X0}" y="60" width="{X1-X0}" height="260"/></clipPath>
</defs>""", card(W, H, t, 22), corner_marks(W, H, t)]
    s.append(f'<text class="mono" x="40" y="44" font-size="11.5" fill="{t["dim"]}" letter-spacing="1.5">SAMPLE <tspan fill="{t["text"]}">Kamran5H/toolchain</tspan>   MODE <tspan fill="{t["text"]}">ATR</tspan>   SCANS <tspan fill="{t["text"]}">2,048</tspan></text>')
    s.append(f'<text class="mono" x="{W-40}" y="44" font-size="11.5" fill="{t["dim"]}" text-anchor="end" letter-spacing="1.5">FIG. 4 — FTIR OF A DEVELOPER</text>')
    for label, a, b, ck in REGIONS:
        s.append(f'<rect x="{a}" y="62" width="{b-a}" height="{Y0+D+18-62}" fill="{t[ck]}" opacity=".045"/>')
        s.append(f'<text class="mono" x="{a+8}" y="80" font-size="10" fill="{t[ck]}" letter-spacing="1.8">{label}</text>')
    # axes
    for v in range(4000, 399, -500):
        x = X0 + (4000 - v) / 3600 * (X1 - X0)
        s.append(f'<line x1="{x:.1f}" y1="{Y0-8}" x2="{x:.1f}" y2="{Y0+D+18}" stroke="{t["line"]}" stroke-dasharray="2 5"/>')
        s.append(f'<text class="mono" x="{x:.1f}" y="{Y0+D+38}" font-size="10.5" fill="{t["dim"]}" text-anchor="middle">{v}</text>')
    s.append(f'<line x1="{X0}" y1="{Y0+D+18}" x2="{X1}" y2="{Y0+D+18}" stroke="{t["line2"]}"/>')
    s.append(f'<text class="mono" x="{(X0+X1)/2}" y="{Y0+D+62}" font-size="11" fill="{t["muted"]}" text-anchor="middle">wavenumber / cm-1</text>')
    s.append(f'<text class="mono" x="52" y="{Y0+4}" font-size="10.5" fill="{t["dim"]}" text-anchor="end">100</text>')
    s.append(f'<text class="mono" x="52" y="{Y0+D+4}" font-size="10.5" fill="{t["dim"]}" text-anchor="end">0</text>')
    s.append(f'<text class="mono" x="40" y="{Y0+D/2}" font-size="10.5" fill="{t["muted"]}" transform="rotate(-90 40 {Y0+D/2})" text-anchor="middle">%T</text>')
    s.append(f'<line x1="{X0}" y1="{Y0}" x2="{X1}" y2="{Y0}" stroke="{t["line2"]}" stroke-dasharray="1 3"/>')
    # curve
    s.append(f'<g clip-path="url(#plot)"><path class="areaf" d="{area}" fill="url(#sf)"/>'
             f'<path class="drawspec" pathLength="1" d="{curve}" fill="none" stroke="url(#ss)" stroke-width="1.8" stroke-linejoin="round"/></g>')
    s.append(f'<line class="scan" x1="{X0}" y1="62" x2="{X0}" y2="{Y0+D+18}" stroke="{t["cyan"]}" stroke-width="1.5"/>')
    # labels
    for label, px, dep, rk in PEAKS:
        py = y_at(px)
        c = t[RKEY[rk]]
        delay = 0.35 + 3.6 * (px - X0) / (X1 - X0)
        w = mono_w(label, 11) + 12
        s.append(f'<g class="lbl" style="animation-delay:{delay:.2f}s">'
                 f'<circle cx="{px}" cy="{py:.1f}" r="3.2" fill="{t["bg"]}" stroke="{c}" stroke-width="1.6"/>'
                 f'<rect x="{px - w/2:.1f}" y="{py+9:.1f}" width="{w:.1f}" height="18" rx="4" fill="{t["bg"]}" opacity=".88"/>'
                 f'<text class="mono" x="{px}" y="{py+22:.1f}" font-size="11" fill="{t["text"]}" text-anchor="middle">{esc(label)}</text></g>')
    s.append(f'<text class="mono" x="40" y="{H-26}" font-size="11" fill="{t["dim"]}">peak depth = how often it ships in my repos</text>')
    css = f"""
.drawspec{{stroke-dasharray:1;stroke-dashoffset:0;animation:draw 4s cubic-bezier(.45,0,.25,1) .3s both}}
@keyframes draw{{from{{stroke-dashoffset:1}}to{{stroke-dashoffset:0}}}}
.areaf{{animation:fadeonly 1.2s ease 3.8s both}}
@keyframes fadeonly{{from{{opacity:0}}to{{opacity:1}}}}
.lbl{{animation:fadeonly .5s ease both}}
.scan{{opacity:0;animation:scan 4s cubic-bezier(.45,0,.25,1) .3s both}}
@keyframes scan{{0%{{transform:translateX(0);opacity:.9}}92%{{opacity:.9}}100%{{transform:translateX({X1-X0}px);opacity:0}}}}
"""
    return svg(W, H, "".join(s), "Tech stack drawn as an FTIR spectrum: Python, TypeScript, FastAPI, Playwright, Quantum ESPRESSO and more", css)


# ──────────────────────────── 8. RESEARCH ───────────────────────────
def research(t):
    """MPhil topic (confirmed): Ce-doped NiCo metal–organic frameworks for electrocatalysis.
    The schematic is conceptual: no measured data is drawn."""
    W, H = 1200, 440
    s = [card(W, H, t, 22), corner_marks(W, H, t)]
    s.append(f'<text class="mono" x="60" y="74" font-size="12" fill="{t["amber"]}" letter-spacing="3">MPHIL RESEARCH · QUAID-I-AZAM UNIVERSITY</text>')
    s.append(f'<text class="serif" x="58" y="134" font-size="48" fill="{t["text"]}">Ce-doped NiCo</text>')
    s.append(f'<text class="serif i" x="58" y="186" font-size="48" fill="{t["amber"]}">MOF electrocatalysts</text>')
    para = ["How does cerium in a NiCo metal–organic framework",
            "change its activity for water splitting — oxygen and",
            "hydrogen evolution? Supervised by Prof. Dr. Safeer Ahmed."]
    for i, p in enumerate(para):
        s.append(f'<text class="sans" x="60" y="{232 + i*24}" font-size="15" fill="{t["muted"]}">{esc(p)}</text>')
    spec = [("focus", "OER / HER · structure–property links"),
            ("model", "DFT with Quantum ESPRESSO"),
            ("before", "BS: green CaO for dye removal & sensing")]
    for i, (k, v) in enumerate(spec):
        s.append(f'<text class="mono" x="60" y="{332 + i*27}" font-size="12.5"><tspan fill="{t["dim"]}">{k:<8}</tspan><tspan fill="{t["text"]}">{esc(v)}</tspan></text>')

    # schematic: electrolysis cell, MOF-coated anode, gas evolution
    cx0, cy0, cw, ch = 660, 200, 300, 160
    s.append(f'<rect x="{cx0}" y="{cy0}" width="{cw}" height="{ch}" rx="6" fill="{t["cyan"]}" fill-opacity=".06" stroke="{t["line2"]}"/>')
    s.append(f'<line x1="{cx0}" y1="{cy0+22}" x2="{cx0+cw}" y2="{cy0+22}" stroke="{t["cyan"]}" stroke-opacity=".4" stroke-dasharray="3 5"/>')
    ax, kx, ew_ = cx0 + 46, cx0 + 206, 48
    for x in (ax, kx):
        s.append(f'<rect x="{x}" y="{cy0-28}" width="{ew_}" height="{ch+8}" rx="4" fill="{t["line2"]}" fill-opacity=".55" stroke="{t["line2"]}"/>')
    # MOF lattice on the anode: Ni / Co nodes, one Ce site, linkers
    for r in range(5):
        for c in range(2):
            x = ax + 14 + c * 20
            y = cy0 + 40 + r * 22
            if c == 0:
                s.append(f'<line x1="{x}" y1="{y}" x2="{x+20}" y2="{y}" stroke="{t["muted"]}" stroke-opacity=".5"/>')
            if r < 4:
                s.append(f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y+22}" stroke="{t["muted"]}" stroke-opacity=".5"/>')
            col = t["amber"] if (r == 2 and c == 1) else (t["green"] if c == 0 else t["rose"])
            rr = 5.5 if (r == 2 and c == 1) else 4
            s.append(f'<circle cx="{x}" cy="{y}" r="{rr}" fill="{col}"/>')
    # rising bubbles
    for i, (dx, y, d) in enumerate([(10, 128, 0), (18, 98, .9), (8, 70, 1.8), (16, 140, 2.6)]):
        s.append(f'<circle class="bub" style="animation-delay:{d}s" cx="{ax + ew_ + dx}" cy="{cy0 + y}" r="{5 + i % 2}" fill="none" stroke="{t["cyan"]}" stroke-width="1.6"/>')
    for i, (dx, y, d) in enumerate([(8, 136, .4), (16, 108, 1.2), (10, 80, 2.1), (20, 124, 2.9), (6, 96, .1), (14, 146, 1.6)]):
        s.append(f'<circle class="bub bubh" style="animation-delay:{d}s" cx="{kx - dx}" cy="{cy0 + y}" r="{3 + i % 2}" fill="none" stroke="{t["amber"]}" stroke-width="1.5"/>')
    s.append(f'<text class="mono" x="{ax+ew_/2}" y="{cy0-40}" font-size="10.5" fill="{t["cyan"]}" text-anchor="middle" letter-spacing="1.5">OER · O2</text>')
    s.append(f'<text class="mono" x="{kx+ew_/2}" y="{cy0-40}" font-size="10.5" fill="{t["amber"]}" text-anchor="middle" letter-spacing="1.5">HER · H2</text>')
    s.append(f'<text class="mono" x="{cx0+cw/2+4}" y="{cy0+ch-24}" font-size="11" fill="{t["dim"]}" text-anchor="middle">H2O</text>')
    # legend
    lx, ly = cx0, cy0 + ch + 34
    for i, (lab, col) in enumerate((("Ni", t["green"]), ("Co", t["rose"]), ("Ce", t["amber"]))):
        s.append(f'<circle cx="{lx + i*58 + 5}" cy="{ly-4}" r="4.5" fill="{col}"/>')
        s.append(f'<text class="mono" x="{lx + i*58 + 15}" y="{ly}" font-size="10.5" fill="{t["muted"]}">{lab}</text>')
    # schematic polarisation curve
    px0, py0, pw, ph = 1000, 196, 140, 150
    s.append(f'<path d="M{px0},{py0} V{py0+ph} H{px0+pw}" fill="none" stroke="{t["line2"]}"/>')
    s.append(f'<path class="sig" pathLength="1" d="M{px0+4},{py0+ph-4} C{px0+70},{py0+ph-4} {px0+92},{py0+ph-14} {px0+104},{py0+ph-40} S{px0+122},{py0+20} {px0+132},{py0+6}" fill="none" stroke="{t["cyan"]}" stroke-width="2"/>')
    s.append(f'<path d="M{px0+4},{py0+ph-4} C{px0+54},{py0+ph-4} {px0+72},{py0+ph-14} {px0+84},{py0+ph-40} S{px0+102},{py0+20} {px0+112},{py0+6}" fill="none" stroke="{t["amber"]}" stroke-width="1.6" stroke-dasharray="5 4"/>')
    s.append(f'<text class="mono" x="{px0-6}" y="{py0+10}" font-size="10" fill="{t["dim"]}" text-anchor="end">j</text>')
    s.append(f'<text class="mono" x="{px0+pw}" y="{py0+ph+16}" font-size="10" fill="{t["dim"]}" text-anchor="end">E</text>')
    s.append(f'<text class="mono" x="{cx0}" y="{cy0-86}" font-size="10" fill="{t["dim"]}" letter-spacing="1.5">FIG. 3 — CONCEPTUAL SKETCH · NOT MEASURED DATA</text>')
    css = """
.bub{animation:bub 3.2s ease-in infinite both}.bubh{animation-duration:2.6s}
@keyframes bub{0%{transform:translateY(0);opacity:0}15%{opacity:1}100%{transform:translateY(-70px);opacity:0}}
.sig{stroke-dasharray:1;stroke-dashoffset:0;animation:sig 5s ease-in-out infinite both}
@keyframes sig{0%{stroke-dashoffset:1}60%{stroke-dashoffset:0}100%{stroke-dashoffset:0}}
"""
    return svg(W, H, "".join(s), "Research: Ce-doped NiCo metal-organic frameworks for electrocatalytic water splitting", css)


# ─────────────────────────── 9. MILESTONE ───────────────────────────
def milestone(t):
    W, H = 1200, 452
    photo = data_uri(os.path.join(PHOTOS, "milestone-latex.jpg"))
    px, py, pw, ph = 40, 40, 640, 360
    X = 730
    s = [f'<defs><clipPath id="mp"><rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="12"/></clipPath></defs>',
         card(W, H, t, 22), corner_marks(W, H, t)]
    s.append(f'<image href="{photo}" x="{px}" y="{py}" width="{pw}" height="{ph}" clip-path="url(#mp)" preserveAspectRatio="xMidYMid slice"/>')
    s.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="12" fill="none" stroke="{t["line2"]}"/>')
    s.append(f'<text class="mono" x="{px}" y="{py+ph+32}" font-size="11.5" fill="{t["dim"]}" letter-spacing=".5">FIG. 2 — Receiving the certificate. Quaid-i-Azam University, Islamabad.</text>')
    s.append(f'<text class="mono" x="{X}" y="80" font-size="12" fill="{t["cyan"]}" letter-spacing="3">MILESTONE · CERTIFIED</text>')
    s.append(f'<text class="serif" x="{X-2}" y="138" font-size="46" fill="{t["text"]}">Certificate of</text>')
    s.append(f'<text class="serif i" x="{X-2}" y="186" font-size="46" fill="{t["amber"]}">Participation</text>')
    for i, ln in enumerate(["LaTeX training workshop on writing research", "papers and theses — typesetting science the", "way journals expect it."]):
        s.append(f'<text class="sans" x="{X}" y="{226 + i*23}" font-size="15" fill="{t["muted"]}">{esc(ln)}</text>')
    bx, by, bw, bh = X, 312, 420, 92
    s.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="10" fill="{t["bg2"]}" stroke="{t["line"]}"/>')
    code = [
        (f'<tspan fill="{t["violet"]}">\\usepackage</tspan>{{chemfig}}'),
        (f'<tspan fill="{t["violet"]}">\\chemfig</tspan>{{H_2N-C(=[2]O)-NH_2}}'),
        (f'<tspan fill="{t["dim"]}">% urea — from my undergraduate sensing work</tspan>'),
    ]
    for i, c in enumerate(code):
        s.append(f'<text class="mono" x="{bx+18}" y="{by+28 + i*22}" font-size="12.5" fill="{t["text"]}">{c}</text>')
    return svg(W, H, "".join(s), "Milestone: Certificate of Participation, LaTeX training workshop, Quaid-i-Azam University")


# ──────────────────────────── 10. CONTACT ───────────────────────────
CONTACTS = [
    ("email", "Email", "chkamran32b@gmail.com", "cyan"),
    ("linkedin", "LinkedIn", "in/kamran-ashraf", "violet"),
    ("orcid", "ORCID", "0009-0003-2997-2954", "green"),
    ("github", "GitHub", "@Kamran5H", "rose"),
    ("kalam", "QAU Kalam", "qaukalam.me · live", "amber"),
    ("portfolio", "Portfolio", "Next.js source", "muted"),
]


def contact_pill(t, key, label, sub, ck):
    W, H = 286, 64
    c = t[ck]
    icon = {
        "email": f'<rect x="20" y="22" width="22" height="16" rx="3" fill="none" stroke="{c}" stroke-width="1.6"/><path d="M21,24 L31,31 L41,24" fill="none" stroke="{c}" stroke-width="1.6"/>',
        "github": f'<circle cx="31" cy="30" r="10" fill="none" stroke="{c}" stroke-width="1.6"/><circle cx="31" cy="30" r="3" fill="{c}"/>',
        "kalam": f'<path d="M23,38 L37,22 L40,25 L26,41 Z" fill="none" stroke="{c}" stroke-width="1.6" stroke-linejoin="round"/><path d="M23,38 L21,43 L26,41" fill="none" stroke="{c}" stroke-width="1.6"/>',
        "portfolio": f'<polygon points="{pts(hex_pts(31, 30, 11))}" fill="none" stroke="{c}" stroke-width="1.6"/>',
        "linkedin": f'<rect x="20" y="19" width="22" height="22" rx="5" fill="none" stroke="{c}" stroke-width="1.6"/>'
                    f'<text class="sans b" x="31" y="35" font-size="12" fill="{c}" text-anchor="middle">in</text>',
        "orcid": f'<circle cx="31" cy="30" r="11" fill="none" stroke="{c}" stroke-width="1.6"/>'
                 f'<text class="sans b" x="31" y="34.5" font-size="11" fill="{c}" text-anchor="middle">iD</text>',
    }[key]
    body = (
        f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="16" fill="{t["panel"]}" stroke="{t["line"]}"/>'
        f'<rect x="8" y="8" width="46" height="46" rx="12" fill="{c}" opacity=".1"/>{icon}'
        f'<text class="sans b" x="68" y="29" font-size="15" fill="{t["text"]}">{esc(label)}</text>'
        f'<text class="mono" x="68" y="47" font-size="11.5" fill="{t["muted"]}">{esc(sub)}</text>'
        + ne_arrow(W - 30, 37, t["dim"], 7, 1.4)
    )
    return svg(W, H, body, f"{label}: {sub}")


# ──────────────────────────── 11. FOOTER ────────────────────────────
def footer(t):
    W, H = 1200, 250
    L = 240

    def wave(amp, y, phase):
        p = []
        for k in range(0, 1200 + L * 2 + 1, 6):
            p.append(f"{'M' if k == 0 else 'L'}{k - L:.0f},{y + amp*math.sin(2*math.pi*(k/L) + phase):.1f}")
        return " ".join(p)

    s = [f"""<defs><linearGradient id="fm" x1="0" y1="0" x2="1" y2="0">
<stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".2" stop-color="#fff" stop-opacity="1"/>
<stop offset=".8" stop-color="#fff" stop-opacity="1"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<mask id="wm"><rect width="{W}" height="{H}" fill="url(#fm)"/></mask></defs>"""]
    s.append(f'<g mask="url(#wm)">')
    for i, (amp, col, dur, op) in enumerate(((14, t["cyan"], 9, .7), (10, t["amber"], 13, .55), (18, t["violet"], 17, .35))):
        s.append(f'<path class="wv" style="animation-duration:{dur}s" d="{wave(amp, 196, i*1.3)}" fill="none" stroke="{col}" stroke-width="1.4" opacity="{op}"/>')
    s.append("</g>")
    s.append(f'<text class="serif i" x="{W/2}" y="92" font-size="38" fill="{t["text"]}" text-anchor="middle">Synthesizing intelligence, from atoms to autonomous code.</text>')
    s.append(f'<text class="mono" x="{W/2}" y="134" font-size="11.5" fill="{t["dim"]}" text-anchor="middle" letter-spacing="3.5">M. K. ASHRAF  ·  ISLAMABAD  ·  THANKS FOR SCROLLING THIS FAR</text>')
    css = f".wv{{animation:wv 10s linear infinite}}@keyframes wv{{to{{transform:translateX(-{L}px)}}}}"
    return svg(W, H, "".join(s), "Synthesizing intelligence, from atoms to autonomous code.", css)


# ───────────────────────────── main ─────────────────────────────────
def main():
    import sys
    os.makedirs(OUT, exist_ok=True)
    if len(sys.argv) > 1 and sys.argv[1] == "contacts":  # fast path: contact pills only
        for name, t in THEMES.items():
            for key, label, sub, ck in CONTACTS:
                save(f"contact-{key}", name, contact_pill(t, key, label, sub, ck))
        print("contacts rebuilt")
        return
    if len(sys.argv) > 1 and sys.argv[1] == "research":  # fast path: research card only
        for name, t in THEMES.items():
            save("research", name, research(t))
        print("research rebuilt")
        return
    for name, t in THEMES.items():
        save("hero", name, hero(t))
        for num, label in NAV:
            save(f"nav-{label.lower()}", name, nav_pill(t, num, label))
        for num, key, title, sub in SECTIONS:
            save(f"h-{key}", name, header(t, num, title, sub))
        save("about", name, about(t))
        for i, d in enumerate(FLAGSHIPS, 1):
            save(f"work-{d['repo'].lower()}", name, flagship(t, i, d))
        for i, el in enumerate(ELEMENTS):
            save(f"el-{el[0].lower()}", name, tile(t, i, el))
        save("legend", name, legend(t))
        save("spectrum", name, spectrum(t))
        save("research", name, research(t))
        save("milestone", name, milestone(t))
        for key, label, sub, ck in CONTACTS:
            save(f"contact-{key}", name, contact_pill(t, key, label, sub, ck))
        save("footer", name, footer(t))
    total = 0
    for f in sorted(os.listdir(OUT)):
        total += os.path.getsize(os.path.join(OUT, f))
    print(f"{len(os.listdir(OUT))} files, {total/1024:.0f} KB total")


if __name__ == "__main__":
    main()
