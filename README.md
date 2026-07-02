# T Krobot Stickers

This repo stores the source sticker library and generation guidance for T Krobot, Tinkertanker's robot mascot with glasses.

## Layout

- `originals/tkrobot/` — PNGs downloaded from `https://tk.sg/stickerlib`, plus the captured source HTML and manifest.
- `generated/rejected-v1/` — generated candidates kept for version history, but rejected for style issues.
- `generated/sources-v2/` — chroma-key source renders for the improved replacements.
- `generated/rejected-v2/` — transparent PNG candidates rejected because the glasses used pupils too freely.
- `references/kiapkiap/` — copied Kiap Kiap sticker reference set for scenario and prompt inspiration.
- `prompts/` — reusable prompt guidance.
- `skills/tkrobot-sticker-generation/` — local Codex skill for future T Krobot sticker work.

## Current Replacement Candidates

The first improved batch covered the weaker originals: `gasp`, `salute`, `yay`, `snooze`, and `shock`, but v2 is rejected because pupils became the default expression language.

The current candidate batch is `generated/replacements-v9/`. `generated/rejected-v8/` is preserved because the hand still read too much like a glove rather than a palm blob with fingers emerging from it. Keep older generated versions in place so style decisions remain traceable.

## Character Rules

T Krobot is a simple black robot with large white glasses, black palm blobs with light grey fingers, oversized black feet, smooth plain light grey limbs, and a flat red diamond chest mark. Use light grey body parts around `#ccc`; do not make them charcoal-dark. Arms and legs should be about 20% skinnier than the current v8 candidates. Hands have a round black palm blob, with one longer light grey thumb and three longer light grey rounded fingers emerging from the blob's edge; the black palm is not a glove over the fingers. Do not add a neck. Separate the head from the body with a very thin 1px-style light grey shine/border along the bottom edge of the head.

Do not draw a mouth. Do not draw joints, segment rings, bend lines, or any black interior lines on the white arms or legs. Do not draw pupils by default; reserve pupils only for special looks where they are part of the concept, such as charging or happy.
