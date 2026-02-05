from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from app.core.db import get_db
from app.core.models import Asset

router = APIRouter()


@router.post("/")
async def add_asset(
    target: str,
    type: str = "domain",
    db: AsyncSession = Depends(get_db),
):
    asset = Asset(target=target, type=type)
    db.add(asset)
    await db.commit()
    await db.refresh(asset)
    return {"status": "added", "id": asset.id, "target": target, "type": type}


@router.get("/")
async def list_assets(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Asset).order_by(Asset.created_at.desc()))
    assets = res.scalars().all()
    return [
        {"id": a.id, "target": a.target, "type": a.type, "created_at": a.created_at.isoformat()}
        for a in assets
    ]


@router.delete("/{asset_id}")
async def delete_asset(asset_id: int, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Asset).where(Asset.id == asset_id))
    asset = res.scalar_one_or_none()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    await db.delete(asset)
    await db.commit()
    return {"status": "deleted", "id": asset_id}
