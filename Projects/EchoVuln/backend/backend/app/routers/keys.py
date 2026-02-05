from __future__ import annotations

from datetime import datetime
from secrets import token_urlsafe
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.auth import require_tenant_from_api_key
from app.core.security import hash_secret
from app.db.models import ApiKey, EnrollKey
from app.db.session import get_db

router = APIRouter(prefix="/v2/keys", tags=["keys"])

ITERATIONS = 200_000


def make_key(prefix: str) -> str:
    # compound key: <key_id>.<secret>
    return f"{prefix}_{token_urlsafe(20)}.{token_urlsafe(32)}"


class CreateKeyRequest(BaseModel):
    kind: str = Field(..., pattern="^(admin|enroll)$")
    label: Optional[str] = None


class CreateKeyResponse(BaseModel):
    key: str
    key_id: str
    kind: str
    label: str


class KeyRow(BaseModel):
    id: int
    kind: str
    key_id: str
    label: str
    created_at: Optional[datetime] = None
    revoked_at: Optional[datetime] = None


@router.get("", response_model=list[KeyRow])
def list_keys(
    db: Session = Depends(get_db),
    tenant_id: int = Depends(require_tenant_from_api_key),
):
    api_rows = db.execute(select(ApiKey).where(ApiKey.tenant_id == tenant_id)).scalars().all()
    enroll_rows = db.execute(select(EnrollKey).where(EnrollKey.tenant_id == tenant_id)).scalars().all()

    out: list[KeyRow] = []
    for r in api_rows:
        out.append(
            KeyRow(
                id=r.id,
                kind="admin",
                key_id=r.key_id,
                label=r.label or "admin",
                created_at=getattr(r, "created_at", None),
                revoked_at=getattr(r, "revoked_at", None),
            )
        )
    for r in enroll_rows:
        out.append(
            KeyRow(
                id=r.id,
                kind="enroll",
                key_id=r.key_id,
                label=r.label or "enroll",
                created_at=getattr(r, "created_at", None),
                revoked_at=getattr(r, "revoked_at", None),
            )
        )

    out.sort(key=lambda x: (x.kind, x.id))
    return out


@router.post("", response_model=CreateKeyResponse)
def create_key(
    req: CreateKeyRequest,
    db: Session = Depends(get_db),
    tenant_id: int = Depends(require_tenant_from_api_key),
):
    if req.kind == "admin":
        compound = make_key("ak")
        key_id, _secret = compound.split(".", 1)
        row = ApiKey(
            tenant_id=tenant_id,
            key_id=key_id,
            key_hash=hash_secret(compound, iters=ITERATIONS),
            label=req.label or "admin",
        )
        db.add(row)
        db.commit()
        db.refresh(row)
        return CreateKeyResponse(key=compound, key_id=key_id, kind="admin", label=row.label)

    if req.kind == "enroll":
        compound = make_key("ek")
        key_id, _secret = compound.split(".", 1)
        row = EnrollKey(
            tenant_id=tenant_id,
            key_id=key_id,
            key_hash=hash_secret(compound, iters=ITERATIONS),
            label=req.label or "enroll",
        )
        db.add(row)
        db.commit()
        db.refresh(row)
        return CreateKeyResponse(key=compound, key_id=key_id, kind="enroll", label=row.label)

    raise HTTPException(status_code=400, detail="Invalid kind")


@router.delete("/{kind}/{key_id}")
def revoke_key(
    kind: str,
    key_id: str,
    db: Session = Depends(get_db),
    tenant_id: int = Depends(require_tenant_from_api_key),
):
    now = datetime.utcnow()

    if kind == "admin":
        row = db.execute(
            select(ApiKey).where(
                ApiKey.tenant_id == tenant_id,
                ApiKey.key_id == key_id,
            )
        ).scalar_one_or_none()
        if not row:
            raise HTTPException(status_code=404, detail="Not found")
        row.revoked_at = now
        db.commit()
        return {"ok": True}

    if kind == "enroll":
        row = db.execute(
            select(EnrollKey).where(
                EnrollKey.tenant_id == tenant_id,
                EnrollKey.key_id == key_id,
            )
        ).scalar_one_or_none()
        if not row:
            raise HTTPException(status_code=404, detail="Not found")
        row.revoked_at = now
        db.commit()
        return {"ok": True}

    raise HTTPException(status_code=400, detail="Invalid kind")
