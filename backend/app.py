from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv()

from database.models import init_db, log_trade
from data_fetch.prices import get_price
from data_fetch.news import get_news
from sentiment.analyzer import analyze_news_sentiment
from trading_logic.strategy import trade_decision

init_db()

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Financial Trading Bot API"}

@app.get("/trade/{ticker}")
def auto_trade(ticker: str):
    # Use updated get_price (handles yfinance & finnhub)
    price_info = get_price(ticker)
    if "error" in price_info:
        return price_info

    # Use updated get_news (handles yfinance & finnhub)
    news = get_news(ticker)
    for article in news:
        print(f"Title: {article.get('title')}")
        print(f"Source: {article.get('source')}")
        print(f"PubDate: {article.get('pubDate')}")
        print("---")

    sentiment = analyze_news_sentiment(news)

    price_change_pct = ((price_info["current"] - price_info["previous_close"]) / price_info["previous_close"]) * 100

    decision = trade_decision(sentiment, price_change_pct)

    log_trade(
        ticker=ticker,
        price=price_info["current"],
        sentiment_score=sentiment,
        price_change_pct=price_change_pct,
        decision=decision
    )

    return {
        "ticker": ticker,
        "price": price_info,
        "sentiment": sentiment,
        "price_change_pct": round(price_change_pct, 2),
        "decision": decision
    }
