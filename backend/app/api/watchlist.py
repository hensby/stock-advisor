from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.watchlist import Watchlist, WatchlistItem
from app.models.stock import Stock
from app.schemas.watchlist import WatchlistCreate, WatchlistOut, WatchlistItemAdd
from app.schemas.stock import StockItem

router = APIRouter(prefix="/watchlist", tags=["watchlist"])

@router.get("", response_model=list[WatchlistOut])
async def list_watchlists(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Watchlist))
    watchlists = result.scalars().all()
    out = []
    for wl in watchlists:
        items_result = await db.execute(
            select(WatchlistItem, Stock).join(Stock, WatchlistItem.stock_id == Stock.id)
            .where(WatchlistItem.watchlist_id == wl.id)
        )
        rows = items_result.all()
        stocks = [
            StockItem(ticker=s.ticker, name=s.name, sector=s.sector, market_cap=s.market_cap)
            for _, s in rows
        ]
        out.append(WatchlistOut(id=wl.id, name=wl.name, item_count=len(stocks), stocks=stocks))
    return out

@router.post("", response_model=WatchlistOut, status_code=201)
async def create_watchlist(body: WatchlistCreate, db: AsyncSession = Depends(get_db)):
    wl = Watchlist(name=body.name)
    db.add(wl)
    await db.commit()
    await db.refresh(wl)
    return WatchlistOut(id=wl.id, name=wl.name, item_count=0, stocks=[])

@router.delete("/{watchlist_id}", status_code=204)
async def delete_watchlist(watchlist_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Watchlist).where(Watchlist.id == watchlist_id))
    wl = result.scalar_one_or_none()
    if wl:
        await db.delete(wl)
        await db.commit()

@router.post("/{watchlist_id}/items", status_code=201)
async def add_stock_to_watchlist(watchlist_id: int, body: WatchlistItemAdd, db: AsyncSession = Depends(get_db)):
    stock_result = await db.execute(select(Stock).where(Stock.ticker == body.ticker.upper()))
    stock = stock_result.scalar_one_or_none()
    if not stock:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail=f"股票 {body.ticker} 不存在")
    existing = await db.execute(
        select(WatchlistItem).where(
            WatchlistItem.watchlist_id == watchlist_id,
            WatchlistItem.stock_id == stock.id
        )
    )
    if existing.scalar_one_or_none():
        from fastapi import HTTPException
        raise HTTPException(status_code=409, detail="股票已在自选中")
    item = WatchlistItem(watchlist_id=watchlist_id, stock_id=stock.id)
    db.add(item)
    await db.commit()
    return {"status": "added"}

@router.delete("/{watchlist_id}/items/{ticker}", status_code=204)
async def remove_stock_from_watchlist(watchlist_id: int, ticker: str, db: AsyncSession = Depends(get_db)):
    stock_result = await db.execute(select(Stock).where(Stock.ticker == ticker.upper()))
    stock = stock_result.scalar_one_or_none()
    if not stock:
        return
    item_result = await db.execute(
        select(WatchlistItem).where(
            WatchlistItem.watchlist_id == watchlist_id,
            WatchlistItem.stock_id == stock.id
        )
    )
    item = item_result.scalar_one_or_none()
    if item:
        await db.delete(item)
        await db.commit()
