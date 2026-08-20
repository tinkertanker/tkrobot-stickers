# TT Stickers (iOS)

SwiftUI host app and Messages sticker extension for the locked T Krobot pack. Masters stay in `stickers/` (1254×1254). This project never bundles those masters; Xcode exports 512px chat assets at build time.

App Store name: **TT Stickers**
Apple ID (listing to restore): `1551965798`

## How to open and ship

1. From the repo root, generate derived chat assets (optional locally; Xcode also runs this):

   ```bash
   python3 tools/scripts/export_chat_pack.py
   ```

   Needs Python 3 and Pillow with WebP (`pip install -r tools/requirements.txt`). The Xcode Run Script phase runs the same command, so that install must be on the Mac that builds the app.

2. On a Mac, open `ios/TTStickers.xcodeproj`.

3. Confirm signing:

   - Team: `PQ6U5ESLN2`
   - App bundle ID: `com.tinkertanker.stickers`
   - Messages extension bundle ID: `com.tinkertanker.stickers.StickerPackExtension`

4. Restore the App Store listing for Apple ID `1551965798` in App Store Connect, then archive and submit marketing version **2.0** (current project version **9**).

## Derived files are gitignored

`ios/Derived/` is produced by `tools/scripts/export_chat_pack.py` and is **not** committed.

| Output | Use |
| --- | --- |
| `ios/Derived/whatsapp/<pack-id>/*.webp` plus `tray.png` | Copied into the app as `WhatsAppStickers/` |
| `ios/Derived/imessage/*.png` | Copied into the app as `PreviewStickers/` and into the Messages extension as `Stickers/` |

The host app Run Script phase runs `python3 tools/scripts/export_chat_pack.py` from the repo root, then copies those folders and `ios/pack-config.json` into the built products. The extension target runs the same export and copies the iMessage PNGs.

## App icon

The asset catalogue has a placeholder iOS universal 1024 slot and no artwork. In Xcode, set the App Icon from `stickers/greetings.png` (or a dedicated 1024×1024 marketing crop) before shipping.

## Layout

```
ios/
  pack-config.json          # WhatsApp pack split + emoji (committed)
  legacy-emoji-map.json     # 2021 emoji map (committed; not bundled)
  Derived/                  # gitignored export output
  App/                      # SwiftUI host app
  StickerPackExtension/     # MSStickerBrowserViewController
  TTStickers.xcodeproj/
```

Do not copy the 2021 `WebP.framework` / YYImage tree. WhatsApp send uses the current pasteboard JSON (`net.whatsapp.third-party.sticker-pack` → `whatsapp://stickerPack`) and the pre-exported WebP files.
