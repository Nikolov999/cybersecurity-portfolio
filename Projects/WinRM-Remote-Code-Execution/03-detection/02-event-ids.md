\# Event IDs Cheat Sheet (WinRM RCE)



\## WinRM Operational (Microsoft-Windows-WinRM/Operational)

Exact IDs can vary by Windows build/config; use the channel as authoritative evidence.

Focus on:

\- Session creation/termination

\- Authentication/authorization outcomes

\- Listener activity



Hunt approach:

\- Filter by:

&nbsp; - Channel = WinRM Operational

&nbsp; - Time window of attack

&nbsp; - Source IP correlation in message fields (where present)



\## Security (Windows Security Log)

\- \*\*4624\*\* Successful logon

&nbsp; - Validate source IP = `192.168.1.13`

&nbsp; - Look for remote/network logon types (commonly \*\*3\*\*)

\- \*\*4625\*\* Failed logon (if you test failures)

\- \*\*4648\*\* Logon with explicit credentials (often appears around remote auth)

\- \*\*4688\*\* Process creation

&nbsp; - Look for `wsmprovhost.exe`

&nbsp; - Look for `powershell.exe`, `cmd.exe` spawned as children



\## PowerShell (Microsoft-Windows-PowerShell/Operational)

\- \*\*4104\*\* Script Block Logging

&nbsp; - Captures executed PowerShell content

\- \*\*4103\*\* Module Logging

&nbsp; - Captures pipeline/module usage (noisier)



\## Sysmon (If Installed)

\- \*\*1\*\* Process Create

\- \*\*3\*\* Network Connection

