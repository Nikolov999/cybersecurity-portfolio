import json
import os
from typing import Dict
from uuid import uuid4


def _state_path(state_dir: str) -> str:
    return os.path.join(state_dir, "state.json")


def _agent_id_path(state_dir: str) -> str:
    return os.path.join(state_dir, "agent_id.txt")


def load_state(state_dir: str) -> Dict[str, int]:
    path = _state_path(state_dir)
    if not os.path.exists(path):
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            return {str(k): int(v) for k, v in data.items()}
    except Exception:
        return {}
    return {}


def save_state(state_dir: str, state: Dict[str, int]) -> None:
    path = _state_path(state_dir)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, sort_keys=True)
    os.replace(tmp, path)


def get_or_create_agent_id(state_dir: str) -> str:
    """
    Stable endpoint identity for inventory + evidence workflows.
    Stored once and reused across restarts.
    """
    path = _agent_id_path(state_dir)
    try:
        if os.path.exists(path):
            v = (open(path, "r", encoding="utf-8").read() or "").strip()
            if v and len(v) >= 16:
                return v
    except Exception:
        pass

    v = str(uuid4())
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(v)
    os.replace(tmp, path)
    return v