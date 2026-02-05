from __future__ import annotations

import json
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import Agent, Asset, Snapshot
from app.models.schemas import SnapshotIngestV2


def ingest_snapshot_v2(db: Session, tenant_id: int, agent: Agent, payload: SnapshotIngestV2) -> int:
    if payload.schema_version != 2:
        raise HTTPException(status_code=400, detail="Unsupported schema_version")
    if payload.agent_id != agent.agent_id:
        raise HTTPException(status_code=403, detail="agent_id mismatch")

    asset = None
    if payload.asset_id is not None:
        asset = db.execute(
            select(Asset).where(Asset.tenant_id == tenant_id, Asset.id == payload.asset_id)
        ).scalar_one_or_none()

    if asset is None:
        asset = db.execute(
            select(Asset).where(Asset.tenant_id == tenant_id, Asset.id == agent.asset_id)
        ).scalar_one_or_none()

    if asset is None:
        asset = Asset(
            tenant_id=tenant_id,
            name=f"Asset {payload.agent_id}",
            agent_id=payload.agent_id,
        )
        db.add(asset)
        db.commit()
        db.refresh(asset)

    if not asset.agent_id:
        asset.agent_id = payload.agent_id
        db.add(asset)
        db.commit()

    raw = payload.model_dump()

    s = Snapshot(
        tenant_id=tenant_id,
        asset_id=asset.id,
        agent_id=payload.agent_id,
        collected_at=payload.collected_at_utc,
        payload_json=json.dumps(raw, default=str),
    )
    db.add(s)
    db.commit()
    db.refresh(s)
    return s.id
