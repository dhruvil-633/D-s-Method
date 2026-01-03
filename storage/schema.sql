CREATE TABLE IF NOT EXISTS features (
    Datetime TEXT PRIMARY KEY,
    ret_1 REAL, ret_3 REAL, ret_6 REAL,
    hl_range REAL, clv REAL, ema_gap REAL, ret_accel REAL,
    vol_10 REAL, vol_30 REAL, vol_ratio REAL, vol_norm REAL,
    pv REAL, minute_of_day REAL,
    target REAL
);

CREATE TABLE IF NOT EXISTS predictions (
    Datetime TEXT,
    r_hat REAL,
    z_score REAL,
    decision TEXT,
    position INTEGER
);

CREATE TABLE IF NOT EXISTS trades (
    Datetime TEXT,
    position INTEGER,
    pnl REAL,
    cum_pnl REAL
);

CREATE TABLE IF NOT EXISTS predictions (
    Datetime TEXT PRIMARY KEY,
    r_hat_num REAL,
    r_hat_final REAL,
    z_score REAL,
    decision TEXT,
    position INTEGER
);

CREATE TABLE IF NOT EXISTS execution (
    Datetime TEXT PRIMARY KEY,
    price REAL,
    position INTEGER,
    pnl REAL,
    cum_pnl REAL
);

CREATE TABLE IF NOT EXISTS verification (
    Datetime TEXT PRIMARY KEY,
    realized_return REAL,
    direction_correct INTEGER,
    abs_error REAL
);
