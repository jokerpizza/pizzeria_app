
import asyncio
import datetime
from .ingestor_rest import fetch_and_store

async def scheduler():
    while True:
        try:
            added = await asyncio.to_thread(fetch_and_store)
            print(f"Fetched {added} new order items")
        except Exception as e:
            print("Scheduler error:", e)
        await asyncio.sleep(300)  # 5 minutes
