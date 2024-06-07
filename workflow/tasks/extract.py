from prefect import task
import requests
from workflow.config.settings import (
    COINS_GECKO_BASE_URL,
)

from workflow.schemas.coins_trending_api_response import CoinsTrendingResponse


@task(
    name="fetch_trending_coins",
    description="Fetch the top trending coins from the CoinGecko API.",
)
def fetch_trending_coins(n_coins: int) -> CoinsTrendingResponse:
    """
    Fetch the top trending coins from the CoinGecko API.

    Returns:
        CoinsTrendingResponse

    """
    if n_coins > 15:
        raise Exception("The max number of coins is 15")
    url = f"{COINS_GECKO_BASE_URL}/search/trending"

    response = requests.get(url, timeout=3)
    response.raise_for_status()
    return CoinsTrendingResponse(response.json()["coins"][:n_coins])
