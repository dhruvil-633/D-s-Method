from datetime import datetime, time
import pytz

NY = pytz.timezone("America/New_York")

MARKET_OPEN = time(9, 30)
MARKET_CLOSE = time(16, 0)

def is_market_open(now_utc: datetime) -> bool:
    now_ny = now_utc.astimezone(NY)

    # Monday = 0, Sunday = 6
    if now_ny.weekday() >= 5:
        return False

    return MARKET_OPEN <= now_ny.time() <= MARKET_CLOSE


def is_new_trading_day(prev_dt, current_dt) -> bool:
    if prev_dt is None:
        return True
    return prev_dt.date() != current_dt.date()
