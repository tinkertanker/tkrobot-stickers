#!/usr/bin/env python3
"""Verify the definitive T Krobot sticker pack is consistent and agent-ready."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
STICKERS = ROOT / "stickers"
MANIFEST = STICKERS / "manifest.json"
CONTACT_SHEET = STICKERS / "contact-sheet.png"
EXPECTED_SIZE = (1254, 1254)
EXPECTED_MODE = "RGBA"


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--strict-sources",
        action="store_true",
        help="Require every item.source_path to exist on disk.",
    )
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []

    if not MANIFEST.is_file():
        print(f"error: missing manifest at {MANIFEST.relative_to(ROOT)}", file=sys.stderr)
        return 1

    manifest = json.loads(MANIFEST.read_text())
    items = manifest.get("items", [])
    if not isinstance(items, list) or not items:
        fail(errors, "manifest.items must be a non-empty list")

    declared_count = manifest.get("count")
    if declared_count != len(items):
        fail(errors, f"manifest.count is {declared_count}, but items has {len(items)} entries")

    png_files = sorted(
        p for p in STICKERS.glob("*.png") if p.is_file() and p.name != CONTACT_SHEET.name
    )
    png_names = {p.name for p in png_files}
    manifest_names = {item.get("filename") for item in items}

    missing_files = sorted(manifest_names - png_names)
    orphan_files = sorted(png_names - manifest_names)
    if missing_files:
        fail(errors, f"manifest lists missing PNG files: {', '.join(missing_files)}")
    if orphan_files:
        fail(errors, f"PNG files missing from manifest: {', '.join(orphan_files)}")

    if not CONTACT_SHEET.is_file():
        fail(errors, "missing stickers/contact-sheet.png")

    seen_slugs: set[str] = set()
    for item in items:
        slug = item.get("slug")
        filename = item.get("filename")
        sticker_path = item.get("sticker_path")
        source_path = item.get("source_path")

        if not slug:
            fail(errors, f"item missing slug: {item!r}")
            continue
        if slug in seen_slugs:
            fail(errors, f"duplicate slug: {slug}")
        seen_slugs.add(slug)

        if filename != f"{slug}.png":
            fail(errors, f"{slug}: filename must be '{slug}.png', got {filename!r}")

        if sticker_path != f"stickers/{filename}":
            fail(errors, f"{slug}: sticker_path must be 'stickers/{filename}', got {sticker_path!r}")

        path = ROOT / sticker_path if sticker_path else None
        if path is None or not path.is_file():
            fail(errors, f"{slug}: sticker file missing at {sticker_path}")
            continue

        with Image.open(path) as image:
            if image.mode != EXPECTED_MODE:
                fail(errors, f"{slug}: expected mode {EXPECTED_MODE}, got {image.mode}")
            if image.size != EXPECTED_SIZE:
                fail(
                    errors,
                    f"{slug}: expected size {EXPECTED_SIZE[0]}x{EXPECTED_SIZE[1]}, got {image.size[0]}x{image.size[1]}",
                )
            if "A" not in image.getbands():
                fail(errors, f"{slug}: missing alpha channel")

        if source_path:
            source = ROOT / source_path
            if not source.is_file():
                message = f"{slug}: source_path missing on disk: {source_path}"
                if args.strict_sources:
                    fail(errors, message)
                else:
                    warnings.append(message)
        else:
            warnings.append(f"{slug}: no source_path recorded")

        if "description" not in item:
            warnings.append(f"{slug}: missing description")
        if "tags" not in item:
            warnings.append(f"{slug}: missing tags")

    if warnings:
        print("warnings:")
        for warning in warnings:
            print(f"  - {warning}")

    if errors:
        print("errors:")
        for error in errors:
            print(f"  - {error}")
        print(f"\nverify_pack: FAILED ({len(errors)} error(s), {len(warnings)} warning(s))")
        return 1

    print(
        f"verify_pack: OK ({len(items)} stickers, {len(warnings)} warning(s), size {EXPECTED_SIZE[0]}x{EXPECTED_SIZE[1]} {EXPECTED_MODE})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
