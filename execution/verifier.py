def cross_verify(
    predicted_return,
    prev_close,
    current_close
):
    """
    Returns:
    - realized_return
    - direction_correct (0/1)
    - abs_error
    """

    if prev_close == 0:
        return 0.0, 0, 0.0

    realized_return = (current_close - prev_close) / prev_close
    direction_correct = int(
        (predicted_return > 0 and realized_return > 0) or
        (predicted_return < 0 and realized_return < 0)
    )

    abs_error = abs(predicted_return - realized_return)

    return realized_return, direction_correct, abs_error
