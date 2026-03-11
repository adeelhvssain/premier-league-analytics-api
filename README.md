# Premier League Analytics API

## Project focus

- `app/main.py` – FastAPI app creation and startup setup
- `app/config.py` – environment loading via `python-dotenv`
- `app/database.py` – SQLAlchemy PostgreSQL connection/session setup
- `app/models/` – SQLAlchemy models (`Team`, `Player`, `PlayerSeasonStats`)
- `app/schemas/` – request/response schemas
- `app/routers/` – endpoints for teams, players, and player season stats
- `scripts/` – utility scripts, including EPL CSV import
- `tests/` – coursework test placeholder

## Prerequisites

- Python 3.10+
- `pip` and `venv`

## Local setup

1. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Copy environment config and adjust values:

   ```bash
   cp .env.example .env
   ```

4. Run the API locally:

   ```bash
   uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
   ```

## API endpoints

- `GET /`  
  Returns a small service welcome payload.
- `GET /health`  
  Returns basic service health and environment info.
- `GET /teams`, `GET /teams/{team_id}`, `POST /teams`  
  Manage club records.
- `GET /players`, `GET /players/{player_id}`, `GET /teams/{team_id}/players`, `POST /players`  
  Manage players and query players by club.
- `GET /player-season-stats`, `GET /player-season-stats/{stat_id}`, `GET /players/{player_id}/season-stats`, `POST /player-season-stats`  
  Store and retrieve player season statistics.

## Analytics focus

- Player analytics can be built from `player season stats` records (for example goals, assists, cards, passing, and minutes played).
- Club analytics can be derived from aggregated player-season data (for example top scorers by club, card counts, averages, and per-club summaries).

## Data import

To load EPL 2020/21 CSV data into PostgreSQL, run:

```bash
python scripts/import_epl_20_21.py
```
