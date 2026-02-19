\## 04-logging-baseline.md`



\# Logging Baseline (Windows 10 Target)



Goal: ensure the target produces high-signal telemetry for WinRM and PowerShell.



\## 1) Enable WinRM Operational Log

In Event Viewer:

\- Applications and Services Logs →

&nbsp; Microsoft →

&nbsp; Windows →

&nbsp; \*\*WinRM\*\* →

&nbsp; \*\*Operational\*\*



PowerShell to confirm channel exists:

```powershell

wevtutil gl Microsoft-Windows-WinRM/Operational

