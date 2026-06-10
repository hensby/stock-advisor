from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class AnalystRatingOut(BaseModel):
    id: int
    analyst_name: Optional[str] = None
    firm: Optional[str] = None
    date: date
    rating: Optional[str] = None
    rating_prior: Optional[str] = None
    target_price: Optional[float] = None

    model_config = {"from_attributes": True}

class InstitutionalSummary(BaseModel):
    buy_count: int = 0
    hold_count: int = 0
    sell_count: int = 0
    avg_target_price: Optional[float] = None
    upside_pct: Optional[float] = None
    recent_ratings: list[AnalystRatingOut] = []

class InsiderTradeOut(BaseModel):
    insider_name: Optional[str] = None
    title: Optional[str] = None
    transaction_type: Optional[str] = None
    transaction_date: Optional[date] = None
    shares: Optional[int] = None
    value: Optional[int] = None

    model_config = {"from_attributes": True}

class YoutubeVideoOut(BaseModel):
    video_id: str
    channel_name: Optional[str] = None
    channel_subscribers: Optional[int] = None
    title: Optional[str] = None
    published_at: Optional[datetime] = None
    view_count: int = 0
    like_count: int = 0
    finbert_score: Optional[float] = None
    finbert_label: Optional[str] = None

    model_config = {"from_attributes": True}

class YoutubeSummary(BaseModel):
    overall_sentiment: str = "neutral"
    finbert_avg: Optional[float] = None
    video_count: int = 0
    recent_videos: list[YoutubeVideoOut] = []
