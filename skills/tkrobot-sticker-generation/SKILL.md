---
name: tkrobot-sticker-generation
description: Generate, review, and refine T Krobot sticker assets for the Tinkertanker mascot. Use when Codex is asked to create new T Krobot stickers, replace weak stickers from the sticker library, write image-generation prompts for T Krobot, check generated candidates against the mascot style, or preserve/version sticker assets in the tkrobot-stickers repo.
---

# T Krobot Sticker Generation

## Overview

Use this skill to keep generated T Krobot stickers visually consistent with the existing sticker library.

## Quick Workflow

1. Read `references/style-guide.md` before drafting prompts or judging outputs.
2. Compare candidates against the locked pack in `stickers/` and `contact-sheets/tkrobot-stickers.png` when available.
3. Preserve originals; save definitive transparent PNGs in `stickers/` and matching green sources in `sources/chroma-key/`.
4. Generate on a flat chroma-key background when transparent PNGs are needed, then remove the background locally.
5. Reject candidates that break the mascot invariants: mouths, default pupils, segmented limbs, joint rings, or black interior lines on white limbs.

## Prompting Rules

Start from this compact prompt shape:

```text
Create a T Krobot sticker for "<slug>" on a perfectly flat solid #00ff00 chroma-key background.
T Krobot is a black softened trapezoid robot matching the locked v11 anchor proportions: the head is not wide or rectangular, the head top is about 90% as wide as the bottom edge, and the body is also trapezoidal with larger rounded corners. Head and body use a subtle near-black-to-black gradient, plus a very thin 1px-style light grey shine line along the bottom edge of the head; large round white glasses with black rims, smooth plain light grey tube arms and legs around #e1e1e1 that are moderately slim, thicker than the too-thin v9/v10 attempts and still slimmer than the earliest baseline, hands with round black palm blobs plus light grey #e1e1e1 thumbs and fingers emerging from the blob edges, oversized black oval feet, and a flat red diamond chest mark.
No mouth. No neck. No joints. No segment lines. No black lines across arms or legs. Light grey limbs must be continuous plain shapes with only an outer black outline. Palms must be round black blobs that fingers emerge from, not gloves wrapped around the fingers; fingers and thumbs must be light grey #e1e1e1 and longer, not stubby black bits. No pupils by default; use pupils only for special looks such as charging, happy, and snooze lightning.
Use clean 2D cartoon sticker styling with thick black outlines, simple flat shapes, subtle highlights, expressive pose marks, generous padding, and no cropping.
```

Add the requested pose and emotion after the invariant block. Keep expression readable through pose, blank glasses, and motion marks rather than through a mouth or default pupils.

## Resources

- `references/style-guide.md`: canonical character/style rules and known replacement notes.
- `stickers/`: definitive transparent PNG sticker pack.
- `contact-sheets/tkrobot-stickers.png`: locked full-pack style overview.
- `assets/tkrobot-originals-contact-sheet.png`: original T Krobot set for style comparison.
- `assets/kiapkiap-contact-sheet.png`: scenario and pose inspiration, not a character style target.
