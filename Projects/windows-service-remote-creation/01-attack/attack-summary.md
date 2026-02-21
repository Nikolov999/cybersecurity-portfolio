# Attack summary

## Pattern
Remote service creation is used to establish persistence and execute a payload.

## Observables (what you should capture)
- `sc.exe create <svc>` with binPath/start parameters
- Service install event (Security)
- Sysmon registry set for `HKLM\System\CurrentControlSet\Services\<svc>\ImagePath`
- Payload staged under `C:\ProgramData\...`
- Service started (`sc.exe start <svc>`)
- Payload execution + child process spawning
