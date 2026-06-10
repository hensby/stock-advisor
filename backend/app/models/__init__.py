from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


from app.models.stock import Stock, PriceData  # noqa: E402
from app.models.technical import TechnicalIndicator  # noqa: E402
from app.models.sentiment import AnalystRating, InsiderTransaction, YoutubeVideo  # noqa: E402
from app.models.scoring import CompositeScore, SignalChange  # noqa: E402
from app.models.watchlist import Watchlist, WatchlistItem  # noqa: E402
