# Tools

Helper scripts for the definitive sticker pack. Run them from the repo root.

| Script | Purpose |
| --- | --- |
| `scripts/verify_pack.py` | Check manifest schema, pack directory contents, PNG size/RGBA/transparency, and optional source paths |
| `scripts/make_contact_sheet.py` | Build a labelled contact sheet from a sticker folder |
| `scripts/sync_pack_readme.py` | Regenerate `stickers/README.md` from the manifest (root README points at the catalogue; it is not a second file list) |
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
