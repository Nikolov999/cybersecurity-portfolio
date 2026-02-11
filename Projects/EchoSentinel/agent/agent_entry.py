# agent_entry.py
import sys

def main() -> int:
    # Import as a package so relative imports inside sentinel_agent work
    from sentinel_agent.main import main as agent_main
    try:
        return int(agent_main() or 0)
    except SystemExit as e:
        return int(getattr(e, "code", 0) or 0)

if __name__ == "__main__":
    raise SystemExit(main())