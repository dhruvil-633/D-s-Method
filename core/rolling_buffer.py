from collections import deque
import numpy as np
from core.feature_schema import FEATURE_COLUMNS, WINDOW_SIZE

class RollingFeatureBuffer:
    def __init__(self):
        self.buffer = deque(maxlen=WINDOW_SIZE)
        self.current_day = None

    # -----------------------------
    # Daily reset enforcement
    # -----------------------------
    def reset(self, trading_day=None):
        self.buffer.clear()
        self.current_day = trading_day

    # -----------------------------
    # Add one feature row
    # -----------------------------
    def add(self, feature_row: dict, trading_day):
        # HARD cross-day check
        if self.current_day is None:
            self.current_day = trading_day
        elif trading_day != self.current_day:
            raise RuntimeError(
                "Cross-day feature insertion detected. "
                "Call reset() at market close."
            )

        # STRICT schema enforcement
        for col in FEATURE_COLUMNS:
            if col not in feature_row:
                raise ValueError(f"Missing feature: {col}")

        # Ordered numeric row
        row = np.array(
            [feature_row[col] for col in FEATURE_COLUMNS],
            dtype=float
        )

        # HARD numeric validation
        if np.any(np.isnan(row)) or np.any(np.isinf(row)):
            raise ValueError("Invalid feature row (NaN or Inf)")

        self.buffer.append(row)

    # -----------------------------
    # Readiness check
    # -----------------------------
    def is_ready(self) -> bool:
        return len(self.buffer) == WINDOW_SIZE

    # -----------------------------
    # Matrix view (model input)
    # -----------------------------
    def matrix(self) -> np.ndarray:
        if not self.is_ready():
            raise RuntimeError(
                f"Rolling buffer not full: "
                f"{len(self.buffer)}/{WINDOW_SIZE}"
            )
        return np.vstack(self.buffer)

    # -----------------------------
    # Latest row
    # -----------------------------
    def latest(self) -> np.ndarray:
        if not self.buffer:
            raise RuntimeError("Rolling buffer empty")
        return self.buffer[-1]
