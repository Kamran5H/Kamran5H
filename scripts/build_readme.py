"""
Compose README.md from the same data that drives the artwork.

    python scripts/build_readme.py            # README.md (absolute URLs, for GitHub)
    python scripts/build_readme.py --local X  # preview copy with relative paths
"""
from __future__ import annotations

import argparse
import os

from build_assets import CONTACTS, ELEMENTS, FLAGSHIPS, NAV, SECTIONS

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USER = "Kamran5H"
RAW = f"https://raw.githubusercontent.com/{USER}/{USER}"

DESCRIPTIONS = {
    "AI-Coding": "Local autonomous coding agent — web GUI, SSE streaming, human-approval gate on every shell command.",
    "Humanizer": "AI-text naturalisation pipeline with a local heuristic AI-detection scorer and GUI.",
    "VideoStudio": "Text-to-video and image-to-video studio on Gradio with free cloud-GPU acceleration.",
    "Urdu-Poetry-Studio": "4K Urdu poetry typography designer — Nastaliq fonts, Wasli backdrops, one-click export.",
    "ArticlesDownloader": "Scholarly paper discovery across 9 academic APIs with SQLite search history.",
    "ReviewForge": "Config-driven engine for critical, reproducible academic review articles with LLMs.",
    "ResearchDaybook": "Single-file, offline research journal on HTML5 localStorage.",
    "Early-Coding-Archive": "Where it started: early Python scripts, Tkinter GUIs and a boiling-point ML model.",
    "SourceGenius": "Autonomous Amazon brand-website finder — Chrome MV3, Playwright reader, VPN controller.",
    "SourceGenius-Share": "Turnkey deployment bundle for the Source Genius extension and scraper.",
    "BrandScrapers": "Amazon brand-extraction pipeline — ASIN scrapers, Keepa integration, threaded cleaners.",
    "TikTokProductHunter": "Cross-platform Amazon to TikTok Shop product-discovery scraper (Playwright).",
    "Quidian-MediaDownloader": "4K / playlist / subtitle downloader on yt-dlp + aria2c with a web dashboard.",
    "GmailZenith": "Bulk inbox automation and rule-based cleaning on the official Gmail API.",
    "FacebookCleaner": "Bulk triage of friends, groups and pages with FastAPI, Playwright and a web GUI.",
    "DiskOptimizerPro": "Dual-drive Windows cleanup suite with a 3-stage duplicate hunter.",
    "ChromeMonitor": "Background utility tracking Chrome profiles, extensions and memory.",
    "AutoClearExtension": "Chrome MV3 extension for instant cache, cookie and history cleanup.",
    "Subah-TaskBook": "Daily focus book — task rollover, surprise rewards, life diary. Electron, offline.",
    "Portfolio": "Developer portfolio — Next.js 14, TypeScript, Tailwind.",
}

CONTACT_LINKS = {
    "email": "mailto:chkamran32b@gmail.com",
    "github": f"https://github.com/{USER}",
    "kalam": "https://qaukalam.me",
    "portfolio": f"https://github.com/{USER}/Portfolio",
}


def pic(base: str, name: str, alt: str, width: str = "100%", live: bool = False) -> str:
    if live and base.startswith("http"):
        d, l = f"{RAW}/output/{name}-dark.svg", f"{RAW}/output/{name}-light.svg"
    else:
        d, l = f"{base}/{name}-dark.svg", f"{base}/{name}-light.svg"
    return (
        f'<picture><source media="(prefers-color-scheme: dark)" srcset="{d}">'
        f'<source media="(prefers-color-scheme: light)" srcset="{l}">'
        f'<img src="{d}" alt="{alt}" width="{width}"></picture>'
    )


def build(base: str) -> str:
    sec = {key: (num, title) for num, key, title, _ in SECTIONS}

    def header(key):
        num, title = sec[key]
        return f'<a name="{key}"></a>\n<div align="center">{pic(base, "h-" + key, f"{num} — {title}")}</div>\n'

    nav_target = dict(about="about", work="work", builds="builds", stack="stack", research="research", contact="contact")
    nav = "".join(
        f'<a href="#{nav_target[label.lower()]}">{pic(base, "nav-" + label.lower(), label, "15.6%")}</a>\n'
        for _, label in NAV
    )

    work = []
    for i in range(0, len(FLAGSHIPS), 2):
        row = []
        for d in FLAGSHIPS[i:i + 2]:
            row.append(f'<a href="https://github.com/{USER}/{d["repo"]}">{pic(base, "work-" + d["repo"].lower(), d["title"], "49%")}</a>')
        work.append("\n".join(row))

    tiles = []
    for i in range(0, len(ELEMENTS), 5):
        row = [
            f'<a href="https://github.com/{USER}/{e[0]}">{pic(base, "el-" + e[0].lower(), e[2], "19%")}</a>'
            for e in ELEMENTS[i:i + 5]
        ]
        tiles.append("\n".join(row))

    index_rows = "\n".join(
        f"| `{i+1:02d}` **{e[1]}** | [{e[0]}](https://github.com/{USER}/{e[0]}) | {DESCRIPTIONS[e[0]]} |"
        for i, e in enumerate(ELEMENTS)
    )

    contacts = "\n".join(
        f'<a href="{CONTACT_LINKS[k]}">{pic(base, "contact-" + k, f"{label}: {sub}", "24%")}</a>'
        for k, label, sub, _ in CONTACTS
    )

    return f"""<!--
  Muhammad Kamran Ashraf — GitHub profile.
  Every image here is hand-built SVG: scripts/build_assets.py renders the artwork (dark + light),
  scripts/stats.py renders live telemetry twice a day via .github/workflows/profile.yml.
  No third-party stat widgets, no tracking pixels.
-->

<div align="center">

{pic(base, "hero", "Muhammad Kamran Ashraf — AI systems architect and computational chemist")}

{nav}
</div>

<br>

{header("about")}
<div align="center">{pic(base, "about", "About: atoms plus algorithms yields autonomous systems")}</div>

> I'm an MPhil chemistry scholar at **Quaid-i-Azam University** who builds software the way an experimentalist runs a lab:
> state the hypothesis, control the variables, make the result reproducible. By day that means polymer-nanocomposite
> biosensors and DFT spectra; by night, local-first AI agents, resilient scrapers and the desktop tools I wish existed.

<details>
<summary><b>The 30-second version for recruiters</b></summary>
<br>

- **Builds end to end:** Python & TypeScript back ends (FastAPI, Flask, Express), browser automation (Playwright, Chrome MV3), desktop apps (Electron, CustomTkinter).
- **Ships AI responsibly:** agentic loops with human-approval gates, local-first data, streaming UIs.
- **Tests what he ships:** flagship repos carry automated suites (Quidian alone runs 152 tests).
- **Brings a scientist's rigor:** computational chemistry (Quantum ESPRESSO / DFT), instrument data (FTIR, UV-Vis), and literature tooling.
- **Has a live product:** [qaukalam.me](https://qaukalam.me), a platform for Quaid-i-Azam University students.

</details>

<br>

{header("work")}
<div align="center">

{work[0]}

{work[1]}

</div>

<details>
<summary><b>Architecture notes</b> — how the AI-Coding agent stays safe</summary>
<br>

```mermaid
flowchart LR
    T([Task]) --> P[Plan]
    P --> R[Read and search files]
    R --> E[Propose edit or command]
    E --> G{{Shell command?}}
    G -- no --> X[Apply in sandboxed workspace]
    G -- yes --> H[[Human approval gate]]
    H -- approved --> X
    H -- rejected --> P
    X --> S[Stream result to web GUI over SSE]
    S --> P
```

The model never touches the terminal on its own. Every command is shown to a human first, and the agent is confined to its workspace directory.

</details>

<br>

{header("builds")}
<div align="center">

{pic(base, "legend", "Legend: AI, research, data, automation, apps")}

{tiles[0]}

{tiles[1]}

{tiles[2]}

{tiles[3]}

</div>

<details>
<summary><b>Full index</b> — every element, one line each</summary>
<br>

| Element | Repository | What it does |
| :-- | :-- | :-- |
{index_rows}

</details>

<br>

{header("stack")}
<div align="center">{pic(base, "spectrum", "Tech stack drawn as an FTIR spectrum")}</div>

<br>

{header("research")}
<div align="center">

{pic(base, "research", "Research: green urea-imprinted PANi@CaO biosensors")}

{pic(base, "milestone", "Milestone: Certificate of Participation, LaTeX training workshop")}

</div>

<details>
<summary><b>Lab notebook</b> — methods & instruments</summary>
<br>

| | |
| :-- | :-- |
| **Synthesis** | Plant-mediated (green) CaO nanoparticles from *Syzygium cumini* extract |
| **Recognition layer** | Molecularly imprinted polyaniline (PANi) — urea-shaped cavities left after template removal |
| **Characterisation** | FTIR, UV-Vis, electrochemical response |
| **Computation** | Density functional theory with Quantum ESPRESSO — geometry optimisation, phonons, vibrational spectra |
| **Writing** | LaTeX, reproducible figures, literature pipelines built with [ArticlesDownloader](https://github.com/{USER}/ArticlesDownloader) & [ReviewForge](https://github.com/{USER}/ReviewForge) |

</details>

<br>

{header("telemetry")}
<div align="center">

{pic(base, "stats", "Live GitHub telemetry", live=True)}

{pic(base, "snake", "Contribution graph being eaten by a snake", live=True)}

</div>

<br>

{header("contact")}
<div align="center">

{contacts}

<br><br>

{pic(base, "footer", "Synthesizing intelligence, from atoms to autonomous code.")}

</div>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--local", help="write a preview README with relative asset paths to this file")
    a = ap.parse_args()
    if a.local:
        out = build("assets/svg")
        with open(a.local, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(out)
    else:
        with open(os.path.join(ROOT, "README.md"), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(build(f"{RAW}/main/assets/svg"))
    print("ok")


if __name__ == "__main__":
    main()
