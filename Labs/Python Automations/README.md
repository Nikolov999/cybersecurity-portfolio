# 🤖 Python Blue Team Automation Tools

This folder contains my **Python automation scripts** designed for Blue Team operations — focused on detection engineering, log triage, and threat intelligence enrichment.

Each script is lightweight, documented, and can be adapted for SOC or IR workflows.

---

## Overview

| Script | Description | Primary Use Case |
|---------|--------------|------------------|
| [`ioc_enricher.py`](./ioc_enricher.py) | Enriches IOCs (IPs, domains, hashes) using VirusTotal and AbuseIPDB APIs. | Threat Intel / IOC Triage |
| [`failed_login_triage.py`](./failed_login_triage.py) | Parses Windows Security 4625 events and summarizes brute-force patterns. | Authentication Attack Detection |
| [`zeek_conn_summary.py`](./zeek_conn_summary.py) | Parses Zeek `conn.log` and summarizes top talkers, services, and failed connections. | Network Forensics / Detection |

---

## ⚙️ Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Nikolov999/cybersecurity-portfolio.git
   cd cybersecurity-portfolio/Tools/Automation

