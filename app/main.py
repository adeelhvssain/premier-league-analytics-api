"""Application entrypoint for the FastAPI API."""

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import config
from .database import engine
from .models.base import Base
from .models.player import Player
from .models.player_season_stats import PlayerSeasonStats
from .models.team import Team
from .routers.analytics import router as analytics_router
from .routers.players import router as players_router
from .routers.player_season_stats import router as player_season_stats_router
from .routers.teams import router as teams_router
from .security import get_api_key, rate_limit


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""

    app = FastAPI(
        title=config.APP_NAME,
        version=config.APP_VERSION,
        debug=config.DEBUG,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.FRONTEND_ORIGINS or ["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
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
    protected_dependencies = [Depends(get_api_key), Depends(rate_limit)]
    app.include_router(teams_router, dependencies=protected_dependencies)
    app.include_router(players_router, dependencies=protected_dependencies)
    app.include_router(player_season_stats_router, dependencies=protected_dependencies)
    app.include_router(analytics_router, dependencies=protected_dependencies)

    return app


# ASGI app used by uvicorn.
app = create_app()
