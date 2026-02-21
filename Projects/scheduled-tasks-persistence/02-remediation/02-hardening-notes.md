# 02  Hardening Notes (Lab-Appropriate)

## Logging
- Keep Sysmon enabled (event IDs 1 and 11 are extremely high value here).
- Enable TaskScheduler/Operational channel for richer task telemetry (register/run/complete).
- Keep Security auditing that surfaces 4624/4672.

## Detection Surface
- Monitor `schtasks.exe` usage, especially:
  - `/create`
  - `/run`
  - `/delete`
- Prioritize if parent process is `wsmprovhost.exe` (WinRM) or if created shortly after a remote logon.
- Flag tasks where `/ru SYSTEM` and action path is outside `C:\Windows\` or `C:\Program Files\`.

## Access Control (Conceptual)
- Restrict who can WinRM into endpoints.
- Enforce admin hygiene (separate admin accounts; limit local admin sprawl).
