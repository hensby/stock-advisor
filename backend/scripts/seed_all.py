#!/usr/bin/env python3
"""Seed: init stock universe + fetch OHLCV + compute indicators + composite scores."""

import asyncio, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import yfinance as yf, pandas as pd
from datetime import date
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app.database import AsyncSessionLocal, engine
from app.models import Base, Stock, PriceData, TechnicalIndicator, CompositeScore
from app.services.technical_service import compute_indicators
from app.services.scoring_service import compute_composite_score

TICKERS = ["AAPL","MSFT","GOOGL","AMZN","NVDA","META","TSLA","BRK-B","JPM","JNJ","V","PG","UNH","HD","MA","BAC","XOM","DIS","ADBE","CRM","NFLX","CSCO","PEP","KO","MRK","TMO","WMT","ABT","CVX","PFE","COST","WFC","MS","ABBV","BMY","AMD","ORCL","NKE","PM","QCOM","TXN","UNP","NEE","LOW","AMGN","HON","UPS","RTX","CAT","INTC"]
MAX = int(os.environ.get("SEED_COUNT", "10"))


def flat_columns(df: pd.DataFrame) -> pd.DataFrame:
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(1)
    df.columns = [str(c).lower() for c in df.columns]
    return df


async def init_db():
    async with engine.begin() as c: await c.run_sync(Base.metadata.create_all)
    print("✓ Tables created")


async def seed(db, tks):
    n = 0
    for t in tks:
        if (await db.execute(select(Stock).where(Stock.ticker == t))).scalar_one_or_none(): continue
        try:
            i = yf.Ticker(t).info
            s = Stock(ticker=t, name=i.get("longName",t), sector=i.get("sector"), industry=i.get("industry"),
                      market_cap=i.get("marketCap"), exchange=i.get("exchange","NASDAQ"))
        except Exception:
            s = Stock(ticker=t, name=t)
        db.add(s); n += 1
    await db.commit()
    print(f"✓ Stocks: {n} seeded")


async def fetch(db, ticker):
    r = await db.execute(select(Stock).where(Stock.ticker == ticker))
    s = r.scalar_one_or_none()
    if not s: return

    # Skip if we already have enough data for this stock
    cnt = await db.execute(select(PriceData).where(PriceData.stock_id == s.id).limit(1))
    if cnt.scalar_one_or_none(): return

    print(f"  Fetching {ticker}...", end=" ")
    try:
        df = yf.download(ticker, period="2y", progress=False)
        if df.empty:
            print("empty"); return
    except Exception as e:
        print(f"fail: {e}"); return

    df = flat_columns(df)
    n = 0
    for ix, row in df.iterrows():
        d = ix.date() if hasattr(ix,'date') else ix
        try:
            db.add(PriceData(stock_id=s.id, date=d,
                open=row.get('open'), high=row.get('high'), low=row.get('low'),
                close=row.get('close'), adjusted_close=row.get('adj_close',row.get('close')),
                volume=row.get('volume')))
            n += 1
        except Exception:
            pass  # skip duplicates

    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        # retry one-by-one
        for ix, row in df.iterrows():
            d = ix.date() if hasattr(ix,'date') else ix
            try:
                db.add(PriceData(stock_id=s.id, date=d,
                    open=row.get('open'), high=row.get('high'), low=row.get('low'),
                    close=row.get('close'), adjusted_close=row.get('adj_close',row.get('close')),
                    volume=row.get('volume')))
                await db.commit()
            except IntegrityError:
                await db.rollback()
        await db.commit()  # final commit for any leftovers

    print(f"{n} prices", end=" ")

    # Indicators
    try:
        ind = compute_indicators(df[['open','high','low','close','volume']].copy())
    except Exception as e:
        print(f"✗ indicators: {e}"); return

    ni = 0
    for ix, row in ind.iterrows():
        if row.isna().all(): continue
        d = ix.date() if hasattr(ix,'date') else ix
        try:
            db.add(TechnicalIndicator(stock_id=s.id, date=d,
                sma_20=row.get('sma_20'),sma_50=row.get('sma_50'),sma_200=row.get('sma_200'),
                ema_12=row.get('ema_12'),ema_26=row.get('ema_26'),
                macd=row.get('macd'),macd_signal=row.get('macd_signal'),macd_histogram=row.get('macd_histogram'),
                adx=row.get('adx'),plus_di=row.get('plus_di'),minus_di=row.get('minus_di'),
                rsi=row.get('rsi'),stochastic_k=row.get('stochastic_k'),stochastic_d=row.get('stochastic_d'),
                cci=row.get('cci'),obv=row.get('obv'),mfi=row.get('mfi'),
                volume_sma_20=row.get('volume_sma_20'),
                bb_upper=row.get('bb_upper'),bb_middle=row.get('bb_middle'),bb_lower=row.get('bb_lower'),
                atr=row.get('atr'),kc_upper=row.get('kc_upper'),kc_lower=row.get('kc_lower')))
            ni += 1
        except Exception:
            pass
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
    print(f"{ni} indicators ✓")


async def score(db):
    r = await db.execute(select(Stock).where(Stock.is_active == True))
    today, n = date.today(), 0
    for s in r.scalars().all():
        if not (await db.execute(select(PriceData).where(PriceData.stock_id == s.id).limit(1))).scalar_one_or_none(): continue
        if (await db.execute(select(CompositeScore).where(CompositeScore.stock_id == s.id, CompositeScore.date == today))).scalar_one_or_none():
            n += 1; continue
        try:
            await compute_composite_score(db, s.id, today); n += 1
        except Exception as e:
            print(f"  ✗ {s.ticker}: {e}")
    print(f"✓ Scores: {n}")


async def main():
    tks = TICKERS[:MAX]
    print(f"\n📊 Seed — {len(tks)} stocks\n")
    await init_db()
    async with AsyncSessionLocal() as db:
        await seed(db, tks)
        for i,t in enumerate(tks,1):
            print(f"[{i}/{len(tks)}]", end=" ")
            await fetch(db, t)
        print()
        await score(db)
    print("\n✅ Done.\n")

if __name__ == "__main__":
    asyncio.run(main())
