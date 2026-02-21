# Results

## Observed telemetry chain
- Successful logon (remote auth)
- Service created/installed (TelemetrySvc)
- Registry value set for service configuration (ImagePath)
- Payload created under ProgramData (updater.exe)
- Service start event
- Payload execution + child process spawning (whoami redirection)

## Key artifacts
- Service: `TelemetrySvc`
- Payload: `C:\ProgramData\svc\updater.exe`
- Output artifact example: `C:\Users\Public\owned.txt`

## Why this matters
Remote service creation is a common persistence + execution pattern in enterprise intrusions.
The chain is high-signal when you correlate:
**sc.exe create**  **registry set**  **payload drop**  **service start**  **payload execution**
