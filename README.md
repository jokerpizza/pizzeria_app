# FoodCost V2

Now includes:
- **Półprodukty** (receptury jako składniki) – checkbox `is_semi`.
- **Kategorie produktów i receptur**.
- **Raport z sortowaniem i filtrami** (FC%, marża, półprodukty).
- **Alert FC%** – próg ustawiany w aplikacji (Settings).
- Walidacje (brak wartości ujemnych), UI PL.
- SPA rewrites (`frontend/public/_redirects`).

## Stack
Backend: FastAPI + SQLAlchemy  
Frontend: React + Vite + Tailwind  
DB: Postgres

## Deploy (Render)
1. Push repo to GitHub.
2. Backend Web Service (root: `backend`)
   - Build: `pip install -r requirements.txt`
   - Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Env: `DB_URL` (Postgres), optional default threshold `FC_THRESHOLD` (number).
3. Frontend Static Site (root: `frontend`)
   - Build: `npm install && npm run build`
   - Publish: `dist`
   - Env: `VITE_API_URL` (backend URL)

## Local dev
See V1 README, identical steps.
