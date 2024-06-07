from prefect import task
from prefect.context import get_run_context
import requests
from workflow.config import ENVIRONMENT

from workflow.schemas.coins_trending_api_response import CoinsTrendingResponse
import time


@task(
    name="fetch_trending_coins",
    description="Fetch the top trending coins from the CoinGecko API.",
    timeout_seconds=1.5,
    retries=4,
)
def fetch_trending_coins(n_coins: int) -> CoinsTrendingResponse:
    """
    Fetch the top trending coins from the CoinGecko API.

    Returns:
        CoinsTrendingResponse

    Notes:
        - The function simulates failures in the first two attempts to demonstrate the retry mechanism.
        - The execution context is used to check the current attempt number.
        - If the attempt number is less than 2, the function sleeps for 3 seconds, causing a timeout.
        - On the third attempt, the function is expected to succeed as normal.
        - The variable `SIMULATE_TIMEOUT_FETCH_TRENDING_COINS` is an environment variable used to enable or disable the
        timeout simulation. The default value is 'true'.

    Example:
        >>> fetch_trending_coins(5)
        Attempt 1: Timeout
        Attempt 2: Timeout
        Attempt 3: Success
    """
    if n_coins > 15:
        raise Exception("The max number of coins is 15")
    url = f"{ENVIRONMENT.COINS_GECKO_BASE_URL}/search/trending"

    if ENVIRONMENT.SIMULATE_TIMEOUT_FETCH_TRENDING_COINS:
        context = get_run_context()
        attempt_number = context.task_run.run_count

        if attempt_number < 4:
            time.sleep(5)

    response = requests.get(url, timeout=3)
    response.raise_for_status()
    return CoinsTrendingResponse(response.json()["coins"][:n_coins])
