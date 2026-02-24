# Telemetry Event Map

## Security Log

### 4624  An account was successfully logged on
- **Logon Type:** 3 (Network)
- **Source Network Address:** attacker IP (e.g., 192.168.1.13)
- **Target Account:** vagrant
- **Use:** initial access anchor + correlation start

### 4672  Special privileges assigned to new logon
- Indicates elevated token privileges
- Common in admin WinRM sessions
- **Use:** privilege context / risk scoring

### 4674  An operation was attempted on a privileged object
- Often noisy during admin activity
- **Use:** supporting signal, not primary anchor

### 4634  An account was logged off
- Use Logon ID to pair with 4624
- **Use:** correlation close / session boundary

## Sysmon (Microsoft-Windows-Sysmon/Operational)

### Event ID 1  Process Create
Key fields:
- Image
- CommandLine
- ParentImage
- ParentCommandLine
- User
- IntegrityLevel

**WinRM baseline pattern:**
- ParentImage = C:\Windows\System32\wsmprovhost.exe
- ParentCommandLine contains -Embedding

## PowerShell (Microsoft-Windows-PowerShell/Operational)

### Event ID 4103  Module Logging / Command Invocation
Observed:
- Add-Type invoked
- AssemblyName = System.IO.Compression
- Script/Module path: Microsoft.PowerShell.Archive.psm1

**Use:** compression-stage validation + correlation with WinRM host chain
