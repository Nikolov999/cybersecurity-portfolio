# Windows Services  Remote Service Creation (Detection + IR)

## Scenario
Remote execution is used to create and start a Windows Service that points to a staged payload under **C:\ProgramData\svc\**.

## What you proved (from telemetry)
1. Remote authentication occurred (successful logon observed).
2. Service persistence was created:
   - `sc.exe create TelemetrySvc binPath= "C:\Windows\System32\svchost.exe -k netsvcs" start= demand`
3. Service configuration was written (registry ImagePath set).
4. Payload was staged:
   - `C:\ProgramData\svc\updater.exe` created
5. Service was started:
   - `sc.exe start TelemetrySvc` (or your service name)
6. Payload executed and spawned commands:
   - example: `whoami > C:\Users\Public\owned.txt`

## Evidence
Place screenshots in `evidence/screenshots/` and reference them here in order:

1. `01-logon.png`  successful logon (remote auth)
2. `02-sc-create.png`  Sysmon Process Create showing `sc.exe create ...`
3. `03-registry-imagepath.png`  Sysmon Registry Value Set (service ImagePath/config)
4. `04-service-installed.png`  Security A service was installed
5. `05-payload-created.png`  Sysmon File Create: `C:\ProgramData\svc\updater.exe`
6. `06-service-start.png`  Sysmon Process Create: `sc.exe start ...`
7. `07-payload-executed.png`  Sysmon Process Create: `updater.exe` executed
8. `08-child-process.png`  Sysmon Process Create: child process spawned by updater.exe

## Repo map
- `01-attack/`  exact chain narrative
- `02-detection/`  what to alert on + correlations
- `03-remediation/`  kill/remove/harden
- `04-validation/`  retest + verification
