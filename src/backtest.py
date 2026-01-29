from src.data_fetcher import fetch_stock_data
from src.feature_engineering import add_features
from src.predict import trade_recommendation
import joblib


# Load models
try:
    low_model = joblib.load("models/low_model.pkl")
    high_model = joblib.load("models/high_model.pkl")
except:
    low_model = None
    high_model = None


def backtest_stock(symbol: str, lookback_days=60):
    """
    Walk-forward backtesting for UI & API
    """

    if low_model is None or high_model is None:
        return {"error": "Models not loaded for backtesting"}

    df = fetch_stock_data(symbol, period="6mo")

    if df is None or df.empty or len(df) < lookback_days + 5:
        return {"error": "Not enough data for backtesting"}

    df = add_features(df)

    correct_direction = 0
    total_predictions = 0

    correct_trade = 0
    total_trades = 0

    # Walk-forward backtesting
    for i in range(lookback_days, len(df) - 1):
        today = df.iloc[i:i + 1]
        tomorrow = df.iloc[i + 1]

        close_price = float(today["Close"].values[0])
        next_close = float(tomorrow["Close"])

        low_pct = float(low_model.predict(today)[0])
        high_pct = float(high_model.predict(today)[0])

        predicted_low = close_price * (1 + low_pct)
        predicted_high = close_price * (1 + high_pct)

        # Predicted direction
        if predicted_high > close_price and predicted_low >= close_price * 0.995:
            predicted_direction = "Bullish"
        elif predicted_low < close_price and predicted_high <= close_price * 1.005:
            predicted_direction = "Bearish"
        else:
            predicted_direction = "Sideways"

        # Actual direction
        if next_close > close_price:
            actual_direction = "Bullish"
        elif next_close < close_price:
            actual_direction = "Bearish"
        else:
            actual_direction = "Sideways"

        if predicted_direction == actual_direction:
            correct_direction += 1

        total_predictions += 1

        # Trade accuracy
        recommendation = trade_recommendation(
            close_price,
            predicted_low,
            predicted_high,
            predicted_direction,
            "Medium"
        )

        if recommendation in ["BUY", "SELL"]:
            total_trades += 1

            if (
                recommendation == "BUY" and next_close > close_price
            ) or (
                recommendation == "SELL" and next_close < close_price
            ):
                correct_trade += 1

    return {
        "symbol": symbol,
        "directional_accuracy": round((correct_direction / total_predictions) * 100, 2),
        "trade_accuracy": round((correct_trade / total_trades) * 100, 2)
        if total_trades > 0 else 0,
        "total_predictions": total_predictions,
        "total_trades": total_trades
    }
