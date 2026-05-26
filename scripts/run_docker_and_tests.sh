#!/usr/bin/env bash
set -euo pipefail

# Helper script to start Docker Compose, run migrations, and run tests against Postgres.
# Usage: ./scripts/run_docker_and_tests.sh

if ! command -v docker >/dev/null 2>&1; then
  echo "Error: 'docker' is not installed or not in PATH. Please install Docker and Docker Compose."
  echo "See: https://docs.docker.com/get-docker/"
  exit 2
fi

echo "Starting Docker Compose services..."
docker compose up --build -d

echo "Waiting 3 seconds for Postgres to initialize..."
sleep 3

echo "Running migrations against Postgres..."
./scripts/migrate_postgres.sh

echo "Running Django test suite against Postgres..."
python manage.py test

echo "Tests finished. To view logs: docker compose logs -f"
