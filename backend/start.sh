#!/bin/sh
set -e

# Wait for DB host to be available (simple loop)
if [ -n "$DB_HOST" ]; then
  echo "Waiting for DB host: $DB_HOST..."
  until nc -z "$DB_HOST" 3306 >/dev/null 2>&1; do
    printf '.'
    sleep 1
  done
  echo "\nDB is available"
fi
