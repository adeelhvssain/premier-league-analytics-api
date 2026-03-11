"""Configuration loading for the FastAPI app.

This module loads environment variables from a `.env` file and exposes
typed settings with safe defaults for a minimal coursework setup.
"""

from pathlib import Path
import os

from dotenv import load_dotenv


# Project root (two levels up from this file: app/ -> project root)
BASE_DIR = Path(__file__).resolve().parent.parent


def _env_bool(name: str, default: bool = False) -> bool:
    """Parse common string boolean environment values."""
    return os.getenv(name, str(default)).strip().lower() in {"1", "true", "yes", "on"}


def _env_int(name: str, default: int) -> int:
    """Parse int environment variables with a fallback default."""
    try:
        return int(os.getenv(name, str(default)))
    except (TypeError, ValueError):
        return default


# Read environment variables from `.env` when present.
load_dotenv(BASE_DIR / ".env")


# App settings
APP_NAME = os.getenv("APP_NAME", "Premier League Analytics API")
APP_VERSION = os.getenv("APP_VERSION", "0.1.0")
API_PREFIX = os.getenv("API_PREFIX", "").strip()
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DEBUG = _env_bool("DEBUG", default=True)

# Server settings
HOST = os.getenv("HOST", "127.0.0.1")
PORT = _env_int("PORT", 8000)

# Database placeholder for future expansion.
# Add SQLAlchemy/driver dependencies only when the project grows.
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:postgres@localhost:5432/premier_league_analytics",
)

# Security defaults
API_KEY = os.getenv("API_KEY", "premier-league-coursework-key")
RATE_LIMIT_REQUESTS = _env_int("RATE_LIMIT_REQUESTS", 60)
RATE_LIMIT_WINDOW_SECONDS = _env_int("RATE_LIMIT_WINDOW_SECONDS", 60)
