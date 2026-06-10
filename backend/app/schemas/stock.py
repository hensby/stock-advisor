from datetime import datetime, date
from pydantic import BaseModel
from typing import Optional
from app.schemas.scoring import ScoreBreakdown

class StockItem(BaseModel):
    ticker: str
    name: str
    sector: Optional[str] = None
    market_cap: Optional[int] = None
    composite_score: Optional[float] = None
    signal: Optional[str] = None
    price: Optional[float] = None
    change: Optional[float] = None
    change_pct: Optional[float] = None
    volume: Optional[int] = None

    model_config = {"from_attributes": True}

class TechnicalSignal(BaseModel):
    indicator: str
    signal: str  # bullish, bearish, neutral
    value: Optional[float] = None
    description: str

class StockDetail(BaseModel):
    ticker: str
    name: str
    sector: Optional[str] = None
    industry: Optional[str] = None
    market_cap: Optional[int] = None
    exchange: Optional[str] = None
    price: Optional[float] = None
    change: Optional[float] = None
    change_pct: Optional[float] = None
    previous_close: Optional[float] = None
    day_range: Optional[str] = None
    week52_range: Optional[str] = None
    avg_volume: Optional[int] = None
    composite_score: Optional[float] = None
    signal: Optional[str] = None
    scores: Optional[ScoreBreakdown] = None
    technical_signals: list[TechnicalSignal] = []
    investment_thesis: Optional[str] = None
    bull_reasons: list[str] = []
    bear_reasons: list[str] = []

    model_config = {"from_attributes": True}

class ChartCandle(BaseModel):
    date: date
    open: Optional[float] = None
    high: Optional[float] = None
    low: Optional[float] = None
    close: Optional[float] = None
    volume: Optional[int] = None
    sma_20: Optional[float] = None
    sma_50: Optional[float] = None
    sma_200: Optional[float] = None
    bb_upper: Optional[float] = None
    bb_middle: Optional[float] = None
    bb_lower: Optional[float] = None
    macd: Optional[float] = None
    macd_signal: Optional[float] = None
    rsi: Optional[float] = None

class ChartData(BaseModel):
    ticker: str
    data: list[ChartCandle]

class SignalEvent(BaseModel):
    date: date
    signal: Optional[str] = None
    composite_score: Optional[float] = None
    trigger_reasons: list[str] = []

class PaginatedResponse(BaseModel):
    items: list
    total: int
    page: int
    page_size: int
