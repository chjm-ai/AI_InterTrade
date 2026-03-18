#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

if [[ -f .env && "${1:-}" != "--force" ]]; then
  echo ".env already exists. Use --force to regenerate."
  exit 0
fi

secret_key_base="$(openssl rand -hex 64)"
pg_password="$(openssl rand -hex 24)"
redis_password="$(openssl rand -hex 24)"

cat > .env <<EOF
SECRET_KEY_BASE=${secret_key_base}
FRONTEND_URL=http://localhost:3000
FORCE_SSL=false
ENABLE_ACCOUNT_SIGNUP=false

REDIS_URL=redis://redis:6379
REDIS_PASSWORD=${redis_password}

POSTGRES_HOST=postgres
POSTGRES_DATABASE=chatwoot
POSTGRES_USERNAME=postgres
POSTGRES_PASSWORD=${pg_password}
RAILS_ENV=production
RAILS_MAX_THREADS=5

MAILER_SENDER_EMAIL=Chatwoot <accounts@example.com>
SMTP_ADDRESS=
SMTP_PORT=1025
SMTP_USERNAME=
SMTP_PASSWORD=
SMTP_AUTHENTICATION=
SMTP_ENABLE_STARTTLS_AUTO=true
SMTP_OPENSSL_VERIFY_MODE=peer

ACTIVE_STORAGE_SERVICE=local
RAILS_LOG_TO_STDOUT=true
LOG_LEVEL=info
EOF

echo ".env generated at $(pwd)/.env"
