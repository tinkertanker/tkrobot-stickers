#!/usr/bin/env python3
"""Export chat-sized WhatsApp/iMessage derivatives from the locked sticker pack."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from io import BytesIO
from pathlib import Path

from PIL import Image, features


ROOT = Path(__file__).resolve().parents[2]
STICKER_MANIFEST = ROOT / "stickers" / "manifest.json"
PACK_CONFIG = ROOT / "ios" / "pack-config.json"
DERIVED = ROOT / "ios" / "Derived"
WHATSAPP_DIR = DERIVED / "whatsapp"
IMESSAGE_DIR = DERIVED / "imessage"
DERIVED_MANIFEST = DERIVED / "manifest.json"

MASTER_SIZE = (1254, 1254)
CHAT_SIZE = (512, 512)
TRAY_SIZE = (96, 96)
WEBP_MAX_BYTES = 100_000
TRAY_MAX_BYTES = 50_000
WEBP_START_QUALITY = 80
WEBP_MIN_QUALITY = 30
WEBP_METHOD = 6
PACK_MIN_STICKERS = 3
PACK_MAX_STICKERS = 30


def fail(errors: list[str], message: str) -> None:
    """Append a hard export failure."""
    errors.append(message)


def load_json(path: Path, errors: list[str], label: str) -> dict | None:
    """Load a JSON object, or record an error and return None."""
    if not path.is_file():
        fail(errors, f"missing {label} at {path.relative_to(ROOT).as_posix()}")
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        fail(errors, f"could not read {label}: {error}")
        return None
    if not isinstance(data, dict):
        fail(errors, f"{label} root must be an object")
        return None
    return data


def repo_path(path: Path) -> str:
    """Return a POSIX path relative to the repo root."""
    return path.relative_to(ROOT).as_posix()


def confirm_webp() -> str | None:
    """Return an error message if Pillow cannot save WebP."""
    if not features.check("webp"):
        return (
            "Pillow has no WebP support; install a build with WebP "
            "(e.g. pip install --upgrade Pillow)"
        )
    try:
        probe = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
        buffer = BytesIO()
        probe.save(buffer, format="WEBP", quality=WEBP_START_QUALITY, method=WEBP_METHOD, lossless=False)
        if not buffer.getvalue():
            return "Pillow WebP save produced an empty file"
    except (OSError, ValueError, TypeError) as error:
        return f"Pillow cannot save WebP: {error}"
    return None


def load_master(slug: str, sticker_path: str, errors: list[str]) -> Image.Image | None:
    """Open a locked master PNG as RGBA."""
    path = ROOT / sticker_path
    if not path.is_file():
        fail(errors, f"{slug}: master missing at {sticker_path}")
        return None
    try:
        with Image.open(path) as image:
            if image.size != MASTER_SIZE:
                fail(
                    errors,
                    f"{slug}: expected master size {MASTER_SIZE[0]}x{MASTER_SIZE[1]}, "
                    f"got {image.size[0]}x{image.size[1]}",
                )
                return None
            return image.convert("RGBA")
    except (OSError, Image.DecompressionBombError) as error:
        fail(errors, f"{slug}: could not read master PNG: {error}")
        return None


def encode_webp(image: Image.Image, slug: str, errors: list[str]) -> tuple[bytes, int] | None:
    """Encode a 512×512 RGBA image as lossy WebP under the static size cap."""
    last_size = 0
    for quality in range(WEBP_START_QUALITY, WEBP_MIN_QUALITY - 1, -1):
        buffer = BytesIO()
        image.save(
            buffer,
            format="WEBP",
            quality=quality,
            method=WEBP_METHOD,
            lossless=False,
        )
        data = buffer.getvalue()
        last_size = len(data)
        if last_size <= WEBP_MAX_BYTES:
            return data, quality
    fail(
        errors,
        f"{slug}: WebP is {last_size} bytes at quality {WEBP_MIN_QUALITY} "
        f"(limit {WEBP_MAX_BYTES})",
    )
    return None


def save_png(image: Image.Image, path: Path) -> int:
    """Write an RGBA PNG and return its byte size."""
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, format="PNG", optimize=True)
    return path.stat().st_size


def validate_pack_config(
    config: dict,
    manifest_slugs: set[str],
    errors: list[str],
) -> list[dict]:
    """Return normalised WhatsApp packs after checking coverage and counts."""
    packs_raw = config.get("whatsapp_packs")
    if not isinstance(packs_raw, list) or not packs_raw:
        fail(errors, "pack-config.whatsapp_packs must be a non-empty list")
        return []

    tray_slug = config.get("tray_slug")
    if not isinstance(tray_slug, str) or not tray_slug.strip():
        fail(errors, "pack-config.tray_slug must be a non-empty string")
    elif tray_slug not in manifest_slugs:
        fail(errors, f"pack-config.tray_slug {tray_slug!r} is not in the sticker manifest")

    packs: list[dict] = []
    assigned: dict[str, str] = {}
    seen_identifiers: set[str] = set()

    for index, pack in enumerate(packs_raw):
        label = f"whatsapp_packs[{index}]"
        if not isinstance(pack, dict):
            fail(errors, f"{label}: must be an object")
            continue

        identifier = pack.get("identifier")
        name = pack.get("name")
        slugs = pack.get("slugs")

        if not isinstance(identifier, str) or not identifier.strip():
            fail(errors, f"{label}: identifier must be a non-empty string")
            identifier = ""
        elif identifier in seen_identifiers:
            fail(errors, f"{label}: duplicate identifier {identifier!r}")
        else:
            seen_identifiers.add(identifier)

        if not isinstance(name, str) or not name.strip():
            fail(errors, f"{label}: name must be a non-empty string")
            name = ""

        if not isinstance(slugs, list) or not slugs:
            fail(errors, f"{label}: slugs must be a non-empty list")
            continue

        cleaned: list[str] = []
        seen_in_pack: set[str] = set()
        for slug in slugs:
            if not isinstance(slug, str) or not slug:
                fail(errors, f"{label}: each slug must be a non-empty string")
                continue
            if slug in seen_in_pack:
                fail(errors, f"{identifier or label}: duplicate slug {slug!r}")
                continue
            seen_in_pack.add(slug)
            cleaned.append(slug)
            if slug not in manifest_slugs:
                fail(errors, f"{identifier or label}: slug {slug!r} is not in the sticker manifest")
            elif slug in assigned:
                fail(
                    errors,
                    f"{slug}: appears in more than one WhatsApp pack "
                    f"({assigned[slug]} and {identifier or label})",
                )
            elif identifier:
                assigned[slug] = identifier

        count = len(cleaned)
        if count < PACK_MIN_STICKERS or count > PACK_MAX_STICKERS:
            fail(
                errors,
                f"{identifier or label}: pack must have {PACK_MIN_STICKERS}–"
                f"{PACK_MAX_STICKERS} stickers, got {count}",
            )

        packs.append(
            {
                "identifier": identifier,
                "name": name,
                "slugs": cleaned,
            }
        )

    missing = sorted(manifest_slugs - set(assigned))
    if missing:
        fail(
            errors,
            "manifest slugs missing from WhatsApp packs: " + ", ".join(missing),
        )

    return packs


def print_failures(errors: list[str]) -> int:
    """Print collected errors and return a failure exit code."""
    print("errors:")
    for error in errors:
        print(f"  - {error}")
    print(f"\nexport_chat_pack: FAILED ({len(errors)} error(s))")
    return 1


def newest_mtime(paths: list[Path]) -> float:
    """Return the latest modification time among existing paths."""
    mtimes = [path.stat().st_mtime for path in paths if path.is_file()]
    return max(mtimes) if mtimes else 0.0


def derived_is_fresh(master_paths: list[Path]) -> bool:
    """True when ios/Derived/manifest.json is newer than config, masters, and this script."""
    if not DERIVED_MANIFEST.is_file():
        return False
    sources = [
        Path(__file__).resolve(),
        STICKER_MANIFEST,
        PACK_CONFIG,
        *master_paths,
    ]
    return DERIVED_MANIFEST.stat().st_mtime >= newest_mtime(sources)


def main() -> int:
    """Build gitignored chat-sized derivatives under ios/Derived/."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--force",
        action="store_true",
        help="Rebuild even if ios/Derived/ is newer than the masters and pack config.",
    )
    args = parser.parse_args()

    errors: list[str] = []

    webp_error = confirm_webp()
    if webp_error:
        fail(errors, webp_error)

    sticker_manifest = load_json(STICKER_MANIFEST, errors, "stickers/manifest.json")
    pack_config = load_json(PACK_CONFIG, errors, "ios/pack-config.json")
    if errors or sticker_manifest is None or pack_config is None:
        return print_failures(errors)

    items = sticker_manifest.get("items")
    if not isinstance(items, list) or not items:
        fail(errors, "stickers/manifest.json items must be a non-empty list")
        return print_failures(errors)

    masters: dict[str, str] = {}
    for index, item in enumerate(items):
        label = f"items[{index}]"
        if not isinstance(item, dict):
            fail(errors, f"{label}: must be an object")
            continue
        slug = item.get("slug")
        sticker_path = item.get("sticker_path")
        if not isinstance(slug, str) or not slug:
            fail(errors, f"{label}: slug must be a non-empty string")
            continue
        if slug in masters:
            fail(errors, f"{slug}: duplicate slug in sticker manifest")
            continue
        if not isinstance(sticker_path, str) or not sticker_path:
            fail(errors, f"{slug}: sticker_path must be a non-empty string")
            continue
        masters[slug] = sticker_path

    manifest_slugs = set(masters)
    packs = validate_pack_config(pack_config, manifest_slugs, errors)
    if errors:
        return print_failures(errors)

    master_files = [ROOT / path for path in masters.values()]
    if not args.force and derived_is_fresh(master_files):
        print("export_chat_pack: skip (ios/Derived is newer than masters and pack-config)")
        print("  pass --force to rebuild")
        return 0

    tray_slug = pack_config["tray_slug"]
    emojis_map = pack_config.get("emojis")
    if emojis_map is None:
        emojis_map = {}
    elif not isinstance(emojis_map, dict):
        fail(errors, "pack-config.emojis must be an object when present")
        return print_failures(errors)

    if DERIVED.exists():
        shutil.rmtree(DERIVED)
    IMESSAGE_DIR.mkdir(parents=True)
    WHATSAPP_DIR.mkdir(parents=True)

    loaded: dict[str, Image.Image] = {}
    for slug, sticker_path in masters.items():
        image = load_master(slug, sticker_path, errors)
        if image is not None:
            loaded[slug] = image
    if errors:
        return print_failures(errors)

    chat_images = {
        slug: image.resize(CHAT_SIZE, Image.Resampling.LANCZOS)
        for slug, image in loaded.items()
    }

    imessage_entries: list[dict] = []
    for slug in sorted(chat_images):
        dest = IMESSAGE_DIR / f"{slug}.png"
        size_bytes = save_png(chat_images[slug], dest)
        imessage_entries.append(
            {
                "slug": slug,
                "path": repo_path(dest),
                "bytes": size_bytes,
                "size": list(CHAT_SIZE),
            }
        )

    tray_master = loaded[tray_slug].resize(TRAY_SIZE, Image.Resampling.LANCZOS)

    whatsapp_manifest: list[dict] = []
    webp_sizes: list[int] = []
    tray_sizes: list[int] = []

    for pack in packs:
        identifier = pack["identifier"]
        pack_dir = WHATSAPP_DIR / identifier
        pack_dir.mkdir(parents=True, exist_ok=True)

        tray_path = pack_dir / "tray.png"
        tray_bytes = save_png(tray_master, tray_path)
        tray_sizes.append(tray_bytes)
        if tray_bytes > TRAY_MAX_BYTES:
            fail(
                errors,
                f"{identifier}: tray.png is {tray_bytes} bytes (limit {TRAY_MAX_BYTES})",
            )

        sticker_entries: list[dict] = []
        for slug in pack["slugs"]:
            encoded = encode_webp(chat_images[slug], slug, errors)
            if encoded is None:
                continue
            data, quality = encoded
            dest = pack_dir / f"{slug}.webp"
            dest.write_bytes(data)
            size_bytes = dest.stat().st_size
            webp_sizes.append(size_bytes)
            raw_emojis = emojis_map.get(slug, [])
            if isinstance(raw_emojis, list):
                sticker_emojis = [item for item in raw_emojis if isinstance(item, str)]
            else:
                sticker_emojis = []
            sticker_entries.append(
                {
                    "slug": slug,
                    "path": repo_path(dest),
                    "bytes": size_bytes,
                    "size": list(CHAT_SIZE),
                    "quality": quality,
                    "emojis": sticker_emojis,
                }
            )

        whatsapp_manifest.append(
            {
                "identifier": identifier,
                "name": pack["name"],
                "tray": {
                    "path": repo_path(tray_path),
                    "bytes": tray_bytes,
                    "size": list(TRAY_SIZE),
                    "slug": tray_slug,
                },
                "stickers": sticker_entries,
            }
        )

    if errors:
        return print_failures(errors)

    derived = {
        "publisher": pack_config.get("publisher"),
        "ios_app_store_id": pack_config.get("ios_app_store_id"),
        "tray_slug": tray_slug,
        "source_manifest": repo_path(STICKER_MANIFEST),
        "pack_config": repo_path(PACK_CONFIG),
        "limits": {
            "webp_max_bytes": WEBP_MAX_BYTES,
            "tray_max_bytes": TRAY_MAX_BYTES,
            "sticker_size": list(CHAT_SIZE),
            "tray_size": list(TRAY_SIZE),
        },
        "imessage": {
            "count": len(imessage_entries),
            "stickers": imessage_entries,
        },
        "whatsapp": {
            "pack_count": len(whatsapp_manifest),
            "sticker_count": len(webp_sizes),
            "packs": whatsapp_manifest,
        },
    }
    DERIVED_MANIFEST.write_text(json.dumps(derived, indent=2) + "\n", encoding="utf-8")

    pack_summary = ", ".join(
        f"{pack['identifier']} ({len(pack['stickers'])})" for pack in whatsapp_manifest
    )
    print("export_chat_pack: OK")
    print(f"  iMessage: {len(imessage_entries)} PNGs at {CHAT_SIZE[0]}x{CHAT_SIZE[1]}")
    print(
        f"  WhatsApp: {len(whatsapp_manifest)} packs, {len(webp_sizes)} WebP, "
        f"{len(tray_sizes)} trays ({pack_summary})"
    )
    print(f"  WebP bytes: min={min(webp_sizes)} max={max(webp_sizes)}")
    print(f"  tray bytes: min={min(tray_sizes)} max={max(tray_sizes)}")
    print(f"  wrote {repo_path(DERIVED_MANIFEST)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
