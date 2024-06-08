import pytest
from datetime import datetime
from unittest.mock import patch, MagicMock
from workflow.schemas.coins import CoinTranding
from workflow.schemas.market_chart import MarketChartPriceIndicatorItem
from workflow.tasks.save import save_coins_tranding, save_market_chart_price_indicator
from tests.fixtures import *


def test_save_coins_tranding(mocked_database):
    data = [
        CoinTranding(
            id="bitcoin",
            coin_id=1,
            name="Bitcoin",
            price_btc=1.0,
            price_usd=45000.0,
            price_change_percentage_24h_btc=0.5,
            price_change_percentage_24h_usd=5.0,
            market_cap_usd=850000000000.0,
            market_cap_btc=850000.0,
            total_volume_usd=1000000000.0,
            total_volume_btc=1000.0,
        ),
        CoinTranding(
            id="ethereum",
            coin_id=2,
            name="Ethereum",
            price_btc=0.066,
            price_usd=3000.0,
            price_change_percentage_24h_btc=0.3,
            price_change_percentage_24h_usd=3.0,
            market_cap_usd=350000000000.0,
            market_cap_btc=350000.0,
            total_volume_usd=500000000.0,
            total_volume_btc=500.0,
        ),
    ]

    result = save_coins_tranding.fn(data)

    mocked_database.save.assert_called_once()

    args, kwargs = mocked_database.save.call_args
    assert kwargs["table_name"] == "trending_coins"

    saved_data = kwargs["data"]
    assert "coins_name" in saved_data
    assert "coins_data" in saved_data
    assert "date" in saved_data

    assert saved_data["coins_name"] == ["Bitcoin", "Ethereum"]
    assert len(saved_data["coins_data"]) == 2
    assert saved_data["coins_data"][0]["name"] == "Bitcoin"
    assert saved_data["coins_data"][1]["name"] == "Ethereum"


def test_save_market_chart_price_indicator(mocked_database):
    item = MarketChartPriceIndicatorItem(rsi=60.0, sma=50.0, date=datetime(2023, 1, 1))
    coin_id = "bitcoin"

    result = save_market_chart_price_indicator.fn(item, coin_id)
    mocked_database.save.assert_called_once()

    args, kwargs = mocked_database.save.call_args
    assert kwargs["table_name"] == "market_chart_price_indicator"

    saved_data = kwargs["data"]
    assert "coin_id" in saved_data
    assert "rsi" in saved_data
    assert "sma" in saved_data
    assert "date" in saved_data
    assert "processed_at" in saved_data

    assert saved_data["coin_id"] == coin_id
    assert saved_data["rsi"] == 60.0
    assert saved_data["sma"] == 50.0
    assert saved_data["date"] == item.date.isoformat()
    assert isinstance(saved_data["processed_at"], str)
