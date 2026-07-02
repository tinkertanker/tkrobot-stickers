# Definitive Chroma-Key Sources

These flat green source renders correspond one-to-one with the transparent PNGs in `stickers/`.

Regenerate a transparent sticker with:

```sh
python3 /Users/yingjie/.codex/skills/.system/imagegen/scripts/remove_chroma_key.py \
  --input sources/chroma-key/<slug>.png \
  --out stickers/<slug>.png \
  --auto-key border --soft-matte --transparent-threshold 35 --opaque-threshold 180 --despill --force
```

