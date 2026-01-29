import yfinance as yf

def fetch_stock_data(symbol, period="6y"):
    stock = yf.Ticker(symbol)
    df = stock.history(period=period)

    df = df[['Open', 'High', 'Low', 'Close', 'Volume']]
    df.dropna(inplace=True)

    return df
