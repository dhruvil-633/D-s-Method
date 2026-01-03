import time
from datetime import datetime, timezone

from config.market_hours import is_market_open, is_new_trading_day
from config.settings import MAX_CAPITAL
from core.rolling_buffer import RollingFeatureBuffer
from core.feature_engineering import build_features
from core.state import TradingState
from etl.price_etl import fetch_latest_10min
from storage.database import Database
from core.numeric_model import NumericModel


def main():
    buffer = RollingFeatureBuffer(maxlen=40)
    db = Database()
    state = TradingState(MAX_CAPITAL)

    last_bar_time = None

    while True:
        now = datetime.now(timezone.utc)

        if not is_market_open(now):
            print("Market closed. Sleeping 60s.")
            time.sleep(60)
            continue

        bar = fetch_latest_10min("NVDA")
        if bar is None:
            time.sleep(30)
            continue

        bar_time = bar["Datetime"]

        # avoid duplicate processing
        if last_bar_time == bar_time:
            time.sleep(30)
            continue

        # new trading day detection
        if is_new_trading_day(last_bar_time, bar_time):
            print("New trading day detected → resetting state")
            state.reset_day()

        last_bar_time = bar_time

        # append to rolling buffer
        buffer.append(bar)

        if not buffer.is_ready():
            print("Warming up buffer...")
            continue

        # build features
        df = buffer.to_dataframe()
        features = build_features(df).iloc[-1]

        feature_row = features.to_dict()
        feature_row["Datetime"] = str(feature_row["Datetime"])

        # store features
        db.insert("features", feature_row)

        print("Stored features at", feature_row["Datetime"])

        # wait until next cycle
        time.sleep(60)


if __name__ == "__main__":
    main()
