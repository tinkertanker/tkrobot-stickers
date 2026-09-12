# T Krobot Stickers

Transparent PNG sticker assets for T Krobot, Tinkertanker's robot mascot with glasses, and the TT Stickers iOS app that ships them.

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
- Helper scripts (`verify_pack`, contact sheet, README sync, site manifest, chat export) live under `tools/scripts/`.
- No licence is granted by default; treat these as Tinkertanker mascot assets unless separately approved.

## iOS app

The TT Stickers iOS app (iMessage + WhatsApp) lives in `ios/`. Open `ios/README.md` for Xcode setup and bundle IDs.

Chat-sized assets are generated, not committed. After changing the pack, run:

```sh
python3 tools/scripts/export_chat_pack.py
```

That writes 512 WebP/PNG files into `ios/Derived/` from the 1254×1254 masters. Remaining App Store and 2021-repo work is listed in `docs/ios-app-migration.md`.

## Website

The static gallery lives in `site/` and is hosted on Cloudflare Workers Static Assets in the **Tinkertanker** account (`b8b1032c61d9475cd00229c74db7ec72`). Worker `tkrobot-stickers` serves `stickers.tk.sg` and `tkrobot-stickers.tinkertanker.workers.dev`. It shows each PNG without cropping, supports direct single downloads and separate multi-file downloads, and derives each sticker's updated date from Git history during the build.

Use Node.js 22+ and Python 3 with a full Git checkout (`git fetch --unshallow` if needed):

```sh
npm ci
npm run build
# With CLOUDFLARE_API_TOKEN supplied securely:
npm run deploy
```

The build refreshes `site/stickers.json` and stages only the public site and pack in ignored `dist/`. No iOS assets, archives, or credentials are uploaded. PNGs retain immutable caching; site files revalidate. `/healthz` returns `ok`.

The Cloudflare release workflow deploys on `v*` tags or manual dispatch. Before enabling it, configure the repository Actions secret `CLOUDFLARE_API_TOKEN` with access to the Tinkertanker account (Workers Scripts Edit and Account Settings Read, plus tk.sg Zone Read and DNS Edit for custom-domain management). The migration's orb credential is not automatically available to GitHub Actions.

### Docker fallback and rollback

The legacy Docker deployment on `dev.tk.sg` was disabled on 12 September 2026 after verifying Cloudflare production. Container `tkrobot-stickers-stickers-1` was stopped with restart policy `no`. Its checkout and a checksummed image export are preserved at `/home/tinkertanker-server/disabled-deployments/tkrobot-stickers-20260912T0630Z`; `RUNBOOK.txt` there contains exact restore commands. The archived Dockerfile and Compose file have `.disabled` suffixes. A root-owned immutable tombstone at the original `/home/tinkertanker-server/Docker/tkrobot-stickers` path blocks the old SSH workflow from redeploying there.

`deploy.sh`, `Dockerfile`, `docker-compose.yml`, and `nginx.conf` in this repository are historical fallback tooling, not the Cloudflare deploy path. Do not run the old deployment script without deliberately restoring the legacy service. The server's existing weekly Docker prune may remove the stopped container/image; the independent image export preserves recovery without relying on them.

To roll back, first restore Docker using the archived runbook, then verify the old origin with `curl --resolve stickers.tk.sg:443:66.96.215.10 https://stickers.tk.sg/healthz`. Only after origin verification, detach `stickers.tk.sg` from this Worker's custom domains and remove its Worker-managed DNS record if still present. With no explicit record, the unchanged `*.tk.sg` CNAME to `office.tk.sg` resolves to the old server again. Verify DNS, HTTPS, gallery metadata, and a PNG after caches expire. Do not change the wildcard. A subsequent Cloudflare deployment will reattach the custom domain specified in `wrangler.jsonc`.
