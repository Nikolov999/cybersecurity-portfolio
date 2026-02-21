# Scheduled Tasks / Persistence (WinRM)  EchoSentinel Security Series

## Summary
This project simulates realistic post-compromise persistence by creating and running a Windows Scheduled Task over **WinRM** and validates that **EchoSentinel** ingests and surfaces the full investigation chain.

You get a clean SOC-style storyline:

**WinRM authenticated access  privileged logon context  scheduled task creation  task artifact written  task executed  payload executed**

## What Was Done (High Level)
- Established WinRM session (PowerShell Remoting)
- Dropped a small test payload (`C:\Users\Public\updater.ps1`)
- Created scheduled task (`WindowsUpdateCheck`) using `schtasks.exe`
- Ran the task immediately (`schtasks /run`)
- Observed telemetry in EchoSentinel across Security + Sysmon

## Telemetry Captured (What Your Screenshots Prove)
### WinRM / Remote Auth
- **Security 4624**: Logon Type **3** (network logon), user `vagrant`
- **Security 4672**: Special privileges assigned to new logon

### Scheduled Task Persistence
- **Sysmon 1**: Process creation for `schtasks.exe` with `/create` and `/run`
- **Sysmon 11**: File created/modified for the task definition:
  - `C:\Windows\System32\Tasks\WindowsUpdateCheck`

### Payload / Execution Context
- Task runs as **SYSTEM** (`NT AUTHORITY\SYSTEM`)
- Parent chain shows WinRM context via **wsmprovhost.exe** (PowerShell Remoting host)

## MITRE ATT&CK Mapping
- **T1021.006**  Remote Services: WinRM
- **T1053.005**  Scheduled Task/Job: Scheduled Task
- **T1059.001**  Command and Scripting Interpreter: PowerShell

## Repo Layout
- `01-detection-and-ir`  investigation narrative + triage steps
- `02-remediation`  containment + cleanup + hardening
- `03-EchoSentinel-engineering`  how to tune/validate coverage
- `04-validation-pentest`  exact attack steps and verification checklist
- `evidence/`  screenshots + exported logs

## Evidence
Screenshots referenced in this repo (place them in `evidence/screenshots/`):
- `Screenshot 2026-02-19 155932.png`
- `Screenshot 2026-02-19 155959.png`
- `Screenshot 2026-02-19 160403.png`
- `Screenshot 2026-02-19 160506.png`
- `Screenshot 2026-02-19 160520.png`
- `Screenshot 2026-02-19 160710.png`
