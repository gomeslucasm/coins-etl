import pytest
from datetime import datetime
from unittest.mock import MagicMock
from workflow.schemas.market_chart import (
    MarketChartPriceIndicatorItem,
    MarketChartItem,
    MarketChartData,
)
from workflow.schemas.coins_market_chart_api_response import (
    MarketChartDataResponse,
)
from workflow.flows.analyze_bitcoin_prices import analyze_bitcoin_prices


def test_analyze_bitcoin_prices(mocker):
    historical_prices_response = MarketChartDataResponse(
        prices=[[1609459200000, 29000.0], [1609545600000, 31000.0]],
        market_caps=[
            [1609459200000, 600000000000.0],
            [1609545600000, 620000000000.0],
        ],
        total_volumes=[
            [1609459200000, 50000000000.0],
            [1609545600000, 52000000000.0],
        ],
    )

    mock_fetch = mocker.patch(
        "workflow.flows.analyze_bitcoin_prices.fetch_historical_prices",
        return_value=historical_prices_response,
    )
    formatted_data = MarketChartData(
        prices=[
            MarketChartItem(value=29000.0, date=datetime(2021, 1, 1)),
            MarketChartItem(value=31000.0, date=datetime(2021, 1, 2)),
        ],
        market_caps=[
            MarketChartItem(value=600000000000.0, date=datetime(2021, 1, 1)),
            MarketChartItem(value=620000000000.0, date=datetime(2021, 1, 2)),
        ],
        total_volumes=[
            MarketChartItem(value=50000000000.0, date=datetime(2021, 1, 1)),
            MarketChartItem(value=52000000000.0, date=datetime(2021, 1, 2)),
        ],
    )

    mock_format = mocker.patch(
        "workflow.flows.analyze_bitcoin_prices.format_market_chart_data",
        return_value=formatted_data,
    )
    indicators = [
        MarketChartPriceIndicatorItem(rsi=70.0, sma=30000.0, date=datetime(2021, 1, 1)),
        MarketChartPriceIndicatorItem(rsi=65.0, sma=30500.0, date=datetime(2021, 1, 2)),
    ]
    mock_get_indicators = mocker.patch(
        "workflow.flows.analyze_bitcoin_prices.get_price_indicators",
        return_value=indicators,
    )
    mock_save = mocker.patch(
        "workflow.flows.analyze_bitcoin_prices.save_market_chart_price_indicator"
    )
    mock_notify = mocker.patch("workflow.flows.analyze_bitcoin_prices.send_rsi_alert")

    analyze_bitcoin_prices.fn()

    mock_fetch.assert_called_once_with("bitcoin", "usd", 30)
    mock_format.assert_called_once_with(historical_prices_response)
    mock_get_indicators.assert_called_once_with(formatted_data.prices)
    mock_save.assert_called_once_with(indicators[-1], "bitcoin")
    mock_notify.assert_called_once_with(indicators[-1], "Bitcoin")
