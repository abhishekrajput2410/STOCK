import yfinance as yf
import ta

def get_index_trend(index_symbol):
    df = yf.download(index_symbol, period="6mo", interval="1d")
    df.dropna(inplace=True)

    df["ema_20"] = ta.trend.EMAIndicator(df["Close"], 20).ema_indicator()
    df["ema_50"] = ta.trend.EMAIndicator(df["Close"], 50).ema_indicator()

    latest = df.iloc[-1]

    if latest["ema_20"] > latest["ema_50"]:
        return "Bullish"
    elif latest["ema_20"] < latest["ema_50"]:
        return "Bearish"
    else:
        return "Sideways"
