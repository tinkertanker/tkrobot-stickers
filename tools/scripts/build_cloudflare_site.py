#!/usr/bin/env python3
"""Stage the public gallery for Cloudflare Workers Static Assets."""

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "dist"


def main() -> None:
    subprocess.run(
        [sys.executable, str(ROOT / "tools/scripts/build_site_manifest.py")],
        check=True,
    )
    if OUTPUT.exists():
        shutil.rmtree(OUTPUT)
    shutil.copytree(ROOT / "site", OUTPUT)
    shutil.copytree(ROOT / "stickers", OUTPUT / "stickers")
    (OUTPUT / "healthz").write_text("ok\n")
    (OUTPUT / "_headers").write_text(
        "/*\n"
        "  X-Content-Type-Options: nosniff\n"
        "  Referrer-Policy: strict-origin-when-cross-origin\n"
        "  Permissions-Policy: camera=(), microphone=(), geolocation=()\n"
        "  Cache-Control: no-cache, must-revalidate\n"
        "/stickers/*\n"
        "  ! Cache-Control\n"
        "  Cache-Control: public, max-age=31536000, immutable\n"
        "/healthz\n"
        "  Content-Type: text/plain; charset=utf-8\n"
    )


if __name__ == "__main__":
    main()
