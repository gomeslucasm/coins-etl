from pydantic import BaseModel, Field
from typing import List, Tuple


class MarketChartDataResponse(BaseModel):
    prices: List[Tuple[int, float]] = Field(
        ..., description="List of price data points (timestamp, price)."
    )
    market_caps: List[Tuple[int, float]] = Field(
        ..., description="List of market cap data points (timestamp, market cap)."
    )
    total_volumes: List[Tuple[int, float]] = Field(
        ..., description="List of total volume data points (timestamp, total volume)."
    )
