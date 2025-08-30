#!/bin/sh
set -e

if [ "${RUN_MIGRATIONS:-true}" = "true" ]; then
  echo "Running Alembic migrations..."
  alembic upgrade head
fi

WORKERS=${WORKERS:-2}
APP_IMPORT="${APP_NAME:-app.main:app}"
BIND_HOST="${HOST:-0.0.0.0}"
BIND_PORT="${PORT:-8000}"

exec uvicorn "${APP_IMPORT}" --host "${BIND_HOST}" --port "${BIND_PORT}" --no-access-log