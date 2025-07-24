# Rentownosc-App Full Nested Routes

## Struktura
- backend/: Flask API
- frontend/: React + Vite + Tailwind SPA

## Uruchomienie lokalne

### Backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=app.py
flask run

### Frontend
cd frontend
npm install
npm run dev

## Deployment na Render

Backend:
- Root: backend
- Build: pip install -r requirements.txt
- Start: gunicorn app:app --preload --workers 2
- Add DATABASE_URL

Frontend:
- Root: frontend
- Build: npm install && npm run build
- Publish: dist
