from datetime import datetime, time
import pytz

IST = pytz.timezone("Asia/Kolkata")

MARKET_OPEN = time(9, 15)
MARKET_CLOSE = time(15, 30)

def is_market_open(now=None):
    now = now or datetime.now(IST)
    t = now.time()
    return MARKET_OPEN <= t <= MARKET_CLOSE
