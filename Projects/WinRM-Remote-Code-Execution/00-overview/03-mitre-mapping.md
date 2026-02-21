# MITRE ATT\&CK Mapping



## Primary Techniques

- T1021.006 — Remote Services: Windows Remote Management (WinRM)

- Credentialed remote management sessions and command execution.

- T1059.001 — Command and Scripting Interpreter: PowerShell

- Remote execution through PowerShell remoting and scripted actions.



## Common Supporting Techniques 

- T1087 — Account Discovery

- `whoami`, `net user`, `Get-LocalUser`, `net localgroup administrators`

- T1082 — System Information Discovery

- `systeminfo`, `Get-ComputerInfo`

- T1049 — System Network Connections Discovery

- `netstat -ano`, `Get-NetTCPConnection`

- T1105 — Ingress Tool Transfer

- `Invoke-WebRequest`, `bitsadmin`, SMB copy (if used)

- T1562.001 — Impair Defenses: Disable or Modify Tools

- `Set-MpPreference`, service stop attempts (if used)



## Detection Mapping 

- WinRM Operational event hits + source IP (`192.168.1.13`)

- Security logon patterns (4624/4648)

- Process chain: `svchost.exe` → `wsmprovhost.exe` → `powershell.exe`/`cmd.exe`

\- PowerShell Script Block 4104 content


