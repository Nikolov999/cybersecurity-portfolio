from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.health import router as health_router
from app.api.scan import router as scan_router
from app.api.assets import router as assets_router
from app.core.db import init_db

app = FastAPI(title="EchoExposure API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/api/health", tags=["health"])
app.include_router(scan_router, prefix="/api/scan", tags=["scan"])
app.include_router(assets_router, prefix="/api/assets", tags=["assets"])


@app.on_event("startup")
async def startup():
    await init_db()
