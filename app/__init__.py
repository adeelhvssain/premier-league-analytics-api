"""Primary application package for the Premier League Analytics API."""

# Re-exporting the FastAPI app from `main` is a convenient import path for
# tooling and keeps startup simple while we continue to keep the project small.
from .main import app

__all__ = ["app"]
