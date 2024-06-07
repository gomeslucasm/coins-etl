from typing import List
from prefect import task
from workflow.schemas.coins import CoinTranding
from workflow.utils.notification import get_notification_service


@task(log_prints=True)
def send_coins_tranding_price_change_alert(
    coins_tranding: List[CoinTranding], price_change_percentage_24h_usd_treshold: int
):
    """
    Sends a price change alert for coins whose price change percentage
    in USD exceeds a predefined threshold in the last 24 hours.

    Args:
        coins_tranding (List[CoinTranding]): List of trending coins with their price details.
    """
    notification_service = get_notification_service()
    for coin_tranding in coins_tranding:
        if abs(coin_tranding.price_change_percentage_24h_usd) > abs(
            price_change_percentage_24h_usd_treshold
        ):
            notification_service.send(
                f"ALERT | Coin [{coin_tranding.name}] price changed {coin_tranding.price_change_percentage_24h_usd}% in USD in the last 24 hours"
            )
