import yfinance as yf
from sqlalchemy.exc import IntegrityError
import pandas as pd
import numpy as np
import asyncio
from datetime import date, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.stock import Stock, PriceData
from app.models.technical import TechnicalIndicator
from app.services.technical_service import compute_indicators

SP500_TICKERS = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "BRK-B", "JPM", "JNJ",
    "V", "PG", "UNH", "HD", "MA", "BAC", "XOM", "DIS", "ADBE", "CRM",
    "NFLX", "CSCO", "PEP", "KO", "MRK", "TMO", "WMT", "ABT", "CVX", "PFE",
    "COST", "WFC", "MS", "ABBV", "BMY", "AMD", "ORCL", "NKE", "PM", "QCOM",
    "TXN", "UNP", "NEE", "LOW", "AMGN", "HON", "UPS", "RTX", "CAT", "INTC"
]


def _yf_to_flat_df(ticker: str, df: pd.DataFrame) -> pd.DataFrame:
    """将 yfinance 的 MultiIndex 列扁平化。"""
    if isinstance(df.columns, pd.MultiIndex):
        cols = {}
        for col in df.columns:
            field = col[0].lower().replace(' ', '_')
            sym = col[1]
            if sym == ticker:
                cols[col] = field
        return df.rename(columns=cols)
    df.columns = [c.lower().replace(' ', '_') for c in df.columns]
    return df


async def seed_sp500(db: AsyncSession, limit: int = 50):
    """种子 S&P 500 成分股。"""
    added = 0
    tickers = SP500_TICKERS[:limit]
    for ticker in tickers:
        stmt = select(Stock).where(Stock.ticker == ticker)
        result = await db.execute(stmt)
        if result.scalar_one_or_none() is not None:
            continue
        try:
            t = yf.Ticker(ticker)
            info = t.info
            stock = Stock(
                ticker=ticker,
                name=info.get("longName", info.get("shortName", ticker)),
                sector=info.get("sector"),
                industry=info.get("industry"),
                market_cap=info.get("marketCap"),
                exchange=info.get("exchange", "NASDAQ"),
            )
            db.add(stock)
            added += 1
        except Exception:
            stock = Stock(ticker=ticker, name=ticker)
            db.add(stock)
            added += 1
    await db.commit()
    return added


async def fetch_ohlcv(db: AsyncSession, ticker: str, period: str = "2y"):
    """拉取单只股票 OHLCV + 指标。"""
    stmt = select(Stock).where(Stock.ticker == ticker)
    result = await db.execute(stmt)
    stock = result.scalar_one_or_none()
    if not stock:
        return

    today = date.today()
    existing = await db.execute(
        select(PriceData).where(PriceData.stock_id == stock.id, PriceData.date == today)
    )
    if existing.scalar_one_or_none():
        return

    try:
        df = yf.download(ticker, period=period, progress=False)
        if df.empty:
            return
    except Exception:
        return

    df = _yf_to_flat_df(ticker, df)

    # 写入 price_data
    for idx, row in df.iterrows():
        d = idx.date() if hasattr(idx, 'date') else idx
        p = PriceData(
            stock_id=stock.id, date=d,
            open=row.get('open'), high=row.get('high'),
            low=row.get('low'), close=row.get('close'),
            adjusted_close=row.get('adj_close', row.get('close')),
            volume=row.get('volume'),
        )
        db.add(p)
    await db.commit()

    # 计算指标
    try:
        td = df[['open', 'high', 'low', 'close', 'volume']].copy()
        indicator_df = compute_indicators(td)
    except Exception:
        return

    for idx, row in indicator_df.iterrows():
        if row.isna().all():
            continue
        d = idx.date() if hasattr(idx, 'date') else idx
        ti = TechnicalIndicator(
            stock_id=stock.id, date=d,
            sma_20=row.get('sma_20'), sma_50=row.get('sma_50'), sma_200=row.get('sma_200'),
            ema_12=row.get('ema_12'), ema_26=row.get('ema_26'),
            macd=row.get('macd'), macd_signal=row.get('macd_signal'), macd_histogram=row.get('macd_histogram'),
            adx=row.get('adx'), plus_di=row.get('plus_di'), minus_di=row.get('minus_di'),
            rsi=row.get('rsi'), stochastic_k=row.get('stochastic_k'), stochastic_d=row.get('stochastic_d'),
            cci=row.get('cci'), obv=row.get('obv'), mfi=row.get('mfi'),
            volume_sma_20=row.get('volume_sma_20'),
            bb_upper=row.get('bb_upper'), bb_middle=row.get('bb_middle'), bb_lower=row.get('bb_lower'),
            atr=row.get('atr'), kc_upper=row.get('kc_upper'), kc_lower=row.get('kc_lower'),
        )
        db.add(ti)
    await db.commit()
