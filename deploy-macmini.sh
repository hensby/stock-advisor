#!/bin/bash
# StockAdvisor — Mac Mini 部署脚本
# 用法: ./deploy-macmini.sh [branch]

set -e

BRANCH="${1:-main}"
REMOTE_DIR="~/stock-advisor"
MACMINI="192.168.50.4"
COMPOSE_FILE="docker-compose.yml"

echo "=============================="
echo " StockAdvisor — Mac Mini 部署"
echo "=============================="

# 1) 确保本地有最新代码
echo ""
echo "📦 构建 Docker 镜像..."
docker compose -f "$COMPOSE_FILE" build
echo "   ✓ 镜像构建完成"

# 2) 保存镜像为 tar 文件
echo ""
echo "💾 导出镜像..."
docker save stock-backend:latest -o /tmp/stock-backend.tar 2>/dev/null || true
docker save stock-frontend:latest -o /tmp/stock-frontend.tar 2>/dev/null || true
echo "   ✓ 镜像已导出"

# 3) 复制到 Mac Mini
echo ""
echo "🔗 传输到 Mac Mini ($MACMINI)..."
ssh "hengchaowang@$MACMINI" "mkdir -p $REMOTE_DIR/data"
scp docker-compose.yml "hengchaowang@$MACMINI:$REMOTE_DIR/"
scp .env.example "hengchaowang@$MACMINI:$REMOTE_DIR/.env"
scp /tmp/stock-backend.tar "hengchaowang@$MACMINI:$REMOTE_DIR/" 2>/dev/null || true
scp /tmp/stock-frontend.tar "hengchaowang@$MACMINI:$REMOTE_DIR/" 2>/dev/null || true
echo "   ✓ 传输完成"

# 4) Mac Mini 上加载并启动
echo ""
echo "🚀 在 Mac Mini 上启动..."
ssh "hengchaowang@$MACMINI" "
  cd $REMOTE_DIR
  docker load -i stock-backend.tar 2>/dev/null || true
  docker load -i stock-frontend.tar 2>/dev/null || true
  docker compose up -d
  echo '  ✓ 已启动'
  docker compose ps
"

echo ""
echo "=============================="
echo " ✅ 部署完成!"
echo "  http://$MACMINI:3000 (前端)"
echo "  http://$MACMINI:8000/docs (API)"
echo "=============================="
