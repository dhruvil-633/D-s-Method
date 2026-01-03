def compute_rt_variant(
    numeric_output,
    sigma_t,
    Sm, Sc, Si,
    cfg,
    variant
):
    sentiment_linear = (
        cfg.w_market * Sm +
        cfg.w_company * Sc +
        cfg.w_index * Si
    )

    interaction = cfg.theta * Si * Sc

    sentiment_block = 0.0

    if variant.use_linear_sentiment:
        sentiment_block += sentiment_linear

    if variant.use_interaction:
        sentiment_block += interaction

    return numeric_output + sigma_t * sentiment_block
