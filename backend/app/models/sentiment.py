from datetime import datetime
from sqlalchemy import String, Float, Integer, BigInteger, Boolean, Date, DateTime, Text, Index, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models import Base


class AnalystRating(Base):
    __tablename__ = "analyst_ratings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    stock_id: Mapped[int] = mapped_column(Integer, ForeignKey("stocks.id"), nullable=False)
    date: Mapped[datetime] = mapped_column(Date, nullable=False)
    analyst_name: Mapped[str | None] = mapped_column(String(200))
    firm: Mapped[str | None] = mapped_column(String(200))
    rating: Mapped[str | None] = mapped_column(String(20))
    rating_prior: Mapped[str | None] = mapped_column(String(20))
    target_price: Mapped[float | None] = mapped_column(Float)
    target_price_prior: Mapped[float | None] = mapped_column(Float)
    source: Mapped[str] = mapped_column(String(50), default="finnhub")

    __table_args__ = (Index("idx_ratings_stock_date", "stock_id", "date"),)


class InsiderTransaction(Base):
    __tablename__ = "insider_transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    stock_id: Mapped[int] = mapped_column(Integer, ForeignKey("stocks.id"), nullable=False)
    filing_date: Mapped[datetime] = mapped_column(Date, nullable=False)
    transaction_date: Mapped[datetime | None] = mapped_column(Date)
    insider_name: Mapped[str | None] = mapped_column(String(200))
    title: Mapped[str | None] = mapped_column(String(200))
    transaction_type: Mapped[str | None] = mapped_column(String(10))
    shares: Mapped[int | None] = mapped_column(BigInteger)
    price: Mapped[float | None] = mapped_column(Float)
    value: Mapped[int | None] = mapped_column(BigInteger)

    __table_args__ = (Index("idx_insider_stock", "stock_id", "filing_date"),)


class YoutubeVideo(Base):
    __tablename__ = "youtube_videos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    stock_id: Mapped[int] = mapped_column(Integer, ForeignKey("stocks.id"), nullable=False)
    video_id: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    channel_id: Mapped[str | None] = mapped_column(String(50))
    channel_name: Mapped[str | None] = mapped_column(String(200))
    channel_subscribers: Mapped[int | None] = mapped_column(BigInteger)
    title: Mapped[str | None] = mapped_column(String(500))
    description: Mapped[str | None] = mapped_column(Text)
    published_at: Mapped[datetime | None] = mapped_column(DateTime)
    view_count: Mapped[int] = mapped_column(BigInteger, default=0)
    like_count: Mapped[int] = mapped_column(BigInteger, default=0)
    comment_count: Mapped[int] = mapped_column(BigInteger, default=0)
    duration_seconds: Mapped[int | None] = mapped_column(Integer)
    has_captions: Mapped[bool] = mapped_column(Boolean, default=False)
    caption_text: Mapped[str | None] = mapped_column(Text)
    finbert_score: Mapped[float | None] = mapped_column(Float)
    finbert_label: Mapped[str | None] = mapped_column(String(20))
    collected_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    __table_args__ = (Index("idx_yt_stock", "stock_id", "published_at"),)
