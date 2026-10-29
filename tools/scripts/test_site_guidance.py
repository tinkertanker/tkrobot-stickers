#!/usr/bin/env python3
"""Check the built agent guide and catalog: run after npm run build."""

import hashlib
import json
import re
import unittest
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parents[2]


class SiteGuidanceTest(unittest.TestCase):
    def test_guide_and_catalog_cover_the_pack(self):
        manifest = json.loads((ROOT / "stickers/manifest.json").read_text())
        catalog = json.loads((ROOT / "dist/stickers.json").read_text())
        guide = (ROOT / "dist/llms.txt").read_text()
        expected = {item["slug"]: item for item in manifest["items"]}
        self.assertEqual(catalog["count"], len(expected))
        self.assertEqual([item["slug"] for item in catalog["items"]], list(expected))
        for item in catalog["items"]:
            with self.subTest(slug=item["slug"]):
                source = expected[item["slug"]]
                self.assertEqual(item["description"], source["description"])
                self.assertEqual(item["tags"], source["tags"])
                self.assertEqual(item["filename"], source["filename"])
                path = urlsplit(item["path"])
                self.assertEqual(path.path, "/" + source["sticker_path"])
                digest = hashlib.sha256((ROOT / source["sticker_path"]).read_bytes()).hexdigest()[:12]
                self.assertEqual(parse_qs(path.query), {"v": [digest]})

        links = re.findall(r"\[([^\]]+)\]\((https://stickers\.tk\.sg[^)]+)\)", guide)
        sticker_slugs = []
        for label, url in links:
            path = urlsplit(url).path
            self.assertTrue((ROOT / "dist" / path.lstrip("/")).exists(), url)
            if label in expected:
                self.assertEqual(path, "/" + expected[label]["sticker_path"])
                sticker_slugs.append(label)
        self.assertCountEqual(sticker_slugs, expected.keys())


if __name__ == "__main__":
    unittest.main()
