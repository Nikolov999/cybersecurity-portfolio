# 01  Detection and IR

## Objective
Document the analyst workflow for identifying **WinRM-delivered scheduled task persistence** using EchoSentinel telemetry.

## Incident Storyline (What Happened)
1. A remote network logon occurred (**4624 Logon Type 3**) for user `vagrant`.
2. The session received elevated privileges (**4672**).
3. From that remote context, `schtasks.exe` was used to create a persistence task:
   - Task name: `WindowsUpdateCheck`
   - Trigger: `ONLOGON`
   - Runs as: `SYSTEM`
   - Action: `powershell.exe -ExecutionPolicy Bypass -File C:\Users\Public\updater.ps1`
4. The task definition was written to disk:
   - `C:\Windows\System32\Tasks\WindowsUpdateCheck`
5. The task was executed immediately (`schtasks /run`), validating persistence and execution.

## Key Data Sources
- **Security**: 4624, 4672
- **Sysmon/Operational**: 1 (Process Create), 11 (File Create)

## Key Artifacts
- Scheduled task file:
  - `C:\Windows\System32\Tasks\WindowsUpdateCheck`
- Payload script:
  - `C:\Users\Public\updater.ps1`

## Evidence References (Screenshots)
- 4624 logon type 3: `Screenshot 2026-02-19 155959.png`
- 4672 privileges: `Screenshot 2026-02-19 155932.png`
- schtasks /create: `Screenshot 2026-02-19 160506.png`
- task file written (SYSTEM): `Screenshot 2026-02-19 160403.png`
- schtasks /run: `Screenshot 2026-02-19 160520.png`
- updater.ps1 written from WinRM host: `Screenshot 2026-02-19 160710.png`
