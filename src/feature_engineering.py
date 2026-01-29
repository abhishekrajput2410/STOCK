import ta

def add_features(df):
    df = df.copy()

    df['rsi'] = ta.momentum.RSIIndicator(df['Close']).rsi()
    df['ema_20'] = ta.trend.EMAIndicator(df['Close'], window=20).ema_indicator()
    df['ema_50'] = ta.trend.EMAIndicator(df['Close'], window=50).ema_indicator()

    bb = ta.volatility.BollingerBands(df['Close'])
    df['bb_high'] = bb.bollinger_hband()
    df['bb_low'] = bb.bollinger_lband()

    df['atr'] = ta.volatility.AverageTrueRange(
        df['High'], df['Low'], df['Close']
    ).average_true_range()

    df.dropna(inplace=True)
    return df
