#!/usr/bin/env bash
set -euo pipefail

REMOTE_HOST="${REMOTE_HOST:-tinkertanker@dev.tk.sg}"
REMOTE_PATH="${REMOTE_PATH:-/home/tinkertanker-server/Docker/tkrobot-stickers}"
REPO_URL="${REPO_URL:-git@github.com:tinkertanker/tkrobot-stickers.git}"
REF="${REF:-main}"
SSH_OPTS="${SSH_OPTS:--o BatchMode=yes -o IdentityAgent=none -o IdentitiesOnly=yes}"

ssh ${SSH_OPTS} "${REMOTE_HOST}" "mkdir -p \"$(dirname "${REMOTE_PATH}")\""

ssh ${SSH_OPTS} "${REMOTE_HOST}" "
  set -euo pipefail

  if [ ! -d \"${REMOTE_PATH}/.git\" ]; then
    rm -rf \"${REMOTE_PATH}\"
    git clone \"${REPO_URL}\" \"${REMOTE_PATH}\"
  fi

  cd \"${REMOTE_PATH}\"
  git fetch --prune --tags origin
  git checkout --detach \"${REF}\"

  docker compose up -d --build --remove-orphans
  docker compose ps

  container_id=\"\$(docker compose ps -q stickers)\"
  if [ -z \"\${container_id}\" ]; then
    echo 'Stickers container was not created.' >&2
    exit 1
  fi

  for attempt in 1 2 3 4 5 6; do
    health=\"\$(docker inspect --format '{{if .State.Health}}{{.State.Health.Status}}{{else}}{{.State.Status}}{{end}}' \"\${container_id}\")\"
    if [ \"\${health}\" = 'healthy' ]; then
      break
    fi
    if [ \"\${health}\" = 'unhealthy' ] || [ \"\${health}\" = 'exited' ]; then
      docker compose logs --tail=100 stickers
      exit 1
    fi
    sleep 2
  done

  health=\"\$(docker inspect --format '{{if .State.Health}}{{.State.Health.Status}}{{else}}{{.State.Status}}{{end}}' \"\${container_id}\")\"
  if [ \"\${health}\" != 'healthy' ]; then
    echo \"Stickers container did not become healthy (status: \${health}).\" >&2
    docker compose logs --tail=100 stickers
    exit 1
  fi

  docker compose exec -T stickers \
    wget -q -O /dev/null http://127.0.0.1:8080/healthz
"

curl --fail --silent --show-error --retry 5 --retry-delay 2 \
  https://stickers.tk.sg/healthz

echo "Deployed ${REF} to https://stickers.tk.sg"
