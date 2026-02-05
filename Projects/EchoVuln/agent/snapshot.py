from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, Optional

from agent.http_client import Http
from agent.collectors.common import collect_common_extras
from agent.collectors.windows import collect_windows_snapshot_parts, is_windows
from agent.collectors.linux import collect_linux_snapshot_parts, is_linux

def build_snapshot_payload(
    *,
    agent_id: str,
    asset_id: Optional[int],
    signal_internet_facing: bool,
    signal_business_critical: bool,
) -> Dict[str, Any]:
    collected_at = datetime.now(timezone.utc).isoformat()

    os_part = None
    reboot_pending = False
    missing_updates = []
    hotfix = None
    extras: Dict[str, Any] = {}

    if is_windows():
        os_part, reboot_pending, missing_updates, hotfix, extras = collect_windows_snapshot_parts()
    elif is_linux():
        os_part, reboot_pending, missing_updates, hotfix, extras = collect_linux_snapshot_parts()

    # merge common extras (interfaces, uptime, etc.)
    extras2 = collect_common_extras()
    extras = {**extras, **extras2}

    payload: Dict[str, Any] = {
        "schema_version": 2,
        "agent_id": agent_id,
        "asset_id": asset_id,
        "collected_at_utc": collected_at,
        "os": os_part,
        "reboot_pending": bool(reboot_pending),
        "missing_updates": missing_updates,
        "hotfix": hotfix,
        "signals": {
            "internet_facing": bool(signal_internet_facing),
            "business_critical": bool(signal_business_critical),
        },
        "extras": extras,
    }

    # drop Nones that your server schema allows as optional
    if payload["asset_id"] is None:
        payload.pop("asset_id", None)
    if payload["os"] is None:
        payload.pop("os", None)
    if payload["hotfix"] is None:
        payload.pop("hotfix", None)

    return payload

def send_snapshot(http: Http, bearer_token: str, payload: Dict[str, Any]) -> int:
    headers = {"Authorization": f"Bearer {bearer_token}"}
    r = http.post("/v2/ingest/snapshot", headers=headers, json_body=payload)
    if r.status_code >= 300:
        raise RuntimeError(f"Snapshot ingest failed: {r.status_code} {r.text}")
    data = r.json()
    sid = data.get("snapshot_id")
    return int(sid) if sid is not None else 0
