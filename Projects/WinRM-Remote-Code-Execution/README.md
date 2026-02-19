# WinRM Remote Code Execution (PowerShell Remoting) — Detection + Remediation + Validation



This project documents an end-to-end WinRM (Windows Remote Management) remote code execution path using PowerShell Remoting, then builds detection coverage in EchoSentinel, applies hardening, and validates that controls and detections work.



## Lab Topology (This Repo)

- EchoSentinel (collector / SIEM):\*\* `192.168.1.27`

- Attacker (Kali):\*\* `192.168.1.13`

- Target (Windows 10):\*\* `192.168.1.32`



## What This Covers

- WinRM enablement and baseline telemetry

- Credentialed remote execution via:

  - `evil-winrm`

  - PowerShell Remoting (`Invoke-Command`, `Enter-PSSession`) where applicable

  - Spray/enum tooling signals (optional)

- Detection engineering:

    - WinRM Operational logs

    - Security logon telemetry

    - PowerShell logging (Script Block / Module logging)

    - Process creation (4688 / Sysmon)

- Remediation:

    - Reduce/disable exposure

    - Require encryption, disable weak auth

    - Tight access control (least privilege + allowlists)

- Validation:

    - Test cases

    - Expected alerts

    - Pass/Fail criteria



 ## Folder Map

 - `00-overview/` scope, threat model, MITRE mapping

 - `01-lab-setup/` topology, prerequisites, WinRM enablement, logging baseline

 - `02-attack/` attack execution steps (credentialed)

 - `03-detection/` telemetry sources, event IDs, process chains, correlations, EchoSentinel queries

 - `04-remediation/` hardening steps + config + access control + results

 - `05-validation/` test cases, expected alerts, pass/fail rubric


 ## Notes

 - This repo assumes \*\*credentialed WinRM\*\* (common in real intrusions after credential theft/reuse).




