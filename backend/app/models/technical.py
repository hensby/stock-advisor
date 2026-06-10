from datetime import datetime
from sqlalchemy import String, Float, Integer, BigInteger, Date, UniqueConstraint, Index, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import Base


class TechnicalIndicator(Base):
    __tablename__ = "technical_indicators"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    stock_id: Mapped[int] = mapped_column(Integer, ForeignKey("stocks.id"), nullable=False)
    date: Mapped[datetime] = mapped_column(Date, nullable=False)
    sma_20: Mapped[float | None] = mapped_column(Float)
    sma_50: Mapped[float | None] = mapped_column(Float)
    sma_200: Mapped[float | None] = mapped_column(Float)
    ema_12: Mapped[float | None] = mapped_column(Float)
    ema_26: Mapped[float | None] = mapped_column(Float)
    macd: Mapped[float | None] = mapped_column(Float)
    macd_signal: Mapped[float | None] = mapped_column(Float)
    macd_histogram: Mapped[float | None] = mapped_column(Float)
    adx: Mapped[float | None] = mapped_column(Float)
    plus_di: Mapped[float | None] = mapped_column(Float)
    minus_di: Mapped[float | None] = mapped_column(Float)
    rsi: Mapped[float | None] = mapped_column(Float)
    stochastic_k: Mapped[float | None] = mapped_column(Float)
    stochastic_d: Mapped[float | None] = mapped_column(Float)
    cci: Mapped[float | None] = mapped_column(Float)
    obv: Mapped[float | None] = mapped_column(Float)
    mfi: Mapped[float | None] = mapped_column(Float)
    volume_sma_20: Mapped[float | None] = mapped_column(Float)
    bb_upper: Mapped[float | None] = mapped_column(Float)
    bb_middle: Mapped[float | None] = mapped_column(Float)
    bb_lower: Mapped[float | None] = mapped_column(Float)
    atr: Mapped[float | None] = mapped_column(Float)
    kc_upper: Mapped[float | None] = mapped_column(Float)
    kc_lower: Mapped[float | None] = mapped_column(Float)

    stock: Mapped["Stock"] = relationship("Stock", back_populates="technical_indicators")

    __table_args__ = (
        UniqueConstraint("stock_id", "date"),
        Index("idx_tech_stock_date", "stock_id", "date"),
    )
