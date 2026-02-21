# Event IDs Cheat Sheet (WinRM RCE)



## WinRM Operational (Microsoft-Windows-WinRM/Operational)

Exact IDs can vary by Windows build/config; use the channel as authoritative evidence.

Focus on:

- Session creation/termination

- Authentication/authorization outcomes

- Listener activity



Hunt approach:

- Filter by:

 - Channel = WinRM Operational

 - Time window of attack

 - Source IP correlation in message fields (where present)



## Security (Windows Security Log)

- 4624 Successful logon

- Validate source IP = `192.168.1.13`

- Look for remote/network logon types (commonly 3)

- 4625 Failed logon 

- 4648 Logon with explicit credentials (often appears around remote auth)

- 4688 Process creation

- Look for `wsmprovhost.exe`

- Look for `powershell.exe`, `cmd.exe` spawned as children



## PowerShell (Microsoft-Windows-PowerShell/Operational)

- 4104 Script Block Logging

- Captures executed PowerShell content

- 4103 Module Logging

- Captures pipeline/module usage (noisier)



## Sysmon 

- 1 Process Create

- 3 Network Connection


