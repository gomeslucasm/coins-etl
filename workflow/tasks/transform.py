from typing import List, Tuple
from datetime import datetime
from prefect import task
from workflow.schemas.coins import CoinTranding
from workflow.schemas.coins_trending_api_response import CoinsTrendingResponse
from workflow.schemas.market_chart import (
    MarketChartData,
    MarketChartItem,
    MarketChartPriceIndicatorItem,
)
from workflow.schemas.coins_market_chart_api_response import MarketChartDataResponse
from workflow.utils.math import calculate_moving_average, calculate_rsi


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


@task
def format_market_chart_data(
    market_chat_data_response: MarketChartDataResponse,
) -> MarketChartData:
    """
    Format market chart data from the CoinGecko API response into a MarketChartData object.

    Args:
        market_chat_data_response (MarketChartDataResponse): The response object from the CoinGecko API containing market chart data.

    Returns:
        MarketChartData: A formatted MarketChartData object.
    """

    def convert_item(item: Tuple[int, float]):
        return MarketChartItem(
            value=item[1], date=datetime.fromtimestamp(item[0] / 1000)
        )

    return MarketChartData(
        prices=list(map(convert_item, market_chat_data_response.prices)),
        market_caps=list(map(convert_item, market_chat_data_response.market_caps)),
        total_volumes=list(map(convert_item, market_chat_data_response.total_volumes)),
    )


@task
def get_price_indicators(
    prices: List[MarketChartItem],
) -> List[MarketChartPriceIndicatorItem]:
    """
    Analyze historical prices and calculate technical indicators (RSI and SMA).

    Args:
        prices (List[MarketChartItem]): List of MarketChartItem objects containing historical price data.

    Returns:
        List[MarketChartPriceIndicatorItem]: A list of MarketChartPriceIndicatorItem objects, each containing
        the RSI, SMA, and the corresponding date.
    """
    price_values = [p.value for p in prices]
    sma = calculate_moving_average(price_values, window=20)

    rsi = calculate_rsi(price_values, window=14)

    return [
        MarketChartPriceIndicatorItem(
            date=p.date,
            rsi=r,
            sma=s,
        )
        for p, s, r in zip(prices, sma, rsi)
    ]
