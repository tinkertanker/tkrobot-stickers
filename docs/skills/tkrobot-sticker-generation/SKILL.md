---
name: tkrobot-sticker-generation
description: Generate, review, and refine T Krobot sticker assets for the Tinkertanker mascot. Use when asked to create new T Krobot stickers, replace weak stickers, write image-generation prompts for T Krobot, check candidates against the mascot style, or version sticker assets in this repo.
---

# T Krobot Sticker Generation

## Overview

Keep generated T Krobot stickers visually consistent with the definitive pack in `stickers/`.

Repo map and commit checklist: root `AGENTS.md`.

## Quick Workflow

1. Scan `stickers/manifest.json` for existing slugs, descriptions, and tags so you do not duplicate a pose.
2. Read `references/style-guide.md` before drafting prompts or judging outputs.
3. Compare candidates against `stickers/contact-sheet.png` and the hand-size lock at `docs/references/hand-size-anchor.png`.
4. Generate one sticker at a time on a flat `#00ff00` chroma-key background when transparent PNGs are needed, then remove the background locally.
5. Save the definitive 1254×1254 transparent PNG in `stickers/<slug>.png` and record it in `stickers/manifest.json` with a non-empty `source_path`, `description`, and `tags`; preserve the referenced source under `archive/` when useful.
6. Refresh the contact sheet / sticker README / site manifest via `tools/scripts/`.
7. Run `python3 tools/scripts/verify_pack.py` before committing.
8. If `ios/` is present, add the slug to `ios/pack-config.json` (emoji and one WhatsApp pack), then run `python3 tools/scripts/export_chat_pack.py`. Do not invent poses inside `ios/` or resize masters by hand.
9. Reject candidates that break the mascot invariants: mouths, default pupils, segmented limbs, joint rings, or black interior lines on white limbs.

## Prompting Rules

Start from this compact prompt shape:

```text
Create a T Krobot sticker for "<slug>" on a perfectly flat solid #00ff00 chroma-key background.
T Krobot is a black softened trapezoid robot matching the locked v11 anchor proportions: the head is not wide or rectangular, the head top is about 90% as wide as the bottom edge, and the body is also trapezoidal with larger rounded corners. Head and body use a subtle near-black-to-black gradient, plus a very thin 1px-style light grey shine line along the bottom edge of the head; large round white glasses with black rims kept at their locked wide round proportions independently of the head taper—the glasses must not be shrunk or horizontally compressed to fit, and their frames may extend beyond the head sides—smooth plain light grey tube arms and legs around #e1e1e1 that are moderately slim, thicker than the too-thin v9/v10 attempts and still slimmer than the earliest baseline, hands with round black palm blobs plus light grey #e1e1e1 thumbs and fingers emerging from the blob edges, oversized black oval feet, and a flat red diamond chest mark.
No mouth. No neck. No joints. No segment lines. No black lines across arms or legs. Light grey limbs must be continuous plain shapes with only an outer black outline. Palms must be round black blobs that fingers emerge from, not gloves wrapped around the fingers; each visible hand must have exactly three fingers plus one thumb; fingers and thumbs must be light grey #e1e1e1 flat rectangular tabs with hard sides and flat or slightly rounded corners, not sausage-like tubes. Keep the glasses wide and round; never compress them to fit inside the tapered head, and allow them to overhang the head sides. No pupils by default; use pupils only for special looks such as charging, happy, and snooze lightning.
Use clean 2D cartoon sticker styling with thick black outlines, simple flat shapes, subtle highlights, expressive pose marks, generous padding, and no cropping.
```

Add the requested pose and emotion after the invariant block. Keep expression readable through pose, blank glasses, and motion marks rather than through a mouth or default pupils.

For the longer prompt skeleton and pose-specific notes, use `docs/prompts/tkrobot-sticker-guidelines.md`.

## Resources

- `references/style-guide.md`: canonical character/style rules and known replacement notes.
- `docs/references/hand-size-anchor.png`: locked hand and finger scale.
- `stickers/`: definitive transparent PNG sticker pack.
- `stickers/manifest.json`: slug catalogue with descriptions and tags.
- `stickers/contact-sheet.png`: locked full-pack style overview.
- `assets/tkrobot-originals-contact-sheet.png`: original T Krobot set for style comparison.
- `assets/kiapkiap-contact-sheet.png`: scenario and pose inspiration, not a character style target.
