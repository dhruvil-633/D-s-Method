INTRADAY_FEATURES = [
    "date",
    "time",
    "ret_1","ret_3","ret_6",
    "hl_range","clv","ema_gap","ret_accel",
    "vol_10","vol_30","vol_ratio","vol_norm",
    "pv","minute_of_day"
]

FUSION_OUTPUTS = [
    "date",
    "time",
    "numeric_output",
    "sigma_t",
    "Sm","Sc","Si",
    "sentiment_linear",
    "cross_interaction",
    "sentiment_effect",
    "rt_plus_1"
]

DAILY_SUMMARY = [
    "date",
    "n_points",
    "avg_rt_plus_1",
    "avg_numeric",
    "avg_sigma",
    "avg_sentiment_effect",
    "sentiment_alignment_score"
]
