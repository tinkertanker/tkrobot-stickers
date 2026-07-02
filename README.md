# T Krobot Stickers

This repo stores the source sticker library and generation guidance for T Krobot, Tinkertanker's robot mascot with glasses.

## Layout

- `originals/tkrobot/` — PNGs downloaded from `https://tk.sg/stickerlib`, plus the captured source HTML and manifest.
- `stickers/` — definitive transparent PNG sticker pack. Use these files for actual sharing/importing.
- `sources/chroma-key/` — definitive flat green source renders used to produce `stickers/`.
- `contact-sheets/tkrobot-stickers.png` — definitive overview sheet for the current pack.
- `generated/` — historical workbench for candidates, rejected attempts, and style iteration traceability.
- `references/kiapkiap/` — copied Kiap Kiap sticker reference set for scenario and prompt inspiration.
- `prompts/` — reusable prompt guidance.
- `skills/tkrobot-sticker-generation/` — local Codex skill for future T Krobot sticker work.

## Definitive Pack

The locked style is based on the approved v11 direction: softened trapezoid head/body, light grey `#e1e1e1` limbs and fingers, black palm blobs, no neck, no mouth, no default pupils, flat red diamond, and sparse motion marks.

The definitive pack contains all 22 stickers from `originals/tkrobot/manifest.json`, regenerated into `stickers/`. The matching chroma-key sources are in `sources/chroma-key/`. Older generated versions stay in place only as historical provenance.

## Character Rules

T Krobot is a simple black robot with large white glasses, black palm blobs with light grey fingers, oversized black feet, smooth plain light grey limbs, and a flat red diamond chest mark. Use light grey body parts around `#e1e1e1`; do not make them charcoal-dark. Match the v11 anchor proportions: arms and legs should be moderately slim, thicker than the too-thin v9/v10 attempts but still slimmer than the earliest baseline. Hands have a round black palm blob, with one longer light grey thumb and three longer light grey rounded fingers emerging from the blob's edge; the black palm is not a glove over the fingers. Do not add a neck. The head should be a softened trapezoid, not wide or rectangular; the top should be about 90% as wide as the bottom edge. The body should also be trapezoidal, with larger rounded corners. Separate the head from the body with a very thin 1px-style light grey shine/border along the bottom edge of the head.

Do not draw a mouth. Do not draw joints, segment rings, bend lines, or any black interior lines on the white arms or legs. Do not draw pupils by default; reserve pupils only for special looks where they are part of the concept, such as charging or happy.
