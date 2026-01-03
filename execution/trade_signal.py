from dataclasses import dataclass

@dataclass
class TradeSignal:
    timestamp: str
    z_score: float
    position: int   # -1, 0, +1
