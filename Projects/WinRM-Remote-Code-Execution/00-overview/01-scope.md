\# Scope



\## Objective

Demonstrate and defend a credentialed remote code execution path through WinRM (PowerShell Remoting) against a Windows 10 target, using EchoSentinel for detection and validation.



\## In Scope

\- \*\*Target host:\*\* Windows 10 `192.168.1.32`

\- \*\*Management protocol:\*\* WinRM over HTTP `5985` and/or HTTPS `5986`

\- \*\*Execution methods:\*\*

&nbsp; - WinRM interactive shell (`evil-winrm`)

&nbsp; - Remote command execution (`Invoke-Command` style patterns)

&nbsp; - Optional: tooling enumeration signals (`crackmapexec winrm`, connection probes)

\- \*\*Telemetry sources:EchoSentinel\*\*

&nbsp; - WinRM Operational channel

&nbsp; - Windows Security logon and process creation

&nbsp; - PowerShell Operational (Script Block / Module logging)

&nbsp; - Sysmon 



\## Out of Scope

\- Exploit-based RCE (this is not a vulnerability exploit; it is \*\*legitimate management abused with credentials\*\*)

\- Domain-wide lateral movement design (single target focus)



\## Success Criteria

\- \*\*Attack success:\*\* Execute a remote command and retrieve output from `192.168.1.32` via WinRM.

\- \*\*Detection success:\*\* EchoSentinel surfaces the activity with reliable, explainable signals (WinRM + PowerShell + process chain).

\- \*\*Remediation success:\*\* After hardening, WinRM access is blocked or constrained to an allowlist and detections remain functional.

