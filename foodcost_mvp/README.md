# FoodCost MVP

## Uruchomienie lokalne

### Backend
```bash
python -m venv venv && source venv/bin/activate
pip install -r backend/requirements.txt
export DATABASE_URL=sqlite:///./foodcost.db
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Render.com
- Utwórz Web Service z Dockerfile (backend)
- Utwórz Static Site z folderu `frontend` (build command: `npm install && npm run build`, publish dir: `dist`)
- Ustaw zmienne środowiskowe: `DATABASE_URL`, `PAPU_TOKEN`, `PAPU_URL`

## Synchronizacja PAPU
W backendzie `app/services/papu_fetcher.py` – można odpalić jako cron:
```
python -m app.services.papu_fetcher
```
albo dodać APScheduler w `main.py` (co 3 min).
