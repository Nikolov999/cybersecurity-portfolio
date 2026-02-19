\# WinRM Remote Code Execution (PowerShell Remoting) — Detection + Remediation + Validation



This project documents an end-to-end WinRM (Windows Remote Management) remote code execution path using PowerShell Remoting, then builds detection coverage in EchoSentinel, applies hardening, and validates that controls and detections work.



\## Lab Topology (This Repo)

\- \*\*EchoSentinel (collector / SIEM):\*\* `192.168.1.27`

\- \*\*Attacker (Kali):\*\* `192.168.1.13`

\- \*\*Target (Windows 10):\*\* `192.168.1.32`



\## What This Covers

\- WinRM enablement and baseline telemetry

\- Credentialed remote execution via:

&nbsp; - `evil-winrm`

&nbsp; - PowerShell Remoting (`Invoke-Command`, `Enter-PSSession`) where applicable

&nbsp; - Spray/enum tooling signals (optional)

\- Detection engineering:

&nbsp; - WinRM Operational logs

&nbsp; - Security logon telemetry

&nbsp; - PowerShell logging (Script Block / Module logging)

&nbsp; - Process creation (4688 / Sysmon)

\- Remediation:

&nbsp; - Reduce/disable exposure

&nbsp; - Require encryption, disable weak auth

&nbsp; - Tight access control (least privilege + allowlists)

\- Validation:

&nbsp; - Test cases

&nbsp; - Expected alerts

&nbsp; - Pass/Fail criteria



\## Folder Map

\- `00-overview/` scope, threat model, MITRE mapping

\- `01-lab-setup/` topology, prerequisites, WinRM enablement, logging baseline

\- `02-attack/` attack execution steps (credentialed)

\- `03-detection/` telemetry sources, event IDs, process chains, correlations, EchoSentinel queries

\- `04-remediation/` hardening steps + config + access control + results

\- `05-validation/` test cases, expected alerts, pass/fail rubric



\## Evidence to Capture (Portfolio)

\- Screenshots of:

&nbsp; - WinRM listener configuration

&nbsp; - Successful remote command execution

&nbsp; - Key Event Viewer hits (WinRM Operational, Security 4624, PowerShell 4104)

&nbsp; - EchoSentinel detections (alerts + raw events)

\- Exported logs:

&nbsp; - `Microsoft-Windows-WinRM/Operational`

&nbsp; - `Microsoft-Windows-PowerShell/Operational`

&nbsp; - Security log filtered view for 4624/4648/4688

\- Command transcripts (copy/paste) for repeatability



\## Notes

\- This repo assumes \*\*credentialed WinRM\*\* (common in real intrusions after credential theft/reuse).



