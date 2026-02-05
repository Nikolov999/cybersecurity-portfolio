from __future__ import annotations

import json
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.auth import require_tenant_from_api_key, require_agent_from_bearer
from app.db.session import get_db
from app.db.models import Snapshot
from app.models.schemas import SnapshotIngestV2, SnapshotOut
from app.services.ingest_v2 import ingest_snapshot_v2

router = APIRouter(prefix="/v2", tags=["snapshots"])


@router.post("/ingest/snapshot")
def ingest_snapshot(
    payload: SnapshotIngestV2,
    db: Session = Depends(get_db),
    agent_ctx=Depends(require_agent_from_bearer),
):
    tenant_id, agent = agent_ctx
    snapshot_id = ingest_snapshot_v2(db=db, tenant_id=tenant_id, agent=agent, payload=payload)
    return {"ok": True, "snapshot_id": snapshot_id}


@router.post("/ingest/heartbeat")
def ingest_heartbeat(
    db: Session = Depends(get_db),
    agent_ctx=Depends(require_agent_from_bearer),
):
    tenant_id, agent = agent_ctx
    # keepalive; last_seen handled inside auth or later
    return {"ok": True}


@router.get("/assets/{asset_id}/snapshots", response_model=List[SnapshotOut])
def list_snapshots_for_asset(
    asset_id: int,
    limit: int = 50,
    tenant_id: int = Depends(require_tenant_from_api_key),
    db: Session = Depends(get_db),
):
    limit = max(1, min(limit, 200))

    rows = (
        db.execute(
            select(Snapshot)
            .where(Snapshot.tenant_id == tenant_id, Snapshot.asset_id == asset_id)
            .order_by(Snapshot.collected_at.desc())
            .limit(limit)
        )
        .scalars()
        .all()
    )

    out: List[SnapshotOut] = []
    for s in rows:
        out.append(
            SnapshotOut(
                id=s.id,
                asset_id=s.asset_id,
                agent_id=s.agent_id,
                collected_at_utc=s.collected_at,
                payload=json.loads(s.payload_json),
            )
        )
    return out
