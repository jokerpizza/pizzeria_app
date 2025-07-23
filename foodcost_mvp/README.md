# FoodCost MVP (fixed)

## Backend (FastAPI)

### Lokalnie
```
python -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
export DATABASE_URL=sqlite:///./foodcost.db
uvicorn app.main:app --app-dir backend --reload
```

## Frontend
```
cd frontend
npm install
npm run dev
```

## Render.com

### Backend Web Service
- Root Directory: `foodcost_full`
- Dockerfile Path: `foodcost_full/Dockerfile`
- Env:
  - DATABASE_URL
  - PAPU_TOKEN
  - PAPU_URL=https://rest.papu.io/api/orders/order-meal/list-objects/
  - PAPU_LOCALIZATION=801
  - CORS_ORIGINS=https://twoj-frontend.onrender.com

### Worker (opcjonalnie)
Root Directory: `foodcost_full`
Start Command:
```
bash -c "cd backend && export PYTHONPATH=$(pwd) && while true; do python -m app.services.papu_fetcher; sleep 180; done"
```

### Frontend Static Site
- Root Directory: `foodcost_full/frontend`
- Build Command: `npm install && npm run build`
- Publish Directory: `dist`
- Env: `VITE_API_URL=https://twoj-backend.onrender.com`
