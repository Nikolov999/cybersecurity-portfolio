from __future__ import annotations

import requests
from dataclasses import dataclass
from typing import Any, Dict, Optional

@dataclass
class Http:
    base_url: str
    verify_tls: bool
    timeout_seconds: int

    def post(self, path: str, *, headers: Optional[Dict[str,str]] = None, json_body: Any = None) -> requests.Response:
        url = f"{self.base_url}{path}"
        return requests.post(url, headers=headers or {}, json=json_body, timeout=self.timeout_seconds, verify=self.verify_tls)

    def get(self, path: str, *, headers: Optional[Dict[str,str]] = None, params: Optional[Dict[str,Any]] = None) -> requests.Response:
        url = f"{self.base_url}{path}"
        return requests.get(url, headers=headers or {}, params=params, timeout=self.timeout_seconds, verify=self.verify_tls)
