#  PurpleOps-Playground — Blue Team Play-by-Play

**Author:** Bobo Nikolov  
**Project:** PurpleOps-Playground  
**Date:** 27-10-2025  
**Status:** Completed

---

## Overview

**Goal:** Build an isolated attacker ↔ victim lab to demonstrate reconnaissance, initial access, execution, persistence, and privilege escalation — then integrate a defender stack (SecurityOnion planned; Wazuh and Wireshark used here) to capture telemetry and author detection content.

**Defender viewpoint:** This README is written as a *play-by-play* defender report — what I observed, what alerts were generated (Wazuh), what network artifacts were captured (Wireshark PCAPs), and where detection gaps exist.

**Important notes:**
- The lab was isolated (host-only / internal), and virtual machine snapshots were taken before testing and reverted afterwards to ensure reproducibility.
- All activity occurred on my own VMs only.

---

## Lab architecture & scope

- **lab_attacker** — Kali Linux  
  - IP: `10.10.10.10` (labnet)
  - Tools: `msfvenom`, `msfconsole` / `exploit/multi/handler`, `python3 -m http.server`, `nmap`
- **lab_victim** — Ubuntu Desktop (target)  
  - IP: `10.10.10.20` (labnet / intnet)
  - Tools: `wget`, `chmod`, `bash`, `sudo`. Wazuh agent installed and logging; Wireshark capturing on the victim.
- **Network:** Isolated internal network (no internet). Snapshots taken.
- **Evidence storage (local):** `Projects/PurpelOps-playground/Screenshots/` (screenshots, pcaps, Wazuh JSON/alerts)
- **Scope:** Single-host attack chain (recon → initial access → execution → persistence → privilege escalation). Defender proof-of-concept detections from Wazuh & pcap analysis.

---

## MITRE ATT&CK mapping (defender play-by-play)

Below is the mapping used in this lab. Each tactic is followed by the specific technique(s) observed and defender notes.

- **Reconnaissance — T1595 (Active Scanning / Nmap)**  
  Observed: `nmap -sS -sV 10.10.10.20` — large SYN sweep and service probes.  
  Defender notes: Suricata/Zeek / Wazuh rule can detect unusual scanning behavior.

- **Resource Development — T1587**  
  Observed: Payload created locally (msfvenom); not network-visible except when served.  
  Defender notes: Artifact: ELF binary created on attacker. Monitor known msfvenom patterns on dev hosts.

- **Initial Access — T1190 / T1204**  
  Observed: HTTP fetch of ELF payload and manual execution (`wget ... && chmod +x ... && /tmp/shell`).  
  Defender notes: Detect/alert on `wget`/`curl` + immediate execute flows, unexpected HTTP egress to odd hosts.

- **Execution — T1059 + T1110 + T1190 (includes brute-force and SQLi attempts)**  
  Observed: Meterpreter reverse shell execution, attempted brute-force, attempted SQLi (payloads in HTTP requests).  
  Defender notes: Look for abnormal command sequences, unusual shells, `chmod` followed by execution, database query anomalies.

- **Persistence — T1136 / T1547**  
  Observed: Created user `backdoor_user` and added sudoers NOPASSWD entry.  
  Defender notes: Monitor `/etc/sudoers.d` additions, user creation events.

- **Privilege Escalation — T1068 / T1548**  
  Observed: Verified root via `sudo /bin/bash` or `whoami` from interactive session.  
  Defender notes: Alert on suspicious use of `sudo` or escalation sequences when preceded by unknown agent activity.

- **Defense Evasion — T1562**  
  Observed: Minimal attempts; some logging gaps observed (Wazuh missed certain file-download events).  
  Defender notes: Improve host instrumentation; add auditd/Sysmon-like logging for file creations in `/tmp`.

- **Credential Access — T1110**  
  Observed: Attempted brute-force (logged by Wireshark and Wazuh summary).  
  Defender notes: Enforce rate-limits and lockouts; log and alert failed auth spikes.

- **Discovery — T1087 / T1083**  
  Observed: Target enumeration post-compromise (limited).  
  Defender notes: Host-level discovery should emit process creation logs.

- **Command & Control — T1071**  
  Observed: Meterpreter reverse TCP established back to attacker `10.10.10.10:4444`.  
  Defender notes: Monitor reverse TCP beaconing to internal hosts / unexpected IPs.

- **Exfiltration — T1041**  
  Observed: Not performed in this run (file transfer from victim-to-attacker via meterpreter occurred but some detection missed it).  
  Defender notes: Instrument endpoint to detect outbound file transfer commands and large data flows.

---

## Phase-by-phase (defender viewpoint)

Below I walk through each phase, show what I (the defender) observed in Wazuh / Wireshark / host logs, list artifacts, and propose detection rules or mitigations.

---

### Reconnaissance (T1595)

**Attacker activity**
```bash

nmap -sS -sV 10.10.10.20
```

**Defender findings**

Nmap Wazuh Alerts:

![Enumeration](Projects/PurpleOps-playground/Screenshots/Screenshots/Recon/Wazuh/2025-11-06_22-28-54_Recon(nmap)_Enumeration.png)

![Enumeration](Projects/PurpleOps-playground/Screenshots/Screenshots/Recon/Wazuh/2025-11-06_22-29-00_Nmap-Recon_Enumeration_Wazuh.png)

Wazuh: Rule 
