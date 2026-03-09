# Premier League Analytics API

This is a simple FastAPI starter for a university coursework project.
It provides a clean, minimal structure that can be extended later with
PostgreSQL, SQLAlchemy models, and feature routers.

## Project structure

- `app/main.py` – FastAPI app creation and route definitions
- `app/config.py` – environment variable loading via `python-dotenv`
- `app/__init__.py` – package exports
- `tests/__init__.py` – test package placeholder
- `.env.example` – environment variable template
- `.gitignore` – local Python/git ignore rules

## Prerequisites

- Python 3.10+
- `pip`

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

## Next steps (coursework-friendly extensions)

- Add `app/routers/` with route modules (e.g., teams, matches, standings).
- Add SQLAlchemy setup + PostgreSQL connection in `app/database.py`.
- Add tests in `tests/` using `pytest` and `httpx` for endpoint checks.
