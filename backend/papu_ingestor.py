
"""Sanity‑checked Papu.io ingestor – ready for Render.com
----------------------------------------------------------
• Expects the following env‑vars at run‑time:
    PAPU_EMAIL, PAPU_PASSWORD, PAPU_COMPANY_ID, PAPU_LOCALIZATION_ID
• Launches Chromium in true headless mode with --no‑sandbox for Render
• Logs in once, then grabs today's delivered/finished orders and exits
• Emits a CSV called `sales.csv` next to the script (one row per order)
"""

import asyncio, csv, logging, os
from datetime import datetime, timezone

from playwright.async_api import async_playwright, TimeoutError as PWTimeout

LOGIN_URL = "https://admin.papu.io/login"
MEALS_URL = (
    "https://admin.papu.io/meals"
    "?company={company}"
    "&dateRangeName=custom"
    "&order__finished_at_after={after}"
    "&order__finished_at_before={before}"
    "&order__finished_type=delivered"
    "&order__finished_type=finished"
    "&order__localization={loc}"
    "&page=1&page_size=500"
)

LOG = logging.getLogger("papu-ingestor")
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)s │ %(message)s"
)

# ──────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────


def _env(name: str) -> str:
    val = os.getenv(name)
    if not val:
        LOG.error("Missing required env var %s – exiting!", name)
        raise SystemExit(1)
    return val.strip()


async def _login(page, email: str, password: str) -> None:
    """Perform sign‑in, waiting robustly for the relevant fields."""
    await page.goto(LOGIN_URL, wait_until="networkidle")
    try:
        await page.wait_for_selector(
            "input[name=email], input[type=email]", timeout=60_000
        )
    except PWTimeout:
        raise RuntimeError("Login page did not load e‑mail input in time")

    await page.fill("input[name=email], input[type=email]", email)
    await page.fill("input[name=password], input[type=password]", password)
    await page.click("button[type=submit]")
    # successful login redirects to /dashboard – wait for it
    await page.wait_for_url("**/dashboard", timeout=60_000)


async def _scrape_sales(page, company: str, loc_id: str, since: datetime, until: datetime):
    after = since.strftime("%Y-%m-%d+%H:%M")
    before = until.strftime("%Y-%m-%d+%H:%M")
    url = MEALS_URL.format(
        company=company, after=after, before=before, loc=loc_id
    )
    LOG.info("Fetching table URL %s", url)
    await page.goto(url, wait_until="networkidle")
    await page.wait_for_selector("table tbody tr", timeout=60_000)
    rows = page.locator("table tbody tr")
    sales = []
    for i in range(await rows.count()):
        txts = await rows.nth(i).locator("td").all_inner_texts()
        sales.append(txts)
    return sales


async def main() -> None:
    email = _env("PAPU_EMAIL")
    password = _env("PAPU_PASSWORD")
    company = _env("PAPU_COMPANY_ID")
    loc_id = _env("PAPU_LOCALIZATION_ID")

    today = datetime.now(timezone.utc).astimezone()
    since = today.replace(hour=0, minute=0, second=0, microsecond=0)
    until = today

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True, args=["--no-sandbox"])
        context = await browser.new_context()
        page = await context.new_page()

        LOG.info("Logging in to Papu…")
        await _login(page, email, password)

        LOG.info("Pulling today's delivered/finished orders…")
        sales = await _scrape_sales(page, company, loc_id, since, until)
        LOG.info("Got %d rows.", len(sales))

        csv_path = os.path.join(os.path.dirname(__file__), "sales.csv")
        with open(csv_path, "w", newline="", encoding="utf-8") as fh:
            writer = csv.writer(fh)
            writer.writerow(
                [
                    "Kategoria",
                    "Rozmiar",
                    "Nazwa",
                    "Ilość",
                    "Cena",
                    "Nr zam.",
                    "Data zakończenia",
                    "Brand",
                    "Źródło",
                    "Typ zakończenia",
                    "Paragon",
                ]
            )
            writer.writerows(sales)
        LOG.info("✓ sales.csv written (%s)", csv_path)

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
