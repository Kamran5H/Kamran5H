"""Curated public projects used by the profile, not every repository."""

USER = "Kamran5H"
PORTFOLIO = "https://kamranashraf.is-a.dev"
CONTACTS = {
    "Email": "mailto:chkamran32b@gmail.com",
    "LinkedIn": "https://www.linkedin.com/in/kamran-ashraf-762a21363/",
    "ORCID": "https://orcid.org/0009-0003-2997-2954",
}

PROJECTS = [
    dict(
        repo="ArticlesDownloader", name="Articles Downloader", symbol="Ad",
        category="RESEARCH SOFTWARE", color="violet", art="papers",
        summary="Find scholarly papers across multiple databases, review the results, and collect open-access PDFs with citation exports.",
        stack="Python · SQLite · Scholarly APIs · BibTeX / RIS",
        details="Federated search brings together nine documented scholarly sources, DOI deduplication, local search history, and exports for reference managers. Browser, desktop, and command-line interfaces support different research workflows. Provider availability, API keys, and publisher access determine what can be retrieved.",
    ),
    dict(
        repo="AI-Coding", name="AI-Coding", symbol="Ac",
        category="AI & AUTOMATION", color="cyan", art="agent",
        summary="Explore a local coding agent with a browser interface, streamed responses, and human approval before shell commands.",
        stack="JavaScript · Node.js · Express · Server-sent events",
        details="The agent reads and edits project files through a tool loop. Its web interface streams progress and asks a human to approve shell commands. Source and setup notes document the tool loop, workspace restrictions, and approval flow.",
    ),
    dict(
        repo="Subah-TaskBook", name="Subah TaskBook", symbol="Sb",
        category="LOCAL-FIRST DESKTOP", color="amber", art="sunrise",
        summary="A quieter daily planner: carry unfinished tasks into tomorrow, keep a reflective journal, and work offline.",
        stack="Electron · JavaScript · Local storage",
        details="A daily focus queue, task rollover, journal entries, and completion rewards share one desktop application. Personal records stay on the device without a required cloud account. Local storage makes device backups part of the workflow.",
    ),
]

DIRECTORY = {
    "Research & writing": [
        ("ReviewForge", "Config-driven workflows for academic review writing."),
        ("ResearchDaybook", "An offline research journal in a single HTML file."),
    ],
    "Everyday tools": [
        ("Quidian-MediaDownloader", "Media, playlist, and subtitle downloads with yt-dlp and a web dashboard."),
        ("GmailZenith", "Inbox rules and bulk workflows using the Gmail API."),
        ("DiskOptimizerPro", "Windows cleanup and duplicate-file tools."),
        ("ChromeMonitor", "Chrome profile, extension, and resource monitoring."),
        ("AutoClearExtension", "A Chrome extension for clearing browsing data."),
        ("FacebookCleaner", "Browser-driven tools for account cleanup workflows."),
    ],
    "Data & creative experiments": [
        ("SourceGenius", "Brand-website discovery with browser automation."),
        ("SourceGenius-Share", "A deployment bundle for the SourceGenius tools."),
        ("BrandScrapers", "Brand extraction and data-cleaning utilities."),
        ("TikTokProductHunter", "Product discovery across Amazon and TikTok Shop."),
        ("Urdu-Poetry-Studio", "Urdu typography and poetry artwork."),
        ("VideoStudio", "A Gradio interface for generative-video workflows."),
        ("Humanizer", "Text-rewriting experiments and heuristic scoring."),
    ],
    "Web & beginnings": [
        ("Portfolio", "Research, software case studies, and my public CV."),
        ("Early-Coding-Archive", "Early Python, desktop, and machine-learning experiments."),
    ],
}
