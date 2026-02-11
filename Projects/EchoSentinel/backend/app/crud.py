from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import select, desc, func, case
from . import models, schemas


def create_event(db: Session, payload: schemas.IngestEvent) -> models.Event:
    ev = models.Event(
        timestamp=payload.timestamp,
        hostname=payload.hostname,
        event_id=payload.event_id,
        username=payload.username,
        source_ip=payload.source_ip,
        channel=payload.channel,
        record_id=payload.record_id,
        raw=payload.raw,
    )
    db.add(ev)
    db.commit()
    db.refresh(ev)
    return ev


def create_alert(
    db: Session,
    rule_name: str,
    severity: str,
    timestamp: datetime,
    hostname: str,
    details: str,
    event_id: int | None = None,
    username: str | None = None,
    source_ip: str | None = None,
) -> models.Alert:
    al = models.Alert(
        rule_name=rule_name,
        severity=severity,
        timestamp=timestamp,
        hostname=hostname,
        event_id=event_id,
        username=username,
        source_ip=source_ip,
        details=details,
    )
    db.add(al)
    db.commit()
    db.refresh(al)
    return al


def list_events(
    db: Session,
    limit: int = 200,
    hostname: str | None = None,
    event_id: int | None = None,
    username: str | None = None,
):
    stmt = select(models.Event).order_by(desc(models.Event.timestamp)).limit(limit)
    if hostname:
        stmt = stmt.where(models.Event.hostname == hostname)
    if event_id:
        stmt = stmt.where(models.Event.event_id == event_id)
    if username:
        stmt = stmt.where(models.Event.username == username)
    return db.execute(stmt).scalars().all()


def list_alerts(
    db: Session,
    limit: int = 200,
    hostname: str | None = None,
    severity: str | None = None,
):
    stmt = select(models.Alert).order_by(desc(models.Alert.timestamp)).limit(limit)
    if hostname:
        stmt = stmt.where(models.Alert.hostname == hostname)
    if severity:
        stmt = stmt.where(models.Alert.severity == severity)
    return db.execute(stmt).scalars().all()


def recent_events(
    db: Session,
    hostname: str,
    start: datetime,
    end: datetime,
    event_ids: list[int] | None = None,
    source_ip: str | None = None,
    username: str | None = None,
):
    stmt = (
        select(models.Event)
        .where(models.Event.hostname == hostname)
        .where(models.Event.timestamp >= start)
        .where(models.Event.timestamp <= end)
        .order_by(desc(models.Event.timestamp))
    )
    if event_ids:
        stmt = stmt.where(models.Event.event_id.in_(event_ids))
    if source_ip:
        stmt = stmt.where(models.Event.source_ip == source_ip)
    if username:
        stmt = stmt.where(models.Event.username == username)
    return db.execute(stmt).scalars().all()


def alert_suppressed(
    db: Session,
    rule_name: str,
    hostname: str,
    start: datetime,
    username: str | None,
    source_ip: str | None,
) -> bool:
    stmt = (
        select(func.count(models.Alert.id))
        .where(models.Alert.rule_name == rule_name)
        .where(models.Alert.hostname == hostname)
        .where(models.Alert.timestamp >= start)
    )
    if username is None:
        stmt = stmt.where(models.Alert.username.is_(None))
    else:
        stmt = stmt.where(models.Alert.username == username)
    if source_ip is None:
        stmt = stmt.where(models.Alert.source_ip.is_(None))
    else:
        stmt = stmt.where(models.Alert.source_ip == source_ip)
    return int(db.execute(stmt).scalar_one()) > 0


def user_ip_first_seen(
    db: Session,
    username: str,
    source_ip: str,
    start: datetime,
    end: datetime,
) -> bool:
    stmt = (
        select(func.count(models.Event.id))
        .where(models.Event.username == username)
        .where(models.Event.source_ip == source_ip)
        .where(models.Event.timestamp >= start)
        .where(models.Event.timestamp <= end)
    )
    return int(db.execute(stmt).scalar_one()) == 0


def get_alert_by_id(db: Session, alert_id: int) -> models.Alert | None:
    stmt = select(models.Alert).where(models.Alert.id == alert_id).limit(1)
    return db.execute(stmt).scalars().first()


def list_events_window(
    db: Session,
    hostname: str,
    start: datetime,
    end: datetime,
    limit: int = 10000,
) -> list[models.Event]:
    limit = max(1, min(limit, 20000))
    stmt = (
        select(models.Event)
        .where(models.Event.hostname == hostname)
        .where(models.Event.timestamp >= start)
        .where(models.Event.timestamp <= end)
        .order_by(models.Event.timestamp.asc())
        .limit(limit)
    )
    return db.execute(stmt).scalars().all()


def event_to_dict(ev: models.Event) -> dict:
    return {
        "id": ev.id,
        "timestamp": ev.timestamp,
        "hostname": ev.hostname,
        "event_id": ev.event_id,
        "username": ev.username,
        "source_ip": ev.source_ip,
        "channel": ev.channel,
        "record_id": ev.record_id,
        "raw": ev.raw,
        "created_at": ev.created_at,
    }


def alert_to_dict(al: models.Alert) -> dict:
    return {
        "id": al.id,
        "rule_name": al.rule_name,
        "severity": al.severity,
        "timestamp": al.timestamp,
        "hostname": al.hostname,
        "event_id": al.event_id,
        "username": al.username,
        "source_ip": al.source_ip,
        "details": al.details,
        "created_at": al.created_at,
    }


def list_endpoints(db: Session, limit: int = 200, lookback_hours: int = 24):
    """Inventory derived from events (hostname-based)."""
    limit = max(1, min(limit, 2000))
    lookback_hours = max(1, min(lookback_hours, 720))

    now = datetime.utcnow()
    win_start = now - timedelta(hours=lookback_hours)

    sysmon_flag = case(
        (func.lower(func.coalesce(models.Event.channel, "")).like("%sysmon%"), 1),
        else_=0,
    )

    stmt = (
        select(
            models.Event.hostname.label("hostname"),
            func.max(models.Event.timestamp).label("last_seen"),
            func.group_concat(func.distinct(models.Event.channel)).label("channels_csv"),
            func.max(sysmon_flag).label("sysmon_present_int"),
            func.sum(
                case(
                    (models.Event.timestamp >= win_start, 1),
                    else_=0,
                )
            ).label("events_in_window"),
        )
        .group_by(models.Event.hostname)
        .order_by(desc(func.max(models.Event.timestamp)))
        .limit(limit)
    )

    rows = db.execute(stmt).all()

    out = []
    hours = float(lookback_hours)
    for r in rows:
        channels_csv = r.channels_csv or ""
        channels = [c for c in (x.strip() for x in channels_csv.split(",")) if c]
        events_in_window = int(r.events_in_window or 0)
        out.append(
            {
                "hostname": r.hostname,
                "last_seen": r.last_seen,
                "channels_seen": channels,
                "sysmon_present": bool(int(r.sysmon_present_int or 0)),
                "event_rate": events_in_window / hours if hours > 0 else 0.0,
            }
        )
    return out