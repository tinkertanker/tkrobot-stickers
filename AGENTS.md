# AGENTS.md

## Identity

This repository stores T Krobot sticker assets for Tinkertanker. Work here is limited to producing, naming, documenting, verifying, and publishing transparent PNG sticker files for the company mascot. Do not add unrelated brand assets, slide decks, checkerboard previews, or loose generated scratch files to this repo.

## Sticker Style

- T Krobot is a simple black robot mascot with large white glasses, softened trapezoid head and body, smooth light grey `#e1e1e1` limbs and fingers, black palm blobs, oversized black oval feet, and a flat red diamond chest mark.
- Use the locked v11 proportions: moderately slim limbs, no neck, head top about 90% as wide as the bottom, and a thin light grey shine line under the head to separate head and body.
- Do not draw a mouth.
- Do not use pupils by default. Special eye marks are allowed only when they define the sticker concept, such as happy upside-down-U eyes, snooze lightning, glare slits, or knocked-out X marks.
- Do not add joints, segmented limb rings, elbow/knee marks, bend lines, or black interior lines on arms and legs.
- Keep motion marks sparse and readable at sticker size.

## File Rules

- Put final transparent PNG assets in `stickers/`.
- Keep `stickers/` focused on the definitive pack: final PNGs, `manifest.json`, `README.md`, and `contact-sheet.png`.
- Put historical generated attempts, original downloaded stickers, source renders, and reference copies under `archive/`.
- Put reusable prompt guidelines and local skill material under `docs/`.
- Put helper scripts and their dependencies under `tools/`.
- Do not commit generated-image IDs, flattened background exports, checkerboard previews, temporary masks, or source scratch folders.
- Keep `.DS_Store` and other OS metadata ignored.

## Generation Workflow

1. Generate one sticker at a time so filenames can map cleanly to prompts.
2. Preserve the original generated image outside the repo when possible.
3. Copy or export only the intended final asset into `stickers/`.
4. If the generator returns a flattened background, convert only the outside-connected flat background to alpha. Avoid removing white or light interior details inside the mascot.
5. Update `README.md`, `stickers/manifest.json`, and `stickers/contact-sheet.png` when adding, renaming, or removing sticker files.
6. Run a verification pass before committing.

## Verification

Before committing, verify each new PNG:

- It is in `stickers/`.
- It has an alpha channel.
- It is square and consistent with the pack size unless there is a deliberate reason to differ.
- It has no mouth, default pupils, limb joints, accidental text, brand marks, or unwanted background.
- It is visually consistent with the existing T Krobot stickers.

## Git

- Keep commits atomic and stage paths explicitly.
- Use Conventional Commit messages, for example `feat: add tkrobot sticker pack`.
- Push `main` after successful verification when the user asks to publish or update the GitHub repo.
