# TT Stickers iOS app: migrate into this repo

Move the chat sticker app into `tinkertanker/tkrobot-stickers`, keep `stickers/` as the master artwork, and relabel the 2021 Xcode repo so it is no longer mistaken for the current pack.

This is the working plan. Do not copy the 2021 project into `ios/` and “refresh” it. Rewrite the app; reuse identities and the emoji map.

## Why this repo owns the move

| Repo | Role after migration |
| --- | --- |
| `tinkertanker/tkrobot-stickers` (this repo) | Source of truth: locked PNGs, catalogue, site, **and** the iOS consumer |
| `tinkertanker/Tinkertanker-Stickers` (today) | 2021 TT Stickers app, 21 older poses, last commit 7 Feb 2021, removed from the App Store in June 2024 |

The 2021 app already drifted from the art. Combining the other way around (masters into the Xcode tree) would do that again.

`stickers.tk.sg` is unaffected: the Docker image only copies `stickers/`, `site/`, and `tools/scripts/build_site_manifest.py`.

## Target layout

```text
stickers/                 # unchanged 1254×1254 RGBA masters + manifest.json
site/                     # stickers.tk.sg
ios/                      # new SwiftUI app + Messages sticker extension
  TTStickers.xcodeproj
  App/
  StickerPackExtension/
  README.md
tools/scripts/            # existing pack tools + chat export
  export_chat_pack.py     # 1254 PNG → 512 WebP / iMessage assets (derived, not committed)
docs/ios-app-migration.md # this plan
```

Do not commit 512×512 WebP copies or resized PNG duplicates. Generate them in `ios/Derived/` (gitignored) from `stickers/` at export / Xcode build time.

Leave `archive/` for historical art only. Do not vendor the 2021 Xcode tree there.

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
| Telegram set | [t.me/addstickers/Tinkertanker](https://t.me/addstickers/Tinkertanker) |
| Emoji map | `TT Stickers/sticker_packs.wasticker` for slugs that still exist |

Rewrite:

- SwiftUI host app (drop storyboards)
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

Suggested first split (adjust when building `export_chat_pack.py`):

- **Pack 1 — T Krobot** (30): crashed, ded, depressed, facepalm, falling, fingerguns, flailing, gasp, greetings, handraise, hands-on-hips, happy, heart, intenseglare, ok, palm-open, pls, point-left, point-right, salute, shock, shrug, snooze, sus, thumbsdown, thumbsup, wrong, yay, running-right, jumping-for-joy
- **Pack 2 — T Krobot extra** (6): failed-sitting, lobster-claws, rubbing-tummy, running-left, sixseven, face

`face` is a portrait crop; keep it on the extra pack or the website only if it reads poorly at 512px.

Carry emoji over where the slug matches the 2021 `wasticker` file. Assign new emoji for stickers that did not exist then (`greetings`, `happy`, `sixseven`, and so on). The old file’s `right.png` maps to today’s `ok` only if the art still means “correct”; do not assume that from the filename.

Telegram is a hosted set, not something the iOS binary ships. Treat a Telegram refresh as a follow-up (Bot API upload of the same 512 WebP files). Until then, the app can keep linking the existing set.

## Rename the old repo

Do this as soon as this plan is accepted, **before** anyone writes the new app. The current name looks like the live sticker project.

Org precedent: `tinkertanker/binafolio-legacy`.

| | |
| --- | --- |
| Current | [`tinkertanker/Tinkertanker-Stickers`](https://github.com/tinkertanker/Tinkertanker-Stickers) |
| Rename to | `tinkertanker/tt-stickers-ios-legacy` |
| Then | Archive the repository (Settings → Archive) |

`tt-stickers-ios-legacy` is deliberate: `-legacy` matches the org, `ios` stops it being read as the PNG pack, and `tt-stickers` still matches the App Store name. Do not use `Tinkertanker-Stickers-legacy`; that still sounds like the current stickers.

GitHub keeps a redirect from the old URL after a rename. Stars, issues, and clones of `Tinkertanker-Stickers` follow. Local remotes need `git remote set-url`.

### Old-repo README (commit this *before* renaming)

Replace the empty/missing README with:

```markdown
# TT Stickers iOS app (2021, legacy)

This is the February 2021 TT Stickers iOS app (iMessage + WhatsApp + Telegram).
It is **not** the current T Krobot sticker pack.

- Current artwork, catalogue, and site: https://github.com/tinkertanker/tkrobot-stickers
- Browse / download: https://stickers.tk.sg
- App Store listing (TT Stickers, Apple ID 1551965798) was removed in June 2024

Do not add stickers or ship builds from this repository.
```

Also set the GitHub description to the first sentence above, and add a topic such as `legacy`.

Manual steps (org admin, GitHub UI or `gh repo rename`):

1. Merge/push the README on `Tinkertanker-Stickers`
2. Settings → General → Repository name → `tt-stickers-ios-legacy`
3. Confirm the old URL redirects
4. Archive

Do not delete the repo. App Store provenance and the emoji map should stay cloneable.

## Charter changes in this repo (when `ios/` lands)

Update `AGENTS.md` so it is no longer “PNG files only”:

- This repo holds the definitive T Krobot **artwork** and the **chat apps that ship it**
- Agents that are asked to add a sticker still only touch `stickers/`, the manifest, and pack scripts, then run `export_chat_pack.py` if `ios/` exists
- Agents must not invent poses inside `ios/` or resize masters by hand
- `stickers/` remains 1254×1254 transparent PNG only; chat-sized derivatives stay generated

Add `ios/` to the “Where things live” table. Ignore `ios/Derived/`, `xcuserdata`, and `.DS_Store` (already ignored).

## Phased work

### 0. Land this plan

This document, plus a `docs/README.md` link. No app code yet.

### 1. Relabel the 2021 repo

README, rename to `tt-stickers-ios-legacy`, archive. Copy `sticker_packs.wasticker` into this repo as `ios/legacy-emoji-map.json` (or under `docs/`) so the mapping survives without cloning the legacy tree. Do not copy PNGs or Xcode.

### 2. Export pipeline

`tools/scripts/export_chat_pack.py`:

- Read `stickers/manifest.json`
- Write 512×512 WebP (and a 96×96 tray icon) into `ios/Derived/`
- Fail the build if any static sticker exceeds 100 KB or the tray exceeds 50 KB
- Emit a WhatsApp pack JSON (two packs) and an iMessage asset list
- Optionally extend the manifest later with `emojis` and `whatsapp_pack`; until then keep the split in the export script or a small `ios/pack-config.json`

Wire `verify_pack.py` so a full pack check still passes without Xcode. Chat export can be a second command.

### 3. New iOS app

New Xcode project under `ios/`, current iOS deployment target (not 12.1):

- Host app: grid of the current pack, Add to WhatsApp (per pack), Add to Telegram (link), short note that iMessage stickers install with the app
- Messages sticker pack extension using the derived assets
- Same bundle IDs as the 2021 app so App Store Connect can restore TT Stickers rather than creating a second listing

### 4. Relist

In App Store Connect, restore Apple ID `1551965798` if it is still in a removed state, bump marketing version (1.1 or 2.0), attach a privacy manifest, TestFlight, then submit. Screenshot and description should show the locked v11 art, not the 2021 set.

Confirm the developer team `PQ6U5ESLN2` still belongs to Tinkertanker before the first signed build.

### 5. Follow-ups (not blocking relist)

- Upload the same 512 WebP files to Telegram so the hosted set matches the site
- Mention the iOS app on `stickers.tk.sg` once it is live again
- Point Tapplet and any other consumers at this repo only (they already do)

## Out of scope

- Android / Play Store WhatsApp sticker app
- Changing the 1254×1254 master size
- Checkerboard previews or flattened marketing exports in `stickers/`
- Putting Xcode signing secrets in GitHub Actions on this repo until someone is actually shipping from CI

## Done when

- [ ] `Tinkertanker-Stickers` redirects to `tt-stickers-ios-legacy` and that repo is archived with a README pointing here
- [ ] `ios/` builds against derived assets from `stickers/`
- [ ] WhatsApp accepts both packs (size and count limits)
- [ ] Messages extension shows the current pack
- [ ] TT Stickers is back on the App Store under Apple ID `1551965798`
- [ ] `AGENTS.md` describes artwork vs `ios/` so pack work and app work cannot be mixed up
