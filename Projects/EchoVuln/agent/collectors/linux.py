from __future__ import annotations

import platform
import subprocess
from typing import Any, Dict, List, Optional, Tuple

def is_linux() -> bool:
    return platform.system().lower() == "linux"

def _run(cmd: list[str], timeout: int = 30) -> Tuple[int, str, str]:
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    return p.returncode, p.stdout.strip(), p.stderr.strip()

def _get_os() -> Optional[Dict[str, Any]]:
    try:
        rc, out, _ = _run(["bash", "-lc", "cat /etc/os-release | grep -E '^(NAME|VERSION|VERSION_ID)='"], timeout=5)
        name = None
        release = None
        build = None
        for line in out.splitlines():
            if line.startswith("NAME="):
                name = line.split("=",1)[1].strip().strip('"')
            if line.startswith("VERSION_ID="):
                release = line.split("=",1)[1].strip().strip('"')
            if line.startswith("VERSION="):
                build = line.split("=",1)[1].strip().strip('"')
        return {"name": name, "release": release, "build": build}
    except Exception:
        return None

def _reboot_pending() -> bool:
    rc, _, _ = _run(["bash", "-lc", "test -f /var/run/reboot-required"], timeout=5)
    return rc == 0

def _missing_updates_best_effort() -> List[Dict[str, Any]]:
    # Debian/Ubuntu best-effort: count upgradable packages; no KB/CVE mapping here.
    rc, out, _ = _run(["bash","-lc","apt-get -s upgrade 2>/dev/null | grep '^Inst ' | wc -l"], timeout=20)
    try:
        n = int(out.strip())
    except Exception:
        n = 0
    return [{"kb": None, "cve": None, "count": n}] if n > 0 else []

def _hotfix_info() -> Optional[Dict[str, Any]]:
    # Not meaningful on linux; keep None
    return None

def collect_linux_snapshot_parts() -> Tuple[Optional[Dict[str,Any]], bool, List[Dict[str,Any]], Optional[Dict[str,Any]], Dict[str,Any]]:
    os_part = _get_os()
    reboot_pending = _reboot_pending()
    missing_updates = _missing_updates_best_effort()
    hotfix = _hotfix_info()
    extras: Dict[str, Any] = {}
    return os_part, reboot_pending, missing_updates, hotfix, extras
