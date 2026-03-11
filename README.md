# Premier League Analytics API

This project is a FastAPI backend for Premier League data, focused on:

- Teams
- Players
- Player season statistics
- Simple player and club analytics

It uses:

- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- `python-dotenv`

## Current active features

- Core endpoints:
  - `GET /` and `GET /health`
  - Teams CRUD:
    - `GET /teams`
    - `GET /teams/{team_id}`
    - `POST /teams`
    - `PUT /teams/{team_id}`
    - `DELETE /teams/{team_id}`
  - Players:
    - `GET /players`
    - `GET /players/{player_id}`
    - `POST /players`
    - `GET /teams/{team_id}/players`
  - Player season stats:
    - `GET /player-season-stats`
    - `GET /player-season-stats/{stat_id}`
    - `POST /player-season-stats`
    - `GET /players/{player_id}/season-stats`
  - Analytics:
    - `GET /analytics/top-scorers`
    - `GET /analytics/top-assisters`
    - `GET /analytics/top-xg`
    - `GET /analytics/discipline`
    - `GET /analytics/club-summary/{team_id}`

- Security and usage controls:
  - API key auth using `X-API-Key` via `APIKeyHeader`
  - In-memory rate limiting per API key
  - Missing/invalid API key -> `401`
  - Exceeding limit -> `429`

- Data import:
  - `scripts/import_epl_20_21.py` imports clubs, players and stats from `EPL_20_21.csv`

## Files you should expect

- `app/main.py`  
  App creation, startup table creation, and router registration.
- `app/config.py`  
  Loads `.env` variables with defaults.
- `app/database.py`  
  SQLAlchemy engine/session setup.
- `app/security.py`  
  API key authentication and rate limiting.
- `app/models/`  
  SQLAlchemy models (`Team`, `Player`, `PlayerSeasonStats`).
- `app/schemas/`  
  Pydantic schemas for request/response validation.
- `app/routers/`  
  API endpoints for teams, players, stats, and analytics.
- `app/services/`  
  Query/service logic for analytics.
- `scripts/`  
  Import and utility scripts.
- `requirements.txt` and `.env.example`  
  Runtime and environment configuration.

## Prerequisites

- Python 3.9+
- PostgreSQL (local database for development)
- `pip` and `venv`

## Setup

1. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Copy environment variables:

   ```bash
   cp .env.example .env
   ```

4. Update `.env` with your values:

   - `DATABASE_URL`
   - `API_KEY`
   - `RATE_LIMIT_REQUESTS`
   - `RATE_LIMIT_WINDOW_SECONDS`

5. Run the API:

   ```bash
   uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
   ```

## API key setup in Swagger UI

This API is protected. In Swagger, you must send the API key with requests:

1. Open Swagger at `/docs`.
2. Click **Authorize**.
3. Enter your key in the `X-API-Key` field.
4. Click **Authorize** and then try protected endpoints.

You can also pass the key with curl using `-H "X-API-Key: <your-key>"`.

Example:

```bash
curl -H "X-API-Key: change_me" http://127.0.0.1:8000/teams
```

## CSV import

Load dataset data:

```bash
python scripts/import_epl_20_21.py
```

The import script:

- Creates teams from `Club` when missing
- Creates players from `Name + Club` when missing
- Creates season stat rows for season `2020/21`
- Marks imported teams as not user-created

## Notes

- Teams imported via the CSV are marked as not user-created and are protected from update/delete in the current rules.
- Teams created with `POST /teams` are user-created.