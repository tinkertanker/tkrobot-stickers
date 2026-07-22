# T Krobot Stickers

Transparent PNG sticker assets for T Krobot, Tinkertanker's robot mascot with glasses.

Browse and download the pack at [stickers.tk.sg](https://stickers.tk.sg).

**Agents:** start at `AGENTS.md`. The definitive pack is `stickers/`; the catalogue is `stickers/manifest.json`.

## Files

All definitive rectangular-finger stickers are in `stickers/` as 1254 x 1254 transparent PNGs.
The authoritative catalogue is `stickers/manifest.json`; do not maintain a second handwritten inventory.

## Notes

- `stickers/contact-sheet.png` is the full-pack overview.
- `stickers/manifest.json` maps each sticker to its description, tags, and source path.
- `docs/references/hand-size-anchor.png` is the locked hand/finger scale for new generations.
- Historical generated attempts, original downloads, and reference copies live under `archive/` — ignore them unless a manifest `source_path` points there.
- Reusable generation guidance and the local skill live under `docs/`.
- Helper scripts (`verify_pack`, contact sheet, README sync, site manifest) live under `tools/scripts/`.
- No licence is granted by default; treat these as Tinkertanker mascot assets unless separately approved.

## Website

The static gallery lives in `site/`. It shows each PNG without cropping, supports direct single downloads and separate multi-file downloads, and derives each sticker's updated date from Git history during the container build.

Run `python3 tools/scripts/build_site_manifest.py` to refresh local site metadata. Production releases deploy automatically when a `v*` tag is pushed; `./deploy.sh` can deploy a chosen ref manually with `REF=<tag-or-commit>`.
