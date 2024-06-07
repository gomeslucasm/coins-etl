from prefect import flow

from workflow.tasks.extract import fetch_historical_prices
from workflow.tasks.notify import send_rsi_alert
from workflow.tasks.save import save_market_chart_price_indicator
from workflow.tasks.transform import format_market_chart_data, get_price_indicators


@flow(name="analyze_bitcoin_prices")
def analyze_bitcoin_prices():
    """
    Analyze the historical prices of Bitcoin and calculate technical indicators.

    This flow performs the following steps:
    1. Fetch historical prices for Bitcoin in USD over the last 30 days.
    2. Format the market chart data.
    3. Calculate technical indicators such as RSI and SMA.
    4. Save the latest market chart price indicator to the database.
    5. Send RSI alerts based on the calculated indicators.

    Args:
        None

    Returns:
        None
    """
    coin_id = "bitcoin"
    historical_prices = fetch_historical_prices(coin_id, "usd", 30)
    formatted_data = format_market_chart_data(historical_prices)
    indicators = get_price_indicators(formatted_data.prices)
    save_market_chart_price_indicator(indicators[-1], coin_id)
    send_rsi_alert(indicators[-1], "Bitcoin")


if __name__ == "__main__":
    analyze_bitcoin_prices()
