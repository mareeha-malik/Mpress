#!/usr/bin/env bash
# start.sh - entrypoint for hosting platforms (Railway/Railpack, Heroku-style)
# It expects $PORT to be set by the platform; default to 8000 locally.
set -euo pipefail

PORT=${PORT:-8000}

# Collect static files (optional; uncomment if configured)
# echo "Collecting static files..."
# python manage.py collectstatic --noinput

echo "Starting Gunicorn on port ${PORT}"
exec gunicorn mpress.wsgi:application \
  --bind 0.0.0.0:${PORT} \
  --workers 3 \
  --log-level info
