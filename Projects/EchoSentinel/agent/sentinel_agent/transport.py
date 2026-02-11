from __future__ import annotations

import requests
from requests.adapters import HTTPAdapter


class BackendClient:
    def __init__(self, base_url: str, api_key: str, timeout_seconds: int = 3):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout_seconds = timeout_seconds

        s = requests.Session()

        # HARD disable any urllib3 retries/backoff.
        adapter = HTTPAdapter(max_retries=0, pool_connections=10, pool_maxsize=10)
        s.mount("http://", adapter)
        s.mount("https://", adapter)

        self.s = s

    def ingest_event(self, payload: dict) -> bool:
        url = f"{self.base_url}/ingest/event"
        headers = {"X-API-Key": self.api_key}

        try:
            r = self.s.post(url, json=payload, headers=headers, timeout=self.timeout_seconds)
            if 200 <= r.status_code < 300:
                return True

            body = (r.text or "").strip().replace("\r", " ").replace("\n", " ")
            if len(body) > 400:
                body = body[:400] + "..."
            print(f"[ingest] FAIL status={r.status_code} url={url} body={body}")
            return False

        except requests.RequestException as e:
            print(f"[ingest] ERROR url={url} err={type(e).__name__}: {e}")
            return False