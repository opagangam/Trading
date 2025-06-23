def trade_decision(sentiment_score: float, price_change_pct: float):
    if sentiment_score > 0.3 and price_change_pct > 0.1:
        return "BUY"
    elif sentiment_score < -0.3:
        return "SELL"
    return "HOLD"
