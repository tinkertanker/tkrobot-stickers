#!/usr/bin/env python3
"""Build the public site's sticker metadata from the canonical manifest."""

from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "stickers" / "manifest.json"
OUTPUT = ROOT / "site" / "stickers.json"


def asset_version(path: str) -> str:
    source = ROOT / path
    return hashlib.sha256(source.read_bytes()).hexdigest()[:12]


def last_updated(path: str) -> str:
    result = subprocess.run(
        ["git", "log", "-1", "--format=%cs", "--", path],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    date = result.stdout.strip()
    if date:
        return date

    source = ROOT / path
    if not source.exists():
        raise RuntimeError(f"No Git history or source file found for {path}")

    return datetime.fromtimestamp(source.stat().st_mtime, timezone.utc).date().isoformat()


def main() -> None:
    manifest = json.loads(SOURCE.read_text())
    items = [
        {
            "slug": item["slug"],
            "filename": item["filename"],
            "path": f"/{item['sticker_path']}?v={asset_version(item['sticker_path'])}",
            "updated_at": last_updated(item["sticker_path"]),
        }
        for item in manifest["items"]
    ]

    output = {
        "name": manifest["name"],
        "count": len(items),
        "items": items,
    }
    OUTPUT.write_text(json.dumps(output, indent=2) + "\n")


if __name__ == "__main__":
    main()
