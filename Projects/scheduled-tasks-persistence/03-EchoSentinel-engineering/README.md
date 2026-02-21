# 03  EchoSentinel Engineering

## Objective
Document exactly how EchoSentinel captured the chain and what to filter on to reproduce analysis fast.

## What EchoSentinel Already Captured (From Evidence)
- Sysmon process creation for `schtasks.exe`:
  - `/create` and `/run`
- Sysmon file creation for:
  - `C:\Windows\System32\Tasks\WindowsUpdateCheck`
  - `C:\Users\Public\updater.ps1`
- Security authentication/privilege context:
  - 4624 LogonType 3
  - 4672 special privileges

## Fast Filters (Operational)
Use these in EchoSentinel searches:
- `channel:"Microsoft-Windows-Sysmon/Operational" event_id:1 image:*schtasks.exe`
- `channel:"Microsoft-Windows-Sysmon/Operational" event_id:11 target_filename:*\\System32\\Tasks\\*`
- `channel:"Security" event_id:4624`
- `channel:"Security" event_id:4672`

## Evidence References
- schtasks /create: `Screenshot 2026-02-19 160506.png`
- schtasks /run: `Screenshot 2026-02-19 160520.png`
- task file write: `Screenshot 2026-02-19 160403.png`
- updater.ps1 write: `Screenshot 2026-02-19 160710.png`
- 4624/4672: `Screenshot 2026-02-19 155959.png`, `Screenshot 2026-02-19 155932.png`
