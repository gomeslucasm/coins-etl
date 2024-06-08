from typing import List
import pandas as pd


def calculate_moving_average(values: List[float], window: int) -> List[float]:
    """
    Calculate the moving average of a list of values.

    The moving average is a widely used indicator in technical analysis that helps smooth out price data
    by creating a constantly updated average price. It is used to identify the direction of the trend.

    Args:
        prices (list): List of price values.
        window (int): The window size for the moving average.

    Returns:
        list: Moving average values.
    """
    return pd.Series(values).rolling(window=window).mean().tolist()


def calculate_rsi(values: List[float], window: int) -> List[float]:
    """
    Calculate the Relative Strength Index (RSI) of a list of values.

    The Relative Strength Index (RSI) is a momentum oscillator that measures the speed and change of price movements.
    RSI oscillates between 0 and 100. Traditionally, and according to Wilder, RSI is considered overbought when above 70
    and oversold when below 30. RSI can also be used to identify the general trend.

    Args:
        values (list): List of price values.
        window (int): The window size for the RSI calculation.

    Returns:
        list: RSI values.
    """
    values_series = pd.Series(values)

    deltas = values_series.diff()

    gains = deltas.where(deltas > 0, 0)
    losses = -deltas.where(deltas < 0, 0)

    avg_gain = gains.rolling(window=window).mean()
    avg_loss = losses.rolling(window=window).mean()

    rs = avg_gain / avg_loss

    rsi = 100 - (100 / (1 + rs))

    return rsi.tolist()
