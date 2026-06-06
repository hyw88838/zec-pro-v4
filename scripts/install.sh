#!/usr/bin/env bash
set -e
cd "$(dirname "$0")/.."
apt update -y
apt install -y docker.io docker-compose-v2 git curl unzip
systemctl enable docker || true
systemctl start docker || true
[ -f .env ] || cp .env.example .env
docker compose up -d --build
echo "ZEC-PRO V4 已启动：http://服务器IP:8000"
