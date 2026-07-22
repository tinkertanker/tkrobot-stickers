#!/usr/bin/env python3
"""Create a labelled contact sheet for PNG sticker folders."""

from __future__ import annotations

import argparse
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def build_contact_sheet(folder: Path, out: Path, cols: int = 4) -> Path:
    """Build a labelled contact sheet and write it to ``out``."""
    out_path = out.resolve()
    files = sorted(
        p
        for p in folder.glob("*.png")
        if p.is_file()
        and p.name != "contact-sheet.png"
        and p.resolve() != out_path
    )
    if not files:
        raise SystemExit(f"No PNG files found in {folder}")

    font = ImageFont.load_default()
    cell_w, cell_h = 240, 275
    rows = math.ceil(len(files) / cols)
    sheet = Image.new("RGBA", (cols * cell_w, rows * cell_h), (246, 246, 246, 255))
    draw = ImageDraw.Draw(sheet)

    for index, path in enumerate(files):
        col = index % cols
        row = index // cols
        x0 = col * cell_w
        y0 = row * cell_h
        draw.rounded_rectangle(
            [x0 + 8, y0 + 8, x0 + cell_w - 8, y0 + cell_h - 8],
            radius=8,
            fill=(255, 255, 255, 255),
            outline=(218, 218, 218, 255),
        )

        image = Image.open(path).convert("RGBA")
        image.thumbnail((200, 210), Image.LANCZOS)
        sheet.alpha_composite(image, (x0 + (cell_w - image.width) // 2, y0 + 14))
        draw.text((x0 + 16, y0 + 238), path.stem[:30], fill=(20, 20, 20, 255), font=font)

    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.convert("RGB").save(out, quality=95)
    return out


def main() -> None:
    """CLI entrypoint for building a labelled contact sheet."""
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--cols", type=int, default=4)
    args = parser.parse_args()
    print(build_contact_sheet(args.folder, args.out, cols=args.cols))


if __name__ == "__main__":
    main()
