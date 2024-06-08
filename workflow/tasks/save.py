from typing import List
from prefect import task
from datetime import datetime
from workflow.schemas.coins import CoinTranding
from workflow.schemas.market_chart import MarketChartPriceIndicatorItem
from workflow.utils.db import get_db


@task
def save_coins_tranding(coins_tranding: List[CoinTranding]):
    """
    Saves the trending coins data to the database.

    Args:
        coins_tranding (List[CoinTranding]): List of trending coins with their price details.

    Returns:
        dict: A dictionary with the saved data including coin names, coin data, and the current date.
    """
    coins_names = []
    coins_data = []

    for coin_tranding in coins_tranding:
        coins_names.append(coin_tranding)
        coins_data.append(coins_data)

    coins_names = [coin_tranding.name for coin_tranding in coins_tranding]
    coins_data = [coin_tranding.model_dump() for coin_tranding in coins_tranding]

    db = get_db()

    saved = db.save(
        table_name="trending_coins",
        data=dict(
            coins_name=coins_names,
            coins_data=coins_data,
            date=datetime.now().isoformat(),
        ),
    )

    return saved


@task
def save_market_chart_price_indicator(
    item: MarketChartPriceIndicatorItem, coin_id: str
):
    """
    Save market chart price indicators (RSI and SMA) to the database.

    Args:
        item (MarketChartPriceIndicatorItem): The market chart price indicator item to be saved.
        coin_id (str): id of the coin

    Returns:
        dict: The saved data including RSI, SMA, date, and processed timestamp.
    """
    db = get_db()

    return db.save(
        table_name="market_chart_price_indicator",
        data=dict(
            coin_id=coin_id,
            rsi=item.rsi,
            sma=item.sma,
            date=item.date.isoformat(),
            processed_at=datetime.now().isoformat(),
        ),
    )
