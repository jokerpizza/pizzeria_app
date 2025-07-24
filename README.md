# Rentowność Restauracji (rentownosc-app)

## Setup Locally

### Backend

1. Create a virtualenv and install dependencies:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Initialize DB and run migrations:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```
3. Start the server:
   ```bash
   flask run
   ```

### Frontend

1. Install deps and run:
   ```bash
   cd frontend
   yarn install
   yarn dev
   ```

## Deployment

1. Zip and push to GitHub:
   ```bash
   cd rentownosc-app
   git init
   git add .
   git commit -m "Initial commit"
   gh repo create your-username/rentownosc-app --public --source=. --remote=origin
   git push -u origin main
   ```
2. On Render.com:
   - Create two Docker services: one pointing to `/backend`, one to `/frontend`.
   - Attach a PostgreSQL database and set `DATABASE_URL`.
   - Deploy and access your `frontend` and `backend` URLs.
