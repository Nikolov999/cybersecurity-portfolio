# 02  Detection engineering

## High-signal detections
### 1) sc.exe creating a service (remote or local)
- Sysmon EID 1
- `Image` ends with `\sc.exe`
- `CommandLine` contains `create `
- optional: `CommandLine` contains `binPath=`

### 2) Service install event + sc.exe create correlation
- Security: "A service was installed in the system"
- correlate with Sysmon EID 1 `sc.exe create` near the same time

### 3) Service ImagePath registry set
- Sysmon EID 13
- `TargetObject` contains `HKLM\System\CurrentControlSet\Services\`
- value relates to `ImagePath`

### 4) Payload drop + execute from ProgramData
- Sysmon EID 11 create under `C:\ProgramData\`
- followed by Sysmon EID 1 where `Image` is that path

### 5) Payload spawning LOLBins / output redirection
- Sysmon EID 1
- `ParentImage` is ProgramData payload
- Child is `cmd.exe` / `powershell.exe` / `whoami.exe`
- `CommandLine` contains `>`
