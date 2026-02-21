# 02  Timeline Reconstruction

## Timeline (From Evidence)
All timestamps below are taken from EchoSentinel event views in the screenshots.

1. **Remote logon (WinRM context established)**
   - Event: Security 4624 (LogonType 3)
   - Evidence: `Screenshot 2026-02-19 155959.png`

2. **Privileges assigned to session**
   - Event: Security 4672
   - Evidence: `Screenshot 2026-02-19 155932.png`

3. **Payload created on disk**
   - Artifact: `C:\Users\Public\updater.ps1`
   - Parent: `wsmprovhost.exe`
   - Evidence: `Screenshot 2026-02-19 160710.png`

4. **Scheduled task created**
   - Process: `schtasks.exe /create ... WindowsUpdateCheck ... /ru SYSTEM ... /tr powershell.exe ... updater.ps1`
   - Evidence: `Screenshot 2026-02-19 160506.png`

5. **Task definition written**
   - Artifact: `C:\Windows\System32\Tasks\WindowsUpdateCheck`
   - Evidence: `Screenshot 2026-02-19 160403.png`

6. **Task executed**
   - Process: `schtasks.exe /run /tn WindowsUpdateCheck`
   - Evidence: `Screenshot 2026-02-19 160520.png`

## Analyst Conclusion
This is a high-confidence **WinRM-driven persistence** case:
- Remote privileged session created a task configured to run as SYSTEM at logon.
- Artifact is present on disk.
- Task was run immediately to validate execution.
