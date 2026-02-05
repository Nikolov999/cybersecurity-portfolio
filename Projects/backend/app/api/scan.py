from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
import json

from app.core.db import get_db
from app.core.models import Scan
from app.services.scanner import scan_target

router = APIRouter()


@router.post("/")
async def run_scan(target: str, db: AsyncSession = Depends(get_db)):
    result = await scan_target(target)

    row = Scan(target=target, result=json.dumps(result))
    db.add(row)
    await db.commit()
    await db.refresh(row)

    return result


@router.get("/")
async def list_scans(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Scan).order_by(Scan.created_at.desc()))
    scans = res.scalars().all()

    return [
        {
            "id": s.id,
            "target": s.target,
            "result": json.loads(s.result),
            "created_at": s.created_at.isoformat(),
        }
        for s in scans
    ]


@router.delete("/{scan_id}")
async def delete_scan(scan_id: int, db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(Scan).where(Scan.id == scan_id))
    scan = res.scalar_one_or_none()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")

    await db.delete(scan)
    await db.commit()
    return {"status": "deleted", "id": scan_id}


@router.delete("/")
async def clear_scan_history(db: AsyncSession = Depends(get_db)):
    await db.execute(delete(Scan))
    await db.commit()
    return {"status": "cleared"}
