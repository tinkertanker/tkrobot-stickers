# Tools

Helper scripts for the definitive sticker pack. Run them from the repo root.

| Script | Purpose |
| --- | --- |
| `scripts/verify_pack.py` | Check manifest ↔ PNG consistency, size, RGBA/alpha, and optional source paths |
| `scripts/make_contact_sheet.py` | Build a labelled contact sheet from a sticker folder |
| `scripts/sync_pack_readme.py` | Regenerate `stickers/README.md` and the root README file list from the manifest |
| `scripts/build_site_manifest.py` | Refresh `site/stickers.json` for the public gallery |

Install Python deps with:

```bash
pip install -r tools/requirements.txt
```

Typical pack update sequence after adding `stickers/<slug>.png` and a manifest entry:

```bash
python3 tools/scripts/make_contact_sheet.py stickers --out stickers/contact-sheet.png
python3 tools/scripts/sync_pack_readme.py
python3 tools/scripts/build_site_manifest.py
python3 tools/scripts/verify_pack.py
```
