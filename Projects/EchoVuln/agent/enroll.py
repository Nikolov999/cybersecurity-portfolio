from __future__ import annotations

import platform
import socket
from typing import Optional, Tuple

from agent.http_client import Http

def _guess_ip() -> Optional[str]:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return None

def enroll_if_needed(http: Http, *, enroll_key: Optional[str], agent_id: str, existing_token: Optional[str]) -> Tuple[Optional[str], Optional[int]]:
    if existing_token:
        return existing_token, None

    if not enroll_key:
        raise RuntimeError("Missing enroll key for first-time enrollment (ECHOVULN_ENROLL_KEY)")

    hostname = platform.node() or None
    os_name = f"{platform.system()} {platform.release()}".strip() or None
    ip = _guess_ip()

    payload = {
        "agent_id": agent_id,
        "hostname": hostname,
        "os": os_name,
        "ip": ip,
    }

    headers = {"X-ENROLL-KEY": enroll_key}
    r = http.post("/v2/agents/enroll", headers=headers, json_body=payload)
    if r.status_code >= 300:
        raise RuntimeError(f"Enroll failed: {r.status_code} {r.text}")

    data = r.json()
    token = data.get("agent_token")
    asset_id = data.get("asset_id")
    if not token:
        raise RuntimeError("Enroll response missing agent_token")
    return str(token), int(asset_id) if asset_id is not None else None
