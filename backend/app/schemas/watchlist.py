from pydantic import BaseModel
from typing import Optional
from app.schemas.stock import StockItem

class WatchlistCreate(BaseModel):
    name: str

class WatchlistOut(BaseModel):
    id: int
    name: str
    item_count: int = 0
    stocks: list[StockItem] = []

    model_config = {"from_attributes": True}

class WatchlistItemAdd(BaseModel):
    ticker: str
