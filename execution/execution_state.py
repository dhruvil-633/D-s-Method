class ExecutionState:
    def __init__(self):
        self.prev_price = None
        self.cum_pnl = 0.0

    def reset_day(self):
        self.prev_price = None
        self.cum_pnl = 0.0
