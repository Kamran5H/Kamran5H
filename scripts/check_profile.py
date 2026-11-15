"""Validate generated content, local pictures, navigation, and safe SVG assets."""
from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from html.parser import HTMLParser

from build_readme import ROOT, build


class Pictures(HTMLParser):
    def __init__(self):
        super().__init__()
        self.paths = set()
        self.details = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "details":
            self.details += 1
        if tag == "img":
            assert attrs.get("alt"), "Every image needs descriptive alt text"
        if tag in ("img", "source"):
            path = attrs.get("src") or attrs.get("srcset", "")
            if not path.startswith("https://"):
                assert path.startswith("assets/profile/"), f"Unexpected local artwork: {path}"
                assert (ROOT / path).is_file(), f"Missing image: {path}"
                self.paths.add(path)


def main():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert readme == build(), "README is stale; run python scripts/build_readme.py"
    pictures = Pictures()
    pictures.feed(readme)
    assert len(pictures.paths) == 16, "Expected all desktop/mobile, dark/light covers"
    assert pictures.details == readme.count("</details>"), "Unbalanced disclosures"

    headings = set()
    for heading in re.findall(r"^#{1,6} (.+)$", readme, re.M):
        # GitHub removes punctuation when generating anchors.
        headings.add(re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-"))
    for anchor in re.findall(r"\]\(#([^)]+)\)", readme):
        assert anchor in headings, f"Missing navigation target: #{anchor}"

    ns = "{http://www.w3.org/2000/svg}"
    for path in pictures.paths:
        root = ET.parse(ROOT / path).getroot()
        assert root.tag == ns + "svg", f"Not an SVG: {path}"
        assert root.attrib.get("viewBox"), f"Missing scalable viewBox: {path}"
        assert root.find(ns + "title") is not None, f"Missing SVG title: {path}"
        for element in root.iter():
            tag = element.tag.removeprefix(ns)
            assert tag not in {"script", "foreignObject", "animate", "animateMotion", "animateTransform"}, f"Unexpected active SVG content: {path}"
            for attr, value in element.attrib.items():
                assert not attr.lower().startswith("on"), f"Event handler in {path}"
                if attr.endswith("href"):
                    assert value.startswith(("data:image/", "#")), f"External resource in {path}"
    print(f"Profile valid: {len(pictures.paths)} images, {pictures.details} disclosures, navigation and generated README in sync")


if __name__ == "__main__":
    main()
