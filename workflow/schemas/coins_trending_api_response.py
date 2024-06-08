from typing import List, Dict
from pydantic import BaseModel, RootModel


class PriceChangePercentage(BaseModel):
    usd: float
    btc: float


class CoinData(BaseModel):
    price: float
    price_btc: float
    price_change_percentage_24h: PriceChangePercentage
    market_cap: str
    market_cap_btc: float
    total_volume: str
    total_volume_btc: str


class CoinItem(BaseModel):
    id: str
    coin_id: int
    name: str
    symbol: str
    data: CoinData


class CoinItemResponse(BaseModel):
    item: CoinItem


CoinsTrendingResponse = RootModel[List[CoinItemResponse]]
