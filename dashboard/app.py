import streamlit as st
import pandas as pd
import sqlite3
import numpy as np

DB_PATH = "ds_method.db"

st.set_page_config(page_title="D’s Method Dashboard", layout="wide")

# -----------------------------
# Database utilities
# -----------------------------
def load_table(table):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql(f"SELECT * FROM {table}", conn)
    conn.close()
    return df

# -----------------------------
# Load data
# -----------------------------
features = load_table("features")
preds = load_table("predictions")
execs = load_table("execution")

for df in [features, preds, execs]:
    if "Datetime" in df.columns:
        df["Datetime"] = pd.to_datetime(df["Datetime"])

# -----------------------------
# Sidebar controls
# -----------------------------
st.sidebar.title("Controls")

available_days = execs["Datetime"].dt.date.unique()
selected_day = st.sidebar.selectbox(
    "Select Trading Day",
    sorted(available_days, reverse=True)
)

# -----------------------------
# Filter selected day
# -----------------------------
day_exec = execs[execs["Datetime"].dt.date == selected_day]
day_pred = preds[preds["Datetime"].dt.date == selected_day]

# -----------------------------
# Top-level metrics (lightweight)
# -----------------------------
st.title("📈 D’s Method – Model Diagnostics Dashboard")

c1, c2, c3 = st.columns(3)

c1.metric("Total PnL", f"{day_exec['pnl'].sum():.2f}")
c2.metric("Trades", (day_exec["position"] != 0).sum())
c3.metric("Avg σₜ", f"{day_pred['sigma_t'].mean():.4f}")

# ======================================================
# SENTIMENT PANEL (MOST IMPORTANT)
# ======================================================
st.subheader("🧠 Sentiment Decomposition (Sm / Sc / Si)")

sent_df = day_pred.set_index("Datetime")[["Sm", "Sc", "Si"]]
st.line_chart(sent_df, use_container_width=True)

# ======================================================
# SIGNAL DECOMPOSITION
# ======================================================
st.subheader("🔍 Signal Decomposition")

sig_df = day_pred.set_index("Datetime")[
    ["numeric_output", "sentiment_effect", "rt_plus_1"]
]

st.line_chart(sig_df, use_container_width=True)

# ======================================================
# VOLATILITY + POSITION
# ======================================================
st.subheader("⚡ Volatility Regime & Position")

vol_pos = pd.DataFrame({
    "sigma_t": day_pred.set_index("Datetime")["sigma_t"],
    "position": day_exec.set_index("Datetime")["position"]
})

st.line_chart(vol_pos, use_container_width=True)

# ======================================================
# EXECUTION (SECONDARY)
# ======================================================
st.subheader("📉 Intraday PnL")

st.line_chart(
    day_exec.set_index("Datetime")["cum_pnl"],
    use_container_width=True
)

# ======================================================
# TRADE LOG
# ======================================================
st.subheader("📄 Trade Log")

st.dataframe(
    day_exec[["Datetime", "position", "pnl", "cum_pnl"]],
    use_container_width=True
)

# ======================================================
# DAILY SUMMARY (HISTORICAL)
# ======================================================
st.subheader("📊 Historical Daily Summary")

daily_summary = (
    execs.assign(day=execs["Datetime"].dt.date)
    .groupby("day")
    .agg(
        daily_pnl=("pnl", "sum"),
        trades=("position", lambda x: (x != 0).sum())
    )
    .reset_index()
)

st.dataframe(daily_summary, use_container_width=True)

st.metric(
    "Average Daily PnL",
    f"{daily_summary['daily_pnl'].mean():.2f}"
)
