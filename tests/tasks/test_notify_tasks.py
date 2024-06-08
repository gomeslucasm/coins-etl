from workflow.schemas.coins import CoinTranding
from workflow.schemas.market_chart import MarketChartPriceIndicatorItem
from workflow.tasks.notify import send_coins_tranding_price_change_alert, send_rsi_alert
from tests.fixtures import *
from datetime import datetime


@pytest.mark.parametrize("price_change_percentage_24h_usd", [5.1, -5.1, 5.0, -5.0])
def test_send_coins_tranding_price_change_alert(
    mocked_notification_service, price_change_percentage_24h_usd
):

    data = [
        CoinTranding(
            id="bitcoin",
            coin_id=1,
            name="Bitcoin",
            price_btc=1.0,
            price_usd=45000.0,
            price_change_percentage_24h_btc=0.5,
            price_change_percentage_24h_usd=price_change_percentage_24h_usd,
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
            price_change_percentage_24h_usd=2.0,
            market_cap_usd=350000000000.0,
            market_cap_btc=350000.0,
            total_volume_usd=500000000.0,
            total_volume_btc=500.0,
        ),
    ]

    send_coins_tranding_price_change_alert.fn(data, 4)

    mocked_notification_service.send.assert_called_once()
    mocked_notification_service.send.assert_called_once_with(
        f"ALERT | Coin [Bitcoin] price changed {price_change_percentage_24h_usd}% in USD in the last 24 hours"
    )


@pytest.mark.parametrize("price_change_percentage_24h_usd_treshold", [5, 4, -4, -5])
def test_send_coins_tranding_price_change_alert_no_alert(
    mocked_notification_service, price_change_percentage_24h_usd_treshold
):

    data = [
        CoinTranding(
            id="bitcoin",
            coin_id=1,
            name="Bitcoin",
            price_btc=1.0,
            price_usd=45000.0,
            price_change_percentage_24h_btc=0.5,
            price_change_percentage_24h_usd=3.0,
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
            price_change_percentage_24h_usd=2.0,
            market_cap_usd=350000000000.0,
            market_cap_btc=350000.0,
            total_volume_usd=500000000.0,
            total_volume_btc=500.0,
        ),
    ]

    send_coins_tranding_price_change_alert.fn(
        data, price_change_percentage_24h_usd_treshold
    )

    assert not mocked_notification_service.send.called


def test_send_rsi_alert_overbought(mocked_notification_service):
    indicator = MarketChartPriceIndicatorItem(
        rsi=75.0, sma=100.0, date=datetime(2023, 1, 1)
    )
    coin_name = "Bitcoin"

    send_rsi_alert.fn(indicator, coin_name)

    mocked_notification_service.send.assert_called_once_with(
        f"ALERT | RSI Overbought: Coin {coin_name} has an RSI of {indicator.rsi}, which is above the threshold of {ENVIRONMENT.RSI_OVERBOUGHT_THRESHOLD}. It might be a good time to consider selling."
    )


def test_send_rsi_alert_oversold(mocked_notification_service):
    indicator = MarketChartPriceIndicatorItem(
        rsi=25.0,
        sma=100.0,
        date=datetime(2023, 1, 1),
    )
    coin_name = "Bitcoin"

    send_rsi_alert(indicator, coin_name)

    mocked_notification_service.send.assert_called_once_with(
        f"ALERT | RSI Oversold: Coin {coin_name} has an RSI of {indicator.rsi}, which is below the threshold of {ENVIRONMENT.RSI_OVERSOLD_THRESHOLD}. It might be a good time to consider buying."
    )


def test_send_rsi_alert_no_alert(mocked_notification_service):
    indicator = MarketChartPriceIndicatorItem(
        rsi=50.0, sma=100.0, date=datetime(2023, 1, 1)
    )
    coin_name = "Bitcoin"

    send_rsi_alert(indicator, coin_name)

    mocked_notification_service.send.assert_not_called()
