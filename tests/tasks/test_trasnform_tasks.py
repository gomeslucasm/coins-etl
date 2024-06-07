from workflow.schemas.coins import CoinTranding
from workflow.schemas.coins_trending_api_response import (
    CoinData,
    CoinItem,
    CoinItemResponse,
    CoinsTrendingResponse,
    PriceChangePercentage,
)
from workflow.tasks.transform import format_trending_coins_data


def test_format_trending_coins_data_success():
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

    result = format_trending_coins_data(data)

    assert isinstance(result, list)
    assert len(result) == 2

    for coin in result:
        assert isinstance(coin, CoinTranding)
        assert isinstance(coin.id, str)
        assert isinstance(coin.coin_id, int)
        assert isinstance(coin.name, str)
        assert isinstance(coin.price_btc, float)
        assert isinstance(coin.price_usd, float)
        assert isinstance(coin.price_change_percentage_24h_btc, float)
        assert isinstance(coin.price_change_percentage_24h_usd, float)
        assert isinstance(coin.market_cap_usd, float)
        assert isinstance(coin.market_cap_btc, float)
        assert isinstance(coin.total_volume_usd, float)
        assert isinstance(coin.total_volume_btc, float)
