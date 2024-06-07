from prefect import flow
from workflow.config.settings import PRICE_CHANGE_PERCENTAGE_24H_USD_TRESHOLD
from workflow.tasks.save import save_coins_tranding
from workflow.tasks.notify import send_coins_tranding_price_change_alert
from workflow.tasks.transform import format_trending_coins_data
from workflow.tasks.extract import fetch_trending_coins


@flow(name="trending_coins_market_data")
def trending_coins_market_data(n_coins: int = 5):
    """
    Orchestrate the fetching of trending coins and their market data.

    This flow performs the following steps:
    1. Fetch the top trending coins using the CoinGecko API.
    2. Format the fetched trending coins data.
    3. Save the formatted trending coins data to the database.
    4. Send price change alerts if the price change percentage in USD exceeds the specified threshold.

    Args:
        n_coins (int): The number of trending coins to fetch. Defaults to 5.

    Returns:
        None
    """
    trending_coins = fetch_trending_coins(n_coins)
    formatted_trending_coins = format_trending_coins_data(trending_coins)
    save_coins_tranding(formatted_trending_coins)
    send_coins_tranding_price_change_alert(
        formatted_trending_coins, PRICE_CHANGE_PERCENTAGE_24H_USD_TRESHOLD
    )


if __name__ == "__main__":
    trending_coins_market_data(10)
