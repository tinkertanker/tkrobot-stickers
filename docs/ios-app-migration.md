# TT Stickers iOS app: remaining work

The app and export pipeline now live in this repo under `ios/`. Masters stay in `stickers/` as 1254×1254 transparent PNGs. What is left is renaming the 2021 GitHub repo and getting TT Stickers back on the App Store.

Do not copy the 2021 project into `ios/` and “refresh” it. The rewrite is already the path: reuse identities and the emoji map, not the old Xcode tree.

## Status

| Item | State |
| --- | --- |
| Plan in `docs/ios-app-migration.md` | Done |
| Emoji map at `ios/legacy-emoji-map.json` | Done |
| `tools/scripts/export_chat_pack.py` and `ios/` app | In this repo (same change as this layout) |
| README on the 2021 GitHub repo | Done ([tinkertanker/Tinkertanker-Stickers README](https://github.com/tinkertanker/Tinkertanker-Stickers/blob/main/README.md)) |
| Rename 2021 repo to `tt-stickers-ios-legacy`, then archive | **Outstanding** (GitHub UI; org admin) |
| App Store relist under Apple ID `1551965798` | Outstanding |

## Why this repo owns the app

| Repo | Role |
| --- | --- |
| `tinkertanker/tkrobot-stickers` (this repo) | Source of truth: locked PNGs, catalogue, site, and the iOS consumer |
| `tinkertanker/Tinkertanker-Stickers` (still this name on GitHub) | 2021 TT Stickers app, 21 older poses, last commit 7 Feb 2021, removed from the App Store in June 2024. Should become `tt-stickers-ios-legacy` |

The 2021 app already drifted from the art. Combining the other way around (masters into the Xcode tree) would do that again.

`stickers.tk.sg` is unaffected: the Docker image only copies `stickers/`, `site/`, and `tools/scripts/build_site_manifest.py`.

## Layout

```text
stickers/                 # 1254×1254 RGBA masters + manifest.json
site/                     # stickers.tk.sg
ios/                      # SwiftUI app + Messages sticker extension
  pack-config.json        # WhatsApp pack split + emoji
  legacy-emoji-map.json   # copied from the 2021 wasticker file
  Derived/                # generated 512 WebP/PNG, gitignored
  README.md
tools/scripts/
  export_chat_pack.py     # 1254 PNG → 512 WebP / iMessage assets
docs/ios-app-migration.md # remaining App Store / legacy-repo work
```

Do not commit 512×512 WebP copies or resized PNG duplicates. Generate them in `ios/Derived/` from `stickers/` at export / Xcode build time.

Leave `archive/` for historical art only. Do not vendor the 2021 Xcode tree there.

Agents adding a sticker still only touch `stickers/`, the manifest, and pack scripts, then run `export_chat_pack.py`. They must not invent poses inside `ios/` or resize masters by hand.

## Reuse vs rewrite

Reuse from the 2021 app:

| Identity | Value |
| --- | --- |
| App Store name | TT Stickers |
| Apple ID | `1551965798` |
| Bundle ID | `com.tinkertanker.stickers` |
| Messages extension bundle ID | `com.tinkertanker.stickers.StickerPackExtension` |
| Signing team | `PQ6U5ESLN2` (confirm in App Store Connect before the first archive) |
| WhatsApp pack identifier | `sg.tk.tinkertanker.stickers` |
| Emoji map | `ios/legacy-emoji-map.json` for slugs that still exist |

Rewrite (in tree under `ios/`):

- SwiftUI host app (no storyboards)
- Messages sticker pack extension on a current SDK
- WhatsApp add-to-pack flow from the current [WhatsApp/stickers](https://github.com/WhatsApp/stickers) iOS sample, not the 2021 `WebP.framework` + YYImage tree
- Privacy manifest, privacy nutrition labels, and whatever App Store Connect now requires to restore a removed app

Leave behind: the 21 old PNGs, `tray.png` as a unique asset (derive a 96×96 tray icon from a current sticker), `EXCLUDED_ARCHS = arm64`, and the `sms:` “add to Messages” button.

## Chat pack constraints

WhatsApp still wants:

- 512×512, transparent, WebP, ≤100 KB static
- 96×96 tray icon, ≤50 KB
- 3–30 stickers per pack; static and animated must not mix
- Up to 10 packs in one app, added one pack at a time

This catalogue has **36** stickers, so WhatsApp needs two packs (or a 30-sticker cut). iMessage can take the full set.

Split lives in `ios/pack-config.json` (adjust there, not by hand-resizing PNGs):

- **Pack 1 — T Krobot** (30): crashed, ded, depressed, facepalm, falling, fingerguns, flailing, gasp, greetings, handraise, hands-on-hips, happy, heart, intenseglare, ok, palm-open, pls, point-left, point-right, salute, shock, shrug, snooze, sus, thumbsdown, thumbsup, wrong, yay, running-right, jumping-for-joy
- **Pack 2 — T Krobot extra** (6): failed-sitting, lobster-claws, rubbing-tummy, running-left, sixseven, face

`face` is a portrait crop; keep it on the extra pack or the website only if it reads poorly at 512px.

Carry emoji over where the slug matches `ios/legacy-emoji-map.json`. Assign new emoji for stickers that did not exist in 2021 (`greetings`, `happy`, `sixseven`, and so on). The old file’s `right.png` maps to today’s `ok` only if the art still means “correct”; do not assume that from the filename.

Telegram is out. The 2021 set at [t.me/addstickers/Tinkertanker](https://t.me/addstickers/Tinkertanker) is leftover older poses. Do not republish it. Delete it in Telegram: message [@stickers](https://t.me/stickers), send `/delpack`, choose **TT Stickers**. Only the account that created the pack can do that. The iOS app does not link to Telegram.

## Rename the old repo (still outstanding)

The 2021 README is already on GitHub. Rename and archive are **not** done. The current name still looks like the live sticker project. Do it in the GitHub UI (org admin).

Org precedent: `tinkertanker/binafolio-legacy`.

| | |
| --- | --- |
| Current | [`tinkertanker/Tinkertanker-Stickers`](https://github.com/tinkertanker/Tinkertanker-Stickers) |
| Rename to | `tinkertanker/tt-stickers-ios-legacy` |
| Then | Archive the repository (Settings → Archive) |

`tt-stickers-ios-legacy` is deliberate: `-legacy` matches the org, `ios` stops it being read as the PNG pack, and `tt-stickers` still matches the App Store name. Do not use `Tinkertanker-Stickers-legacy`; that still sounds like the current stickers.

GitHub keeps a redirect from the old URL after a rename. Stars, issues, and clones of `Tinkertanker-Stickers` follow. Local remotes need `git remote set-url`.

The README that is already on the 2021 repo:

```markdown
# TT Stickers iOS app (2021, legacy)

This is the February 2021 TT Stickers iOS app.
It is **not** the current T Krobot sticker pack.

The in-app Telegram button pointed at t.me/addstickers/Tinkertanker. That set is leftover 2021 poses and should be deleted in @stickers (`/delpack`). Do not republish it.

- Current artwork, catalogue, site, and iOS app: https://github.com/tinkertanker/tkrobot-stickers
- Browse / download: https://stickers.tk.sg
- App Store listing (TT Stickers, Apple ID 1551965798) was removed in June 2024

Do not add stickers or ship builds from this repository.
```

Also set the GitHub description to the first sentence above, and add a topic such as `legacy`, if that was not done with the README.

Manual steps that remain:

1. ~~Merge/push the README on `Tinkertanker-Stickers`~~ done
2. Settings → General → Repository name → `tt-stickers-ios-legacy`
3. Confirm the old URL redirects
4. Archive

Do not delete the repo. App Store provenance and the original emoji map should stay cloneable.

## Relist on the App Store

In App Store Connect, restore Apple ID `1551965798` if it is still in a removed state, bump marketing version (1.1 or 2.0), attach a privacy manifest, TestFlight, then submit. Screenshot and description should show the locked v11 art, not the 2021 set.

Confirm the developer team `PQ6U5ESLN2` still belongs to Tinkertanker before the first signed build.

Host app expectations: grid of the current pack, Add to WhatsApp (per pack), short note that iMessage stickers install with the app. Same bundle IDs as the 2021 app so App Store Connect can restore TT Stickers rather than creating a second listing.

## Follow-ups (not blocking relist)

- Delete the live 2021 Telegram set. Message [@stickers](https://t.me/stickers) as the account that created it, send `/delpack`, choose **TT Stickers** (`t.me/addstickers/Tinkertanker`). Do not republish it.
- Mention the iOS app on `stickers.tk.sg` once it is live again
- Point Tapplet and any other consumers at this repo only (they already do)
- Android WhatsApp users need a separate Play Store sticker app (out of scope)

## Out of scope

- Telegram sticker set (the 2021 hosted pack is retired; do not republish)
- Android / Play Store WhatsApp sticker app
- Changing the 1254×1254 master size
- Checkerboard previews or flattened marketing exports in `stickers/`
- Putting Xcode signing secrets in GitHub Actions on this repo until someone is actually shipping from CI

## Done when

- [ ] `Tinkertanker-Stickers` redirects to `tt-stickers-ios-legacy` and that repo is archived with a README pointing here
- [x] `ios/` lives in this repo and builds against derived assets from `stickers/`
- [ ] WhatsApp accepts both packs (size and count limits)
- [ ] Messages extension shows the current pack
- [ ] TT Stickers is back on the App Store under Apple ID `1551965798`
- [x] `AGENTS.md` describes artwork vs `ios/` so pack work and app work cannot be mixed up
