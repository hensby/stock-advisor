# StockAdvisor — 美股选股与交易建议平台

将**技术面指标**、**机构情绪**、**YouTube/KOL 散户情绪**聚合为统一评分的美股选股建议系统。

![dashboard preview](https://via.placeholder.com/800x400/1e293b/94a3b8?text=StockAdvisor+Dashboard)

## 核心功能

| 功能 | 说明 |
|---|---|
| 综合评分引擎 | 技术面(40%) + 机构情绪(30%) + YouTube情绪(20%) + 基本面(10%) |
| 20+ 技术指标 | SMA/EMA/MACD/RSI/ADX/布林带/OBV/MFI/CCI/Keltner |
| 信号变化检测 | 当评分跨越阈值时自动记录信号变化及触发原因 |
| 选股策略预设 | 技术面突破、趋势反转、价值发现、动量延续、聪明钱、YouTube热度 |
| 每日简报 | 每日盘后生成 Top 10 优选 + 信号变化汇总 + 行业情绪对比 |
| 自选股管理 | 分组管理自选股，快速查看持仓评分状态 |
| 真实市场指数 | S&P 500 / NASDAQ / DOW / VIX 实时行情 |

## 技术栈

```
Backend         Python 3.12+ / FastAPI / SQLAlchemy 2.0
Frontend        Next.js 16 / TypeScript / Tailwind CSS / shadcn/ui
Database        SQLite (MVP) → PostgreSQL (生产)
Data Sources    yfinance / Finnhub / YouTube Data API
Caching         Redis + Celery (定时数据采集)
AI              FinBERT (ProsusAI/finbert) — 情绪分析
Charts          Lightweight Charts (TradingView) / Recharts
```

## 快速开始

### 本地开发

```bash
# 1. 后端
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# 2. 种子数据 (首次运行)
SEED_COUNT=10 python scripts/seed_all.py

# 3. 启动后端
uvicorn app.main:app --host 127.0.0.1 --port 8000

# 4. 启动前端 (新终端)
cd frontend
npm install
npm run dev
```

访问 `http://localhost:3000` 查看仪表盘。
API 文档：`http://localhost:8000/docs`

### Docker 一键启动

```bash
docker compose up -d
```

访问 `http://localhost:3000`。

> 首次运行需先执行种子数据脚本：`docker compose exec backend python scripts/seed_all.py`

## API 概览

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/api/v1/stocks` | 股票列表 (分页/搜索/排序) |
| GET | `/api/v1/stocks/{ticker}` | 个股详情 (评分+信号+逻辑) |
| GET | `/api/v1/stocks/{ticker}/chart` | K线数据 |
| GET | `/api/v1/stocks/{ticker}/signals` | 信号变化时间线 |
| GET | `/api/v1/screener` | 多条件筛选器 |
| GET | `/api/v1/screener/presets` | 6 个策略预设 |
| GET | `/api/v1/briefing` | 每日简报 |
| GET | `/api/v1/watchlist` | 自选股 CRUD |
| POST | `/api/v1/watchlist` | 创建自选分组 |
| DELETE | `/api/v1/watchlist/{id}` | 删除分组 |
| POST | `/api/v1/watchlist/{id}/items` | 添加股票 |
| DELETE | `/api/v1/watchlist/{id}/items/{ticker}` | 移除股票 |
| GET | `/api/v1/settings/scoring-weights` | 评分权重 |
| PUT | `/api/v1/settings/scoring-weights` | 修改评分权重 |
| GET | `/api/v1/market/indices` | 大盘指数 |

## 评分体系

```
综合评分 = 技术面×0.40 + 机构情绪×0.30 + YouTube情绪×0.20 + 基本面×0.10

信号分级:
  80-100  strong_buy (强烈买入)
  60-79   buy (买入)
  40-59   hold (持有)
  20-39   sell (卖出)
   0-19   strong_sell (强烈卖出)
```

权重可通过 `PUT /api/v1/settings/scoring-weights` 调整。

## 项目结构

```
stock-advisor/
├── backend/
│   ├── app/
│   │   ├── api/          # REST API 路由 (6 个模块)
│   │   ├── models/       # SQLAlchemy 数据模型 (10 张表)
│   │   ├── schemas/      # Pydantic 请求/响应 Schema
│   │   ├── services/     # 业务逻辑层 (评分引擎/数据采集/简报)
│   │   ├── tasks/        # Celery 定时任务
│   │   └── utils/        # FinBERT 情绪分析封装
│   └── scripts/seed_all.py   # 种子数据脚本
├── frontend/
│   ├── app/              # Next.js 页面 (7 个路由)
│   ├── components/       # React 组件 (layout/dashboard/screener/stock-detail/...)
│   └── lib/              # API 客户端 / 类型定义 / 常量
└── docker-compose.yml    # Docker 编排
```

## 数据流

```
yfinance ──→ PriceData ──→ TechnicalIndicator ──→ CompositeScore
                ↓                                       ↓
            AnalystRating ──→ InstitutionalScore ──→ CompositeScore
                ↓                                       ↓
            YoutubeVideo ──→ YouTubeScore ──→ CompositeScore ──→ SignalChange
```

## 路线图

- [x] Phase 1: API / 数据模型 / 评分引擎
- [x] Phase 2: 前端仪表盘 / 筛选器 / 个股详情
- [x] Phase 3: 数据管道 / Celery 定时任务
- [x] Phase 4: 简报 / 自选 / 设置 / 骨架屏
- [x] Phase 5: Docker / 移动端响应 / 最终打磨
- [ ] YouTube Data API 集成 (需 API Key)
- [ ] Finnhub 机构数据集成 (需 API Key)
- [ ] FinBERT 真实模型加载 (transformers)
- [ ] 用户系统 / 邮箱简报通知
- [ ] 扩展至纳斯达克 100

## 环境变量

```bash
# backend/.env
DATABASE_URL=sqlite+aiosqlite:///./data/stock_advisor.db
FINNHUB_API_KEY=your_key       # 可选
YOUTUBE_API_KEY=your_key       # 可选

# frontend/.env.local
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

---

**免责声明:** 本系统仅提供数据分析供参考，不构成投资建议。投资有风险，入市需谨慎。

---

## 部署到 Mac Mini

项目附带 `deploy-macmini.sh` 一键部署脚本，通过 SSH 将 Docker 镜像传输到 Mac Mini 并启动。

### 前置条件

- Mac Mini 已安装 Docker
- 本机能 SSH 免密登录 Mac Mini
- 网络互通 (默认 IP: `192.168.50.4`)

### 部署

```bash
# 一键构建 + 传输 + 启动
./deploy-macmini.sh

# 指定分支
./deploy-macmini.sh develop
```

### 手动部署

```bash
# 1. 构建
docker compose build

# 2. 传输 (或直接 ssh 到 Mac Mini 上 git pull)
scp docker-compose.yml miniuser@192.168.50.4:~/stock-advisor/

# 3. 在 Mac Mini 上
ssh miniuser@192.168.50.4
cd ~/stock-advisor
docker compose up -d
```

访问 `http://192.168.50.4:3000`。
