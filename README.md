# T Krobot Stickers

Transparent PNG sticker assets for T Krobot, Tinkertanker's robot mascot with glasses, and the TT Stickers iOS app that ships them.

Browse and download the pack at [stickers.tk.sg](https://stickers.tk.sg).

**Agents:** start at `AGENTS.md`.

## Files

- `stickers/`: definitive 1254×1254 transparent PNG masters, with `manifest.json` as the authoritative catalogue (descriptions, tags, provenance) and `contact-sheet.png` as the visual overview.
- `docs/`: generation guidance and skills; `references/hand-size-anchor.png` locks hand/finger scale.
- `tools/scripts/`: pack verification, contact sheet, README sync, site manifest, and chat export helpers.
- `archive/`: historical attempts and references; consult when a manifest `source_path` points there.

No licence is granted by default; treat these as Tinkertanker mascot assets unless separately approved.

## iOS app

See `ios/README.md` for TT Stickers (iMessage + WhatsApp) Xcode setup and bundle IDs, and `docs/ios-app-migration.md` for remaining App Store and legacy-repo work.

After changing the pack, generate 512 WebP/PNG chat assets in gitignored `ios/Derived/`:

```sh
python3 tools/scripts/export_chat_pack.py
```

## Website

The gallery in `site/` uses Cloudflare Workers Static Assets: Worker `tkrobot-stickers`, **Tinkertanker** account (`b8b1032c61d9475cd00229c74db7ec72`), serving `stickers.tk.sg` and `tkrobot-stickers.tinkertanker.workers.dev`. It offers uncropped previews, single and multi-file downloads, and update dates from Git history.

Use Node.js 22+ and Python 3 with a full Git checkout (`git fetch --unshallow` if needed):

```sh
npm ci
npm run build
# With CLOUDFLARE_API_TOKEN supplied securely:
npm run deploy
```

The build refreshes `site/stickers.json` and stages only the public site and pack in gitignored `dist/`, excluding iOS assets, archives, and credentials. PNGs use immutable caching; site files revalidate. `/healthz` returns `ok`.

The release workflow deploys on `v*` tags or manual dispatch. Set the repository Actions secret `CLOUDFLARE_API_TOKEN` with Tinkertanker account permissions **Workers Scripts Edit** and **Account Settings Read**, plus **tk.sg Zone Read** and **DNS Edit** for custom domains. Orb credentials do not carry over to GitHub Actions.
