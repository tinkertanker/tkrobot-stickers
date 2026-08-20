#!/usr/bin/env bash
# Export chat-sized stickers and copy them into the built app / Messages extension.
set -euo pipefail

if [[ -z "${SRCROOT:-}" || -z "${BUILT_PRODUCTS_DIR:-}" || -z "${UNLOCALIZED_RESOURCES_FOLDER_PATH:-}" ]]; then
  echo "error: this script must run from an Xcode build phase" >&2
  exit 1
fi

REPO_ROOT="$(cd "${SRCROOT}/.." && pwd)"
cd "${REPO_ROOT}"

if ! command -v python3 >/dev/null 2>&1; then
  echo "error: python3 is required to export chat stickers" >&2
  exit 1
fi

python3 tools/scripts/export_chat_pack.py

WHATSAPP_SRC="${SRCROOT}/Derived/whatsapp"
IMESSAGE_SRC="${SRCROOT}/Derived/imessage"

if [[ ! -d "${WHATSAPP_SRC}" || ! -d "${IMESSAGE_SRC}" ]]; then
  echo "error: expected ios/Derived/whatsapp and ios/Derived/imessage after export" >&2
  exit 1
fi

DEST="${BUILT_PRODUCTS_DIR}/${UNLOCALIZED_RESOURCES_FOLDER_PATH}"
mkdir -p "${DEST}"

copy_tree() {
  local src="$1"
  local dest="$2"
  mkdir -p "${dest}"
  if command -v rsync >/dev/null 2>&1; then
    rsync -a --delete "${src}/" "${dest}/"
  else
    rm -rf "${dest}"
    mkdir -p "${dest}"
    cp -R "${src}/." "${dest}/"
  fi
}

case "${TARGET_NAME}" in
  TTStickers)
    cp "${SRCROOT}/pack-config.json" "${DEST}/pack-config.json"
    copy_tree "${WHATSAPP_SRC}" "${DEST}/WhatsAppStickers"
    copy_tree "${IMESSAGE_SRC}" "${DEST}/PreviewStickers"
    ;;
  StickerPackExtension)
    copy_tree "${IMESSAGE_SRC}" "${DEST}/Stickers"
    ;;
  *)
    echo "error: unknown TARGET_NAME '${TARGET_NAME:-}'" >&2
    exit 1
    ;;
esac
