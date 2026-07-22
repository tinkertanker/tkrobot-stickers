#!/usr/bin/env python3
"""Regenerate stickers/README.md from stickers/manifest.json."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "stickers" / "manifest.json"
STICKERS_README = ROOT / "stickers" / "README.md"


def main() -> None:
    manifest = json.loads(MANIFEST.read_text())
    items = sorted(manifest["items"], key=lambda item: item["slug"])
    width, height = manifest.get("pack_size", [1254, 1254])

    lines = [
        "# Definitive T Krobot Sticker Pack",
        "",
        "Use these transparent PNGs as the current locked rectangular-finger T Krobot sticker set.",
        "",
        f"- Count: {len(items)} stickers.",
        f"- Size: {width} x {height} RGBA PNGs.",
        "- Catalogue: `stickers/manifest.json` (slug, description, tags, source path).",
        "- Full overview sheet: `stickers/contact-sheet.png`.",
        "- Chroma-key / generation sources are recorded per item in the manifest; older scrape sources live under `archive/chroma-key-sources/`.",
        "",
        "## Stickers",
        "",
    ]
    for item in items:
        tags = ", ".join(item.get("tags", [])) or "untagged"
        description = item.get("description", "").strip() or "No description yet."
        lines.append(f"- `{item['filename']}` — {description} _{tags}_")
    lines.append("")
    STICKERS_README.write_text("\n".join(lines))
    print(f"Synced stickers/README.md for {len(items)} stickers")


if __name__ == "__main__":
    main()
