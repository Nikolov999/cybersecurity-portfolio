# 01  Initial Triage Steps

## Goal
Confirm whether scheduled task persistence was created remotely and identify the execution chain.

## Step 1  Confirm Remote Auth Context
Look for:
- **Security 4624** LogonType **3**
- Account name and workstation/source indicators
- Elevated token (if present)

Evidence:
- `Screenshot 2026-02-19 155959.png`

## Step 2  Confirm Privilege Context
Look for:
- **Security 4672** Special privileges assigned
- Confirms high-priv session that can create persistence

Evidence:
- `Screenshot 2026-02-19 155932.png`

## Step 3  Identify Persistence Creation Command
Look for:
- **Sysmon 1** where `Image = schtasks.exe`
- CommandLine contains `/create`
- Note:
  - task name (`/tn`)
  - trigger (`/sc ONLOGON`)
  - run-as (`/ru SYSTEM`)
  - action (`/tr ... updater.ps1`)

Evidence:
- `Screenshot 2026-02-19 160506.png`

## Step 4  Confirm Task Artifact on Disk
Look for:
- **Sysmon 11** file create where TargetFilename is:
  - `C:\Windows\System32\Tasks\WindowsUpdateCheck`
- Confirms the task is truly registered (not just attempted)

Evidence:
- `Screenshot 2026-02-19 160403.png`

## Step 5  Confirm Execution
Look for:
- **Sysmon 1** for `schtasks.exe /run`
- (Optional) TaskScheduler/Operational 200/201/102 if enabled

Evidence:
- `Screenshot 2026-02-19 160520.png`

## Step 6  Identify Payload
Look for:
- Script created:
  - `C:\Users\Public\updater.ps1`
- Correlate parent process to WinRM host:
  - `wsmprovhost.exe`

Evidence:
- `Screenshot 2026-02-19 160710.png`
