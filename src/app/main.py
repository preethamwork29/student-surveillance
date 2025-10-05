"""FastAPI application assembly."""
from __future__ import annotations

from fastapi import FastAPI

from src.app.routes import analytics, enrollment, recognition, status, ui


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(title="Face Recognition API", version="2.0.0")

    app.include_router(status.router)
    app.include_router(enrollment.router)
    app.include_router(recognition.router)
    app.include_router(analytics.router)
    app.include_router(ui.router)

    return app


app = create_app()


__all__ = ["app", "create_app"]
