from __future__ import annotations

import os
import platform
import socket
import time
from typing import Any, Dict, List

def _interfaces_best_effort() -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    # portable best-effort: hostname->IPs
    try:
        host = socket.gethostname()
        infos = socket.getaddrinfo(host, None)
        ips = sorted({i[4][0] for i in infos if i and i[4]})
        for ip in ips:
            out.append({"ip": ip})
    except Exception:
        pass
    return out

def collect_common_extras() -> Dict[str, Any]:
    return {
        "hostname": platform.node(),
        "platform": platform.platform(),
        "pid": os.getpid(),
        "uptime_seconds_best_effort": int(time.time() - ps_start_time()),
        "interfaces_best_effort": _interfaces_best_effort(),
    }

_PS_START = time.time()
def ps_start_time() -> float:
    return _PS_START
