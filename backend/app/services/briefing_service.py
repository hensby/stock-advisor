from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, func
from app.models.scoring import CompositeScore, SignalChange
from app.models.stock import Stock
from app.schemas.briefing import BriefingOut, SignalChangeItem, SectorSentiment
from app.schemas.stock import StockItem, PaginatedResponse
import json


async def generate_briefing(db: AsyncSession, target_date: date) -> BriefingOut:
    """生成每日简报"""

    # Top 10 综合评分
    result = await db.execute(
        select(CompositeScore, Stock).join(Stock, CompositeScore.stock_id == Stock.id)
        .where(CompositeScore.date == target_date)
        .order_by(desc(CompositeScore.composite_score))
        .limit(10)
    )
    rows = result.all()

    top_picks = []
    for cs, s in rows:
        top_picks.append(StockItem(
            ticker=s.ticker, name=s.name, sector=s.sector,
            market_cap=s.market_cap, composite_score=cs.composite_score,
            signal=cs.signal
        ))

    # 信号变化
    sc_result = await db.execute(
        select(SignalChange, Stock).join(Stock, SignalChange.stock_id == Stock.id)
        .where(SignalChange.date == target_date)
        .order_by(desc(SignalChange.composite_change))
        .limit(10)
    )
    sc_rows = sc_result.all()

    signal_changes = []
    for sc, s in sc_rows:
        reasons = []
        try:
            reasons = json.loads(sc.trigger_reasons) if sc.trigger_reasons else []
        except json.JSONDecodeError:
            pass

        signal_changes.append(SignalChangeItem(
            ticker=s.ticker, name=s.name,
            previous_signal=sc.previous_signal, current_signal=sc.current_signal,
            composite_change=sc.composite_change, trigger_reasons=reasons[:5]
        ))

    # 行业情绪
    sector_result = await db.execute(
        select(Stock.sector, func.avg(CompositeScore.institutional_score), func.avg(CompositeScore.youtube_score))
        .join(Stock, CompositeScore.stock_id == Stock.id)
        .where(CompositeScore.date == target_date, Stock.sector.isnot(None))
        .group_by(Stock.sector)
    )
    sectors = sector_result.all()
    sector_sentiment = [
        SectorSentiment(sector=s[0] or "Unknown", institutional_avg_score=s[1], youtube_avg_score=s[2])
        for s in sectors
    ]

    return BriefingOut(
        date=target_date,
        signal_changes=signal_changes,
        top_picks=top_picks,
        sector_sentiment=sector_sentiment,
        risk_reminders=["⚠️ 市场有风险，本建议仅供参考，不构成投资建议。"]
    )
