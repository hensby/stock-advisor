# StockAdvisor — US Stock Selection & Trading Advisory Platform

A composite-scoring stock advisory system that aggregates **technical indicators**, **institutional sentiment**, and **YouTube/retail sentiment** into actionable recommendations.

![dashboard preview](https://via.placeholder.com/800x400/1e293b/94a3b8?text=StockAdvisor+Dashboard)

## Features

| Feature | Description |
|---|---|
| Composite Scoring | Technical(40%) + Institutional(30%) + YouTube sentiment(20%) + Fundamentals(10%) |
| 20+ Indicators | SMA/EMA/MACD/RSI/ADX/Bollinger Bands/OBV/MFI/CCI/Keltner |
| Signal Change Detection | Automatic logging when scores cross thresholds, with trigger reasons |
| Strategy Presets | Technical Breakout, Reversal Capture, Value Discovery, Momentum, Smart Money, YouTube Heat |
| Daily Briefing | Top 10 picks + signal changes summary + sector sentiment comparison |
| Watchlist Management | Group-based portfolio tracking with real-time score visibility |
| Live Market Indices | S&P 500 / NASDAQ / DOW / VIX via yfinance |

## Tech Stack

```
Backend         Python 3.12+ / FastAPI / SQLAlchemy 2.0
Frontend        Next.js 16 / TypeScript / Tailwind CSS / shadcn/ui
Database        SQLite (MVP) → PostgreSQL (production)
Data Sources    yfinance / Finnhub / YouTube Data API
Caching         Redis + Celery (scheduled data collection)
AI              FinBERT (ProsusAI/finbert) — sentiment analysis
Charts          Lightweight Charts (TradingView) / Recharts
```

## Quick Start

### Local Development

```bash
# 1. Backend
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# 2. Seed data (first run)
SEED_COUNT=10 python scripts/seed_all.py

# 3. Start backend
uvicorn app.main:app --host 127.0.0.1 --port 8000

# 4. Start frontend (new terminal)
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000`.
API docs: `http://localhost:8000/docs`

### Docker

```bash
docker compose up -d
```

> First run requires seed data: `docker compose exec backend python scripts/seed_all.py`

### Deploy to Mac Mini

Prerequisites: Passwordless SSH to Mac Mini (default `192.168.50.4`), Docker installed.

```bash
./deploy-macmini.sh
```

Access at `http://192.168.50.4:3000`.

## API Reference

| Method | Path | Description |
|---|---|---|
| GET | `/api/v1/stocks` | List stocks (paginated/searchable) |
| GET | `/api/v1/stocks/{ticker}` | Stock detail (score + signals + thesis) |
| GET | `/api/v1/stocks/{ticker}/chart` | OHLCV data with technical indicators |
| GET | `/api/v1/stocks/{ticker}/signals` | Signal change timeline |
| GET | `/api/v1/screener` | Multi-filter stock screener |
| GET | `/api/v1/screener/presets` | 6 strategy presets |
| GET | `/api/v1/briefing` | Daily briefing |
| GET | `/api/v1/watchlist` | Watchlist CRUD |
| POST | `/api/v1/watchlist` | Create watchlist group |
| DELETE | `/api/v1/watchlist/{id}` | Delete group |
| POST | `/api/v1/watchlist/{id}/items` | Add stock |
| DELETE | `/api/v1/watchlist/{id}/items/{ticker}` | Remove stock |
| GET | `/api/v1/settings/scoring-weights` | Scoring weights |
| PUT | `/api/v1/settings/scoring-weights` | Update scoring weights |
| GET | `/api/v1/market/indices` | Market indices |

## Scoring System

```
Composite = Technical×0.40 + Institutional×0.30 + YouTube×0.20 + Fundamentals×0.10

Signal Thresholds:
  80-100  strong_buy
  60-79   buy
  40-59   hold
  20-39   sell
   0-19   strong_sell
```

Weights can be adjusted via `PUT /api/v1/settings/scoring-weights`.

## Project Structure

```
stock-advisor/
├── backend/
│   ├── app/
│   │   ├── api/          # REST API routes (6 modules)
│   │   ├── models/       # SQLAlchemy models (10 tables)
│   │   ├── schemas/      # Pydantic request/response schemas
│   │   ├── services/     # Business logic (scoring/collection/briefing)
│   │   ├── tasks/        # Celery scheduled tasks
│   │   └── utils/        # FinBERT sentiment wrapper
│   └── scripts/seed_all.py
├── frontend/
│   ├── app/              # Next.js pages (7 routes)
│   ├── components/       # React components
│   └── lib/              # API client / types / constants
├── docker-compose.yml
├── deploy-macmini.sh
└── .env.example
```

## Data Pipeline

```
yfinance ──→ PriceData ──→ TechnicalIndicator ──→ CompositeScore
                ↓                                       ↓
            AnalystRating ──→ InstitutionalScore ──→ CompositeScore
                ↓                                       ↓
            YoutubeVideo  ──→ YouTubeScore ──→ CompositeScore ──→ SignalChange
```

## Environment Variables

```bash
# backend/.env — optional, core features work without API keys
FINNHUB_API_KEY=your_key       # analyst ratings, insider trades
YOUTUBE_API_KEY=your_key       # video sentiment analysis

# frontend/.env.local
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

## Roadmap

- [x] Phase 1: API / Data models / Scoring engine
- [x] Phase 2: Frontend dashboard / Screener / Stock detail
- [x] Phase 3: Data pipeline / Celery scheduler
- [x] Phase 4: Briefing / Watchlist / Settings / Loading states
- [x] Phase 5: Docker / Mobile responsive / Polish
- [ ] YouTube Data API integration (requires API key)
- [ ] Finnhub institutional data (requires API key)
- [ ] Full FinBERT model (transformers)
- [ ] User system / email briefing
- [ ] Expand to NASDAQ 100

---

**Disclaimer:** This system provides data analysis for reference only. It does not constitute investment advice. Investing involves risk.
