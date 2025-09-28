#!/usr/bin/env bash
set -euo pipefail

if [[ -d ".venv" ]]; then
  source .venv/bin/activate
fi

# Запуск uvicorn
uvicorn app.main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --log-level info
