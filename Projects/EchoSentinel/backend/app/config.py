from pydantic_settings import BaseSettings, SettingsConfigDict


def _split_csv(v: str) -> list[str]:
    items = [x.strip() for x in (v or "").split(",")]
    return [x for x in items if x]


def _split_csv_int(v: str) -> list[int]:
    out: list[int] = []
    for x in _split_csv(v):
        try:
            out.append(int(x))
        except Exception:
            continue
    return out


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="SENTINEL_", case_sensitive=False)

    db_path: str = "sentinel.db"
    api_key: str = "CHANGE_ME_LONG_RANDOM"

    # allowlists / safelists (comma-separated)
    admin_users_csv: str = "Administrator,DOMAIN\\Administrator"
    management_ips_csv: str = "127.0.0.1"
    allow_4672_users_csv: str = "Administrator,DOMAIN\\Administrator"
    allowed_service_names_csv: str = ""  # exact matches
    allowed_task_names_csv: str = ""  # exact matches
    allowed_host_pairs_csv: str = ""  # entries like SRC->DST

    # suppression (collapse identical alerts)
    suppress_window_seconds_low: int = 900      # 15m
    suppress_window_seconds_medium: int = 1800  # 30m
    suppress_window_seconds_high: int = 1800    # 30m

    # windows / thresholds (defaults)
    brute_fail_threshold: int = 5
    brute_fail_window_seconds: int = 120

    spray_fail_threshold: int = 15
    spray_window_seconds: int = 300
    spray_distinct_user_threshold: int = 6

    rdp_brute_fail_threshold: int = 3
    rdp_brute_window_seconds: int = 60

    impossible_travel_window_seconds: int = 600

    first_seen_lookback_days: int = 30

    service_start_correlation_seconds: int = 120

    # --------------------------
    # Catalog (for projects)
    # --------------------------
    # Does NOT enforce ingest; it’s just a canonical list the UI/agent can display/use.
    supported_channels_csv: str = (
        "Security,"
        "System,"
        "Microsoft-Windows-PowerShell/Operational,"
        "Windows PowerShell,"
        "Microsoft-Windows-WinRM/Operational,"
        "Microsoft-Windows-TaskScheduler/Operational,"
        "Microsoft-Windows-DNS-Client/Operational,"
        "Microsoft-Windows-Sysmon/Operational"
    )

    supported_event_ids_csv: str = (
        # Security (auth/session)
        "4624,4625,4634,4647,4648,4672,"
        "4778,4779,"
        "4768,4769,4771,4776,"
        # Account / privilege / posture
        "4720,4722,4728,4729,4732,4733,4738,4740,"
        "1102,4719,"
        # SMB
        "5140,5145,"
        # Persistence (security)
        "4697,4698,"
        # System (services)
        "7036,7040,7045,"
        # Sysmon
        "1,3,7,10,11,13,22"
    )

    @property
    def admin_users(self) -> list[str]:
        return _split_csv(self.admin_users_csv)

    @property
    def management_ips(self) -> list[str]:
        return _split_csv(self.management_ips_csv)

    @property
    def allow_4672_users(self) -> list[str]:
        return _split_csv(self.allow_4672_users_csv)

    @property
    def allowed_service_names(self) -> list[str]:
        return _split_csv(self.allowed_service_names_csv)

    @property
    def allowed_task_names(self) -> list[str]:
        return _split_csv(self.allowed_task_names_csv)

    @property
    def allowed_host_pairs(self) -> list[str]:
        return _split_csv(self.allowed_host_pairs_csv)

    @property
    def supported_channels(self) -> list[str]:
        return _split_csv(self.supported_channels_csv)

    @property
    def supported_event_ids(self) -> list[int]:
        return _split_csv_int(self.supported_event_ids_csv)


settings = Settings()