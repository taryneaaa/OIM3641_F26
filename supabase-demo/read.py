import os

from supabase import create_client

# The publishable key: allowed to do only what the table's rules permit
supabase = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_PUBLISHABLE_KEY"])

rows = supabase.table("stock_records").select("ticker, initial_price, final_price, percent_change").execute().data
for row in rows:
    print(row)

