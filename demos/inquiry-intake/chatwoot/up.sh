#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

export NO_PROXY="${NO_PROXY:-127.0.0.1,localhost}"
export no_proxy="${no_proxy:-127.0.0.1,localhost}"

if ! command -v docker >/dev/null 2>&1; then
  echo "docker is not installed or not in PATH"
  exit 1
fi

if command -v docker-compose >/dev/null 2>&1; then
  compose_cmd=(docker-compose)
elif docker compose version >/dev/null 2>&1; then
  compose_cmd=(docker compose)
else
  echo "docker compose is not available"
  exit 1
fi

if [[ ! -f .env ]]; then
  echo ".env is missing. Run ./prepare-env.sh first."
  exit 1
fi

if command -v colima >/dev/null 2>&1; then
  if ! colima status >/dev/null 2>&1; then
    echo "starting colima..."
    colima start --cpu 4 --memory 8 --disk 60
  fi
fi

echo "starting containers..."
"${compose_cmd[@]}" -f docker-compose.local.yml up -d

echo "preparing database..."
"${compose_cmd[@]}" -f docker-compose.local.yml run --rm rails bundle exec rails db:chatwoot_prepare

echo "Chatwoot should be available at http://127.0.0.1:3000"
