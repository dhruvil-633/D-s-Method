def normalized_signal(rt_plus_1: float, sigma_t: float, eps: float = 1e-6) -> float:
    """
    Volatility-normalized execution signal
    """
    return rt_plus_1 / (sigma_t + eps)
