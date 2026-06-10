from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, func, or_
from datetime import date, timedelta
from app.database import get_db
from app.models.stock import Stock, PriceData
from app.models.scoring import CompositeScore, SignalChange
from app.models.technical import TechnicalIndicator
from app.schemas.stock import StockItem, StockDetail, ChartData, ChartCandle, SignalEvent, PaginatedResponse, TechnicalSignal
from app.schemas.scoring import ScoreBreakdown
from app.services.technical_service import generate_technical_signals
from app.services.scoring_service import compute_composite_score
import json

router = APIRouter(prefix="/stocks", tags=["stocks"])


@router.get("", response_model=PaginatedResponse)
async def list_stocks(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    sector: str | None = Query(None),
    search: str | None = Query(None),
    sort: str = Query("ticker"),
    order: str = Query("asc"),
    db: AsyncSession = Depends(get_db),
):
    today = date.today()

    latest_score = (
        select(CompositeScore.stock_id, CompositeScore.composite_score, CompositeScore.signal)
        .where(CompositeScore.date == today)
        .subquery()
    )

    latest_price = (
        select(PriceData.stock_id, PriceData.close, PriceData.volume)
        .where(PriceData.date == today)
        .subquery()
    )

    query = select(
        Stock, latest_score.c.composite_score, latest_score.c.signal,
        latest_price.c.close, latest_price.c.volume
    ).outerjoin(latest_score, Stock.id == latest_score.c.stock_id) \
     .outerjoin(latest_price, Stock.id == latest_price.c.stock_id) \
     .where(Stock.is_active == True)

    if sector:
        query = query.where(Stock.sector == sector)
    if search:
        query = query.where(or_(Stock.ticker.ilike(f"%{search}%"), Stock.name.ilike(f"%{search}%")))

    sort_map = {
        "ticker": Stock.ticker, "name": Stock.name,
        "composite_score": latest_score.c.composite_score,
    }
    sort_col = sort_map.get(sort, Stock.ticker)
    query = query.order_by(desc(sort_col) if order == "desc" else sort_col)

    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0

    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)
    result = await db.execute(query)
    rows = result.all()

    items = []
    for row in rows:
        s, cs, sig, price, vol = row
        items.append(StockItem(
            ticker=s.ticker, name=s.name, sector=s.sector,
            market_cap=s.market_cap, composite_score=cs, signal=sig,
            price=price, volume=vol,
        ))

    return PaginatedResponse(items=items, total=total, page=page, page_size=page_size)


@router.get("/{ticker}", response_model=StockDetail)
async def get_stock_detail(ticker: str, db: AsyncSession = Depends(get_db)):
    today = date.today()

    stmt = select(Stock).where(Stock.ticker == ticker.upper())
    result = await db.execute(stmt)
    stock = result.scalar_one_or_none()
    if not stock:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail=f"股票 {ticker} 不存在")

    price_result = await db.execute(
        select(PriceData).where(PriceData.stock_id == stock.id)
        .order_by(PriceData.date.desc()).limit(2)
    )
    prices = price_result.scalars().all()
    current = prices[0] if prices else None
    prev_price = prices[1] if len(prices) > 1 else None

    price = current.close if current else None
    prev_close = prev_price.close if prev_price else None
    change = round(price - prev_close, 2) if price and prev_close else None
    change_pct = round((price - prev_close) / prev_close * 100, 2) if price and prev_close and prev_close > 0 else None

    score_result = await db.execute(
        select(CompositeScore).where(CompositeScore.stock_id == stock.id, CompositeScore.date == today)
    )
    score = score_result.scalar_one_or_none()
    if not score:
        score = await compute_composite_score(db, stock.id, today)

    scores = ScoreBreakdown(
        technical_score=score.technical_score, institutional_score=score.institutional_score,
        youtube_score=score.youtube_score, fundamental_score=score.fundamental_score,
        composite_score=score.composite_score, signal=score.signal,
    ) if score else None

    tech_result = await db.execute(
        select(TechnicalIndicator).where(TechnicalIndicator.stock_id == stock.id)
        .order_by(TechnicalIndicator.date.desc()).limit(1)
    )
    tech = tech_result.scalar_one_or_none()
    raw_signals = generate_technical_signals(tech.__dict__ if tech else None)
    technical_signals = [
        TechnicalSignal(indicator=s["indicator"], signal=s["signal"], value=s.get("value"), description=s["description"])
        for s in raw_signals
    ]

    bull_reasons, bear_reasons = [], []
    high_score = score.composite_score is not None and score.composite_score >= 60 if score else False
    if score and score.technical_score and score.technical_score >= 60:
        bull_reasons.append("技术面信号偏多")
    if score and score.institutional_score and score.institutional_score >= 60:
        bull_reasons.append("机构情绪积极")
    if score and score.youtube_score and score.youtube_score >= 60:
        bull_reasons.append("YouTube/散户情绪偏多")
    if score and score.composite_score and score.composite_score < 40:
        bear_reasons.append("综合评分较低，需谨慎")
    if tech and tech.rsi and tech.rsi > 70:
        bear_reasons.append(f"RSI={tech.rsi:.1f}，处于超买区域")
    if price and tech and tech.sma_200 and price < tech.sma_200:
        bear_reasons.append("价格低于200日均线")

    thesis = None
    if score and score.signal:
        signal_text = {"strong_buy": "强烈买入", "buy": "买入", "hold": "持有", "sell": "卖出", "strong_sell": "强烈卖出"}.get(score.signal, "")
        thesis = f"综合评分{score.composite_score:.0f}分，建议{signal_text}。" + (" 技术面和机构情绪共振看多。" if high_score else "")

    return StockDetail(
        ticker=stock.ticker, name=stock.name, sector=stock.sector, industry=stock.industry,
        market_cap=stock.market_cap, exchange=stock.exchange,
        price=price, change=change, change_pct=change_pct,
        previous_close=prev_close,
        composite_score=score.composite_score if score else None,
        signal=score.signal if score else None,
        scores=scores,
        technical_signals=technical_signals,
        investment_thesis=thesis,
        bull_reasons=bull_reasons,
        bear_reasons=bear_reasons,
    )


@router.get("/{ticker}/chart", response_model=ChartData)
async def get_stock_chart(
    ticker: str,
    range: str = Query("1y"),
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Stock).where(Stock.ticker == ticker.upper())
    result = await db.execute(stmt)
    stock = result.scalar_one_or_none()
    if not stock:
        from fastapi import HTTPException
        raise HTTPException(status_code=404)

    days_map = {"1m": 30, "3m": 90, "6m": 180, "1y": 365, "all": 730}
    days = days_map.get(range, 365)
    since = date.today() - timedelta(days=days)

    price_result = await db.execute(
        select(PriceData).where(PriceData.stock_id == stock.id, PriceData.date >= since)
        .order_by(PriceData.date)
    )
    prices = price_result.scalars().all()

    tech_result = await db.execute(
        select(TechnicalIndicator).where(TechnicalIndicator.stock_id == stock.id, TechnicalIndicator.date >= since)
        .order_by(TechnicalIndicator.date)
    )
    techs = {t.date: t for t in tech_result.scalars().all()}

    data = []
    for p in prices:
        t = techs.get(p.date)
        data.append(ChartCandle(
            date=p.date, open=p.open, high=p.high, low=p.low, close=p.close, volume=p.volume,
            sma_20=t.sma_20 if t else None, sma_50=t.sma_50 if t else None, sma_200=t.sma_200 if t else None,
            bb_upper=t.bb_upper if t else None, bb_middle=t.bb_middle if t else None, bb_lower=t.bb_lower if t else None,
            macd=t.macd if t else None, macd_signal=t.macd_signal if t else None, rsi=t.rsi if t else None,
        ))

    return ChartData(ticker=ticker, data=data)


@router.get("/{ticker}/signals")
async def get_signal_timeline(ticker: str, db: AsyncSession = Depends(get_db)):
    stmt = select(Stock).where(Stock.ticker == ticker.upper())
    result = await db.execute(stmt)
    stock = result.scalar_one_or_none()
    if not stock:
        from fastapi import HTTPException
        raise HTTPException(status_code=404)

    sc_result = await db.execute(
        select(SignalChange).where(SignalChange.stock_id == stock.id)
        .order_by(desc(SignalChange.date)).limit(30)
    )
    changes = sc_result.scalars().all()

    history = []
    for sc in changes:
        reasons = []
        try:
            reasons = json.loads(sc.trigger_reasons) if sc.trigger_reasons else []
        except json.JSONDecodeError:
            pass
        history.append(SignalEvent(date=sc.date, signal=sc.current_signal, trigger_reasons=reasons))

    return {"history": history}
