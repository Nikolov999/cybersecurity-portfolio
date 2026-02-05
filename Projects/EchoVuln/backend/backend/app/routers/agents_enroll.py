from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.auth import require_tenant_from_enroll_key
from app.core.config import settings
from app.core.security import mint_token, hash_secret
from app.db.session import get_db
from app.db.models import Asset, Agent
from app.models.schemas import EnrollRequest, EnrollResponse

router = APIRouter(prefix="/v2", tags=["agents"])

TOKEN_BYTES = 32  # CHANGED: settings.token_bytes does not exist in your config


@router.post("/agents/enroll", response_model=EnrollResponse)
def enroll_agent(
    payload: EnrollRequest,
    tenant_id: int = Depends(require_tenant_from_enroll_key),
    db: Session = Depends(get_db),
):
    # If agent already exists, rotate token
    agent = db.execute(
        select(Agent).where(
            Agent.tenant_id == tenant_id,
            Agent.agent_id == payload.agent_id,
            Agent.revoked_at.is_(None),
        )
    ).scalar_one_or_none()

    # mint compound agent token: at_xxx.secret
    def _mint_compound_agent_token() -> tuple[str, str]:
        # token_id stored, secret returned once
        import secrets, string
        alphabet = string.ascii_lowercase + string.digits
        token_id = "at_" + "".join(secrets.choice(alphabet) for _ in range(10))
        secret = mint_token(TOKEN_BYTES)  # CHANGED
        return token_id, secret

    if agent:
        token_id, secret = _mint_compound_agent_token()
        compound = f"{token_id}.{secret}"
        agent.token_id = token_id
        agent.token_hash = hash_secret(compound, iters=settings.pbkdf2_iters)
        db.add(agent)
        db.commit()
        db.refresh(agent)
        return EnrollResponse(agent_token=compound, asset_id=agent.asset_id)

    # Create asset for this agent
    asset = Asset(
        tenant_id=tenant_id,
        name=payload.hostname or f"Endpoint {payload.agent_id}",
        description=payload.os,
        environment="endpoint",
        tags_json=None,
        agent_id=payload.agent_id,
    )
    db.add(asset)
    db.commit()
    db.refresh(asset)

    token_id, secret = _mint_compound_agent_token()
    compound = f"{token_id}.{secret}"
    agent = Agent(
        tenant_id=tenant_id,
        agent_id=payload.agent_id,
        asset_id=asset.id,
        token_id=token_id,
        token_hash=hash_secret(compound, iters=settings.pbkdf2_iters),
    )
    db.add(agent)
    db.commit()
    db.refresh(agent)

    return EnrollResponse(agent_token=compound, asset_id=asset.id)
