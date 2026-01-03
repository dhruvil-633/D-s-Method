import numpy as np

class VolatilityEstimator:
    def __init__(self, lookback: int = 10, vol_floor: float = 1e-5):
        self.lookback = lookback
        self.vol_floor = vol_floor

    def compute(self, buffer_matrix: np.ndarray) -> float:
        """
        Compute realized short-horizon volatility σₜ.

        Parameters
        ----------
        buffer_matrix : np.ndarray
            Shape (40, num_features)
            ret_1 must be column 0

        Returns
        -------
        float
            σₜ >= vol_floor
        """

        if buffer_matrix.shape[0] < self.lookback:
            raise RuntimeError("Insufficient buffer for volatility")

        returns = buffer_matrix[-self.lookback:, 0]

        # numerical safety
        if np.any(np.isnan(returns)) or np.any(np.isinf(returns)):
            raise ValueError("Invalid returns for volatility")

        sigma = np.std(returns, ddof=1)

        # hard floor (prevents division blow-ups)
        return max(sigma, self.vol_floor)
