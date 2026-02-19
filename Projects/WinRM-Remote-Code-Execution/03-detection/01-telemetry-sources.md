\# Telemetry Sources for WinRM Remote Execution



\## 1) Microsoft-Windows-WinRM/Operational

Best source to confirm WinRM session activity, listener usage, and operational context.



\## 2) Security Log

\- \*\*4624\*\* successful logon (network-style)

\- \*\*4625\*\* failed logon (if brute/spray occurs)

\- \*\*4648\*\* explicit credentials (often appears with remote auth flows)

\- \*\*4688\*\* process creation (requires auditing enabled)



\## 3) PowerShell Operational

\- \*\*4104\*\* Script Block Logging (highest-value)

\- \*\*4103\*\* Module Logging (good context)



Channel:

\- `Microsoft-Windows-PowerShell/Operational`



\## 4) Sysmon (If Installed)

\- \*\*Event ID 1:\*\* Process Create

\- \*\*Event ID 3:\*\* Network connection

\- Useful to tie `wsmprovhost.exe` → child execution and network egress.



\## 5) Firewall / Network Telemetry (Optional)

\- Windows Filtering Platform events (advanced)

\- Switch/router logs (not required here)



\## Minimum Viable Detection Stack

\- WinRM Operational + Security 4624 + Process Create (4688 or Sysmon 1)

\- PowerShell 4104 strongly recommended

