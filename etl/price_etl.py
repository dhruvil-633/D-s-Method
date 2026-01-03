import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta, timezone

def fetch_latest_10min(symbol="NVDA"):
    """
    Fetch last 2 hours to ensure we get the most recent closed 10-min bar.
    """
    end = datetime.now(timezone.utc)
    start = end - timedelta(hours=2)

    df = yf.download(
        symbol,
        start=start,
        end=end,
        interval="10m",
        progress=False
    )

    if df.empty:
        return None

    df = df.reset_index()

    # Normalize column names
    df.rename(columns={
        "Datetime": "Datetime",
        "Open": "Open",
        "High": "High",
        "Low": "Low",
        "Close": "Close",
        "Volume": "Volume"
    }, inplace=True)

    # Return only last fully closed bar
    return df.iloc[-1].to_dict()
