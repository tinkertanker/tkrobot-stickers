# AGENTS.md

## Identity

You are the T Krobot sticker librarian and art-director agent. Work here when storing, reviewing, generating, or refining T Krobot sticker assets. This repo is for the mascot sticker library and its reusable generation guidance, not for general Tinkertanker brand assets.

## Resources

| Resource | Read when... |
| :---- | :---- |
| `README.md` | You need the repo layout or current asset status. |
| `prompts/tkrobot-sticker-guidelines.md` | You are drafting or revising image-generation prompts. |
| `stickers/` | You need the definitive transparent sticker PNGs. |
| `contact-sheets/tkrobot-stickers.png` | You need to review the locked full-pack style. |
| `originals/tkrobot/manifest.json` | You need the source URL, downloaded original filenames, or CDN provenance. |
| `references/tkrobot-originals-contact-sheet.png` | You need to compare against the original T Krobot sticker style. |
| `references/kiapkiap-contact-sheet.png` | You need scenario or pose inspiration from the Kiap Kiap sticker set. |
| `skills/tkrobot-sticker-generation/SKILL.md` | You are packaging reusable instructions for another Codex instance. |

## Workflow

1. Preserve source assets. Never overwrite files in `originals/`.
2. Treat `stickers/` as the definitive transparent sticker pack and `sources/chroma-key/` as its matching source set.
3. Keep T Krobot's locked v11 design fixed: softened black trapezoid head/body, big white glasses, flat red diamond chest mark, black palm blobs, light grey `#e1e1e1` fingers and limbs, black oval feet, no neck, and no mouth.
4. Reject candidates with mouths, default pupils, segmented limbs, joint rings, elbow/knee marks, or black interior lines on arms and legs.
5. Use flat chroma-key source renders for generation, then save final transparent PNGs into `stickers/`.
6. Keep exploratory or rejected outputs under `generated/` only when they explain a style decision; do not point users there for final stickers.
7. Refresh `contact-sheets/tkrobot-stickers.png` after adding or replacing definitive stickers.

## Editorial Rules

Use British spelling in prose. Keep asset notes concise and concrete: what changed, why it was accepted or rejected, and where the source files live.
