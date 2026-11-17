import os
import yfinance as yf
from supabase import create_client
from datetime import datetime, timedelta

supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_SECRET_KEY"])

def ingest_stock_data(symbol: str):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)

    ticker = yf.Ticker(symbol)
    df = ticker.history(start=start_date, end=end_date)

    if not df.empty:
        initial_p = float(df['Close'].iloc[0])
        final_p = float(df['Close'].iloc[-1])

        data = {
            "ticker": symbol.upper(),
            "initial_price": initial_p,
            "final_price": final_p
        }
        supabase.table("stock_records").insert(data).execute()
        print(f"Successfully ingested {symbol}")

ingest_stock_data("AAPL")
ingest_stock_data("TSLA")
ingest_stock_data("MSFT")
ingest_stock_data("NVDA")
ingest_stock_data("AMZN")