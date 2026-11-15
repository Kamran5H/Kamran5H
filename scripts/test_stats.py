"""Offline regression checks for public telemetry collection and failure handling."""
import datetime as dt
import io
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import stats


def calendar_html(count=1, total=None, day_count=365):
    start = dt.date(2025, 1, 1)
    cells = []
    for i in range(day_count):
        day = start + dt.timedelta(days=i)
        text = "No contributions" if count == 0 else f"{count:,} contributions"
        # Deliberately use the opposite attribute order to GitHub's current HTML.
        cells.append(f'<td id="day-{i}" data-date="{day}"></td>'
                     f'<tool-tip for="day-{i}"><span>{text}</span> on {day}.</tool-tip>')
    total = count * day_count if total is None else total
    return f'<h2>{total:,} contributions in the last year</h2>' + "".join(cells)


class StatsTests(unittest.TestCase):
    def test_calendar_handles_leap_year_and_week_boundary_ranges(self):
        for day_count in (364, 365, 366, 371):
            with self.subTest(day_count=day_count), patch.object(stats, "_req", return_value=calendar_html(day_count=day_count)):
                self.assertEqual(stats.contributions("example"), (day_count, [1] * day_count))

    def test_calendar_attribute_order_nested_text_and_thousands(self):
        with patch.object(stats, "_req", return_value=calendar_html(1234)):
            total, days = stats.contributions("example")
        self.assertEqual(total, 1234 * 365)
        self.assertEqual(days, [1234] * 365)

    def test_zero_calendar_is_valid_but_missing_calendar_is_not(self):
        with patch.object(stats, "_req", return_value=calendar_html(0)):
            self.assertEqual(stats.contributions("example"), (0, [0] * 365))
        with patch.object(stats, "_req", return_value="<html>Sign in</html>"):
            with self.assertRaisesRegex(ValueError, "Incomplete"):
                stats.contributions("example")

    def test_missing_daily_count_and_inconsistent_total_are_rejected(self):
        for html in (calendar_html().replace("1 contributions", "unknown count", 1),
                     calendar_html(total=999)):
            with self.subTest(html=html[:70]), patch.object(stats, "_req", return_value=html):
                with self.assertRaises(ValueError):
                    stats.contributions("example")

    def test_all_pages_and_only_public_original_projects_are_counted(self):
        def repo(name, **extra):
            return {"name": name, "fork": False, "private": False,
                    "stargazers_count": 1, "languages_url": f"languages/{name}", **extra}

        first = [repo(f"project-{i}") for i in range(100)]
        second = [repo("last"), repo("example"), repo("private", private=True), repo("fork", fork=True)]
        calls = []

        def request(url):
            calls.append(url)
            if url.endswith("&page=1"):
                return first
            if url.endswith("&page=2"):
                return second
            return {"Python": 10}

        with patch.object(stats, "_req", side_effect=request), patch.object(stats, "contributions", return_value=(3, [3])):
            data = stats.collect("example")
        self.assertEqual(data["repos"], 101)
        self.assertEqual(data["stars"], 101)
        self.assertEqual(data["langs"], {"Python": 1010})
        self.assertNotIn("languages/private", calls)
        self.assertNotIn("languages/fork", calls)
        self.assertNotIn("languages/example", calls)

    def test_token_is_not_sent_to_public_calendar(self):
        requests = []

        def open_request(request, **kwargs):
            requests.append(request)
            return io.BytesIO(b"{}")

        with patch.dict(os.environ, {"GITHUB_TOKEN": "test-token"}), patch.object(stats.urllib.request, "urlopen", side_effect=open_request):
            stats._req(f"{stats.API}/users/example/repos")
            stats._req("https://github.com/users/example/contributions", raw=True)
        self.assertEqual(requests[0].get_header("Authorization"), "Bearer test-token")
        self.assertIsNone(requests[1].get_header("Authorization"))

    def test_render_failure_preserves_both_existing_cards(self):
        with tempfile.TemporaryDirectory() as out:
            paths = [Path(out) / f"stats-{theme}.svg" for theme in stats.THEMES]
            for path in paths:
                path.write_text("previous valid card")
            with patch("sys.argv", ["stats.py", "--out", out]), patch.object(stats, "collect", return_value={}), patch.object(stats, "render", side_effect=["new card", RuntimeError("font failure")]):
                with self.assertRaisesRegex(RuntimeError, "font failure"):
                    stats.main()
            self.assertTrue(all(path.read_text() == "previous valid card" for path in paths))


if __name__ == "__main__":
    unittest.main()
