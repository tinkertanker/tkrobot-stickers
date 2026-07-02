# T Krobot Stickers

This repo stores the source sticker library and generation guidance for T Krobot, Tinkertanker's robot mascot with glasses.

## Layout

- `originals/tkrobot/` — PNGs downloaded from `https://tk.sg/stickerlib`, plus the captured source HTML and manifest.
- `generated/rejected-v1/` — generated candidates kept for version history, but rejected for style issues.
- `generated/sources-v11/` — chroma-key source renders for the current anchor-adapted replacements.
- `generated/replacements-v11/` — current transparent PNG replacement candidates.
- `generated/rejected-v*/` — generated candidates kept for version history and style traceability.
- `references/kiapkiap/` — copied Kiap Kiap sticker reference set for scenario and prompt inspiration.
- `prompts/` — reusable prompt guidance.
- `skills/tkrobot-sticker-generation/` — local Codex skill for future T Krobot sticker work.

## Current Replacement Candidates

The current candidate batch is `generated/replacements-v11/`, covering `gasp`, `salute`, `yay`, `snooze`, and `shock`. This pass adapts the proportions from the preferred first calibration render, preserved as `generated/sources-v11-calibration/gasp-v11-anchor-source.png`.

Keep older generated versions in place so style decisions remain traceable. `generated/rejected-v9/` is preserved because the arms and legs became too thin; `generated/rejected-v10/` is preserved because the head became too wide; `generated/sources-v11-calibration/` preserves the proportion drift from the non-anchor calibration renders.

## Character Rules

T Krobot is a simple black robot with large white glasses, black palm blobs with light grey fingers, oversized black feet, smooth plain light grey limbs, and a flat red diamond chest mark. Use light grey body parts around `#e1e1e1`; do not make them charcoal-dark. Match the `gasp-v11` anchor proportions: arms and legs should be moderately slim, thicker than the too-thin v9/v10 attempts but still slimmer than the earliest baseline. Hands have a round black palm blob, with one longer light grey thumb and three longer light grey rounded fingers emerging from the blob's edge; the black palm is not a glove over the fingers. Do not add a neck. The head should be a softened trapezoid, not wide or rectangular; the top should be about 90% as wide as the bottom edge. The body should also be trapezoidal, with larger rounded corners. Separate the head from the body with a very thin 1px-style light grey shine/border along the bottom edge of the head.

Do not draw a mouth. Do not draw joints, segment rings, bend lines, or any black interior lines on the white arms or legs. Do not draw pupils by default; reserve pupils only for special looks where they are part of the concept, such as charging or happy.
