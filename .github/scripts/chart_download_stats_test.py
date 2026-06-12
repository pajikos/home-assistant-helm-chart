import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
MODULE_PATH = SCRIPT_DIR / "chart_download_stats.py"
FIXTURE_PATH = SCRIPT_DIR / "fixtures" / "releases.json"


class ChartDownloadStatsTest(unittest.TestCase):
    def load_module(self):
        self.assertTrue(
            MODULE_PATH.exists(),
            "chart_download_stats.py should exist before generator tests can run",
        )
        spec = importlib.util.spec_from_file_location("chart_download_stats", MODULE_PATH)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def load_releases(self):
        with FIXTURE_PATH.open() as fixture:
            return json.load(fixture)

    def test_build_stats_aggregates_chart_archive_downloads(self):
        module = self.load_module()

        stats = module.build_stats(
            self.load_releases(),
            generated_at="2026-06-12T00:00:00Z",
        )

        self.assertEqual(55445, stats["totalDownloads"])
        self.assertEqual(4, stats["releaseCount"])
        self.assertEqual("0.3.65", stats["latestVersion"])
        self.assertEqual(1, stats["latestVersionDownloads"])
        self.assertEqual(
            ["0.3.65", "0.3.64", "0.3.63", "0.2.102"],
            [version["version"] for version in stats["versions"]],
        )
        self.assertEqual(
            {"version": "0.2.102", "downloadCount": 53037},
            stats["topVersions"][0],
        )

    def test_compact_count_uses_floor_for_badge_values(self):
        module = self.load_module()

        self.assertEqual("999", module.compact_count(999))
        self.assertEqual("1k", module.compact_count(1000))
        self.assertEqual("471k", module.compact_count(471856))
        self.assertEqual("1.2M", module.compact_count(1234567))

    def test_write_outputs_badge_json_and_escaped_dashboard(self):
        module = self.load_module()
        stats = module.build_stats(
            self.load_releases(),
            generated_at="2026-06-12T00:00:00Z",
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir)
            module.write_outputs(stats, output_dir)

            downloads = json.loads((output_dir / "stats" / "downloads.json").read_text())
            badge = json.loads((output_dir / "stats" / "downloads-badge.json").read_text())
            dashboard = (output_dir / "stats" / "index.html").read_text()

        self.assertEqual(stats, downloads)
        self.assertEqual(
            {
                "schemaVersion": 1,
                "label": "chart downloads",
                "message": "55k",
                "color": "blue",
            },
            badge,
        )
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", dashboard)
        self.assertNotIn("<script>alert(1)</script>", dashboard)
        self.assertIn("GitHub release asset downloads, not confirmed installs", dashboard)


if __name__ == "__main__":
    unittest.main()
