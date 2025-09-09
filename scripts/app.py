from fastapi import FastAPI, Query
from fetchers.binance_fetcher import fetch_binance_data
from fetchers.bybit_fetcher import fetch_bybit_data
from fetchers.okx_fetcher import fetch_okx_data
from fetchers.coinbase_fetcher import fetch_coinbase_data
from analysis.analyzer import analyze_klines

app = FastAPI(title="Tea Activity Reporter API", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "Tea Activity Reporter API"}

@app.get("/binance/{token}")
async def get_binance_data(token: str):
    """Fetch data from Binance for the specified token."""
    try:
        data = fetch_binance_data(token)
        analysis = analyze_klines(data)
        return {
            "exchange": "binance",
            "token": token,
            "data": data,
            "analysis": analysis
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/bybit/{token}")
async def get_bybit_data(token: str):
    """Fetch data from Bybit for the specified token."""
    try:
        data = fetch_bybit_data(token)
        analysis = analyze_klines(data)
        return {
            "exchange": "bybit", 
            "token": token,
            "data": data,
            "analysis": analysis
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/okx/{token}")
async def get_okx_data(token: str):
    """Fetch data from OKX for the specified token."""
    try:
        data = fetch_okx_data(token)
        analysis = analyze_klines(data)
        return {
            "exchange": "okx",
            "token": token, 
            "data": data,
            "analysis": analysis
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/coinbase/{token}")
async def get_coinbase_data(token: str):
    """Fetch data from Coinbase for the specified token."""
    try:
        data = fetch_coinbase_data(token)
        analysis = analyze_klines(data)
        return {
            "exchange": "coinbase",
            "token": token,
            "data": data, 
            "analysis": analysis
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/analyze")
async def analyze_all_exchanges(token: str = Query(..., description="Token to analyze across all exchanges")):
    """Analyze a token across all supported exchanges."""
    results = {}
    
    exchanges = {
        "binance": fetch_binance_data,
        "bybit": fetch_bybit_data,
        "okx": fetch_okx_data,
        "coinbase": fetch_coinbase_data
    }
    
    for exchange_name, fetcher_func in exchanges.items():
        try:
            data = fetcher_func(token)
            analysis = analyze_klines(data)
            results[exchange_name] = {
                "data": data,
                "analysis": analysis
            }
        except Exception as e:
            results[exchange_name] = {"error": str(e)}
    
    return {
        "token": token,
        "exchanges": results
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)