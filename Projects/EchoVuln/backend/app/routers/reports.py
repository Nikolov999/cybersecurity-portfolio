from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from app.core.auth import require_tenant_from_api_key
from app.db.session import get_db
from app.db.models import Report
from app.models.schemas import ReportCreate, ReportOut

router = APIRouter(prefix="/v2", tags=["reports"])


@router.get("/reports", response_model=List[ReportOut])
def list_reports(
    tenant_id: int = Depends(require_tenant_from_api_key),
    db: Session = Depends(get_db),
):
    rows = db.execute(
        select(Report).where(Report.tenant_id == tenant_id).order_by(Report.id.desc())
    ).scalars().all()
    return [ReportOut(id=r.id, asset_id=r.asset_id, title=r.title, markdown=r.markdown, created_at=r.created_at) for r in rows]


@router.post("/reports", response_model=ReportOut)
def create_report(
    payload: ReportCreate,
    tenant_id: int = Depends(require_tenant_from_api_key),
    db: Session = Depends(get_db),
):
    r = Report(tenant_id=tenant_id, asset_id=payload.asset_id, title=payload.title, markdown=payload.markdown)
    db.add(r)
    db.commit()
    db.refresh(r)
    return ReportOut(id=r.id, asset_id=r.asset_id, title=r.title, markdown=r.markdown, created_at=r.created_at)


@router.get("/reports/{report_id}", response_model=ReportOut)
def get_report(
    report_id: int,
    tenant_id: int = Depends(require_tenant_from_api_key),
    db: Session = Depends(get_db),
):
    r = db.execute(select(Report).where(Report.tenant_id == tenant_id, Report.id == report_id)).scalar_one_or_none()
    if not r:
        raise HTTPException(status_code=404, detail="Report not found")
    return ReportOut(id=r.id, asset_id=r.asset_id, title=r.title, markdown=r.markdown, created_at=r.created_at)


@router.delete("/reports/{report_id}")
def delete_report(
    report_id: int,
    tenant_id: int = Depends(require_tenant_from_api_key),
    db: Session = Depends(get_db),
):
    res = db.execute(delete(Report).where(Report.tenant_id == tenant_id, Report.id == report_id))
    if res.rowcount == 0:
        raise HTTPException(status_code=404, detail="Report not found")
    db.commit()
    return {"ok": True}
