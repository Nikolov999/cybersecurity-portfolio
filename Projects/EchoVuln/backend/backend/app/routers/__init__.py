from .health import router as health_router
from .assets import router as assets_router
from .os_snapshots import router as snapshots_router
from .priorities import router as priorities_router
from .reports import router as reports_router
from .agents_enroll import router as agents_router
from .keys import router as keys_router


__all__ = [
    "health_router",
    "assets_router",
    "snapshots_router",
    "priorities_router",
    "reports_router",
    "agents_router",
    "keys_router"
]
