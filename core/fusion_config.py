from dataclasses import dataclass

@dataclass(frozen=True)
class FusionConfig:
    theta: float = 0.1

    w_market: float = 0.4
    w_company: float = 0.4
    w_index: float = 0.2
