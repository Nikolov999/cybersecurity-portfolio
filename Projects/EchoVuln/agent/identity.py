from __future__ import annotations

import json
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

@dataclass
class AgentState:
    agent_id: str
    asset_id: Optional[int] = None
    agent_token: Optional[str] = None  # compound token_id.secret

def load_state(path: Path) -> AgentState:
    if path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
        agent_id = str(data.get("agent_id") or "").strip()
        if agent_id:
            return AgentState(
                agent_id=agent_id,
                asset_id=data.get("asset_id"),
                agent_token=data.get("agent_token"),
            )

    agent_id = uuid.uuid4().hex
    st = AgentState(agent_id=agent_id, asset_id=None, agent_token=None)
    save_state(path, st)
    return st

def save_state(path: Path, state: AgentState) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "agent_id": state.agent_id,
        "asset_id": state.asset_id,
        "agent_token": state.agent_token,
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
