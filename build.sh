#!/usr/bin/env bash
set -o errexit

echo "=== Installing dependencies ==="
pip install -r requirements.txt

echo "=== Preparing static directories ==="
mkdir -p core/static/core/css
mkdir -p core/static/core/js

echo "=== Collecting static files ==="
python manage.py collectstatic --no-input --clear

echo "=== Running migrations ==="
python manage.py migrate --no-input

echo "=== Seeding data ==="
python manage.py create_superuser

echo "=== Build complete ==="
