#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."
git pull || true
[ -f .env ] || cp .env.example .env
docker compose up -d --build
docker compose ps
