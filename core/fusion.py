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
        """
        D's Method (FINAL):
        r_{t+1} = f_num(X_t) + sigma_t * (Σ w_k S_k + θ S_i S_c)
        """

        # 1. Weighted sentiment sum
        sentiment_linear = (
            self.cfg.w_market * Sm +
            self.cfg.w_company * Sc +
            self.cfg.w_index * Si
        )

        # 2. Cross interaction (UNSCALED here)
        cross_interaction = self.cfg.theta * Si * Sc

        # 3. FULL sentiment block (IMPORTANT)
        sentiment_block = sentiment_linear + cross_interaction

        # 4. Volatility-scaled sentiment effect
        sentiment_effect = sigma_t * sentiment_block

        # 5. Final prediction
        r_t_plus_1 = numeric_output + sentiment_effect

        return {
            "rt_plus_1": r_t_plus_1,
            "numeric_output": numeric_output,
            "sigma_t": sigma_t,
            "sentiment_linear": sentiment_linear,
            "cross_interaction": cross_interaction,
            "sentiment_effect": sentiment_effect
        }
