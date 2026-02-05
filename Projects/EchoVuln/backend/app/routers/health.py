from __future__ import annotations

from fastapi import APIRouter
from app.models.schemas import ApiOk

router = APIRouter(tags=["health"])


@router.get("/health", response_model=ApiOk)
def health() -> ApiOk:
    return ApiOk(ok=True)
