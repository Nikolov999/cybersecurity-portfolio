# Pre-Exfiltration Initial Access, Staging and Compression (Exfiltration Series)

**Status:** Complete (Attack Vector + Telemetry + Alerting)  
**Date:** 2026-02-24  
**Focus:** WinRM remote execution baseline  local staging behavior  compression prep (no outbound transfer)

## Scope

This project validates **pre-exfiltration preparation** behaviors executed over **WinRM**:

- Remote authentication to target
- Remote command execution via WinRM PowerShell host chain
- Local data **staging** into a single directory
- **Compression preparation** using PowerShell archive module (no network exfil)

**Explicitly out of scope:** outbound transfer (SMB/HTTP/SCP), C2, persistence, privilege escalation.

## Lab Environment

| Role | Hostname | IP | Notes |
|---|---|---:|---|
| Attacker | Kali | 192.168.1.13 | WinRM client tooling |
| Target | lab-win-client | (lab) | Windows endpoint (Sysmon + PowerShell logging enabled) |
| User | vagrant | - | WinRM session user |

## Attack Narrative (High-Level)

1. **WinRM Initial Access** establishes a remote session to the target.
2. **Remote Execution Baseline** is confirmed by the WinRM host chain: wsmprovhost.exe  child process.
3. **Staging** concentrates files into a public directory (behavioral clustering).
4. **Compression Preparation** loads archive/compression assembly and generates an archive artifact.
5. Session ends (logoff).

## Key Telemetry Observed

### Security Log (Windows)
- **4624**  Logon success (**Type 3**) from attacker IP (initial access anchor)
- **4672 / 4674**  Privileged context activity during admin session (expected in elevated work)
- **4634**  Logoff (session end / correlation close)

### Sysmon (Operational)
- **Sysmon Event ID 1**  Process creation showing child process spawned by:
  - Parent: C:\Windows\System32\wsmprovhost.exe -Embedding
  - Example child: whoami.exe (baseline validation)

### PowerShell Operational
- **4103**  Module / command invocation indicating archive/compression usage:
  - Add-Type loading System.IO.Compression
  - Module path: Microsoft.PowerShell.Archive.psm1

## Detection Outcomes (EchoSentinel)

Triggered rules seen in UI:
- **ES-WINRM-001**  WinRM remote execution (wsmprovhost.exe)  
- **ES-AUTH-008**  Special privileges assigned at logon (4672)

## Correlation Model (What This Proves)

This phase proves you can correlate:

**4624 Type 3 (remote logon)**
 **wsmprovhost.exe execution chain**
 **staging / file concentration (behavior)**
 **compression prep (PowerShell Archive / compression assembly)**
 **archive artifact**
 **4634 (session end)**

## Evidence Map

Place your screenshots here (placeholders already created):

- evidence\raw\security_4624_logon_type3.png
- evidence\raw\security_4634_logoff.png
- evidence\raw\sysmon_1_whoami_parent_wsmprovhost.png
- evidence\raw\powershell_4103_addtype_system_io_compression.png
- evidence\ui\echosentinel_events_list.png
- evidence\ui\echosentinel_alerts_winrm_auth.png

## Repo Contents

- docs\attack-narrative.md  narrative + sequence model (non-outbound)
- 	elemetry\event-map.md  event IDs, fields, pivots
- detections\rules.md  detection logic + correlation chain
- alidation\retest-checklist.md  retest steps + expected signals (no attacker commands)
- emediation\hardening.md  practical controls for WinRM + PowerShell
- evidence\README.md  screenshot placement guide

