from workflow.schemas.coins import CoinTranding
from workflow.schemas.coins_trending_api_response import (
    CoinData,
    CoinItem,
    CoinItemResponse,
    CoinsTrendingResponse,
    PriceChangePercentage,
)
from workflow.schemas.market_chart import MarketChartData, MarketChartItem
from workflow.tasks.transform import (
    format_market_chart_data,
    format_trending_coins_data,
)
from datetime import datetime
from workflow.schemas.coins_market_chart_api_response import MarketChartDataResponse


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

    result = format_trending_coins_data.fn(data)

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


def test_format_market_chart_data():
    response_data = MarketChartDataResponse(
        prices=[
            (1711843200000, 69702.3087473573),
            (1711929600000, 71246.95144060145),
            (1711983682000, 68887.74951585678),
        ],
        market_caps=[
            (1711843200000, 1370247487960.0945),
            (1711929600000, 1401370211582.3662),
            (1711983682000, 1355701979725.1584),
        ],
        total_volumes=[
            (1711843200000, 16408802301.837431),
            (1711929600000, 19723005998.21497),
            (1711983682000, 30137418199.643093),
        ],
    )

    expected_data = MarketChartData(
        prices=[
            MarketChartItem(
                value=69702.3087473573, date=datetime.fromtimestamp(1711843200)
            ),
            MarketChartItem(
                value=71246.95144060145, date=datetime.fromtimestamp(1711929600)
            ),
            MarketChartItem(
                value=68887.74951585678, date=datetime.fromtimestamp(1711983682)
            ),
        ],
        market_caps=[
            MarketChartItem(
                value=1370247487960.0945, date=datetime.fromtimestamp(1711843200)
            ),
            MarketChartItem(
                value=1401370211582.3662, date=datetime.fromtimestamp(1711929600)
            ),
            MarketChartItem(
                value=1355701979725.1584, date=datetime.fromtimestamp(1711983682)
            ),
        ],
        total_volumes=[
            MarketChartItem(
                value=16408802301.837431, date=datetime.fromtimestamp(1711843200)
            ),
            MarketChartItem(
                value=19723005998.21497, date=datetime.fromtimestamp(1711929600)
            ),
            MarketChartItem(
                value=30137418199.643093, date=datetime.fromtimestamp(1711983682)
            ),
        ],
    )

    result = format_market_chart_data.fn(response_data)

    assert result == expected_data
