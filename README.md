# T Krobot Stickers

Transparent PNG sticker assets for T Krobot, Tinkertanker's robot mascot with glasses.

Browse and download the pack at [stickers.tk.sg](https://stickers.tk.sg).

## Files

All definitive rectangular-finger stickers are in `stickers/` as 1254 x 1254 transparent PNGs.

- `crashed.png`
- `ded.png`
- `depressed.png`
- `facepalm.png`
- `falling.png`
- `fingerguns.png`
- `flailing.png`
- `gasp.png`
- `greetings.png`
- `handraise.png`
- `heart.png`
- `intenseglare.png`
- `ok.png`
- `pls.png`
- `right.png`
- `salute.png`
- `shock.png`
- `shrug.png`
- `sixseven.png`
- `snooze.png`
- `thumbsup.png`
- `wrong.png`
- `yay.png`

## Notes

- `stickers/contact-sheet.png` is the full-pack overview.
- `stickers/manifest.json` maps each final sticker to its source slug and archived source file.
- The working set intentionally keeps the final sticker pack in `stickers/`.
- Historical generated attempts, original downloaded files, source renders, and reference copies live under `archive/`.
- Reusable generation guidance and the local skill live under `docs/`.
- No licence is granted by default; treat these as Tinkertanker mascot assets unless separately approved.

## Website

The static gallery lives in `site/`. It shows each PNG without cropping, supports direct single downloads and separate multi-file downloads, and derives each sticker's updated date from Git history during the container build.

Run `python3 tools/scripts/build_site_manifest.py` to refresh local site metadata. Production releases deploy automatically when a `v*` tag is pushed; `./deploy.sh` can deploy a chosen ref manually with `REF=<tag-or-commit>`.
