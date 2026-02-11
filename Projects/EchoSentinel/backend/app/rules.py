from __future__ import annotations

from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from . import crud, schemas
from .config import settings
from .utils import (
    parse_logon_type,
    parse_task_name,
    parse_service_name,
    parse_workstation,
    parse_target,
    parse_parent_image,
    parse_image,
    parse_command_line,
    parse_signed_flag,
    parse_loaded_image,
    contains_any,
)


def _suppress_window(severity: str) -> int:
    sev = (severity or "").lower()
    if sev == "high":
        return settings.suppress_window_seconds_high
    if sev == "medium":
        return settings.suppress_window_seconds_medium
    return settings.suppress_window_seconds_low


def _emit(
    db: Session,
    *,
    rule_name: str,
    severity: str,
    now_ts: datetime,
    hostname: str,
    details: str,
    event_id: int | None,
    username: str | None,
    source_ip: str | None,
) -> int | None:
    win = _suppress_window(severity)
    start = now_ts - timedelta(seconds=win)
    if crud.alert_suppressed(
        db,
        rule_name=rule_name,
        hostname=hostname,
        start=start,
        username=username,
        source_ip=source_ip,
    ):
        return None
    al = crud.create_alert(
        db=db,
        rule_name=rule_name,
        severity=severity,
        timestamp=now_ts,
        hostname=hostname,
        event_id=event_id,
        username=username,
        source_ip=source_ip,
        details=details,
    )
    return al.id


def _is_admin_user(username: str | None) -> bool:
    if not username:
        return False
    u = username.strip().lower()
    return any(u == a.strip().lower() for a in settings.admin_users)


def run_rules_on_ingest(db: Session, ev: schemas.IngestEvent) -> list[int]:
    """Returns created alert IDs. Deterministic rules only."""
    created: list[int] = []
    now_ts: datetime = ev.timestamp
    host = ev.hostname

    # -------------------------
    # Pack 1: Auth & Access
    # -------------------------

    # ES-AUTH-001 Brute Force (single user)
    if ev.event_id == 4625 and ev.source_ip and ev.username:
        start = now_ts - timedelta(seconds=settings.brute_fail_window_seconds)
        events = crud.recent_events(
            db,
            hostname=host,
            start=start,
            end=now_ts,
            event_ids=[4625],
            source_ip=ev.source_ip,
            username=ev.username,
        )
        if len(events) >= settings.brute_fail_threshold:
            rule = f"ES-AUTH-001 Brute force suspected (≥{settings.brute_fail_threshold}/{settings.brute_fail_window_seconds}s)"
            aid = _emit(
                db,
                rule_name=rule,
                severity="medium",
                now_ts=now_ts,
                hostname=host,
                event_id=4625,
                username=ev.username,
                source_ip=ev.source_ip,
                details=f"{len(events)} failed logons (4625) for user from same source IP within window.",
            )
            if aid:
                created.append(aid)

    # ES-AUTH-002 Password Spray
    if ev.event_id == 4625 and ev.source_ip:
        start = now_ts - timedelta(seconds=settings.spray_window_seconds)
        events = crud.recent_events(
            db,
            hostname=host,
            start=start,
            end=now_ts,
            event_ids=[4625],
            source_ip=ev.source_ip,
        )
        if events:
            usernames = {e.username.strip().lower() for e in events if e.username}
            if len(events) >= settings.spray_fail_threshold and len(usernames) >= settings.spray_distinct_user_threshold:
                rule = "ES-AUTH-002 Password spray suspected"
                aid = _emit(
                    db,
                    rule_name=rule,
                    severity="high",
                    now_ts=now_ts,
                    hostname=host,
                    event_id=4625,
                    username=None,
                    source_ip=ev.source_ip,
                    details=f"{len(events)} failures from source IP across {len(usernames)} distinct usernames in {settings.spray_window_seconds}s.",
                )
                if aid:
                    created.append(aid)

    # ES-AUTH-003 RDP Brute (LogonType=10)
    if ev.event_id == 4625 and ev.source_ip and ev.username:
        lt = parse_logon_type(ev.raw)
        if lt == 10:
            start = now_ts - timedelta(seconds=settings.rdp_brute_window_seconds)
            events = crud.recent_events(
                db,
                hostname=host,
                start=start,
                end=now_ts,
                event_ids=[4625],
                source_ip=ev.source_ip,
                username=ev.username,
            )
            rdp_events = [e for e in events if parse_logon_type(e.raw) == 10]
            if len(rdp_events) >= settings.rdp_brute_fail_threshold:
                rule = f"ES-AUTH-003 RDP brute force (≥{settings.rdp_brute_fail_threshold}/{settings.rdp_brute_window_seconds}s)"
                aid = _emit(
                    db,
                    rule_name=rule,
                    severity="high",
                    now_ts=now_ts,
                    hostname=host,
                    event_id=4625,
                    username=ev.username,
                    source_ip=ev.source_ip,
                    details=f"{len(rdp_events)} failed RDP logons (LogonType=10) from same source IP within window.",
                )
                if aid:
                    created.append(aid)

    # ES-AUTH-004 Impossible travel substitute (same user, different IP, within 10 min)
    if ev.event_id == 4624 and ev.username and ev.source_ip:
        start = now_ts - timedelta(seconds=settings.impossible_travel_window_seconds)
        events = crud.recent_events(
            db,
            hostname=host,
            start=start,
            end=now_ts,
            event_ids=[4624],
            username=ev.username,
        )
        ips = {e.source_ip for e in events if e.source_ip}
        if len(ips) >= 2:
            sev = "high" if _is_admin_user(ev.username) else "medium"
            rule = "ES-AUTH-004 Rapid IP change for same user"
            aid = _emit(
                db,
                rule_name=rule,
                severity=sev,
                now_ts=now_ts,
                hostname=host,
                event_id=4624,
                username=ev.username,
                source_ip=ev.source_ip,
                details=f"User logged on from multiple source IPs within {settings.impossible_travel_window_seconds}s: {sorted(list(ips))[:10]}",
            )
            if aid:
                created.append(aid)

    # ES-AUTH-005 Privileged logon type focus (4624 type 10/3)
    if ev.event_id == 4624 and ev.username:
        lt = parse_logon_type(ev.raw)
        if _is_admin_user(ev.username) and lt in (10, 3):
            rule = "ES-AUTH-005 Privileged user network/RDP logon"
            aid = _emit(
                db,
                rule_name=rule,
                severity="medium",
                now_ts=now_ts,
                hostname=host,
                event_id=4624,
                username=ev.username,
                source_ip=ev.source_ip,
                details=f"Privileged user successful logon with LogonType={lt}.",
            )
            if aid:
                created.append(aid)

    # ES-AUTH-006 First-seen source IP for user (on success)
    if ev.event_id == 4624 and ev.username and ev.source_ip:
        lookback_start = now_ts - timedelta(days=settings.first_seen_lookback_days)
        end = now_ts - timedelta(microseconds=1)
        first_seen = crud.user_ip_first_seen(
            db,
            username=ev.username,
            source_ip=ev.source_ip,
            start=lookback_start,
            end=end,
        )
        if first_seen:
            sev = "medium" if _is_admin_user(ev.username) else "low"
            rule = "ES-AUTH-006 First-seen source IP for user"
            aid = _emit(
                db,
                rule_name=rule,
                severity=sev,
                now_ts=now_ts,
                hostname=host,
                event_id=4624,
                username=ev.username,
                source_ip=ev.source_ip,
                details=f"First-seen (username, source_ip) within {settings.first_seen_lookback_days} day lookback.",
            )
            if aid:
                created.append(aid)

    # ES-AUTH-007 Explicit credentials used (4648)
    if ev.event_id == 4648 and ev.username:
        tgt = parse_target(ev.raw)
        sev = "high" if _is_admin_user(ev.username) else "medium"
        rule = "ES-AUTH-007 Explicit credentials used (4648)"
        aid = _emit(
            db,
            rule_name=rule,
            severity=sev,
            now_ts=now_ts,
            hostname=host,
            event_id=4648,
            username=ev.username,
            source_ip=ev.source_ip,
            details=f"Explicit credentials used. Target={tgt or 'unknown'} (review raw for details).",
        )
        if aid:
            created.append(aid)

    # ES-AUTH-008 Special privileges at logon (4672) when not allowlisted
    if ev.event_id == 4672 and ev.username:
        u = ev.username.strip().lower()
        allow = any(u == a.strip().lower() for a in settings.allow_4672_users)
        if not allow:
            rule = "ES-AUTH-008 Special privileges assigned at logon (4672)"
            aid = _emit(
                db,
                rule_name=rule,
                severity="medium",
                now_ts=now_ts,
                hostname=host,
                event_id=4672,
                username=ev.username,
                source_ip=ev.source_ip,
                details="Special privileges assigned at logon for non-allowlisted user.",
            )
            if aid:
                created.append(aid)

    # -------------------------
    # Pack 2: Persistence & Privilege
    # -------------------------

    # ES-PERS-001 New service installed (4697)
    if ev.event_id == 4697:
        svc = parse_service_name(ev.raw)
        if not (svc and any(svc.strip().lower() == a.strip().lower() for a in settings.allowed_service_names)):
            rule = "ES-PERS-001 New service installed (4697)"
            aid = _emit(
                db,
                rule_name=rule,
                severity="medium",
                now_ts=now_ts,
                hostname=host,
                event_id=4697,
                username=ev.username,
                source_ip=ev.source_ip,
                details=f"Service install observed. Service={svc or 'unknown'} (review raw for path/binary).",
            )
            if aid:
                created.append(aid)

        # ES-PERS-002 correlate install then start (4697 -> 7045/7036)
        start = now_ts
        end = now_ts + timedelta(seconds=settings.service_start_correlation_seconds)
        sys_events = crud.recent_events(
            db,
            hostname=host,
            start=start,
            end=end,
            event_ids=[7045, 7036],
        )
        if sys_events:
            rule = "ES-PERS-002 Service installed then started shortly after"
            aid = _emit(
                db,
                rule_name=rule,
                severity="high",
                now_ts=now_ts,
                hostname=host,
                event_id=4697,
                username=ev.username,
                source_ip=ev.source_ip,
                details=f"Service install followed by system service activity within {settings.service_start_correlation_seconds}s (7045/7036).",
            )
            if aid:
                created.append(aid)

    # ES-PERS-003 Scheduled task creation (4698) => medium / high if suspicious
    if ev.event_id == 4698:
        task = parse_task_name(ev.raw)
        if not (task and any(task.strip().lower() == a.strip().lower() for a in settings.allowed_task_names)):
            suspicious = False
            if task:
                t = task.lower()
                suspicious = any(x in t for x in ["\\temp", "temp\\", "users\\public", "appdata", "\\public\\"])
            sev = "high" if suspicious else "medium"
            rule = "ES-PERS-003 Scheduled task created (4698)"
            aid = _emit(
                db,
                rule_name=rule,
                severity=sev,
                now_ts=now_ts,
                hostname=host,
                event_id=4698,
                username=ev.username,
                source_ip=ev.source_ip,
                details=f"Scheduled task created. Task={task or 'unknown'}. Suspicious={suspicious}.",
            )
            if aid:
                created.append(aid)

    # ES-PERS-004 Admin group membership changed (4732/4733)
    if ev.event_id in (4732, 4733):
        rule = "ES-PERS-004 Account added/removed from Administrators (4732/4733)"
        aid = _emit(
            db,
            rule_name=rule,
            severity="high",
            now_ts=now_ts,
            hostname=host,
            event_id=ev.event_id,
            username=ev.username,
            source_ip=ev.source_ip,
            details="Group membership changed. Verify Administrators group target (review raw).",
        )
        if aid:
            created.append(aid)

    # ES-PERS-005 New user created (4720)
    if ev.event_id == 4720:
        rule = "ES-PERS-005 New user created (4720)"
        aid = _emit(
            db,
            rule_name=rule,
            severity="high",
            now_ts=now_ts,
            hostname=host,
            event_id=4720,
            username=ev.username,
            source_ip=ev.source_ip,
            details="New local/domain user created. Review raw for creator + created account.",
        )
        if aid:
            created.append(aid)

    # ES-PERS-006 User enabled (4722)
    if ev.event_id == 4722:
        rule = "ES-PERS-006 User enabled (4722)"
        aid = _emit(
            db,
            rule_name=rule,
            severity="high",
            now_ts=now_ts,
            hostname=host,
            event_id=4722,
            username=ev.username,
            source_ip=ev.source_ip,
            details="User account enabled. Review raw for actor + target account.",
        )
        if aid:
            created.append(aid)

    # -------------------------
    # Pack 3: Lateral Movement (best-effort, requires workstation in raw)
    # -------------------------

    # ES-LAT-001 New host pair for admin (source workstation -> target server)
    if ev.event_id == 4624 and ev.username and _is_admin_user(ev.username):
        src = parse_workstation(ev.raw)
        dst = host
        if src:
            pair = f"{src}->{dst}".lower()
            if not any(pair == a.strip().lower() for a in settings.allowed_host_pairs):
                start = now_ts - timedelta(days=30)
                events = crud.recent_events(
                    db,
                    hostname=host,
                    start=start,
                    end=now_ts,
                    event_ids=[4624],
                    username=ev.username,
                )
                seen_pairs = set()
                for e in events:
                    s = parse_workstation(e.raw)
                    if s:
                        seen_pairs.add(f"{s}->{host}".lower())
                if pair not in seen_pairs:
                    rule = "ES-LAT-001 First-seen admin workstation→server logon pair"
                    aid = _emit(
                        db,
                        rule_name=rule,
                        severity="medium",
                        now_ts=now_ts,
                        hostname=host,
                        event_id=4624,
                        username=ev.username,
                        source_ip=ev.source_ip,
                        details=f"First-seen admin host pair: {src} -> {dst} (30d lookback).",
                    )
                    if aid:
                        created.append(aid)

    # -------------------------
    # Pack 4: Sysmon (only if channel indicates Sysmon)
    # -------------------------
    is_sysmon = (ev.channel or "").lower().find("sysmon") >= 0

    if is_sysmon and ev.event_id == 1:
        parent = (parse_parent_image(ev.raw) or "").lower()
        child = (parse_image(ev.raw) or "").lower()
        cmd = (parse_command_line(ev.raw) or "").lower()

        # ES-SYS-001 winword.exe -> scripting/powershell family
        if parent.endswith("winword.exe") and contains_any(
            child,
            ["powershell.exe", "wscript.exe", "cscript.exe", "mshta.exe", "rundll32.exe", "regsvr32.exe"],
        ):
            rule = "ES-SYS-001 Suspicious parent→child (Office → LOLBins)"
            aid = _emit(
                db,
                rule_name=rule,
                severity="high",
                now_ts=now_ts,
                hostname=host,
                event_id=1,
                username=ev.username,
                source_ip=ev.source_ip,
                details=f"Parent={parent} Child={child}. Review command line in raw.",
            )
            if aid:
                created.append(aid)

        # ES-SYS-002 LOLBins with network-ish behavior patterns
        if contains_any(child, ["powershell.exe", "certutil.exe", "bitsadmin.exe", "curl.exe", "wget.exe"]):
            if contains_any(
                cmd,
                [" -enc", " -encodedcommand", "urlcache", "http://", "https://", "bitsadmin", "download", "/transfer"],
            ):
                rule = "ES-SYS-002 LOLBins with network indicators"
                aid = _emit(
                    db,
                    rule_name=rule,
                    severity="high",
                    now_ts=now_ts,
                    hostname=host,
                    event_id=1,
                    username=ev.username,
                    source_ip=ev.source_ip,
                    details=f"Process={child}. CommandLine hints network/download behavior.",
                )
                if aid:
                    created.append(aid)

    if is_sysmon and ev.event_id == 11:
        raw_lower = (ev.raw or "").lower()
        persistence_hits = any(
            p in raw_lower
            for p in [
                "\\startup\\",
                "\\start menu\\programs\\startup",
                "\\scheduledtasks\\",
                "\\system32\\tasks\\",
                "\\services\\",
                "\\run\\",
                "\\runonce\\",
            ]
        )
        if persistence_hits:
            sev = "high" if (ev.username and _is_admin_user(ev.username)) else "medium"
            rule = "ES-SYS-003 File created in persistence path"
            aid = _emit(
                db,
                rule_name=rule,
                severity=sev,
                now_ts=now_ts,
                hostname=host,
                event_id=11,
                username=ev.username,
                source_ip=ev.source_ip,
                details="Sysmon file create in persistence-related location (review raw for path).",
            )
            if aid:
                created.append(aid)

    if is_sysmon and ev.event_id == 7:
        signed = parse_signed_flag(ev.raw)
        proc = (parse_image(ev.raw) or "").lower()
        dll = (parse_loaded_image(ev.raw) or "").lower()
        sensitive = any(x in proc for x in ["lsass.exe", "winlogon.exe", "services.exe", "svchost.exe"])
        if sensitive and signed in ("false", "no", "unsigned"):
            rule = "ES-SYS-004 Unsigned DLL load in sensitive process"
            aid = _emit(
                db,
                rule_name=rule,
                severity="medium",
                now_ts=now_ts,
                hostname=host,
                event_id=7,
                username=ev.username,
                source_ip=ev.source_ip,
                details=f"Process={proc or 'unknown'} Loaded={dll or 'unknown'} Signed={signed}.",
            )
            if aid:
                created.append(aid)

    return created