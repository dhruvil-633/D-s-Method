def execute_trade(
    state,
    position,
    current_price
):
    """
    Executes trade and returns (pnl, cumulative_pnl)
    """

    if state.prev_price is None:
        state.prev_price = current_price
        return 0.0, state.cum_pnl

    pnl = position * (current_price - state.prev_price)
    state.cum_pnl += pnl
    state.prev_price = current_price

    return pnl, state.cum_pnl
