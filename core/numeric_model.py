import numpy as np
import pandas as pd
from sklearn.linear_model import Lasso
from sklearn.preprocessing import StandardScaler
import joblib
import os

FEATURE_COLS = [
    "ret_1","ret_3","ret_6",
    "hl_range","clv","ema_gap","ret_accel",
    "vol_10","vol_30","vol_ratio","vol_norm",
    "pv","minute_of_day"
]

MODEL_PATH = "model/lasso_model.pkl"
SCALER_PATH = "model/scaler.pkl"

class NumericModel:
    def __init__(self):
        self.model = None
        self.scaler = None
        self._load_or_init()

    def _load_or_init(self):
        if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH):
            self.model = joblib.load(MODEL_PATH)
            self.scaler = joblib.load(SCALER_PATH)
        else:
            self.model = Lasso(alpha=0.0005, max_iter=5000)
            self.scaler = StandardScaler()

    def train(self, df: pd.DataFrame):
        df = df.dropna()
        if len(df) < 100:
            return

        X = df[FEATURE_COLS]
        y = df["target"]

        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)

        os.makedirs("model", exist_ok=True)
        joblib.dump(self.model, MODEL_PATH)
        joblib.dump(self.scaler, SCALER_PATH)

    def predict(self, row: pd.Series) -> float:
        X = row[FEATURE_COLS].values.reshape(1, -1)
        X_scaled = self.scaler.transform(X)
        return float(self.model.predict(X_scaled)[0])
