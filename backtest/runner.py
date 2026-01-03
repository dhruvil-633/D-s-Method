from backtest.fusion_variants import compute_rt_variant


def run_backtest(
    data,
    buffer,
    vol_estimator,
    fusion_cfg,
    sentiment_manager,
    fnum_model,
    variants
):
    results = {v.name: [] for v in variants}

    for t in range(len(data) - 1):

        buffer.add(data[t]["features"], data[t]["day"])

        if not buffer.is_ready():
            continue

        X = buffer.matrix()
        sigma_t = vol_estimator.compute(X)

        numeric_output = fnum_model.predict(X)

        sentiments = sentiment_manager.values(data[t]["timestamp"])

        for v in variants:
            rt_pred = compute_rt_variant(
                numeric_output,
                sigma_t,
                sentiments["Sm"],
                sentiments["Sc"],
                sentiments["Si"],
                fusion_cfg,
                v
            )

            results[v.name].append({
                "timestamp": data[t]["timestamp"],
                "rt_pred": rt_pred,
                "real": data[t+1]["ret_1"],
                "sigma_t": sigma_t
            })

    return results
