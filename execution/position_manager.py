from execution.thresholds import Thresholds


class PositionManager:
    """
    Hysteresis-based position state machine
    """

    def __init__(self):
        self.position = 0  # -1 short, 0 flat, +1 long

    def update(self, z: float, thresholds: Thresholds) -> int:
        # ENTRY
        if self.position == 0:
            if z > thresholds.entry:
                self.position = 1
            elif z < -thresholds.entry:
                self.position = -1

        # EXIT
        elif self.position == 1:
            if z < thresholds.exit:
                self.position = 0

        elif self.position == -1:
            if z > -thresholds.exit:
                self.position = 0

        return self.position
