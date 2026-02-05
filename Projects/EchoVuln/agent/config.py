from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path

APP_VENDOR = "EchoPentest"
APP_NAME = "EchoVuln"

def programdata_dir() -> Path:
    pd = os.environ.get("PROGRAMDATA", r"C:\ProgramData")
    d = Path(pd) / APP_VENDOR / APP_NAME / "agent"
    d.mkdir(parents=True, exist_ok=True)
    return d

def default_config_path() -> Path:
    return programdata_dir() / "config.json"

def default_state_path() -> Path:
    return programdata_dir() / "state.json"

@dataclass(frozen=True)
class Settings:
    backend_url: str
    enroll_key: str | None
    heartbeat_seconds: int
    snapshot_seconds: int
    signal_internet_facing: bool
    signal_business_critical: bool
    verify_tls: bool
    timeout_seconds: int
    config_path: Path
    state_path: Path

def _load_file_overrides(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}

def load_settings(argv: list[str] | None = None) -> Settings:
    import argparse

    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--backend-url")
    parser.add_argument("--enroll-key")
    parser.add_argument("--heartbeat-seconds", type=int)
    parser.add_argument("--snapshot-seconds", type=int)
    parser.add_argument("--internet-facing")
    parser.add_argument("--business-critical")
    parser.add_argument("--verify-tls")
    parser.add_argument("--timeout-seconds", type=int)
    args, _ = parser.parse_known_args(argv)

    config_path = default_config_path()
    state_path = default_state_path()

    file_cfg = _load_file_overrides(config_path)

    def _get(name: str, default=None):
        env = os.getenv(name)
        if env is not None:
            return env
        return file_cfg.get(name, default)

    # CLI overrides > env > file
    backend_url = (args.backend_url or str(_get("ECHOVULN_BACKEND_URL", ""))).rstrip("/")
    if not backend_url:
        raise RuntimeError("Missing ECHOVULN_BACKEND_URL")

    enroll_key = args.enroll_key if args.enroll_key is not None else _get("ECHOVULN_ENROLL_KEY", None)
    if enroll_key is not None:
        enroll_key = str(enroll_key).strip() or None

    heartbeat_seconds = int(args.heartbeat_seconds if args.heartbeat_seconds is not None else _get("ECHOVULN_HEARTBEAT_SECONDS", 60))
    snapshot_seconds = int(args.snapshot_seconds if args.snapshot_seconds is not None else _get("ECHOVULN_SNAPSHOT_SECONDS", 3600))

    signal_internet_facing = str(args.internet_facing if args.internet_facing is not None else _get("ECHOVULN_SIGNAL_INTERNET_FACING", "0")).strip().lower() in ("1","true","yes")
    signal_business_critical = str(args.business_critical if args.business_critical is not None else _get("ECHOVULN_SIGNAL_BUSINESS_CRITICAL", "0")).strip().lower() in ("1","true","yes")

    verify_tls = str(args.verify_tls if args.verify_tls is not None else _get("ECHOVULN_VERIFY_TLS", "1")).strip().lower() not in ("0","false","no")
    timeout_seconds = int(args.timeout_seconds if args.timeout_seconds is not None else _get("ECHOVULN_TIMEOUT_SECONDS", 15))

    return Settings(
        backend_url=backend_url,
        enroll_key=enroll_key,
        heartbeat_seconds=max(10, heartbeat_seconds),
        snapshot_seconds=max(60, snapshot_seconds),
        signal_internet_facing=signal_internet_facing,
        signal_business_critical=signal_business_critical,
        verify_tls=verify_tls,
        timeout_seconds=timeout_seconds,
        config_path=config_path,
        state_path=state_path,
    )

