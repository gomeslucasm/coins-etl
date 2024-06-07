from typing import List

from prefect import task
from workflow.schemas.coins import CoinTranding
from workflow.schemas.coins_trending_api_response import CoinsTrendingResponse


@task
def format_trending_coins_data(coins: CoinsTrendingResponse) -> List[CoinTranding]:
    """
    Format trending coins data from the CoinGecko API response into a list of CoinTranding objects.

    Args:
        coins (CoinsTrendingResponse): The response object from the CoinGecko API containing trending coins data.

    Returns:
        List[CoinTranding]: A list of formatted CoinTranding objects.
    """

    def convert_usd_str_to_float(usd_str: str) -> float:
        usd_str = usd_str.replace("$", "").replace(",", "")
        return float(usd_str)

    def get_fields(coin) -> CoinTranding:
        item = coin.item
        return CoinTranding(
            id=item.id,
            coin_id=item.coin_id,
            name=item.name,
            price_btc=float(item.data.price_btc),
            price_usd=item.data.price,
            price_change_percentage_24h_btc=item.data.price_change_percentage_24h.btc,
            price_change_percentage_24h_usd=item.data.price_change_percentage_24h.usd,
            market_cap_usd=convert_usd_str_to_float(item.data.market_cap),
            market_cap_btc=float(item.data.market_cap_btc),
            total_volume_usd=convert_usd_str_to_float(item.data.total_volume),
            total_volume_btc=float(item.data.total_volume_btc),
        )

    return list(map(get_fields, coins.root))
