from execution.signal import normalized_signal
from execution.thresholds import Thresholds
from execution.position_manager import PositionManager

class Executor:
    def __init__(self, entry=1.0, exit=0.4):
        self.pm = PositionManager()
        self.thresholds = Thresholds(entry, exit)

    def step(self, rt_plus_1: float, sigma_t: float):
        z = normalized_signal(rt_plus_1, sigma_t)
        position = self.pm.update(z, self.thresholds)
        return z, position
