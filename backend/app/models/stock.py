from datetime import datetime
from sqlalchemy import String, Float, Integer, BigInteger, Boolean, Date, DateTime, UniqueConstraint, Index, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import Base


class Stock(Base):
    __tablename__ = "stocks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ticker: Mapped[str] = mapped_column(String(10), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    sector: Mapped[str | None] = mapped_column(String(100))
    industry: Mapped[str | None] = mapped_column(String(100))
    market_cap: Mapped[int | None] = mapped_column(BigInteger)
    exchange: Mapped[str | None] = mapped_column(String(20), default="NASDAQ")
    cik: Mapped[str | None] = mapped_column(String(20))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    price_data: Mapped[list["PriceData"]] = relationship(back_populates="stock", lazy="selectin")
    technical_indicators: Mapped[list["TechnicalIndicator"]] = relationship(back_populates="stock", lazy="selectin")
    composite_scores: Mapped[list["CompositeScore"]] = relationship(back_populates="stock", lazy="selectin")

    __table_args__ = (
        Index("idx_stocks_ticker", "ticker"),
        Index("idx_stocks_sector", "sector"),
    )


class PriceData(Base):
    __tablename__ = "price_data"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    stock_id: Mapped[int] = mapped_column(Integer, ForeignKey("stocks.id"), nullable=False)
    date: Mapped[datetime] = mapped_column(Date, nullable=False)
    open: Mapped[float | None] = mapped_column(Float)
    high: Mapped[float | None] = mapped_column(Float)
    low: Mapped[float | None] = mapped_column(Float)
    close: Mapped[float | None] = mapped_column(Float)
    adjusted_close: Mapped[float | None] = mapped_column(Float)
    volume: Mapped[int | None] = mapped_column(BigInteger)

    stock: Mapped["Stock"] = relationship(back_populates="price_data")

    __table_args__ = (
        UniqueConstraint("stock_id", "date"),
        Index("idx_price_data_stock_date", "stock_id", "date"),
    )
