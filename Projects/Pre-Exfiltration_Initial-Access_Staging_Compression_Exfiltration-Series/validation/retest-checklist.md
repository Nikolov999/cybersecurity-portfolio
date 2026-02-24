# Retest Checklist (Expected Outcomes)

## Goal
Reproduce the same telemetry and confirm:
- WinRM baseline detection triggers
- Privilege context triggers
- Compression prep telemetry appears (PS 4103)
- UI shows events + alerts

## Expected Evidence (Minimum)

### Security
- 4624 Type 3 (source IP = attacker)
- 4634 logoff (same Logon ID)

### Sysmon
- Event 1 child process where parent is wsmprovhost.exe -Embedding

### PowerShell
- Event 4103 showing compression/archive usage (System.IO.Compression / Archive module)

### EchoSentinel UI
- Events list contains the above
- Alerts list contains ES-WINRM-001 and ES-AUTH-008

## Pass/Fail

PASS if all minimum evidence above is present and correctly correlated by time/user/host.  
FAIL if:
- No 4624 (Type 3) anchor
- No wsmprovhost parent chain
- No PS 4103 compression signal
- Alerts fail to trigger
