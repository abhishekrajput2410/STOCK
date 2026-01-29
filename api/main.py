from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from src.predict import predict_stock

app = FastAPI(title="Stock Prediction System")

# Serve UI
app.mount("/ui", StaticFiles(directory="ui"), name="ui")

@app.get("/")
def home():
    return FileResponse("ui/index.html")

@app.get("/predict")
def predict(symbol: str = Query(..., examples=["INFY.NS"])):
    return predict_stock(symbol)
