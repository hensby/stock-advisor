from celery import Celery
from celery.schedules import crontab
from app.config import settings

celery_app = Celery(
    "stock_advisor",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="America/New_York",
    enable_utc=True,
    worker_prefetch_multiplier=1,
    task_acks_late=True,
)


@celery_app.task(name="fetch_daily_data")
def fetch_daily_data():
    """每日盘后拉取所有活跃股票的 OHLCV 数据 + 计算指标 + 综合评分。"""
    import asyncio
    from app.database import AsyncSessionLocal
    from app.services.data_collector import fetch_ohlcv
    from sqlalchemy import select
    from app.models.stock import Stock

    async def _run():
        async with AsyncSessionLocal() as db:
            result = await db.execute(select(Stock).where(Stock.is_active == True))
            stocks = result.scalars().all()
            for stock in stocks:
                try:
                    await fetch_ohlcv(db, stock.ticker)
                except Exception:
                    continue

            # 计算综合评分
            from app.services.scoring_service import compute_composite_score
            from datetime import date
            today = date.today()
            for stock in stocks:
                try:
                    from app.models.scoring import CompositeScore
                    existing = await db.execute(
                        select(CompositeScore).where(
                            CompositeScore.stock_id == stock.id,
                            CompositeScore.date == today
                        )
                    )
                    if not existing.scalar_one_or_none():
                        await compute_composite_score(db, stock.id, today)
                except Exception:
                    continue

    asyncio.run(_run())


celery_app.conf.beat_schedule = {
    "daily-market-data": {
        "task": "fetch_daily_data",
        "schedule": crontab(hour=16, minute=30, day_of_week="mon-fri"),
        "options": {"expires": 3600},
    },
}
