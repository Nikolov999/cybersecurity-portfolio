# Expected Alerts (EchoSentinel)



## Alert 1 — WinRM Remote Session From Kali

Trigger:

- Target host `192.168.1.32`

- WinRM Operational activity in time window

- Security 4624 source IP = `192.168.1.13`



Title:

- `WINRM Remote Session (Non-Admin Host)`



Severity:

- High


---


## Alert 2 — wsmprovhost Spawning Shell

Trigger:

- Parent process `wsmprovhost.exe`

- Child `powershell.exe` or `cmd.exe`



Title:

- `WINRM Provider Host Spawned Shell`



Severity:

- High


---


## Alert 3 — PowerShell Script Block Indicates Remote Execution

Trigger:

- PowerShell Operational 4104

- Contains `Invoke-Command` / `Enter-PSSession` / `New-PSSession`

- Optional escalation if contains download/execute primitives



Title:

- `PowerShell Remoting Script Block (WinRM)`



Severity:

- High / Critical (if download-exec)


---


## Alert 4 — WinRM Connection Attempts After Hardening (Optional)

If you enable firewall logging or collect denied events:

Trigger:

- Inbound deny on 5985/5986 from `192.168.1.13`



Title:

- `Blocked WinRM Attempt (Non-Allowlisted Source)`



Severity:

- Medium (High if repeated)


