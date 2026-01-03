from config.settings import (
    TRADING_COST,
    Z_THRESHOLD,
    TRADE_FRACTION
)

MAX_POSITION = 1000


def make_decision(r_hat, vol):
    """
    Returns (decision, position, z_score)
    """

    if vol <= 0:
        return "FLAT", 0, 0.0

    z = r_hat / vol

    # cost & confidence filter
    if abs(r_hat) <= TRADING_COST or abs(z) <= Z_THRESHOLD:
        return "FLAT", 0, z

    position = int(
        (1 if z > 0 else -1)
        * TRADE_FRACTION
        * MAX_POSITION
    )

    return (
        "LONG" if position > 0 else "SHORT",
        position,
        z
    )
