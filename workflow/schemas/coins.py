from pydantic import BaseModel


class CoinTranding(BaseModel):
    id: str
    coin_id: int
    name: str
    price_btc: float
    price_usd: float
    price_change_percentage_24h_btc: float
    price_change_percentage_24h_usd: float
    market_cap_usd: float
    market_cap_btc: float
    total_volume_usd: float
    total_volume_btc: float
