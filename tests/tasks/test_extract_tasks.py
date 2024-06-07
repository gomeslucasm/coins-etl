import pytest
import requests
from workflow.tasks.extract import fetch_trending_coins
from workflow.schemas.coins_trending_api_response import CoinsTrendingResponse
from tests.fixtures import mock_trending_coins_api
from workflow.config.settings import COINS_GECKO_BASE_URL


def test_fetch_trending_coins_success(mock_trending_coins_api):
    result = fetch_trending_coins(n_coins=3)

    assert isinstance(result, CoinsTrendingResponse)
    assert len(result.root) == 3


def test_fetch_trending_coins_invalid_n_coins():
    with pytest.raises(Exception, match="The max number of coins is 15") as excinfo:
        fetch_trending_coins(n_coins=16)


def test_fetch_trending_coins_api_failure(requests_mock):
    url = f"{COINS_GECKO_BASE_URL}/search/trending"
    requests_mock.get(url, status_code=500)

    with pytest.raises(requests.exceptions.HTTPError):
        fetch_trending_coins(n_coins=3)
