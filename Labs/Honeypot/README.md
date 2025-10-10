# Deploying a Cowrie Honeypot

**Goal:** Capture and analyze attacker behavior targeting SSH services.

## Tools Used
- Cowrie (SSH/Telnet Honeypot)  
- Ubuntu Server  
- ELK Stack  
- VirusTotal, AbuseIPDB  

## Setup
1. Deployed an Ubuntu VM on a public cloud with SSH port 22 exposed.  
2. Installed Cowrie and configured it to log session data to `/var/log/cowrie/`.  
3. Shipped logs to ELK using Filebeat for analysis.  
4. Created dashboards for login attempts and command executions.

📸 **Screenshot:**  
_Add a dashboard or log screenshot here._

## Findings
- 250+ login attempts in the first 24 hours.  
- Common credentials: `root`, `admin`, `pi`.  
- Attackers uploaded multiple Mirai-like scripts.  
- Logged unique payload hashes for further enrichment.

## ✅ Outcome
- Validated external scanning activity.  
- Collected IOCs for network-level blocking.  
- Used honeypot data to improve firewall and SIEM detections.

[⬅ Back to Portfolio](https://nikolov999.github.io/cybersecurity-portfolio/)
