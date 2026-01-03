from core.daily_summary import compute_daily_summary


def daily_reset(
    rolling_buffer,
    sentiment_manager,
    intraday_writer,
    fusion_rows,
    db,
    trade_date
):
    # flush remaining rows
    intraday_writer.flush_features()
    intraday_writer.flush_fusion()

    # compute & store summary
    summary = compute_daily_summary(fusion_rows)
    summary["date"] = trade_date
    db.insert("daily_summary", summary)

    # HARD RESET
    rolling_buffer.reset()
    sentiment_manager.state = sentiment_manager.state.__class__()
    fusion_rows.clear()
