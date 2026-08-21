# AGENTS.md

## Start here

This repository stores **T Krobot** artwork and the chat apps that ship it. The locked pack is transparent PNG masters in `stickers/`. The TT Stickers iOS app in `ios/` is the consumer.

When asked to add a sticker, touch only `stickers/`, the manifest, and pack scripts, then run `export_chat_pack.py`. Do not invent poses inside `ios/` or resize masters by hand. `stickers/` remains 1254×1254 transparent PNG only; chat-sized files are generated.

The current TT Stickers app is `ios/`. The 2021 Xcode repo should be renamed `tt-stickers-ios-legacy`; that rename and archive are still outstanding. See `docs/ios-app-migration.md`.

Do **not** add unrelated brand assets, slide decks, checkerboard previews, or loose generated scratch files.

### Where things live

| Path | Use it for |
| --- | --- |
| `stickers/` | **Definitive pack only**: 1254×1254 transparent PNGs, `manifest.json`, `README.md`, `contact-sheet.png` |
| `stickers/manifest.json` | Authoritative catalogue: slug, description, tags, file path, source path |
| `stickers/contact-sheet.png` | Visual overview of the locked pack |
| `ios/` | SwiftUI host app and Messages sticker extension |
| `ios/pack-config.json` | WhatsApp pack split and emoji for `export_chat_pack.py` |
| `ios/Derived/` | Generated 512 WebP/PNG chat assets. Gitignored; do not commit or edit by hand |
| `docs/references/hand-size-anchor.png` | Locked hand/finger scale reference |
| `docs/prompts/tkrobot-sticker-guidelines.md` | Prompt skeleton + pose notes for generation |
| `docs/skills/tkrobot-sticker-generation/` | Local generation skill (style guide + prompt) |
| `docs/skills/tkrobot-illustrations/` | Body-illustration skill: 16:9 white-bg hand-drawn explainer images with sketch-mode T Krobot (adapted from ian-xiaohei-illustrations, MIT) |
| `docs/ios-app-migration.md` | Remaining App Store relist and 2021-repo rename/archive checklist |
| `tools/scripts/` | Pack helpers: verify, contact sheet, site manifest, README sync, `export_chat_pack.py` |
| `archive/` | Historical sources and rejected iterations — **not** the working pack |
| `site/` | Public gallery for stickers.tk.sg |

### Agent quick map

1. **Find existing stickers** → `stickers/` and `stickers/manifest.json` (filter by `tags` / `description`).
2. **See the whole pack** → `stickers/contact-sheet.png`.
3. **Match style before generating** → `docs/skills/tkrobot-sticker-generation/references/style-guide.md` and `docs/prompts/tkrobot-sticker-guidelines.md`.
3b. **Article/tutorial body illustrations** (not stickers) → `docs/skills/tkrobot-illustrations/SKILL.md`. Attach the character and hand lock sheets on every generation call. Hands are a black palm blob with three grey rectangular tabs plus a thumb: **open, point, thumbs-up (palm-closed), or closed at rest** — no gripping. When choosing a look, run the same prompt on Grok and a GPT image model. Reject gloves, five digits, and all-black Xiaohei stick figures.
4. **Match hand size** → `docs/references/hand-size-anchor.png`.
5. **Ignore by default** → almost everything under `archive/generated-iterations/` except when a manifest `source_path` or note points there.

## Sticker style (invariants)

- T Krobot is a simple black robot mascot with large white glasses, softened trapezoid head and body, smooth light grey `#e1e1e1` limbs and fingers, black palm blobs, oversized black oval feet, and a flat red diamond chest mark.
- Locked v11 proportions: moderately slim limbs, no neck, head top about 90% as wide as the bottom, thin light grey shine line under the head.
- Preserve the glasses' locked wide round proportions independently of the head taper. Frames may extend beyond the head sides; do not shrink or compress them to fit.
- Hands must have exactly **three fingers plus one thumb**. Do not generate four fingers plus one thumb.
- Hand-size anchor: `docs/references/hand-size-anchor.png` (copy of the locked v1-size blocky-fingers sheet). Keep the large palm/finger scale with flatter rectangular-tab fingers. Do not shrink toward the smaller v2 rectangular batch.
- Fingers are large flat rectangular tabs with hard sides and flat or slightly rounded corners, not soft sausage-like tubes.
- No mouth.
- No pupils by default. Special eye marks only when they define the concept (happy upside-down-U, snooze lightning, glare slits, knocked-out X marks).
- No joints, segmented limb rings, elbow/knee marks, bend lines, or black interior lines on arms and legs.
- Keep motion marks sparse and readable at sticker size.

Full detail: `docs/skills/tkrobot-sticker-generation/references/style-guide.md`.

## File rules

- Put final transparent PNG assets in `stickers/` only. Masters stay 1254×1254 RGBA.
- Keep `stickers/` focused on the definitive pack: final PNGs, `manifest.json`, `README.md`, and `contact-sheet.png`.
- Record provenance in `stickers/manifest.json` (`source_path`, notes, tags, description).
- Do not invent poses inside `ios/` or resize masters by hand. Chat-sized derivatives belong in `ios/Derived/` and must be generated by `export_chat_pack.py`.
- Put historical attempts, scrape originals, and reference copies under `archive/`.
- Put reusable prompt guidelines and skill material under `docs/`.
- Put helper scripts under `tools/`.
- Do not commit generated-image IDs, flattened background exports, checkerboard previews, temporary masks, or source scratch folders.
- Keep `.DS_Store` and other OS metadata ignored.

## Adding a sticker

1. Choose a kebab-case slug that is not already in `stickers/manifest.json`.
2. Read the style guide and prompt guidelines under `docs/`.
3. Generate **one** sticker at a time on a flat `#00ff00` chroma-key background when you need local background removal.
4. Export a square **1254×1254** transparent RGBA PNG to `stickers/<slug>.png`.
5. Record a non-empty `source_path` in the manifest; preserve that source under `archive/…` when useful.
6. Append a manifest item with `slug`, `filename`, `sticker_path`, `source_path`, `description`, and `tags`.
7. Add the slug to `ios/pack-config.json`: emoji list, and exactly one WhatsApp pack (`extra` if `T Krobot` is already at 30 stickers).
8. Refresh derived files:
   - `python3 tools/scripts/make_contact_sheet.py stickers --out stickers/contact-sheet.png`
   - `python3 tools/scripts/sync_pack_readme.py`
   - `python3 tools/scripts/build_site_manifest.py`
9. Verify: `python3 tools/scripts/verify_pack.py`
10. Export chat assets: `python3 tools/scripts/export_chat_pack.py`
11. Commit only the touched paths with a Conventional Commit message.

## Verification checklist

Before committing a new or replaced PNG:

- [ ] File is in `stickers/<slug>.png`
- [ ] Listed in `stickers/manifest.json` with description and tags
- [ ] Has an alpha channel and is 1254×1254
- [ ] No mouth, default pupils, limb joints, accidental text, brand marks, or leftover background
- [ ] Visually consistent with `stickers/contact-sheet.png`
- [ ] Listed in `ios/pack-config.json` (emoji + one WhatsApp pack)
- [ ] `python3 tools/scripts/verify_pack.py` passes
- [ ] `python3 tools/scripts/export_chat_pack.py` succeeds

## Git

- Keep commits atomic and stage paths explicitly.
- Use Conventional Commit messages, for example `feat: add tkrobot sticker pack`.
- Push `main` only when the user asks to publish or update the GitHub repo.
