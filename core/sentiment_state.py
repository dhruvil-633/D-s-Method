from core.sentiment_channel import SentimentChannel
from datetime import datetime

class SentimentState:
    def __init__(self, decay_lambda: float = 0.03):
        self.market = SentimentChannel(decay_lambda)
        self.company = SentimentChannel(decay_lambda)
        self.index = SentimentChannel(decay_lambda)

    def snapshot(self, now: datetime) -> dict:
        return {
            "Sm": self.market.value(now),
            "Sc": self.company.value(now),
            "Si": self.index.value(now)
        }
