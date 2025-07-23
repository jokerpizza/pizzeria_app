
import asyncio
import datetime as dt
from .ingestor_rest import fetch_orders_period, store_orders

async def scheduler():
    while True:
        try:
            before = dt.datetime.utcnow()
            after = before - dt.timedelta(minutes=5)
            rows = await fetch_orders_period(after, before)
            new_items = await store_orders(rows)
            print(f"Fetched {new_items} new order items")
        except Exception as e:
            print("Scheduler error:", e)
        await asyncio.sleep(300)
