from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
from app.database import get_db
from app.services.briefing_service import generate_briefing

router = APIRouter(prefix="/briefing", tags=["briefing"])

@router.get("")
async def get_briefing(target_date: date | None = Query(None, alias="date"), db: AsyncSession = Depends(get_db)):
    if target_date is None:
        target_date = date.today()
    return await generate_briefing(db, target_date)

@router.get("/history")
async def get_briefing_history(from_date: date = Query(alias="from"), to_date: date = Query(alias="to"), db: AsyncSession = Depends(get_db)):
    from sqlalchemy import select, distinct
    from app.models.scoring import CompositeScore
    result = await db.execute(select(distinct(CompositeScore.date)).where(CompositeScore.date >= from_date, CompositeScore.date <= to_date).order_by(CompositeScore.date.desc()))
    return {"dates": [str(r[0]) for r in result.all()]}
