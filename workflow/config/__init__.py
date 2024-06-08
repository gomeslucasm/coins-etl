import os


class Environment:
    COINS_GECKO_BASE_URL = "https://api.coingecko.com/api/v3"
    PRICE_CHANGE_PERCENTAGE_24H_USD_TRESHOLD = 15
    SIMULATE_TIMEOUT_FETCH_TRENDING_COINS = (
        os.getenv("SIMULATE_TIMEOUT_FETCH_TRENDING_COINS", "true") == "true"
    )
    RSI_OVERBOUGHT_THRESHOLD = 70
    RSI_OVERSOLD_THRESHOLD = 30


ENVIRONMENT = Environment()
