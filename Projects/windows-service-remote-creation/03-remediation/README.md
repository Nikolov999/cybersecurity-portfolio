# 03  Remediation

## Containment
- Stop the suspicious service:
  - `sc stop TelemetrySvc`
- Disable it:
  - `sc config TelemetrySvc start= disabled`

## Eradication
- Delete the service:
  - `sc delete TelemetrySvc`
- Remove payload:
  - delete `C:\ProgramData\svc\updater.exe`
  - inspect `C:\ProgramData\svc\` for extra files

## Hardening
- Alert/block on:
  - service creation from unexpected accounts/hosts
  - services pointing to ProgramData/user-writable paths
- Ensure Sysmon is deployed and collecting EID 1/11/13
- Ensure Security auditing includes service install events
