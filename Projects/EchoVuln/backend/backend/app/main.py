from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.keys import router as keys_router

from app.core.config import settings
from app.core.logging import setup_logging
from app.routers import (
    health_router,
    assets_router,
    snapshots_router,
    priorities_router,
    reports_router,
    agents_router,
)
from app.db.base import Base
from app.db.session import engine


def create_app() -> FastAPI:
    setup_logging()

    app = FastAPI(title=settings.api_title, version=settings.api_version)

    @app.on_event("startup")
    def _startup() -> None:
        Base.metadata.create_all(bind=engine)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "*",
            "http://localhost",
            "http://127.0.0.1",
            "http://localhost:1420",
            "http://tauri.localhost",
            "http://127.0.0.1:1420",
            "https://tauri.localhost",
            "tauri://localhost",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health_router)
    app.include_router(assets_router)
    app.include_router(keys_router)
    app.include_router(snapshots_router)
    app.include_router(priorities_router)
    app.include_router(reports_router)
    app.include_router(agents_router)

    return app


app = create_app()
