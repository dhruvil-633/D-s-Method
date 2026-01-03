import numpy as np
from sklearn.linear_model import Ridge
import joblib

class FNumModel:
    """
    Frozen numeric model for D's Method
    Deterministic, reproducible
    """

    def __init__(self, alpha=1.0):
        self.model = Ridge(alpha=alpha)
        self.is_fitted = False

    def fit(self, X: np.ndarray, y: np.ndarray):
        self.model.fit(X, y)
        self.is_fitted = True

    def predict(self, X: np.ndarray) -> float:
        if not self.is_fitted:
            raise RuntimeError("fnum model not fitted")
        # use last row only (current time)
        return float(self.model.predict(X[-1].reshape(1, -1))[0])

    def save(self, path: str):
        joblib.dump(self.model, path)

    def load(self, path: str):
        self.model = joblib.load(path)
        self.is_fitted = True
