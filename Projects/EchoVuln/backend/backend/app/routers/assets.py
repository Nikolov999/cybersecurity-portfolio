from __future__ import annotations

import json
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy import select, delete
from sqlalchemy.orm import Session
from app.core.auth import require_tenant_from_api_key

from app.core.security import verify_secret
from app.db.models import ApiKey, Asset
from app.models.schemas import AssetCreate, AssetOut
from app.db.session import get_db


router = APIRouter(prefix="/v2", tags=["assets"])


@router.get("/assets", response_model=List[AssetOut])
def list_assets(tenant_id: int = Depends(require_tenant_from_api_key), db: Session = Depends(get_db)):
    assets = db.execute(select(Asset).where(Asset.tenant_id == tenant_id).order_by(Asset.id.desc())).scalars().all()
    out: List[AssetOut] = []
    for a in assets:
        tags = json.loads(a.tags_json) if a.tags_json else None
        out.append(
            AssetOut(
                id=a.id,
                name=a.name,
                description=a.description,
                environment=a.environment,
                tags=tags,
                agent_id=a.agent_id,
                created_at=a.created_at,
            )
        )
    return out


@router.post("/assets", response_model=AssetOut)
def create_asset(payload: AssetCreate, tenant_id: int = Depends(require_tenant_from_api_key), db: Session = Depends(get_db)):
    tags_json = json.dumps(payload.tags or []) if payload.tags is not None else None
    a = Asset(
        tenant_id=tenant_id,
        name=payload.name,
        description=payload.description,
        environment=payload.environment,
        tags_json=tags_json,
        agent_id=payload.agent_id,
    )
    db.add(a)
    db.commit()
    db.refresh(a)

    return AssetOut(
        id=a.id,
        name=a.name,
        description=a.description,
        environment=a.environment,
        tags=payload.tags,
        agent_id=a.agent_id,
        created_at=a.created_at,
    )


@router.delete("/assets/{asset_id}")
def delete_asset(asset_id: int, tenant_id: int = Depends(require_tenant_from_api_key), db: Session = Depends(get_db)):
    res = db.execute(delete(Asset).where(Asset.tenant_id == tenant_id, Asset.id == asset_id))
    if res.rowcount == 0:
        raise HTTPException(status_code=404, detail="Asset not found")
    db.commit()
    return {"ok": True}
