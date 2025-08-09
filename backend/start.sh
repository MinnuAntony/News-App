#!/bin/sh
set -e

# Wait for MySQL
until nc -z "$DB_HOST" 3306; do
  echo "Waiting for MySQL at $DB_HOST:3306..."
  sleep 1
done

exec python app.py
