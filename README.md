# 📈 Stock Prediction System

An ML-based stock market prediction system that predicts:
- Next-day High & Low
- Gap-Up / Gap-Down
- Buy / Sell / Hold recommendation
- Backtesting accuracy

## 🔧 Tech Stack
- Python
- FastAPI
- Machine Learning (Scikit-learn)
- Yahoo Finance (yfinance)
- HTML, CSS, JavaScript

## 🚀 Features
- 3-month rolling window prediction
- NIFTY index confirmation
- News sentiment analysis
- Walk-forward backtesting
- Interactive UI dashboard

## ▶️ How to Run

```bash
python -m uvicorn api.main:app --reload
