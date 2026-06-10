from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models import Base
from app.database import engine
from app.api.stocks import router as stocks_router
from app.api.screener import router as screener_router
from app.api.briefing import router as briefing_router
from app.api.watchlist import router as watchlist_router
from app.api.settings import router as settings_router
from app.api.market import router as market_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="Stock Advisor API", version="0.1.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

api_prefix = "/api/v1"
app.include_router(stocks_router, prefix=api_prefix)
app.include_router(screener_router, prefix=api_prefix)
app.include_router(briefing_router, prefix=api_prefix)
app.include_router(watchlist_router, prefix=api_prefix)
app.include_router(settings_router, prefix=api_prefix)
app.include_router(market_router, prefix=api_prefix)

@app.get("/health")
async def health():
    return {"status": "ok"}
