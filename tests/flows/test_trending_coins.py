import pytest
from unittest.mock import patch, MagicMock
from workflow.flows.trending_coins import trending_coins_market_data
from workflow.config.settings import PRICE_CHANGE_PERCENTAGE_24H_USD_TRESHOLD
from workflow.schemas.coins_trending_api_response import (
    CoinData,
    CoinItem,
    CoinItemResponse,
    CoinsTrendingResponse,
    PriceChangePercentage,
)
from workflow.schemas.coins import CoinTranding


def test_trending_coins_market_data(mocker):
    mock_fetch = mocker.patch("workflow.flows.trending_coins.fetch_trending_coins")
    mock_format = mocker.patch(
        "workflow.flows.trending_coins.format_trending_coins_data"
    )
    mock_save = mocker.patch("workflow.flows.trending_coins.save_coins_tranding")
    mock_notify = mocker.patch(
        "workflow.flows.trending_coins.send_coins_tranding_price_change_alert"
    )

    data = CoinsTrendingResponse(
        root=[
            CoinItemResponse(
                item=CoinItem(
                    id="bitcoin",
                    coin_id=1,
                    name="Bitcoin",
                    symbol="BTC",
                    data=CoinData(
                        price=45000.0,
                        price_btc="1.0",
                        price_change_percentage_24h=PriceChangePercentage(
                            usd=5.0, btc=0.5
                        ),
                        market_cap="$850,000,000,000",
                        market_cap_btc="850000.0",
                        total_volume="$1,000,000,000",
                        total_volume_btc="1000.0",
                    ),
                )
            ),
            CoinItemResponse(
                item=CoinItem(
                    id="ethereum",
                    coin_id=2,
                    name="Ethereum",
                    symbol="ETH",
                    data=CoinData(
                        price=3000.0,
                        price_btc="0.066",
                        price_change_percentage_24h=PriceChangePercentage(
                            usd=3.0, btc=0.3
                        ),
                        market_cap="$350,000,000,000",
                        market_cap_btc="350000.0",
                        total_volume="$500,000,000",
                        total_volume_btc="500.0",
                    ),
                )
            ),
        ]
    )

    mock_fetch.return_value = data
    mock_format.return_value = [
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

    # Run the flow
    trending_coins_market_data.fn(n_coins=2)

    # Assert that each task was called correctly
    mock_fetch.assert_called_once_with(2)
    mock_format.assert_called_once_with(data)
    mock_save.assert_called_once_with(mock_format.return_value)
    mock_notify.assert_called_once_with(
        mock_format.return_value, PRICE_CHANGE_PERCENTAGE_24H_USD_TRESHOLD
    )
