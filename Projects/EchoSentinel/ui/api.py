import os
import requests

BACKEND_URL = os.getenv("SENTINEL_UI_BACKEND_URL", "http://127.0.0.1:8345").rstrip("/")
API_KEY = os.getenv("SENTINEL_UI_API_KEY", "CHANGE_ME_LONG_RANDOM")

_s = requests.Session()


def _headers():
    return {"X-API-Key": API_KEY}


def health():
    r = _s.get(f"{BACKEND_URL}/health", timeout=6)
    r.raise_for_status()
    return r.json()


def get_events(limit=500, hostname=None, event_id=None, username=None):
    params = {"limit": limit}
    if hostname:
        params["hostname"] = hostname
    if event_id:
        params["event_id"] = event_id
    if username:
        params["username"] = username
    r = _s.get(f"{BACKEND_URL}/events", params=params, headers=_headers(), timeout=10)
    r.raise_for_status()
    return r.json()


def get_alerts(limit=500, hostname=None, severity=None):
    params = {"limit": limit}
    if hostname:
        params["hostname"] = hostname
    if severity:
        params["severity"] = severity
    r = _s.get(f"{BACKEND_URL}/alerts", params=params, headers=_headers(), timeout=10)
    r.raise_for_status()
    return r.json()