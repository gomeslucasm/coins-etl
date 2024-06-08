import pytest
import requests
from workflow.config import ENVIRONMENT
from workflow.schemas.coins_market_chart_api_response import MarketChartDataResponse
from workflow.tasks.extract import fetch_historical_prices, fetch_trending_coins
from workflow.schemas.coins_trending_api_response import CoinsTrendingResponse
from tests.fixtures import (
    mock_trending_coins_api,
    disable_timeout_simulation,
    mock_market_chart_api,
)
from prefect._internal.concurrency.cancellation import CancelledError


def test_fetch_trending_coins_success(
    mock_trending_coins_api, disable_timeout_simulation
):
    result = fetch_trending_coins.fn(n_coins=3)

    assert isinstance(result, CoinsTrendingResponse)
    assert len(result.root) == 3


def test_fetch_trending_coins_invalid_n_coins(disable_timeout_simulation):
    with pytest.raises(Exception, match="The max number of coins is 15") as excinfo:
        fetch_trending_coins.fn(n_coins=16)


def test_fetch_trending_coins_api_failure(requests_mock, disable_timeout_simulation):
    url = f"{ENVIRONMENT.COINS_GECKO_BASE_URL}/search/trending"
    requests_mock.get(url, status_code=500)

    with pytest.raises(requests.exceptions.HTTPError):
        fetch_trending_coins.fn(n_coins=3)


def test_fetch_trending_coins_retry_simulation(
    mock_trending_coins_api, requests_mock, mocker
):
    mocked_get_run_context = mocker.patch("workflow.tasks.extract.get_run_context")
    mocked_get_run_context.return_value = mocker.Mock(task_run=mocker.Mock(run_count=4))

    result = fetch_trending_coins(n_coins=3)

    mocked_get_run_context.return_value = mocker.Mock(task_run=mocker.Mock(run_count=3))

    with pytest.raises(Exception):
        fetch_trending_coins(n_coins=3)


def test_fetch_historical_prices_success(mock_market_chart_api):
    result = fetch_historical_prices.fn("bitcoin", "usd", 30)

    assert isinstance(result, MarketChartDataResponse)
    assert isinstance(result.prices, list)
    assert isinstance(result.market_caps, list)
    assert isinstance(result.total_volumes, list)

    assert len(result.prices[0]) == 2
    assert len(result.market_caps[0]) == 2
    assert len(result.total_volumes[0]) == 2


def test_fetch_historical_prices_api_failure(requests_mock):
    url = f"{ENVIRONMENT.COINS_GECKO_BASE_URL}/coins/bitcoin/market_chart?vs_currency=usd&days=30"
    requests_mock.get(url, status_code=500)

    with pytest.raises(requests.exceptions.HTTPError):
        fetch_historical_prices.fn("bitcoin", "usd", 30)
