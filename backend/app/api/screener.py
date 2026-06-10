from fastapi import APIRouter, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, func
from datetime import date
from app.database import get_db
from app.models.stock import Stock, PriceData
from app.models.scoring import CompositeScore
from app.schemas.stock import StockItem, PaginatedResponse

router = APIRouter(prefix="/screener", tags=["screener"])

PRESETS = [
    {"id": "technical_breakout", "name": "技术面突破", "description": "金叉+量增+机构上调", "icon": "trending-up", "match_count": 0, "query_params": {"min_technical_score": 70, "min_institutional_score": 60}},
    {"id": "reversal_capture", "name": "趋势反转捕捉", "description": "RSI超卖+机构逆势看好", "icon": "refresh-cw", "match_count": 0, "query_params": {"min_institutional_score": 60}},
    {"id": "value_discovery", "name": "价值发现", "description": "低PE+回购增加", "icon": "search", "match_count": 0, "query_params": {}},
    {"id": "momentum_continuation", "name": "动量延续", "description": "ADX>25趋势强+RSI不极端", "icon": "zap", "match_count": 0, "query_params": {"min_technical_score": 60}},
    {"id": "smart_money", "name": "跟随聪明钱", "description": "内部人大举买入+13F增持", "icon": "landmark", "match_count": 0, "query_params": {"min_institutional_score": 70}},
    {"id": "youtube_heat", "name": "YouTube热度", "description": "YT一致看多+播放量激增", "icon": "video", "match_count": 0, "query_params": {"min_youtube_score": 70}},
]

@router.get("", response_model=PaginatedResponse)
async def screener(
    page: int = Query(1, ge=1), page_size: int = Query(50, ge=1, le=100),
    sector: str | None = Query(None), min_market_cap: int | None = Query(None),
    min_composite: float | None = Query(None),
    min_technical_score: float | None = Query(None),
    min_institutional_score: float | None = Query(None),
    min_youtube_score: float | None = Query(None),
    sort: str = Query("composite_score"), order: str = Query("desc"),
    db: AsyncSession = Depends(get_db),
):
    today = date.today()
    ls = (select(CompositeScore.stock_id, CompositeScore.composite_score, CompositeScore.signal, CompositeScore.technical_score, CompositeScore.institutional_score, CompositeScore.youtube_score)
          .where(CompositeScore.date == today).subquery())
    sp = (select(PriceData.stock_id, PriceData.close, PriceData.volume).where(PriceData.date == today).subquery())
    query = select(Stock, ls, sp.c.close, sp.c.volume).outerjoin(ls, Stock.id == ls.c.stock_id).outerjoin(sp, Stock.id == sp.c.stock_id).where(Stock.is_active == True)
    if sector: query = query.where(Stock.sector == sector)
    if min_market_cap: query = query.where(Stock.market_cap >= min_market_cap)
    if min_composite is not None: query = query.where(ls.c.composite_score >= min_composite)
    if min_technical_score is not None: query = query.where(ls.c.technical_score >= min_technical_score)
    if min_institutional_score is not None: query = query.where(ls.c.institutional_score >= min_institutional_score)
    if min_youtube_score is not None: query = query.where(ls.c.youtube_score >= min_youtube_score)

    sort_map = {"ticker": Stock.ticker, "composite_score": ls.c.composite_score, "technical_score": ls.c.technical_score, "institutional_score": ls.c.institutional_score, "youtube_score": ls.c.youtube_score}
    sort_col = sort_map.get(sort, ls.c.composite_score)
    query = query.order_by(desc(sort_col) if order == "desc" else sort_col)

    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)
    result = await db.execute(query)
    rows = result.all()

    items = [StockItem(ticker=s.ticker, name=s.name, sector=s.sector, market_cap=s.market_cap, composite_score=ls_data.composite_score, signal=ls_data.signal, price=price, volume=vol)
             for s, ls_data, price, vol in rows if ls_data is not None]

    return PaginatedResponse(items=items, total=total, page=page, page_size=page_size)

@router.get("/presets")
async def get_presets():
    return PRESETS
