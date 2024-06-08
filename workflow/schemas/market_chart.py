from datetime import datetime
from typing import List
from pydantic import BaseModel


class MarketChartItem(BaseModel):
    date: datetime
    value: float


class MarketChartData(BaseModel):
    prices: List[MarketChartItem]
    market_caps: List[MarketChartItem]
    total_volumes: List[MarketChartItem]


class MarketChartPriceIndicatorItem(BaseModel):
    rsi: float
    sma: float
    date: datetime
