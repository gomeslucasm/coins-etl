from typing import List
from prefect import task
from workflow.config import ENVIRONMENT
from workflow.schemas.coins import CoinTranding
from workflow.schemas.market_chart import MarketChartPriceIndicatorItem
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


@task(log_prints=True)
def send_rsi_alert(indicator: MarketChartPriceIndicatorItem, coin_name: str):
    """
    Send alerts based on the RSI values.

    Args:
        indicator (MarketChartPriceIndicatorItem): Price indicator including RSI and SMA.
        coin_name (str): Coin name

    Returns:
        None

    Explanation:
        The Relative Strength Index (RSI) is a momentum oscillator that measures the speed and change of price movements.
        It oscillates between 0 and 100 and is typically used to identify overbought or oversold conditions in a market.

        - Overbought: An RSI above a certain threshold (typically 70) indicates that the asset may be overbought and
          could be due for a correction or pullback. In this context, the threshold is defined as ENVIRONMENT.RSI_OVERBOUGHT_THRESHOLD.
        - Oversold: An RSI below a certain threshold (typically 30) suggests that the asset may be oversold and could be undervalued.
          In this context, the threshold is defined as ENVIRONMENT.RSI_OVERSOLD_THRESHOLD.

    """
    notification_service = get_notification_service()
    if indicator.rsi > ENVIRONMENT.RSI_OVERBOUGHT_THRESHOLD:
        notification_service.send(
            f"ALERT | RSI Overbought: Coin {coin_name} has an RSI of {indicator.rsi}, which is above the threshold of {ENVIRONMENT.RSI_OVERBOUGHT_THRESHOLD}. It might be a good time to consider selling."
        )
    elif indicator.rsi < ENVIRONMENT.RSI_OVERSOLD_THRESHOLD:
        notification_service.send(
            f"ALERT | RSI Oversold: Coin {coin_name} has an RSI of {indicator.rsi}, which is below the threshold of {ENVIRONMENT.RSI_OVERSOLD_THRESHOLD}. It might be a good time to consider buying."
        )
