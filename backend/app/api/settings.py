from fastapi import APIRouter
from pydantic import BaseModel
from app.schemas.scoring import ScoringWeights

router = APIRouter(prefix="/settings", tags=["settings"])

_current_weights = ScoringWeights()

class WeightsUpdate(BaseModel):
    technical: float = 0.40
    institutional: float = 0.30
    youtube: float = 0.20
    fundamental: float = 0.10

@router.get("/scoring-weights", response_model=ScoringWeights)
async def get_scoring_weights():
    return _current_weights

@router.put("/scoring-weights", response_model=ScoringWeights)
async def update_scoring_weights(weights: WeightsUpdate):
    total = weights.technical + weights.institutional + weights.youtube + weights.fundamental
    if abs(total - 1.0) > 0.001:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail=f"权重之和必须为 1.0，当前为 {total}")
    global _current_weights
    _current_weights = ScoringWeights(**weights.model_dump())
    return _current_weights
