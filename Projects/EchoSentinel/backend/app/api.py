from fastapi import APIRouter, Depends, Header, HTTPException
from fastapi.responses import StreamingResponse
import io
import json
import zipfile
from datetime import timedelta
from sqlalchemy.orm import Session
from .db import get_db
from .config import settings
from . import schemas, crud, rules

router = APIRouter()


def require_api_key(x_api_key: str | None):
    if not x_api_key or x_api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="Unauthorized")


@router.post("/ingest/event", response_model=schemas.IngestResponse)
def ingest_event(
    payload: schemas.IngestEvent,
    db: Session = Depends(get_db),
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
):
    require_api_key(x_api_key)

    ev = crud.create_event(db, payload)
    alert_ids = rules.run_rules_on_ingest(db, payload)
    return schemas.IngestResponse(
        stored_event_id=ev.id,
        alerts_created=len(alert_ids),
        alert_ids=alert_ids,
    )


@router.get("/events", response_model=list[schemas.EventOut])
def get_events(
    limit: int = 200,
    hostname: str | None = None,
    event_id: int | None = None,
    username: str | None = None,
    db: Session = Depends(get_db),
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
):
    require_api_key(x_api_key)
    limit = max(1, min(limit, 2000))
    return crud.list_events(db, limit=limit, hostname=hostname, event_id=event_id, username=username)


@router.get("/alerts", response_model=list[schemas.AlertOut])
def get_alerts(
    limit: int = 200,
    hostname: str | None = None,
    severity: str | None = None,
    db: Session = Depends(get_db),
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
):
    require_api_key(x_api_key)
    limit = max(1, min(limit, 2000))
    return crud.list_alerts(db, limit=limit, hostname=hostname, severity=severity)


# -----------------------------
# Endpoints (new)
# -----------------------------
@router.get("/endpoints", response_model=list[schemas.EndpointOut])
def get_endpoints(
    limit: int = 200,
    lookback_hours: int = 24,
    db: Session = Depends(get_db),
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
):
    require_api_key(x_api_key)
    limit = max(1, min(limit, 2000))
    lookback_hours = max(1, min(lookback_hours, 720))  # cap at 30d
    return crud.list_endpoints(db, limit=limit, lookback_hours=lookback_hours)


# -----------------------------
# Evidence bundle export (new)
# -----------------------------
@router.get("/alerts/{alert_id}/evidence.zip")
def export_evidence_zip(
    alert_id: int,
    minutes: int = 5,
    db: Session = Depends(get_db),
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
):
    require_api_key(x_api_key)
    minutes = max(1, min(minutes, 60))

    alert = crud.get_alert_by_id(db, alert_id=alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    t0 = alert.timestamp - timedelta(minutes=minutes)
    t1 = alert.timestamp + timedelta(minutes=minutes)
    events = crud.list_events_window(
        db,
        hostname=alert.hostname,
        start=t0,
        end=t1,
        limit=10000,
    )

    readme = (
        "EchoSentinel Evidence Bundle\n\n"
        f"Alert ID: {alert.id}\n"
        f"Rule: {alert.rule_name}  Severity: {alert.severity}\n"
        f"Time: {alert.timestamp}\n"
        f"Host: {alert.hostname}\n\n"
        "Why it fired:\n"
        f"- {alert.details}\n\n"
        "Included artifacts:\n"
        "- alert.json: full alert payload\n"
        "- events.jsonl: raw related events (± window)\n"
    )

    mem = io.BytesIO()
    with zipfile.ZipFile(mem, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("alert.json", json.dumps(crud.alert_to_dict(alert), indent=2, default=str))
        z.writestr("README.txt", readme)
        jsonl = "\n".join(json.dumps(crud.event_to_dict(e), default=str) for e in events)
        z.writestr("events.jsonl", jsonl)

    mem.seek(0)
    headers = {"Content-Disposition": f'attachment; filename="evidence_{alert.id}.zip"'}
    return StreamingResponse(mem, media_type="application/zip", headers=headers)


# -----------------------------
# Catalog endpoints (new)
# -----------------------------
@router.get("/catalog/channels")
def catalog_channels(
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
):
    require_api_key(x_api_key)
    return {"channels": settings.supported_channels}


@router.get("/catalog/event-ids")
def catalog_event_ids(
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
):
    require_api_key(x_api_key)
    return {"event_ids": settings.supported_event_ids}


@router.get("/health")
def health():
    return {"status": "ok"}