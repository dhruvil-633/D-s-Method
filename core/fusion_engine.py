class FusionEngine:
    def __init__(self, config):
        self.cfg = config

    def compute(
        self,
        numeric_output: float,
        sigma_t: float,
        Sm: float,
        Sc: float,
        Si: float
    ) -> dict:
        # weighted sentiment
        sentiment_linear = (
            self.cfg.w_market * Sm +
            self.cfg.w_company * Sc +
            self.cfg.w_index * Si
        )

        # cross interaction
        cross_interaction = self.cfg.theta * Si * Sc

        sentiment_block = sentiment_linear + cross_interaction

        # volatility-scaled correction
        sentiment_effect = sigma_t * sentiment_block

        r_t_plus_1 = numeric_output + sentiment_effect

        return {
            "rt_plus_1": r_t_plus_1,
            "numeric": numeric_output,
            "sigma_t": sigma_t,
            "sentiment_linear": sentiment_linear,
            "cross_interaction": cross_interaction,
            "sentiment_effect": sentiment_effect
        }
