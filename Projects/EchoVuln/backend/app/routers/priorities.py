from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.auth import require_tenant_from_api_key
from app.db.session import get_db
from app.models.schemas import TopFixesRequest, TopFixesResponse
from app.services.scoring_v2 import compute_top_fixes_v2

router = APIRouter(prefix="/v2", tags=["top-fixes"])


@router.post("/top-fixes", response_model=TopFixesResponse)
def top_fixes(
    req: TopFixesRequest,
    tenant_id: int = Depends(require_tenant_from_api_key),
    db: Session = Depends(get_db),
):
    items = compute_top_fixes_v2(db=db, tenant_id=tenant_id, asset_id=req.asset_id, limit=req.limit)
    return TopFixesResponse(items=items)
