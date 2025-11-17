#  My Cybersecurity Home Lab  
A fully virtualized environment for malware analysis, network monitoring, detection engineering, Active Directory labs, and offensive security testing.

This lab is used for **current, past, and future cybersecurity projects**, including:
- Malware analysis & sandboxing  
- Windows event log investigations  
- Web application attacks  
- Wazuh SIEM monitoring  
- Sysmon log engineering  
- Active Directory simulations  
- Lateral movement experiments  
- Red team / blue team workflows  

---

##  VirtualBox Network Setup  
All machines run in an isolated **Host-Only network** for safe testing.  
NAT adapters are added only when internet access is temporarily needed.

**Host-Only Network:** `10.10.10.0/24`  
**Subnet Mask:** `255.255.255.0`  
**Gateway:** None (isolated lab)

---

##  Machines Overview

###  Windows / Linux Environment
| VM Name | OS | Role | IP Address | Notes |
|--------|----|------|------------|-------|
| **Kali Attacker** | Kali Linux Rolling | Offensive testing (nmap, CME, kerberoasting, exploits) | `10.10.10.10` | Main attacker machine |
| **Defender / Wazuh + Wireshark** | Ubuntu Desktop | Wazuh Manager, Packet Capture, Log Analysis | `10.10.10.15` | SIEM + monitoring |
| **Ubuntu Target 1** | Ubuntu Server | Web app target, exploits | `10.10.10.20` | Vulnerable services for testing |
| **Ubuntu Target 2** | Ubuntu Desktop | Additional web target (future project) | `10.10.10.25` | Secondary vulnerable machine |
| **Windows Server 2022** | Windows Server 2022 (Evaluation) | Domain Controller (AD DS), DNS | `10.10.10.50` | Central server in AD labs |
| **Windows 10 Client** | Windows 10 Pro | Domain-Joined Workstation | `10.10.10.100` | User workstation in AD labs |

---

##  Installed Software & Tools

###  **Windows Server 2022**
- Active Directory Domain Services  
- DNS Server  
- Sysmon (with config)  
- Wazuh Agent  
- PowerShell logging enabled  
- Security auditing enabled  
- Domain: `testlab.local`

###  **Windows 10 Client**
- Joined to AD domain  
- Sysmon installed  
- Wazuh Agent installed  
- Used for:
  - Credential capture tests  
  - Lateral movement  
  - Privilege escalation experiments  

###  **Kali Linux**
- nmap  
- crackmapexec  
- impacket  
- bloodhound-python  
- evil-winrm  
- kerbrute  
- mimikatz (if using wine or prebuilt binaries)  
- linpeas/winpeas for post-exploitation  

###  **Defender / Wazuh Manager**
- Wazuh Manager  
- Filebeat  
- Sysmon ruleset  
- Wireshark  
- Custom Wazuh decoders & rules (future)  

###  **Ubuntu Targets**
- Apache / Nginx  
- Custom vulnerable web apps  
- SSH, SMB, or other services depending on the project  

---

##  Current Capabilities of This Lab

- Host-only isolated cyber range  
- Complete AD domain for attacks  
- Sysmon + Wazuh → SIEM pipeline  
- Packet captures from Wireshark  
- Malware & reverse engineering environment  
- Red team → blue team detection workflow  
- Web application exploitation testing  

---

##  Future Plans
- Kerberoasting lab  
- Lateral movement lab  
- Web app pentesting  
- Beacon simulation (safe / fake C2)  
- Wazuh rule engineering  
- Blue team alert correlations  
- MITRE ATT&CK mapping  
- AD CS escalation (ESC1/4 checks)  
- Password spraying and brute-force monitoring  

---

##  Purpose of This Lab
This environment is used to practice and demonstrate **real cybersecurity skills**, including:

- System hardening  
- Threat hunting  
- Detection engineering  
- SIEM configuration  
- Network forensics  
- Malware analysis  
- Penetration testing  
- Incident response workflow  

This README will continue to evolve as the home lab expands.

---

##  Author
**Bobo Nikolov**  
Cybersecurity Student & Lab Builder  
