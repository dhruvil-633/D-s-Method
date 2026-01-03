class Thresholds:
    def __init__(self, entry: float = 1.0, exit: float = 0.4):
        assert exit < entry, "Exit threshold must be smaller than entry"
        self.entry = entry
        self.exit = exit
