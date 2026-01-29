import joblib
from src.data_fetcher import fetch_stock_data
from src.feature_engineering import add_features

# OPTIONAL modules – wrapped safely
try:
    from src.index_trend import get_index_trend
except:
    get_index_trend = None

try:
    from src.news_sentiment import get_news_sentiment
except:
    get_news_sentiment = None


# Load models safely
try:
    low_model = joblib.load("models/low_model.pkl")
    high_model = joblib.load("models/high_model.pkl")
except:
    low_model = None
    high_model = None


# -----------------------------
# FINAL MARKET DECISION
# -----------------------------
def final_market_decision(stock_move, nifty_trend, news_sentiment):
    score = 0

    if stock_move == "Bullish":
        score += 1
    if nifty_trend == "Bullish":
        score += 1
    if news_sentiment == "Positive":
        score += 1

    if score >= 2:
        return "Bullish"
    elif score <= 0:
        return "Bearish"
    else:
        return "Sideways"


# -----------------------------
# BUY / SELL / HOLD LOGIC
# -----------------------------
def trade_recommendation(
    close_price,
    predicted_low,
    predicted_high,
    final_market_move,
    confidence
):
    upside = (predicted_high - close_price) / close_price
    downside = (close_price - predicted_low) / close_price

    if (
        final_market_move == "Bullish"
        and confidence in ["Medium", "High"]
        and upside > downside
        and upside > 0.01
    ):
        return "BUY"

    if (
        final_market_move == "Bearish"
        and confidence in ["Medium", "High"]
        and downside > upside
        and downside > 0.01
    ):
        return "SELL"

    return "HOLD"


# -----------------------------
# MAIN PREDICTION FUNCTION
# -----------------------------
def predict_stock(symbol: str):
    try:
        # 1️⃣ Fetch recent data (3 months)
        df = fetch_stock_data(symbol)

        if df is None or df.empty:
            return {"error": "No data fetched for symbol"}

        df = add_features(df)

        if df.empty:
            return {"error": "Not enough data after feature engineering"}

        latest = df.iloc[-1:]

        # 2️⃣ Model check
        if low_model is None or high_model is None:
            return {"error": "Models not loaded properly"}

        low_pct = float(low_model.predict(latest)[0])
        high_pct = float(high_model.predict(latest)[0])

        close_price = float(latest["Close"].values[0])

        # 3️⃣ Price prediction
        predicted_low = close_price * (1 + low_pct)
        predicted_high = close_price * (1 + high_pct)

        # ---- GAP LOGIC ----
        gap_signal = "Normal Open"

        if predicted_low > close_price:
            gap_signal = "Gap-Up Expected"
            predicted_low = close_price * 0.998

        elif predicted_high < close_price:
            gap_signal = "Gap-Down Expected"
            predicted_high = close_price * 1.002

        # 4️⃣ Stock-only move
        if predicted_high > close_price and predicted_low >= close_price * 0.995:
            stock_move = "Bullish"
        elif predicted_low < close_price and predicted_high <= close_price * 1.005:
            stock_move = "Bearish"
        else:
            stock_move = "Sideways"

        # 5️⃣ Index trend (SAFE)
        if get_index_trend:
            try:
                nifty_trend = get_index_trend("^NSEI")
            except:
                nifty_trend = "Sideways"
        else:
            nifty_trend = "Sideways"

        # 6️⃣ News sentiment (SAFE)
        if get_news_sentiment:
            try:
                news_sentiment = get_news_sentiment(symbol)
            except:
                news_sentiment = "Neutral"
        else:
            news_sentiment = "Neutral"

        # 7️⃣ Final market move
        final_move = final_market_decision(
            stock_move, nifty_trend, news_sentiment
        )

        # 8️⃣ Confidence
        range_pct = (predicted_high - predicted_low) / close_price
        if range_pct > 0.03:
            confidence = "High"
        elif range_pct > 0.015:
            confidence = "Medium"
        else:
            confidence = "Low"

        # 9️⃣ BUY / SELL / HOLD
        recommendation = trade_recommendation(
            close_price,
            predicted_low,
            predicted_high,
            final_move,
            confidence
        )

        return {
            "stock": symbol,
            "current_close": round(close_price, 2),
            "predicted_low": round(predicted_low, 2),
            "predicted_high": round(predicted_high, 2),
            "expected_range": f"{round(predicted_low,2)} - {round(predicted_high,2)}",
            "gap_signal": gap_signal,
            "stock_move": stock_move,
            "index_trend": nifty_trend,
            "news_sentiment": news_sentiment,
            "final_market_move": final_move,
            "confidence": confidence,
            "recommendation": recommendation
        }

    except Exception as e:
        return {
            "error": "Internal prediction error",
            "details": str(e)
        }
