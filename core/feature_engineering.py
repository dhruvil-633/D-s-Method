import numpy as np
import pandas as pd

def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Input df must contain:
    Datetime, Open, High, Low, Close, Volume
    """

    df = df.copy()

    # returns
    df["ret_1"] = df["Close"].pct_change(1)
    df["ret_3"] = df["Close"].pct_change(3)
    df["ret_6"] = df["Close"].pct_change(6)

    # ranges
    df["hl_range"] = (df["High"] - df["Low"]) / df["Close"]

    # close location value
    df["clv"] = (
        (df["Close"] - df["Low"]) -
        (df["High"] - df["Close"])
    ) / (df["High"] - df["Low"] + 1e-9)

    # EMA gap
    ema_fast = df["Close"].ewm(span=6).mean()
    ema_slow = df["Close"].ewm(span=18).mean()
    df["ema_gap"] = (ema_fast - ema_slow) / df["Close"]

    # return acceleration
    df["ret_accel"] = df["ret_1"] - df["ret_3"]

    # volatility
    df["vol_10"] = df["ret_1"].rolling(10).std()
    df["vol_30"] = df["ret_1"].rolling(30).std()
    df["vol_ratio"] = df["vol_10"] / (df["vol_30"] + 1e-9)
    df["vol_norm"] = df["vol_10"] / (df["vol_10"].mean() + 1e-9)

    # price-volume interaction
    df["pv"] = df["Close"] * df["Volume"]

    # time
    df["minute_of_day"] = (
        df["Datetime"].dt.hour * 60 + df["Datetime"].dt.minute
    )

    # target (next-bar return)
    df["target"] = df["Close"].pct_change().shift(-1)

    return df
