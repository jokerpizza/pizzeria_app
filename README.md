# Rentownosc-App

## Struktura
- backend/: Flask + SQLAlchemy + PostgreSQL API
- frontend/: React + Vite + Tailwind SPA

## Uruchomienie lokalne

### Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=app.py
flask run
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Deployment na Render

1. Stwórz repozytorium na GitHub i wypchnij całość:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin <TWÓJ_REPO_URL>
   git push -u origin main
   ```
2. Na Render – **Backend** (Flask):
   - Repo URL, branch `main`
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Dodaj PostgreSQL Add-on i ustaw `DATABASE_URL`
3. Na Render – **Frontend** (React):
   - Repo URL, branch `main`
   - Root Directory: `frontend`
   - Build Command: `npm install && npm run build`
   - Publish Directory: `dist`