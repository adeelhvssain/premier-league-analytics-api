# Premier League Analytics API

FastAPI + PostgreSQL backend with a React (Vite) frontend for Premier League player-season analytics based on the `EPL_20_21.csv` dataset.

## What this project includes

- Backend:
  - `Team`, `Player`, `PlayerSeasonStats` models
  - CRUD endpoints for teams
  - player and player-season-stats endpoints
  - analytics endpoints (top scorers, assisters, xG, discipline, club summary)
- Frontend:
  - React single-page dashboard in `frontend/`
  - connects to backend API
  - displays teams, players, and analytics

## Prerequisites

- Python 3.10+ (3.9 may work, but 3.10+ is recommended)
- PostgreSQL running locally
- Node.js 18+ and npm (for frontend)

Check versions:

```bash
python --version
node --version
npm --version
```

## 1. Clone and open the project

```bash
git clone <your-repo-url>
cd premier-league-analytics-api
```

## 2. Backend setup

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install backend dependencies:

```bash
pip install -r requirements.txt
```

Create `.env` from the template:

```bash
cp .env.example .env
```

Set at least these values in `.env`:

```env
DATABASE_URL=postgresql+psycopg2://<db_user>:<db_password>@localhost:5432/premier_league_analytics
API_KEY=change_me
FRONTEND_ORIGINS=http://127.0.0.1:5173,http://localhost:5173
```

## 3. PostgreSQL setup

Make sure PostgreSQL is running and create the database named `premier_league_analytics`.

Example commands (if PostgreSQL CLI tools are available):

```bash
createdb premier_league_analytics
```

`DATABASE_URL` format:

```env
DATABASE_URL=postgresql+psycopg2://<db_user>:<db_password>@localhost:5432/premier_league_analytics
```

Use your PostgreSQL credentials here. This is not your Mac login unless you created a DB role with the same name/password.

## 4. Import the CSV dataset

Place `EPL_20_21.csv` in one of these locations:

- project root: `./EPL_20_21.csv`
- data folder: `./data/EPL_20_21.csv`

Run import:

```bash
python scripts/import_epl_20_21.py
```

Important:

- The import script resets the database tables before importing.
- It then creates teams, players, and `player_season_stats` rows from the CSV.

## 5. Run the backend API

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Backend URLs:

- API root: `http://127.0.0.1:8000/`
- Swagger docs: `http://127.0.0.1:8000/docs`

## 6. Run the frontend

Open a second terminal in the project root:

```bash
cd frontend
npm install
npm run dev
```

Frontend URL (default Vite):

- `http://127.0.0.1:5173`

## 7. Use the app

1. Open the frontend in your browser.
2. Enter backend base URL:
   - `http://127.0.0.1:8000`
3. Enter your API key in the UI field:
   - The frontend always sends `X-API-Key`.
   - This must match `API_KEY` in your backend environment.
4. Click `Load Dashboard`.

## Render deployment (Blueprint)

This repo includes `render.yaml` for a simple Render setup with:

- a FastAPI web service (`premier-league-analytics-api`)
- a static React site (`premier-league-analytics-frontend`)
- a PostgreSQL database (`premier-league-analytics-db`)

### Deploy steps

1. Push your repository to GitHub/GitLab.
2. In Render, create a new Blueprint and select this repository.
3. Render will detect `render.yaml` and create all three services.
4. In Render dashboard, set required backend env vars:
   - `API_KEY`
   - `FRONTEND_ORIGINS`
   - `RATE_LIMIT_REQUESTS` (optional, default `60`)
   - `RATE_LIMIT_WINDOW_SECONDS` (optional, default `60`)
   - `DATABASE_URL` is wired from the Render Postgres service automatically.
5. Set frontend env var:
   - `VITE_API_BASE_URL` = your backend Render URL (for example `https://premier-league-analytics-api.onrender.com`)

### Production start command (backend)

Render uses:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### CORS note

Backend CORS allowed origins are read from `FRONTEND_ORIGINS` (comma-separated), for example:

```env
FRONTEND_ORIGINS=https://premier-league-analytics-frontend.onrender.com
```

### Importing dataset on Render

After deployment, the Render Postgres database is empty. Import your CSV by running:

```bash
python scripts/import_epl_20_21.py
```

You can run this as a one-off command in Render shell/job, or locally against the Render `DATABASE_URL`.

## Main backend endpoints

- Health:
  - `GET /`
  - `GET /health`
- Teams:
  - `POST /teams`
  - `GET /teams`
  - `GET /teams/{team_id}`
  - `PUT /teams/{team_id}`
  - `DELETE /teams/{team_id}`
- Players:
  - `POST /players`
  - `GET /players`
  - `GET /players/{player_id}`
  - `GET /teams/{team_id}/players`
- Player season stats:
  - `POST /player-season-stats`
  - `GET /player-season-stats`
  - `GET /player-season-stats/{stat_id}`
  - `GET /players/{player_id}/season-stats`
- Analytics:
  - `GET /analytics/top-scorers?season=2020/21&limit=10`
  - `GET /analytics/top-assisters?season=2020/21&limit=10`
  - `GET /analytics/top-xg?season=2020/21&limit=10`
  - `GET /analytics/discipline?season=2020/21&limit=10`
  - `GET /analytics/club-summary/{team_id}?season=2020/21`

## Troubleshooting

- `npm: command not found`:
  - Install Node.js (includes npm), then restart terminal.
- `connection refused` to PostgreSQL:
  - PostgreSQL is not running, or `DATABASE_URL` is wrong.
- `role does not exist`:
  - Create the PostgreSQL role/user used in `DATABASE_URL`.
- CSV import says file not found:
  - Ensure `EPL_20_21.csv` is in project root or `data/`.
