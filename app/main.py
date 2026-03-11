"""Application entrypoint for the FastAPI API."""

from fastapi import FastAPI

from . import config
from .database import engine
from .models.base import Base
from .models.player import Player
from .models.player_season_stats import PlayerSeasonStats
from .models.team import Team
from .routers.analytics import router as analytics_router
from .routers.players import router as players_router
from .routers.teams import router as teams_router
from .routers.player_season_stats import router as player_season_stats_router


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""

    app = FastAPI(
        title=config.APP_NAME,
        version=config.APP_VERSION,
        debug=config.DEBUG,
    )

    @app.get("/")
    def root() -> dict[str, str]:
        """Basic health/info root route."""
        return {
            "message": "Welcome to the Premier League Analytics API",
            "name": config.APP_NAME,
            "version": config.APP_VERSION,
        }

    @app.get("/health")
    def health() -> dict[str, str]:
        """Liveness endpoint for basic service checks."""
        return {"status": "ok", "environment": config.ENVIRONMENT}

    @app.on_event("startup")
    def on_startup() -> None:
        """Create all tables when the app starts."""
        Base.metadata.create_all(bind=engine)

    # Extension point:
    app.include_router(teams_router)
    app.include_router(players_router)
    app.include_router(player_season_stats_router)
    app.include_router(analytics_router)

    return app


# ASGI app used by uvicorn.
app = create_app()
