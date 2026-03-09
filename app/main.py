"""Application entrypoint for the FastAPI API."""

from fastapi import FastAPI

from . import config


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

    # Extension point:
    # Add routers here as the project grows.
    # from .routers import teams, fixtures
    # app.include_router(teams.router, prefix=f"{config.API_PREFIX}/teams", tags=["teams"])

    return app


# ASGI app used by uvicorn.
app = create_app()
