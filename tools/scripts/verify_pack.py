#!/usr/bin/env python3
"""Verify the definitive T Krobot sticker pack is consistent and agent-ready."""

from __future__ import annotations

import argparse
import filecmp
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = Path(__file__).resolve().parent
STICKERS = ROOT / "stickers"
MANIFEST = STICKERS / "manifest.json"
CONTACT_SHEET = STICKERS / "contact-sheet.png"
STICKERS_README = STICKERS / "README.md"
SITE_MANIFEST = ROOT / "site" / "stickers.json"
EXPECTED_SIZE = (1254, 1254)
EXPECTED_MODE = "RGBA"
ALLOWED_META_FILES = {"manifest.json", "README.md", "contact-sheet.png"}
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

# Sibling helpers live beside this script.
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from make_contact_sheet import build_contact_sheet  # noqa: E402
from sync_pack_readme import render_stickers_readme  # noqa: E402


def fail(errors: list[str], message: str) -> None:
    """Append a hard verification failure."""
    errors.append(message)


def validate_item_schema(
    item: object,
    index: int,
    errors: list[str],
    seen_slugs: set[str],
) -> dict | None:
    """Return a well-typed item dict, or None after recording schema errors."""
    label = f"items[{index}]"
    if not isinstance(item, dict):
        fail(errors, f"{label}: must be an object, got {type(item).__name__}")
        return None

    slug = item.get("slug")
    if not isinstance(slug, str) or not slug:
        fail(errors, f"{label}: slug must be a non-empty string")
        return None
    if not SLUG_RE.fullmatch(slug):
        fail(errors, f"{slug}: slug must be kebab-case ([a-z0-9]+ segments)")
    if slug in seen_slugs:
        fail(errors, f"{slug}: duplicate slug")
    seen_slugs.add(slug)

    filename = item.get("filename")
    sticker_path = item.get("sticker_path")
    source_path = item.get("source_path")
    description = item.get("description")
    tags = item.get("tags")

    if not isinstance(filename, str) or not filename:
        fail(errors, f"{slug}: filename must be a non-empty string")
    elif filename != f"{slug}.png":
        fail(errors, f"{slug}: filename must be '{slug}.png', got {filename!r}")

    if not isinstance(sticker_path, str) or not sticker_path:
        fail(errors, f"{slug}: sticker_path must be a non-empty string")
    elif filename and sticker_path != f"stickers/{filename}":
        fail(errors, f"{slug}: sticker_path must be 'stickers/{filename}', got {sticker_path!r}")

    if not isinstance(source_path, str) or not source_path.strip():
        fail(errors, f"{slug}: source_path must be a non-empty string")

    if not isinstance(description, str) or not description.strip():
        fail(errors, f"{slug}: description must be a non-empty string")

    if not isinstance(tags, list) or not tags:
        fail(errors, f"{slug}: tags must be a non-empty list of strings")
    elif any(not isinstance(tag, str) or not tag.strip() for tag in tags):
        fail(errors, f"{slug}: each tag must be a non-empty string")

    return item


def expected_site_manifest(manifest: dict) -> dict:
    """Build the site gallery payload without writing it."""

    def asset_version(path: str) -> str:
        return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()[:12]

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
        return datetime.fromtimestamp(source.stat().st_mtime, timezone.utc).date().isoformat()

    items = [
        {
            "slug": item["slug"],
            "filename": item["filename"],
            "path": f"/{item['sticker_path']}?v={asset_version(item['sticker_path'])}",
            "updated_at": last_updated(item["sticker_path"]),
        }
        for item in manifest["items"]
    ]
    return {
        "name": manifest["name"],
        "count": len(items),
        "items": items,
    }


def check_derived_readme(manifest: dict, errors: list[str]) -> None:
    """Fail when stickers/README.md is stale relative to the manifest."""
    if not STICKERS_README.is_file():
        fail(errors, "missing stickers/README.md")
        return
    expected = render_stickers_readme(manifest)
    actual = STICKERS_README.read_text()
    if actual != expected:
        fail(
            errors,
            "stickers/README.md is stale; run python3 tools/scripts/sync_pack_readme.py",
        )


def check_derived_site_manifest(manifest: dict, errors: list[str]) -> None:
    """Fail when site/stickers.json is stale relative to the pack."""
    if not SITE_MANIFEST.is_file():
        fail(errors, "missing site/stickers.json")
        return
    expected = expected_site_manifest(manifest)
    actual = json.loads(SITE_MANIFEST.read_text())
    if actual != expected:
        fail(
            errors,
            "site/stickers.json is stale; run python3 tools/scripts/build_site_manifest.py",
        )


def check_derived_contact_sheet(errors: list[str]) -> None:
    """Fail when stickers/contact-sheet.png does not match a fresh rebuild."""
    if not CONTACT_SHEET.is_file():
        fail(errors, "missing stickers/contact-sheet.png")
        return

    with tempfile.TemporaryDirectory() as tmp:
        rebuilt = Path(tmp) / "contact-sheet.png"
        build_contact_sheet(STICKERS, rebuilt, cols=4)
        if not filecmp.cmp(CONTACT_SHEET, rebuilt, shallow=False):
            fail(
                errors,
                "stickers/contact-sheet.png is stale; run "
                "python3 tools/scripts/make_contact_sheet.py stickers --out stickers/contact-sheet.png",
            )


def main() -> int:
    """Validate the definitive pack and its derived catalogue files."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--strict-sources",
        action="store_true",
        help="Require every item.source_path to exist on disk.",
    )
    parser.add_argument(
        "--skip-derived",
        action="store_true",
        help="Skip freshness checks for README, site manifest, and contact sheet.",
    )
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []

    if not MANIFEST.is_file():
        print(f"error: missing manifest at {MANIFEST.relative_to(ROOT)}", file=sys.stderr)
        return 1

    manifest = json.loads(MANIFEST.read_text())
    if not isinstance(manifest, dict):
        fail(errors, "manifest root must be an object")
        print("errors:")
        for error in errors:
            print(f"  - {error}")
        return 1

    pack_size = manifest.get("pack_size")
    if pack_size != list(EXPECTED_SIZE):
        fail(errors, f"manifest.pack_size must be {list(EXPECTED_SIZE)}, got {pack_size!r}")

    items = manifest.get("items")
    if not isinstance(items, list) or not items:
        fail(errors, "manifest.items must be a non-empty list")
        items = []

    declared_count = manifest.get("count")
    if declared_count != len(items):
        fail(errors, f"manifest.count is {declared_count}, but items has {len(items)} entries")

    seen_slugs: set[str] = set()
    valid_items: list[dict] = []
    for index, item in enumerate(items):
        validated = validate_item_schema(item, index, errors, seen_slugs)
        if validated is not None:
            valid_items.append(validated)

    pack_png_names = {
        item["filename"]
        for item in valid_items
        if isinstance(item.get("filename"), str)
    }
    unexpected = sorted(
        path.name
        for path in STICKERS.iterdir()
        if path.is_file()
        and path.name not in ALLOWED_META_FILES
        and path.name not in pack_png_names
    )
    if unexpected:
        fail(
            errors,
            "unexpected files in stickers/ (pack may only contain PNGs + "
            f"manifest.json/README.md/contact-sheet.png): {', '.join(unexpected)}",
        )

    png_files = sorted(
        p for p in STICKERS.glob("*.png") if p.is_file() and p.name != CONTACT_SHEET.name
    )
    png_names = {p.name for p in png_files}
    manifest_names = pack_png_names

    missing_files = sorted(manifest_names - png_names)
    orphan_files = sorted(png_names - manifest_names)
    if missing_files:
        fail(errors, f"manifest lists missing PNG files: {', '.join(missing_files)}")
    if orphan_files:
        fail(errors, f"PNG files missing from manifest: {', '.join(orphan_files)}")

    for item in valid_items:
        slug = item["slug"]
        sticker_path = item.get("sticker_path")
        source_path = item.get("source_path")
        path = ROOT / sticker_path if isinstance(sticker_path, str) else None
        if path is None or not path.is_file():
            fail(errors, f"{slug}: sticker file missing at {sticker_path}")
            continue

        with Image.open(path) as image:
            if image.mode != EXPECTED_MODE:
                fail(errors, f"{slug}: expected mode {EXPECTED_MODE}, got {image.mode}")
            if image.size != EXPECTED_SIZE:
                fail(
                    errors,
                    f"{slug}: expected size {EXPECTED_SIZE[0]}x{EXPECTED_SIZE[1]}, "
                    f"got {image.size[0]}x{image.size[1]}",
                )
            if "A" not in image.getbands():
                fail(errors, f"{slug}: missing alpha channel")
            else:
                alpha = image.getchannel("A")
                if alpha.getextrema()[0] >= 255:
                    fail(
                        errors,
                        f"{slug}: fully opaque export; transparent background required",
                    )

        if isinstance(source_path, str) and source_path.strip():
            source = ROOT / source_path
            if not source.is_file():
                message = f"{slug}: source_path missing on disk: {source_path}"
                if args.strict_sources:
                    fail(errors, message)
                else:
                    warnings.append(message)

    if not args.skip_derived:
        check_derived_readme(manifest, errors)
        check_derived_site_manifest(manifest, errors)
        check_derived_contact_sheet(errors)

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
        f"verify_pack: OK ({len(valid_items)} stickers, {len(warnings)} warning(s), "
        f"size {EXPECTED_SIZE[0]}x{EXPECTED_SIZE[1]} {EXPECTED_MODE})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
