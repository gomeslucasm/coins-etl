import pytest
import requests_mock

import json
import os

from workflow.config import ENVIRONMENT, Environment


@pytest.fixture
def requests_mock():
    """
    Fixture que configura o requests_mock para mockar chamadas HTTP.
    """
    with requests_mock.Mocker() as m:
        yield m


@pytest.fixture
def mock_trending_coins_api(requests_mock):
    """
    Fixture que mocka a resposta da API de trending coins do CoinGecko.
    """

    f = open(os.path.join(os.path.dirname(__file__), "mock", "trending_endpoint.json"))
    data = json.load(f)
    url = f"{ENVIRONMENT.COINS_GECKO_BASE_URL}/search/trending"
    requests_mock.get(
        url,
        json=data,
    )
    return requests_mock


@pytest.fixture()
def mocked_database(mocker):
    FakeDataBase = mocker.patch("workflow.utils.db.DataBase")
    return FakeDataBase()


@pytest.fixture()
def mocked_notification_service(mocker):
    FakeNotificationService = mocker.patch(
        "workflow.utils.notification.NotificationService"
    )
    return FakeNotificationService()


@pytest.fixture
def disable_timeout_simulation(mocker):
    class MockedEnvironment(Environment):
        SIMULATE_TIMEOUT_FETCH_TRENDING_COINS = False

    mocker.patch("workflow.tasks.extract.ENVIRONMENT", MockedEnvironment())
