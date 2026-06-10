from datetime import datetime
from sqlalchemy import String, Float, Integer, Date, Text, Index, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import Base


class CompositeScore(Base):
    __tablename__ = "composite_scores"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    stock_id: Mapped[int] = mapped_column(Integer, ForeignKey("stocks.id"), nullable=False)
    date: Mapped[datetime] = mapped_column(Date, nullable=False)
    technical_score: Mapped[float | None] = mapped_column(Float)
    institutional_score: Mapped[float | None] = mapped_column(Float)
    youtube_score: Mapped[float | None] = mapped_column(Float)
    fundamental_score: Mapped[float | None] = mapped_column(Float)
    composite_score: Mapped[float | None] = mapped_column(Float)
    signal: Mapped[str | None] = mapped_column(String(20))

    stock: Mapped["Stock"] = relationship("Stock", back_populates="composite_scores")

    __table_args__ = (
        Index("idx_scores_date", "date"),
        Index("idx_scores_composite", "date", "composite_score"),
    )


class SignalChange(Base):
    __tablename__ = "signal_changes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    stock_id: Mapped[int] = mapped_column(Integer, ForeignKey("stocks.id"), nullable=False)
    date: Mapped[datetime] = mapped_column(Date, nullable=False)
    previous_signal: Mapped[str | None] = mapped_column(String(20))
    current_signal: Mapped[str | None] = mapped_column(String(20))
    composite_change: Mapped[float | None] = mapped_column(Float)
    trigger_reasons: Mapped[str | None] = mapped_column(Text)

    __table_args__ = (Index("idx_signal_date", "date"),)
