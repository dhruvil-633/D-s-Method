import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


import numpy as np
import pandas as pd

from core.rolling_buffer import RollingFeatureBuffer
from core.volatility import VolatilityEstimator
from core.fusion_config import FusionConfig
from backtest.variants import ALL_VARIANTS
from backtest.fusion_variants import compute_rt_variant
from backtest.metrics import (
    directional_accuracy,
    information_coefficient,
    rmse
)
from models.fnum_model import FNumModel
from core.sentiment_manager import SentimentManager

# -------------------------------------------------
# LOAD DATA (YOU ALREADY HAVE THIS)
# -------------------------------------------------
df = pd.read_csv("data/intraday_data.csv", parse_dates=["Datetime"])

FEATURE_COLUMNS = [
    "ret_1","ret_3","ret_6","hl_range","clv","ema_gap",
    "ret_accel","vol_10","vol_30","vol_ratio","vol_norm",
    "pv","minute_of_day"
]

# -------------------------------------------------
# INIT COMPONENTS
# -------------------------------------------------
buffer = RollingFeatureBuffer()
vol_est = VolatilityEstimator()
fusion_cfg = FusionConfig()
sentiment_mgr = SentimentManager()
fnum = FNumModel(alpha=1.0)

# -------------------------------------------------
# TRAIN FNUM (SIMPLE, ONE PASS)
# -------------------------------------------------
X_train = df[FEATURE_COLUMNS].values
y_train = df["ret_1"].shift(-1).fillna(0).values
fnum.fit(X_train, y_train)

# -------------------------------------------------
# RUN VARIANTS
# -------------------------------------------------
results = {v.name: {"pred": [], "real": []} for v in ALL_VARIANTS}

prev_day = None

for i in range(len(df) - 1):
    row = df.iloc[i]
    feature_row = row[FEATURE_COLUMNS].to_dict()
    trading_day = row["Datetime"].date()

    # -------------------------------
    # HARD daily reset (REQUIRED)
    # -------------------------------
    if prev_day is None or trading_day != prev_day:
        buffer.reset(trading_day)
        sentiment_mgr = SentimentManager()  # reset sentiments
        prev_day = trading_day
        continue  # skip until buffer refills

    buffer.add(feature_row, trading_day)


    if not buffer.is_ready():
        continue

    X = buffer.matrix()
    sigma_t = vol_est.compute(X)
    numeric_out = fnum.predict(X)

    sentiments = sentiment_mgr.values(row["Datetime"])

    for v in ALL_VARIANTS:
        rt = compute_rt_variant(
            numeric_out,
            sigma_t,
            sentiments["Sm"],
            sentiments["Sc"],
            sentiments["Si"],
            fusion_cfg,
            v
        )

        results[v.name]["pred"].append(rt)
        results[v.name]["real"].append(df.iloc[i+1]["ret_1"])

# -------------------------------------------------
# REPORT
# -------------------------------------------------
print("\n===== BACKTEST RESULTS =====\n")

for name, res in results.items():
    pred = np.array(res["pred"])
    real = np.array(res["real"])

    print(f"{name}")
    print("  Directional Acc :", directional_accuracy(pred, real))
    print("  IC              :", information_coefficient(pred, real))
    print("  RMSE            :", rmse(pred, real))
    print("-" * 30)
