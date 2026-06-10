from pydantic import BaseModel
from typing import Optional
from datetime import date

class ScoreBreakdown(BaseModel):
    technical_score: Optional[float] = None
    institutional_score: Optional[float] = None
    youtube_score: Optional[float] = None
    fundamental_score: Optional[float] = None
    composite_score: Optional[float] = None
    signal: Optional[str] = None

    model_config = {"from_attributes": True}

class SignalChangeOut(BaseModel):
    id: int
    stock_id: int
    date: date
    previous_signal: Optional[str] = None
    current_signal: Optional[str] = None
    composite_change: Optional[float] = None
    trigger_reasons: list[str] = []

    model_config = {"from_attributes": True}

class ScoringWeights(BaseModel):
    technical: float = 0.40
    institutional: float = 0.30
    youtube: float = 0.20
    fundamental: float = 0.10
