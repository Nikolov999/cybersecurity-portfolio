from __future__ import annotations

from fastapi import Depends, Header, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import verify_secret
from app.db.models import ApiKey, EnrollKey, Agent
from app.db.session import get_db


def _split_compound(value: str) -> tuple[str, str]:
    if "." not in value:
        raise HTTPException(status_code=401, detail="Invalid key format")
    key_id, secret = value.split(".", 1)
    if not key_id.strip() or not secret.strip():
        raise HTTPException(status_code=401, detail="Invalid key format")
    return key_id.strip(), secret.strip()


def require_tenant_from_api_key(
    db: Session = Depends(get_db),
    x_api_key: str = Header(..., alias="X-API-Key"),
) -> int:
    # lookup by key_id, verify using FULL compound key (matches what you hashed)
    key_id, _ = _split_compound(x_api_key)

    row = db.execute(
        select(ApiKey).where(ApiKey.key_id == key_id, ApiKey.revoked_at.is_(None))
    ).scalar_one_or_none()

    if not row or not verify_secret(x_api_key, row.key_hash):
        raise HTTPException(status_code=401, detail="Invalid API key")

    return row.tenant_id


def require_tenant_from_enroll_key(
    db: Session = Depends(get_db),
    x_enroll_key: str = Header(..., alias="X-ENROLL-KEY"),
) -> int:
    # lookup by key_id, verify using FULL compound key
    key_id, _ = _split_compound(x_enroll_key)

    row = db.execute(
        select(EnrollKey).where(
            EnrollKey.key_id == key_id,
            EnrollKey.revoked_at.is_(None),
        )
    ).scalar_one_or_none()

    if not row or not verify_secret(x_enroll_key, row.key_hash):
        raise HTTPException(status_code=401, detail="Invalid enroll key")

    return row.tenant_id


def require_agent_from_bearer(
    db: Session = Depends(get_db),
    authorization: str = Header(..., alias="Authorization"),
) -> tuple[int, Agent]:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing bearer token")

    token = authorization.replace("Bearer ", "", 1).strip()
    token_id, _ = _split_compound(token)

    agent = db.execute(
        select(Agent).where(Agent.token_id == token_id, Agent.revoked_at.is_(None))
    ).scalar_one_or_none()

    # verify using FULL compound token (matches what you should hash/store)
    if not agent or not verify_secret(token, agent.token_hash):
        raise HTTPException(status_code=401, detail="Invalid agent token")

    return agent.tenant_id, agent
