# Detections (EchoSentinel)

## ES-WINRM-001  WinRM Remote Execution (wsmprovhost.exe)

### Goal
Detect remote execution via WinRM provider host.

### Required telemetry
- Sysmon Event 1 (Process Create) OR Security 4688 (if enabled)

### Logic (concept)
Trigger when:
- ParentImage ends with \wsmprovhost.exe
- ParentCommandLine contains -Embedding
- Child process is not in a strict allowlist (optional)

### Enrichment
- Pivot to nearest Security 4624 Type 3 (same user / LogonId proximity)
- Add attacker source IP if available

## ES-AUTH-008  Special Privileges at Logon (4672)

### Goal
Raise risk when a remote session receives special privileges.

### Required telemetry
- Security 4672

### Logic
- EventID = 4672
- User != expected admin allowlist (optional)
- Correlate to 4624 Type 3 in a short window

## Correlation: Pre-Exfil Preparation Chain (Project Model)

### Target behavior
Remote WinRM session + compression prep.

### Correlation (concept)
Within 1015 minutes:
1. 4624 Type 3 (remote logon)
2. Sysmon 1 showing wsmprovhost.exe  child process
3. PowerShell 4103 indicating compression / archive module usage
4. Optional close: 4634 logoff

### Risk model
- Base: WinRM execution detected
- + privileges (4672)
- + compression prep (4103)
- + staging (if Sysmon FileCreate enabled)
