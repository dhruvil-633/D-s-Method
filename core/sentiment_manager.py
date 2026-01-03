from datetime import datetime
from core.sentiment_state import SentimentState

class SentimentManager:
    def __init__(self, decay_lambda: float = 0.03):
        self.state = SentimentState(decay_lambda)

    def update_market(self, score, confidence, weight, ts: datetime):
        self.state.market.update(score, confidence, weight, ts)

    def update_company(self, score, confidence, weight, ts: datetime):
        self.state.company.update(score, confidence, weight, ts)

    def update_index(self, score, confidence, weight, ts: datetime):
        self.state.index.update(score, confidence, weight, ts)

    def values(self, now: datetime):
        return self.state.snapshot(now)
