#!/bin/sh
set -e

# 如果数据库不存在或为空则自动种子
if [ ! -f /app/data/stock_advisor.db ] || [ "$(stat -f%z /app/data/stock_advisor.db 2>/dev/null)" -lt 1024 ]; then
    echo "📊 首次启动 — 种子数据初始化..."
    python /app/scripts/seed_all.py
fi

exec "$@"
