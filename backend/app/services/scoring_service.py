from app.models.scoring import CompositeScore, SignalChange
from app.models.technical import TechnicalIndicator
from app.models.sentiment import AnalystRating, InsiderTransaction, YoutubeVideo
from app.models.stock import PriceData
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from datetime import date, timedelta
import json

# 默认权重
DEFAULT_WEIGHTS = {"technical": 0.40, "institutional": 0.30, "youtube": 0.20, "fundamental": 0.10}


def signal_from_score(score: float) -> str:
    if score >= 80: return "strong_buy"
    elif score >= 60: return "buy"
    elif score >= 40: return "hold"
    elif score >= 20: return "sell"
    return "strong_sell"


async def compute_technical_score(db: AsyncSession, stock_id: int, target_date: date) -> tuple[float, list[str]]:
    """返回 (技术面评分 0-100, trigger_reasons)"""
    result = await db.execute(
        select(TechnicalIndicator).where(
            TechnicalIndicator.stock_id == stock_id,
            TechnicalIndicator.date <= target_date
        ).order_by(TechnicalIndicator.date.desc()).limit(1)
    )
    latest = result.scalar_one_or_none()
    if not latest:
        return 50.0, []

    # 获前一日 close 用于 volume 判断
    prev_result = await db.execute(
        select(PriceData).where(PriceData.stock_id == stock_id, PriceData.date < target_date)
        .order_by(PriceData.date.desc()).limit(1)
    )
    prev = prev_result.scalar_one_or_none()
    prev_close = prev.close if prev else None

    reasons = []
    score = 0

    # Golden cross (20 pts)
    if latest.sma_50 and latest.sma_200:
        if latest.sma_50 > latest.sma_200:
            score += 20
            reasons.append("金叉形成 (SMA50上穿SMA200)")
        else:
            score -= 20

    # Above SMA200 (20 pts)
    price = await db.execute(
        select(PriceData.close).where(PriceData.stock_id == stock_id, PriceData.date == target_date)
    )
    close_val = price.scalar_one_or_none()
    if close_val and latest.sma_200 and close_val > latest.sma_200:
        score += 20
    elif close_val and latest.sma_200:
        score -= 20

    # MACD (15 pts)
    if latest.macd and latest.macd_signal:
        if latest.macd > latest.macd_signal:
            score += 15
            reasons.append("MACD金叉")
        else:
            score -= 15

    # RSI (15 pts)
    if latest.rsi:
        if 40 <= latest.rsi <= 65:
            score += 15
        elif latest.rsi > 70:
            score -= 15
            reasons.append(f"RSI超买 ({latest.rsi:.1f})")
        elif latest.rsi < 30:
            score -= 7
            reasons.append(f"RSI超卖 ({latest.rsi:.1f})")
        else:
            score += 5

    # Volume (15 pts)
    if close_val and prev_close and latest.volume and latest.volume_sma_20:
        if latest.volume > latest.volume_sma_20 * 1.2:
            if close_val > prev_close:
                score += 15
                reasons.append("放量上涨")
            else:
                score -= 15
                reasons.append("放量下跌")

    # ADX (10 pts)
    if latest.adx and latest.adx > 25:
        if latest.plus_di and latest.minus_di and latest.plus_di > latest.minus_di:
            score += 10
        else:
            score -= 10

    # BB position (5 pts)
    if close_val and latest.bb_upper and latest.bb_lower:
        if close_val < latest.bb_lower * 1.02:
            score += 5
            reasons.append("触及Bollinger下轨")
        elif close_val > latest.bb_upper * 0.98:
            score -= 5

    return max(0, min(100, score + 50)), reasons


async def compute_institutional_score(db: AsyncSession, stock_id: int) -> tuple[float, list[str]]:
    """返回 (机构情绪评分 0-100, reasons)"""
    reasons = []
    ninety_days_ago = date.today() - timedelta(days=90)
    thirty_days_ago = date.today() - timedelta(days=30)

    # 分析师共识
    result = await db.execute(
        select(AnalystRating).where(
            AnalystRating.stock_id == stock_id,
            AnalystRating.date >= ninety_days_ago
        )
    )
    ratings = result.scalars().all()

    buy = sum(1 for r in ratings if r.rating and r.rating.lower() in ('buy', 'overweight', 'outperform'))
    hold = sum(1 for r in ratings if r.rating and r.rating.lower() in ('hold', 'neutral', 'equal-weight'))
    sell = sum(1 for r in ratings if r.rating and r.rating.lower() in ('sell', 'underweight', 'underperform'))
    total = buy + hold + sell

    buy_ratio_score = (buy / total * 35) if total > 0 else 17.5

    # 目标价 upside
    targets = [r.target_price for r in ratings if r.target_price]
    avg_target = sum(targets) / len(targets) if targets else 0
    price_result = await db.execute(
        select(PriceData.close).where(PriceData.stock_id == stock_id)
        .order_by(PriceData.date.desc()).limit(1)
    )
    current_price = price_result.scalar_one_or_none()
    if current_price and avg_target > 0:
        upside = (avg_target / current_price - 1) * 100
        upside_score = max(0, min(1, upside / 100)) * 25
        if upside > 10:
            reasons.append(f"目标价上涨空间 {upside:.1f}%")
    else:
        upside_score = 12.5

    # 近期上调
    upgrades = sum(1 for r in ratings
                   if r.rating and r.rating_prior
                   and r.rating.lower() in ('buy', 'overweight')
                   and r.rating_prior.lower() in ('hold', 'sell', 'neutral')
                   and r.date >= thirty_days_ago)
    upgrade_score = min(upgrades / 3, 1) * 20
    if upgrades > 0:
        reasons.append(f"{upgrades}家机构近期上调评级")

    # 内部人交易
    insider_result = await db.execute(
        select(InsiderTransaction).where(
            InsiderTransaction.stock_id == stock_id,
            InsiderTransaction.filing_date >= ninety_days_ago
        )
    )
    insiders = insider_result.scalars().all()
    buy_val = sum(i.value or 0 for i in insiders if i.transaction_type == 'buy')
    sell_val = sum(i.value or 0 for i in insiders if i.transaction_type == 'sell')
    total_val = buy_val + sell_val
    insider_score = (buy_val / total_val * 15) if total_val > 0 else 7.5
    if buy_val > sell_val and total_val > 0:
        reasons.append("内部人净买入")

    inst_ownership_score = 5  # 默认

    score = buy_ratio_score + upside_score + upgrade_score + insider_score + inst_ownership_score
    return max(0, min(100, score)), reasons


async def compute_youtube_score(db: AsyncSession, stock_id: int) -> tuple[float, list[str]]:
    """返回 (YouTube情绪评分 0-100, reasons)"""
    seven_days_ago = date.today() - timedelta(days=7)
    fourteen_days_ago = date.today() - timedelta(days=14)

    result = await db.execute(
        select(YoutubeVideo).where(
            YoutubeVideo.stock_id == stock_id,
            YoutubeVideo.published_at >= seven_days_ago
        )
    )
    videos = result.scalars().all()

    if not videos:
        return 50.0, ["暂无YouTube视频数据"]

    reasons = []
    finbert_scores = [v.finbert_score for v in videos if v.finbert_score is not None]
    finbert_avg = sum(finbert_scores) / len(finbert_scores) if finbert_scores else 0
    finbert_component = (finbert_avg + 1) / 2 * 40

    engagement = []
    for v in videos:
        if v.view_count and v.view_count > 0:
            engagement.append(v.like_count / v.view_count)
    eng_avg = sum(engagement) / len(engagement) if engagement else 0
    engagement_component = min(eng_avg / 0.05, 1) * 20

    # channel authority
    authority_scores = []
    for v in videos:
        subs = v.channel_subscribers or 0
        if subs > 1_000_000: authority_scores.append(1.0)
        elif subs > 100_000: authority_scores.append(0.6)
        elif subs > 10_000: authority_scores.append(0.4)
        else: authority_scores.append(0.2)
    authority_component = (sum(authority_scores) / len(authority_scores) if authority_scores else 0.4) * 20

    # volume trend
    last_week = await db.execute(
        select(func.count(YoutubeVideo.id)).where(
            YoutubeVideo.stock_id == stock_id,
            YoutubeVideo.published_at >= fourteen_days_ago,
            YoutubeVideo.published_at < seven_days_ago
        )
    )
    last_count = last_week.scalar() or 0
    this_count = len(videos)
    volume_trend = (this_count - last_count) / max(last_count, 1)
    volume_component = max(0, min(1, (volume_trend + 1) / 2)) * 20

    score = finbert_component + engagement_component + authority_component + volume_component

    if finbert_avg > 0.2:
        reasons.append(f"YouTube情绪看多 (FinBERT={finbert_avg:.2f})")
    elif finbert_avg < -0.2:
        reasons.append(f"YouTube情绪看空 (FinBERT={finbert_avg:.2f})")
    if this_count > 0:
        reasons.append(f"近7天{this_count}个分析视频")

    return max(0, min(100, score)), reasons


async def compute_fundamental_score(db: AsyncSession, stock_id: int) -> tuple[float, list[str]]:
    """基本面评分 — 简化版，从 yfinance 信息中获取。暂返回默认值"""
    return 50.0, []


async def compute_composite_score(
    db: AsyncSession, stock_id: int, target_date: date,
    weights: dict | None = None
) -> CompositeScore:
    """计算综合评分，写入 DB，检测信号变化"""
    if weights is None:
        weights = DEFAULT_WEIGHTS

    tech_score, tech_reasons = await compute_technical_score(db, stock_id, target_date)
    inst_score, inst_reasons = await compute_institutional_score(db, stock_id)
    yt_score, yt_reasons = await compute_youtube_score(db, stock_id)
    fund_score, fund_reasons = await compute_fundamental_score(db, stock_id)

    composite = (
        tech_score * weights["technical"]
        + inst_score * weights["institutional"]
        + yt_score * weights["youtube"]
        + fund_score * weights["fundamental"]
    )
    signal = signal_from_score(composite)

    # 检测信号变化
    prev = await db.execute(
        select(CompositeScore).where(
            CompositeScore.stock_id == stock_id,
            CompositeScore.date < target_date
        ).order_by(CompositeScore.date.desc()).limit(1)
    )
    prev_score = prev.scalar_one_or_none()

    if prev_score and prev_score.signal != signal:
        all_reasons = tech_reasons + inst_reasons + yt_reasons + fund_reasons
        signal_change = SignalChange(
            stock_id=stock_id,
            date=target_date,
            previous_signal=prev_score.signal,
            current_signal=signal,
            composite_change=composite - (prev_score.composite_score or 0),
            trigger_reasons=json.dumps(all_reasons, ensure_ascii=False)
        )
        db.add(signal_change)

    # UPSERT composite_score
    css = CompositeScore(
        stock_id=stock_id,
        date=target_date,
        technical_score=tech_score,
        institutional_score=inst_score,
        youtube_score=yt_score,
        fundamental_score=fund_score,
        composite_score=composite,
        signal=signal
    )
    db.add(css)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
    return css
