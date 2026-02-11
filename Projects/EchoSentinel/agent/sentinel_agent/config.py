from dataclasses import dataclass
import os


@dataclass(frozen=True)
class AgentConfig:
    backend_url: str
    api_key: str
    poll_seconds: int
    channels: list[str]
    event_ids: set[int]
    state_dir: str


def load_config() -> AgentConfig:
    # 0.0.0.0 is a bind address (server). Client must use 127.0.0.1 or a real IP/hostname.
    backend_url = os.getenv("SENTINEL_AGENT_BACKEND_URL", "http://127.0.0.1:8345").rstrip("/")
    api_key = os.getenv("SENTINEL_AGENT_API_KEY", "CHANGE_ME_LONG_RANDOM")
    poll_seconds = int(os.getenv("SENTINEL_AGENT_POLL_SECONDS", "5"))

    # Expanded channels for RDP/WinRM/PowerShell/Tasks/DNS + System + Sysmon
    channels_raw = os.getenv(
        "SENTINEL_AGENT_CHANNELS",
        ",".join(
            [
                "Security",
                "System",
                "Microsoft-Windows-PowerShell/Operational",
                "Windows PowerShell",
                "Microsoft-Windows-WinRM/Operational",
                "Microsoft-Windows-TaskScheduler/Operational",
                "Microsoft-Windows-DNS-Client/Operational",
                "Microsoft-Windows-Sysmon/Operational",
            ]
        ),
    )
    channels = [c.strip() for c in channels_raw.split(",") if c.strip()]

    # Expanded event IDs to support the full portfolio series set
    event_ids_raw = os.getenv(
        "SENTINEL_AGENT_EVENT_IDS",
        ",".join(
            str(x)
            for x in [
                # ---- Security: auth / session ----
                4624, 4625, 4634, 4647, 4648, 4672,
                4778, 4779,
                4768, 4769, 4771, 4776,

                # ---- Security: account / privilege / posture ----
                4720, 4722, 4728, 4729, 4732, 4733, 4738, 4740,
                1102, 4719,

                # ---- Security: SMB ----
                5140, 5145,

                # ---- Security: persistence ----
                4697, 4698,

                # ---- System: services / operations ----
                7036, 7040, 7045,

                # ---- Sysmon (only if present) ----
                1, 3, 7, 10, 11, 13, 22,
            ]
        ),
    )
    event_ids = {int(x.strip()) for x in event_ids_raw.split(",") if x.strip().isdigit()}

    programdata = os.getenv("ProgramData", r"C:\ProgramData")
    state_dir = os.path.join(programdata, "EchoSentinel", "agent")
    os.makedirs(state_dir, exist_ok=True)

    return AgentConfig(
        backend_url=backend_url,
        api_key=api_key,
        poll_seconds=max(1, min(poll_seconds, 60)),
        channels=channels,
        event_ids=event_ids,
        state_dir=state_dir,
    )