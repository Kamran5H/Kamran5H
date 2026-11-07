"""
Live telemetry card, rendered from the GitHub API (no third-party stat services).

    GITHUB_TOKEN=... python scripts/stats.py --user Kamran5H --out dist

Writes <out>/stats-dark.svg and <out>/stats-light.svg.
Works without a token too (REST + public contribution calendar), just rate-limited.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import urllib.request

from design import THEMES, card, esc, mono_w, svg, write

API = "https://api.github.com"


def _req(url: str, payload: dict | None = None, raw: bool = False):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "kamran5h-profile-telemetry"}
    tok = os.environ.get("GITHUB_TOKEN")
    if tok:
        headers["Authorization"] = f"Bearer {tok}"
    data = json.dumps(payload).encode() if payload is not None else None
    r = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(r, timeout=30) as fh:
        body = fh.read()
    return body.decode() if raw else json.loads(body)


def contributions(user: str):
    """Return (total_last_year, [daily counts oldest→newest])."""
    if os.environ.get("GITHUB_TOKEN"):
        q = """query($u:String!){user(login:$u){contributionsCollection{contributionCalendar{
               totalContributions weeks{contributionDays{contributionCount date}}}}}}"""
        res = _req(f"{API}/graphql", {"query": q, "variables": {"u": user}})
        cal = res["data"]["user"]["contributionsCollection"]["contributionCalendar"]
        days = [d["contributionCount"] for w in cal["weeks"] for d in w["contributionDays"]]
        return cal["totalContributions"], days
    html = _req(f"https://github.com/users/{user}/contributions", raw=True)
    ids = dict(re.findall(r'data-date="(\d{4}-\d\d-\d\d)" id="([^"]+)"', html))
    ids = {v: k for k, v in ids.items()}  # id -> date
    counts = {}
    for tid, txt in re.findall(r'<tool-tip[^>]*for="([^"]+)"[^>]*>([^<]*)</tool-tip>', html):
        m = re.match(r"(\d+) contribution", txt.strip())
        if tid in ids:
            counts[ids[tid]] = int(m.group(1)) if m else 0
    days = [counts[d] for d in sorted(counts)]
    m = re.search(r"([\d,]+)\s+contributions?\s+in the last year", html)
    total = int(m.group(1).replace(",", "")) if m else sum(days)
    return total, days


def collect(user: str):
    repos = _req(f"{API}/users/{user}/repos?per_page=100&type=owner")
    own = [r for r in repos if not r["fork"] and r["name"].lower() != user.lower()]
    langs: dict[str, int] = {}
    for r in own:
        for k, v in _req(r["languages_url"]).items():
            langs[k] = langs.get(k, 0) + v
    total, days = contributions(user)
    return dict(
        repos=len(own),
        stars=sum(r["stargazers_count"] for r in own),
        langs=langs,
        contrib=total,
        days=days,
    )


def render(t: dict, d: dict) -> str:
    W, H = 1200, 480
    s = [card(W, H, t, 22)]
    for x, y, dx, dy in ((14, 14, 1, 1), (W - 14, 14, -1, 1), (14, H - 14, 1, -1), (W - 14, H - 14, -1, -1)):
        s.append(f'<path d="M{x},{y + dy*12} L{x},{y} L{x + dx*12},{y}" fill="none" stroke="{t["dim"]}" opacity=".7"/>')
    # metrics 2×2
    code_mb = sum(d["langs"].values()) / 1_000_000
    stars_or_code = (
        ("STARS EARNED", f'{d["stars"]:,}', "")
        if d["stars"] >= 50
        else ("CODE SHIPPED", f"{code_mb:.1f}", " MB")
    )
    metrics = [
        ("PUBLIC REPOSITORIES", f'{d["repos"]:,}', ""),
        stars_or_code,
        ("CONTRIBUTIONS · 12 MO", f'{d["contrib"]:,}', ""),
        ("LANGUAGES IN USE", f'{len(d["langs"])}', ""),
    ]
    for i, (label, val, unit) in enumerate(metrics):
        x = 60 + (i % 2) * 250
        y = 92 + (i // 2) * 128
        s.append(f'<text class="mono" x="{x}" y="{y}" font-size="11" fill="{t["dim"]}" letter-spacing="2">{label}</text>')
        u = f'<tspan class="mono" font-size="16" fill="{t["muted"]}">{unit}</tspan>' if unit else ""
        s.append(f'<text class="serif fade" style="animation-delay:{.1 + i*.12:.2f}s" x="{x-2}" y="{y+62}" font-size="68" fill="{t["text"]}">{val}{u}</text>')
    s.append(f'<line x1="560" y1="70" x2="560" y2="296" stroke="{t["line"]}"/>')

    # composition
    X0, BW = 600, 540
    total = sum(d["langs"].values()) or 1
    items = sorted(d["langs"].items(), key=lambda kv: -kv[1])
    top = items[:5]
    other = sum(v for _, v in items[5:])
    if other:
        top.append(("Other", other))
    palette = [t["cyan"], t["amber"], t["violet"], t["green"], t["rose"], t["dim"]]
    s.append(f'<text class="mono" x="{X0}" y="92" font-size="11" fill="{t["dim"]}" letter-spacing="2">ELEMENTAL ANALYSIS · BYTES OF CODE</text>')
    x = X0
    s.append(f'<clipPath id="bar"><rect x="{X0}" y="110" width="{BW}" height="14" rx="7"/></clipPath><g clip-path="url(#bar)">')
    s.append(f'<rect x="{X0}" y="110" width="{BW}" height="14" fill="{t["line"]}"/>')
    for i, (name, v) in enumerate(top):
        w = BW * v / total
        s.append(f'<rect class="seg" style="animation-delay:{.2 + i*.15:.2f}s" x="{x:.1f}" y="110" width="{w + .6:.1f}" height="14" fill="{palette[i]}"/>')
        x += w
    s.append("</g>")
    for i, (name, v) in enumerate(top):
        col, row = i % 2, i // 2
        lx = X0 + col * 280
        ly = 166 + row * 42
        pct = 100 * v / total
        s.append(f'<rect x="{lx}" y="{ly-10}" width="10" height="10" rx="2" fill="{palette[i]}"/>')
        s.append(f'<text class="sans" x="{lx+20}" y="{ly}" font-size="15" fill="{t["text"]}">{esc(name)}</text>')
        s.append(f'<text class="mono" x="{lx+250}" y="{ly}" font-size="13" fill="{t["muted"]}" text-anchor="end">{pct:4.1f}%</text>')

    # contribution sparkline (weekly)
    days = d["days"][-364:]
    weeks = [sum(days[i:i + 7]) for i in range(0, len(days), 7)] or [0]
    sx0, sx1, sy0, sh = 60, 1140, 436, 62
    mx = max(weeks) or 1
    step = (sx1 - sx0) / max(1, len(weeks) - 1)
    ptsl = [(sx0 + i * step, sy0 - sh * w / mx) for i, w in enumerate(weeks)]
    line = " ".join(f"{'M' if i == 0 else 'L'}{x:.1f},{y:.1f}" for i, (x, y) in enumerate(ptsl))
    area = f"M{sx0},{sy0} " + " ".join(f"L{x:.1f},{y:.1f}" for x, y in ptsl) + f" L{sx1},{sy0} Z"
    s.append(f'<defs><linearGradient id="sa" x1="0" y1="{sy0-sh}" x2="0" y2="{sy0}" gradientUnits="userSpaceOnUse">'
             f'<stop offset="0" stop-color="{t["cyan"]}" stop-opacity=".28"/><stop offset="1" stop-color="{t["cyan"]}" stop-opacity="0"/></linearGradient></defs>')
    s.append(f'<text class="mono" x="60" y="{sy0-sh-14}" font-size="11" fill="{t["dim"]}" letter-spacing="2">52 WEEKS OF COMMITS</text>')
    peak = max(range(len(weeks)), key=lambda i: weeks[i])
    s.append(f'<line x1="{sx0}" y1="{sy0}" x2="{sx1}" y2="{sy0}" stroke="{t["line2"]}"/>')
    s.append(f'<path class="afade" d="{area}" fill="url(#sa)"/>')
    s.append(f'<path class="draw" pathLength="1" d="{line}" fill="none" stroke="{t["cyan"]}" stroke-width="1.8" stroke-linejoin="round"/>')
    px, py = ptsl[peak]
    s.append(f'<circle class="afade" cx="{px:.1f}" cy="{py:.1f}" r="4" fill="{t["bg"]}" stroke="{t["amber"]}" stroke-width="2"/>')
    s.append(f'<text class="mono afade" x="{px:.1f}" y="{py-12:.1f}" font-size="11" fill="{t["amber"]}" text-anchor="middle">peak {weeks[peak]}</text>')
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    s.append(f'<line x1="60" y1="{sy0-sh-46}" x2="1140" y2="{sy0-sh-46}" stroke="{t["line"]}"/>')
    s.append(f'<text class="mono" x="{W-40}" y="42" font-size="10.5" fill="{t["dim"]}" text-anchor="end">updated {stamp} · github actions</text>')
    css = """
.fade{animation:fade .8s ease both}@keyframes fade{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:none}}
.seg{transform-box:fill-box;transform-origin:left;animation:seg .9s cubic-bezier(.3,.7,.3,1) both}@keyframes seg{from{transform:scaleX(0)}to{transform:scaleX(1)}}
.draw{stroke-dasharray:1;stroke-dashoffset:0;animation:draw 2.6s cubic-bezier(.5,0,.2,1) .3s both}@keyframes draw{from{stroke-dashoffset:1}to{stroke-dashoffset:0}}
.afade{animation:af 1s ease 2.6s both}@keyframes af{from{opacity:0}to{opacity:1}}
"""
    return svg(W, H, "".join(s), f"Live GitHub stats: {d['repos']} repositories, {d['contrib']} contributions in the last year", css)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--user", default="Kamran5H")
    ap.add_argument("--out", default="dist")
    a = ap.parse_args()
    d = collect(a.user)
    for name, t in THEMES.items():
        write(os.path.join(a.out, f"stats-{name}.svg"), render(t, d))
    print(json.dumps({k: v for k, v in d.items() if k != "days"}, indent=1))


if __name__ == "__main__":
    main()
