from __future__ import annotations

from agent.http_client import Http

def send_heartbeat(http: Http, bearer_token: str) -> None:
    headers = {"Authorization": f"Bearer {bearer_token}"}
    r = http.post("/v2/ingest/heartbeat", headers=headers, json_body=None)
    if r.status_code >= 300:
        raise RuntimeError(f"Heartbeat failed: {r.status_code} {r.text}")
