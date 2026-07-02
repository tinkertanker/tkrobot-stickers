# T Krobot Stickers

This repo stores the source sticker library and generation guidance for T Krobot, Tinkertanker's robot mascot with glasses.

## Layout

- `originals/tkrobot/` — PNGs downloaded from `https://tk.sg/stickerlib`, plus the captured source HTML and manifest.
- `generated/rejected-v1/` — generated candidates kept for version history, but rejected for style issues.
- `generated/sources-v2/` — chroma-key source renders for the improved replacements.
- `generated/replacements-v2/` — transparent PNG replacement candidates.
- `references/kiapkiap/` — copied Kiap Kiap sticker reference set for scenario and prompt inspiration.
- `prompts/` — reusable prompt guidance.
- `skills/tkrobot-sticker-generation/` — local Codex skill for future T Krobot sticker work.

## Current Replacement Candidates

The first improved batch covers the weaker originals: `gasp`, `salute`, `yay`, `snooze`, and `shock`.

Use `generated/replacements-v2/` for the current transparent candidates. Keep older generated versions in place so style decisions remain traceable.

## Character Rules

T Krobot is a simple black robot with large white glasses, black mitten hands, oversized black feet, smooth plain white limbs, and a red diamond chest mark.

Do not draw a mouth. Do not draw joints, segment rings, bend lines, or any black interior lines on the white arms or legs. Pupils are allowed when useful, but they must sit inside the glasses.
