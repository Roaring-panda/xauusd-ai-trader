# Main Flask/FastAPI application
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def status():
    return {
        "status": "running",
        "symbol": "XAUUSD"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}
