# FoodCost MVP

Monorepo (backend + frontend) for calculating food cost and margin of recipes.

## Stack
- Backend: FastAPI + SQLAlchemy + Pydantic
- DB: PostgreSQL
- Frontend: React + Vite + TypeScript + TailwindCSS
- Deployment: Render.com (two services + one DB)

## Features (MVP)
- CRUD for Products (ingredients): name, base_unit (kg/g/l/ml/szt), price_per_kg (PLN)
- CRUD for Recipes: name, sale_price, list of items (product_id, amount, unit)
- Automatic unit conversion (kg↔g, l↔ml)
- Food cost % and margin (PLN) calculated with 2 decimals
- Dashboard with stats: count of products, avg food cost of recipes, top 5 most expensive recipes
- Filtering and search on lists
- Open access (no auth yet)

---

## Quick Start (Local)

### 1. Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # fill DB_URL
uvicorn app.main:app --reload
```

### 2. Frontend

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

### 3. Database
Create Postgres DB (local or Render). Put connection string in backend `.env`.

```
DB_URL=postgresql+psycopg2://user:password@host:port/dbname
```

---

## Deploy to Render.com

1. **Push repo to GitHub.**

2. **Create PostgreSQL on Render**  
   - Dashboard → New → PostgreSQL. Note connection string.

3. **Create Backend Web Service**
   - New → Web Service → select this repo.
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Environment: Python 3.11
   - Add env var `DB_URL` with your Render Postgres connection string.

4. **Create Frontend Static Site**
   - New → Static Site → select repo.
   - Root Directory: `frontend`
   - Build Command: `npm install && npm run build`
   - Publish Directory: `dist`
   - Add env var `VITE_API_URL` pointing to backend URL (e.g. `https://your-backend.onrender.com`)

5. (Optional) Add a `render.yaml` for IaC; basic config provided.

---

## Future (v2)
- Auth & roles
- Semi-finished products (nested recipes)
- Waste / stock
- Imports/exports (CSV)
- Alerts on price changes

---

## Dev Tips
- Units accepted: kg, g, l, ml, szt
- All prices in PLN, decimals with dot.
- Rounding: 2 decimals.

Enjoy!
