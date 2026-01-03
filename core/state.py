class TradingState:
    def __init__(self, max_capital):
        self.max_capital = max_capital
        self.reset_day()

    def reset_day(self):
        self.remaining_capital = self.max_capital
        self.daily_pnl = 0.0
        self.trade_count = 0
