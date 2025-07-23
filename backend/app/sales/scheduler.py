
import asyncio
import logging
from .ingestor_rest import fetch_and_store

logger = logging.getLogger("sales_scheduler")

async def loop():
    logger.info("Sales scheduler started.")
    while True:
        try:
            fetch_and_store()
        except Exception as exc:
            logger.exception("Error during fetch_and_store: %s", exc)
        await asyncio.sleep(300)  # 5 minutes
