import math
from datetime import datetime

class SentimentChannel:
    def __init__(self, decay_lambda: float = 0.03):
        """
        decay_lambda: exponential decay per minute
        """
        self.decay_lambda = decay_lambda
        self.raw_score = 0.0
        self.confidence = 0.0
        self.source_weight = 0.0
        self.last_timestamp: datetime | None = None

    def update(
        self,
        score: float,
        confidence: float,
        source_weight: float,
        timestamp: datetime
    ):
        self.raw_score = score
        self.confidence = confidence
        self.source_weight = source_weight
        self.last_timestamp = timestamp

    def value(self, now: datetime) -> float:
        if self.last_timestamp is None:
            return 0.0

        dt_minutes = (now - self.last_timestamp).total_seconds() / 60.0

        decay = math.exp(-self.decay_lambda * dt_minutes)

        return (
            self.raw_score
            * self.confidence
            * self.source_weight
            * decay
        )
