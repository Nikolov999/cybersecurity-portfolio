\# Correlation Logic (EchoSentinel)



Goal: attribute remote command execution to WinRM from attacker `192.168.1.13` against target `192.168.1.32`.



\## Correlation 1 — WinRM Session + Logon

Time window (example): `T0 to T0+5m`

\- WinRM Operational events present

\- Security 4624 present

\- Source IP matches `192.168.1.13`



Output:

\- “Confirmed WinRM auth/session from Kali to Win10”



\## Correlation 2 — Logon + Process Chain

Within `T0 to T0+2m`:

\- Security 4624 (or explicit credential usage)

\- Process create events:

&nbsp; - `wsmprovhost.exe` present

&nbsp; - child `powershell.exe` or `cmd.exe`



Output:

\- “Remote management session executed commands (provider host + child process)”



\## Correlation 3 — Script Block Confirmation (Best)

Within `T0 to T0+5m`:

\- PowerShell 4104 shows command content

\- Contains:

&nbsp; - `whoami`, `hostname`, or specific executed strings



Output:

\- “WinRM remote execution with content-level proof”



\## Severity Guidance

\- If source IP is not a known admin box (here attacker Kali): High

\- If user is privileged (local admin): High

\- If script block contains download/execute: Critical

