from typing import List
from prefect import task
from datetime import datetime
from workflow.schemas.coins import CoinTranding
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
