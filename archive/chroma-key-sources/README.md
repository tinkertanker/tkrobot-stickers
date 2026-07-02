# Definitive Chroma-Key Sources

These archived flat green source renders correspond one-to-one with the transparent PNGs in `stickers/`.

Regenerate a transparent sticker with:

```sh
python3 /Users/yingjie/.codex/skills/.system/imagegen/scripts/remove_chroma_key.py \
  --input archive/chroma-key-sources/<slug>.png \
  --out stickers/<slug>.png \
  --auto-key border --soft-matte --transparent-threshold 35 --opaque-threshold 180 --despill --force
```
