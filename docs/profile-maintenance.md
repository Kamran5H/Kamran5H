# Maintaining the GitHub profile

Run commands from the repository root. Install the pinned rendering dependencies first:

```sh
python -m pip install -r requirements-profile.txt
```

## Edit and regenerate

- `scripts/profile_data.py` contains the curated selected projects, project directory, descriptions, and contact links. This collection does not claim to list every repository.
- `scripts/build_readme.py` contains the introduction, research, toolkit, and Markdown layout.
- `scripts/build_profile_art.py` generates the hero and project covers in `assets/profile/`. It uses the shared themes and bundled fonts from `scripts/design.py`.

After editing, regenerate and validate:

```sh
python scripts/build_profile_art.py
python scripts/build_readme.py
python scripts/check_profile.py
python -m unittest discover -s scripts -p 'test_stats.py'
```

Commit the generators, source data, generated `README.md`, and generated artwork together. Do not hand-edit generated files. Existing `assets/svg/`, photos, archives, and the developer badge are preserved because other repository READMEs may link to them.

## Preview the result

Artwork paths in the README are relative to this repository, so a branch's README displays that branch's covers. Open the branch README on GitHub to inspect the actual rendering before merging. Keep a local preview Markdown file at the repository root so its relative artwork paths resolve:

```sh
python scripts/build_readme.py --local preview.md
```

Check narrow and wide screens and both light and dark themes. Each cover has mobile and desktop variants; `<picture>` selects the appropriate theme and viewport. Essential information stays in native Markdown. GitHub does not run JavaScript in a README: section anchors, repository links, and `<details>` disclosures provide the interaction.

## Keep claims grounded

Align identity, research status, project descriptions, and public links with the public [Portfolio identity](https://github.com/Kamran5H/Portfolio/blob/main/content/site.json), [research](https://github.com/Kamran5H/Portfolio/blob/main/content/research.json), and [project case studies](https://github.com/Kamran5H/Portfolio/blob/main/content/projects.json), then check the relevant project's README. Distinguish ongoing work, literature interests, and previous projects. Avoid test counts, performance figures, publication claims, or availability claims without current supporting evidence.

HTTP checks on 15 November 2026 returned `200` for the portfolio and public CV. Both `qaukalam.me` and `www.qaukalam.me` returned `403` from the verification environment; QAU Kalam's live availability remains unverified. A `403` does not establish that the application is offline.

## Activity cards

`scripts/stats.py` reads public, original repositories, excluding this profile repository from the language breakdown. It reads the anonymous, publicly visible contribution calendar; a GitHub token is used only for REST API rate limits and is not sent to the calendar page. Language shares represent repository bytes, not proficiency.

Render a local preview without publishing:

```sh
python scripts/stats.py --user Kamran5H --out /tmp/kamran-profile-stats
```

The optional `GITHUB_TOKEN` environment variable raises API rate limits. Never put a token in tracked files.

`.github/workflows/profile.yml` checks collection, renders the cards and contribution artwork, and publishes them to the `output` branch twice daily. The README reads those published files. The timestamp records the last successful render, not a live query. Collection or rendering errors stop publication and leave the last successful output visible; inspect the workflow logs when that timestamp becomes stale.
