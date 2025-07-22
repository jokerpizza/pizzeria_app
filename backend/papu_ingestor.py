""" 
Papu.io → RabbitMQ ingestor
---------------------------------------

- Loguje się do panelu admin.papu.io za pomocą Playwright.
- Co 60 s pobiera nowe sprzedaże z ostatnich 2 min.
- Publikuje każdą pozycję jako JSON do kolejki RabbitMQ (`pos_sales`).

Zmienne środowiskowe:
    PAPU_EMAIL            – login do Papu.io
    PAPU_PASSWORD         – hasło
    PAPU_COMPANY_ID       – np. "758"
    PAPU_LOCALIZATION_ID  – np. "801"
    RABBIT_URL            – amqp://guest:guest@localhost:5672/
    RABBIT_QUEUE          – domyślnie "pos_sales"

Uruchomienie:
    python papu_ingestor.py

Zależności:
    playwright==1.44.0
    pika==1.3.2
    python-dotenv
"""

import os
import asyncio
import json
import logging
from datetime import datetime, timedelta, timezone
from typing import List, Dict

import pika
from playwright.async_api import async_playwright, BrowserContext

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

# -----------  ENV  -----------
PAPU_EMAIL: str = os.getenv("PAPU_EMAIL", "")
PAPU_PASSWORD: str = os.getenv("PAPU_PASSWORD", "")
PAPU_COMPANY_ID: str = os.getenv("PAPU_COMPANY_ID", "")
PAPU_LOCALIZATION_ID: str = os.getenv("PAPU_LOCALIZATION_ID", "")

RABBIT_URL: str = os.getenv("RABBIT_URL", "amqp://guest:guest@localhost:5672/")
QUEUE_NAME: str = os.getenv("RABBIT_QUEUE", "pos_sales")

LIST_ENDPOINT = "https://admin.papu.io/api/meals"
PLAYWRIGHT_STATE = "storage_state.json"

UTC = timezone.utc


def _require_env(var: str) -> None:
    if not os.getenv(var):
        raise RuntimeError(f"Missing required env var {var}")


def _get_datetime_str(dt: datetime) -> str:
    """Return Papu-compatible datetime string: YYYY-MM-DD HH:MM"""
    return dt.astimezone(UTC).strftime("%Y-%m-%d %H:%M")


# -----------  PLAYWRIGHT FLOW  -----------
async def _ensure_context() -> BrowserContext:
    """Create or reuse browser context with saved cookies"""
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        if os.path.exists(PLAYWRIGHT_STATE):
            context = await browser.new_context(storage_state=PLAYWRIGHT_STATE)
            return context
        # First run – login through UI.
        context = await browser.new_context()
        page = await context.new_page()
        logging.info("Logging in to Papu.io UI...")
        await page.goto("https://admin.papu.io/login", wait_until="domcontentloaded")
        await page.goto("https://admin.papu.io/signin", wait_until="domcontentloaded")
        email_input = await page.wait_for_selector("input[name='email'], input[type='email']", timeout=60000)
        await email_input.fill(PAPU_EMAIL)
        password_input = await page.wait_for_selector("input[name='password'], input[type='password']", timeout=60000)
        await password_input.fill(PAPU_PASSWORD)
        await page.click("button[type='submit']")
        await page.wait_for_url("**/dashboard", timeout=15000)
        # Save cookies/state for next launches
        await context.storage_state(path=PLAYWRIGHT_STATE)
        logging.info("Login successful – state saved.")
        return context


async def fetch_sales(since: datetime, until: datetime) -> List[Dict]:
    """Fetch sales items between since/until."""
    context = await _ensure_context()
    request_context = context.request

    params = {
        "company": PAPU_COMPANY_ID,
        "order__localization": PAPU_LOCALIZATION_ID,
        "order__finished_at_after": _get_datetime_str(since),
        "order__finished_at_before": _get_datetime_str(until),
        "order__finished_type": ["delivered", "finished"],
        "page_size": 50,
        "page": 1,
    }

    sales: List[Dict] = []
    while True:
        resp = await request_context.get(LIST_ENDPOINT, params=params)
        if resp.status != 200:
            text = await resp.text()
            logging.error("Papu API error %s – %s", resp.status, text[:200])
            break
        data = await resp.json()
        sales.extend(data.get("results", []))
        if not data.get("next"):
            break
        params["page"] += 1

    await context.close()
    logging.info("Fetched %d sales (since %s)", len(sales), since)
    return sales


# -----------  RABBITMQ  -----------
def publish_sales(sales: List[Dict]):
    if not sales:
        return
    connection = pika.BlockingConnection(pika.URLParameters(RABBIT_URL))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    for sale in sales:
        channel.basic_publish(
            exchange="",
            routing_key=QUEUE_NAME,
            body=json.dumps(sale).encode(),
            properties=pika.BasicProperties(delivery_mode=2),
        )
    connection.close()
    logging.info("Published %d sales to queue '%s'", len(sales), QUEUE_NAME)


# -----------  MAIN LOOP  -----------
async def run_polling():
    logging.info("Starting Papu ingestor…")
    window = timedelta(minutes=2)
    while True:
        until = datetime.utcnow().replace(tzinfo=UTC)
        since = until - window
        try:
            sales = await fetch_sales(since, until)
            publish_sales(sales)
        except Exception as exc:
            logging.exception("Ingestor error: %s", exc)
        await asyncio.sleep(60)  # poll interval


def main():
    for var in [
        "PAPU_EMAIL",
        "PAPU_PASSWORD",
        "PAPU_COMPANY_ID",
        "PAPU_LOCALIZATION_ID",
    ]:
        _require_env(var)
    asyncio.run(run_polling())


if __name__ == "__main__":
    main()