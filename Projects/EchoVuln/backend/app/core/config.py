from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

APP_VENDOR = "EchoPentest"
APP_NAME = "EchoVuln"


def _programdata_data_dir() -> Path:
    pd = os.environ.get("PROGRAMDATA", r"C:\ProgramData")
    return Path(pd) / APP_VENDOR / APP_NAME / "data"


def _default_database_url() -> str:
    data_dir = _programdata_data_dir()
    data_dir.mkdir(parents=True, exist_ok=True)
    db_path = data_dir / "echo_vuln_v2.db"
    return f"sqlite:///{db_path.as_posix()}"


@dataclass(frozen=True)
class Settings:
    database_url: str = os.getenv("DATABASE_URL", _default_database_url())

    # Security knobs
    pbkdf2_iters: int = int(os.getenv("ECHO_PBKDF2_ITERS", "200000"))

    # API metadata (optional)
    api_title: str = "EchoVuln Backend"
    api_version: str = os.getenv("ECHO_API_VERSION", "2.0.0")


settings = Settings()

# Backward-compatible exports used across your codebase
DATABASE_URL = settings.database_url
PBKDF2_ITERS = settings.pbkdf2_iters
API_TITLE = settings.api_title
API_VERSION = settings.api_version
