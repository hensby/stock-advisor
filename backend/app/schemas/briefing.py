from pydantic import BaseModel
from typing import Optional
from datetime import date
from app.schemas.stock import StockItem

class MarketIndexValue(BaseModel):
    value: Optional[float] = None
    change: Optional[float] = None
    change_pct: Optional[float] = None

class MarketSummary(BaseModel):
    sp500: Optional[MarketIndexValue] = None
    nasdaq: Optional[MarketIndexValue] = None
    dow: Optional[MarketIndexValue] = None
    vix: Optional[MarketIndexValue] = None

class SignalChangeItem(BaseModel):
    ticker: str
    name: Optional[str] = None
    previous_signal: Optional[str] = None
    current_signal: Optional[str] = None
    composite_change: Optional[float] = None
    trigger_reasons: list[str] = []

class SectorSentiment(BaseModel):
    sector: str
    institutional_avg_score: Optional[float] = None
    youtube_avg_score: Optional[float] = None

class BriefingOut(BaseModel):
    date: date
    market_summary: Optional[MarketSummary] = None
    signal_changes: list[SignalChangeItem] = []
    top_picks: list[StockItem] = []
    sector_sentiment: list[SectorSentiment] = []
    risk_reminders: list[str] = []
