
import asyncio
from .ingestor_rest import fetch_and_store_period

async def scheduler():
    while True:
        try:
            new_items = await fetch_and_store_period()
            print(f"Fetched {new_items} new order items")
        except Exception as e:
            print("Scheduler error:", e)
        await asyncio.sleep(300)  # 5 minutes
