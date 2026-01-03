def compute_daily_summary(fusion_rows):
    n = len(fusion_rows)

    avg_rt = sum(r["rt_plus_1"] for r in fusion_rows) / n
    avg_num = sum(r["numeric_output"] for r in fusion_rows) / n
    avg_sigma = sum(r["sigma_t"] for r in fusion_rows) / n
    avg_sent = sum(r["sentiment_effect"] for r in fusion_rows) / n

    alignment = sum(
        r["sentiment_linear"] * r["numeric_output"]
        for r in fusion_rows
    ) / n

    return {
        "n_points": n,
        "avg_rt_plus_1": avg_rt,
        "avg_numeric": avg_num,
        "avg_sigma": avg_sigma,
        "avg_sentiment_effect": avg_sent,
        "sentiment_alignment_score": alignment
    }
