import os

from fastapi import FastAPI, HTTPException
from supabase import create_client

app = FastAPI()

supabase = create_client(
    os.environ["SUPABASE_URL"],
    os.environ["SUPABASE_PUBLISHABLE_KEY"],
)


@app.get("/analyze/{symbol}")
def analyze(symbol: str):
    response = (
        supabase.table("stock_records")
        .select("*")
        .eq("ticker", symbol.upper())
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )
    if not response.data:
        raise HTTPException(status_code=404, detail=f"No data for {symbol.upper()}")

    row = response.data[0]
    signal = "Bullish" if row["percent_change"] > 0 else "Bearish"
    return {
        "ticker": row["ticker"],
        "initial_price": row["initial_price"],
        "final_price": row["final_price"],
        "percent_change": row["percent_change"],
        "signal": signal,
    }

@app.get("/history/{symbol}")
def history(symbol: str):
    response = (
        supabase.table("stock_records")
        .select("ticker, initial_price, final_price, percent_change, created_at")
        .eq("ticker", symbol.upper())
        .order("created_at")
        .execute()
    )
    if not response.data:
        raise HTTPException(status_code=404, detail=f"No data for {symbol.upper()}")
    return response.data