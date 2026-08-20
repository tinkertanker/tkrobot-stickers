# Tools

Helper scripts for the definitive sticker pack. Run them from the repo root.

| Script | Purpose |
| --- | --- |
| `scripts/verify_pack.py` | Check manifest schema, pack contents, PNG transparency, and source-path existence (`--strict-sources` makes missing sources errors) |
| `scripts/make_contact_sheet.py` | Build a labelled contact sheet from a sticker folder |
| `scripts/sync_pack_readme.py` | Regenerate `stickers/README.md` from the manifest (root README points at the catalogue; it is not a second file list) |
| `scripts/build_site_manifest.py` | Refresh `site/stickers.json` for the public gallery |
| `scripts/export_chat_pack.py` | Resize locked 1254×1254 PNGs into gitignored 512×512 WhatsApp WebP / iMessage PNG derivatives under `ios/Derived/` |

Install Python deps with:

```bash
pip install -r tools/requirements.txt
```

Typical pack update sequence after adding `stickers/<slug>.png`, a manifest entry, and the slug in `ios/pack-config.json`:

```bash
python3 tools/scripts/make_contact_sheet.py stickers --out stickers/contact-sheet.png
python3 tools/scripts/sync_pack_readme.py
python3 tools/scripts/build_site_manifest.py
python3 tools/scripts/verify_pack.py
```

Chat-sized WhatsApp / iMessage derivatives go in gitignored `ios/Derived/` (not required for pack verification):

```bash
python3 tools/scripts/export_chat_pack.py
```
