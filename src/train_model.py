import os
import joblib
from xgboost import XGBRegressor
from src.data_fetcher import fetch_stock_data
from src.feature_engineering import add_features

os.makedirs("models", exist_ok=True)

df = fetch_stock_data("INFY.NS")
df = add_features(df)

# Targets
df["low_target"] = (df["Low"].shift(-1) - df["Close"]) / df["Close"]
df["high_target"] = (df["High"].shift(-1) - df["Close"]) / df["Close"]
df.dropna(inplace=True)

X = df.drop(columns=["low_target", "high_target"])
y_low = df["low_target"]
y_high = df["high_target"]

low_model = XGBRegressor(n_estimators=300, learning_rate=0.05, max_depth=5)
high_model = XGBRegressor(n_estimators=300, learning_rate=0.05, max_depth=5)

low_model.fit(X, y_low)
high_model.fit(X, y_high)

joblib.dump(low_model, "models/low_model.pkl")
joblib.dump(high_model, "models/high_model.pkl")

print("✅ Low & High models trained and saved")
