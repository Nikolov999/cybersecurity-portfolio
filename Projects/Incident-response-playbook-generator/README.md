# Incident Response Playbook Generator

A streamlined web-based incident response (IR) playbook generator designed for cybersecurity professionals, SOC analysts, and red/blue teamers.  
The tool provides structured, actionable IR workflows enriched with MITRE ATT&CK techniques, severity ratings, impact summaries, and SLA expectations.  
Playbooks are auto-generated through a simple UI and can be exported as a professionally formatted PDF.

---

##  Key Features

###  Multi-Incident Support
The generator includes ready-to-use IR playbooks for:
- Phishing  
- Ransomware  
- SQL Injection  
- DDoS  
- Privilege Escalation  
- Data Breach  
- Brute Force Login  

Each incident type includes:
- **Severity Level**
- **Impact Summary**
- **SLA (Service Level Agreement)**
- **Mapped MITRE ATT&CK techniques**
- **Full IR phases:**
  - Identification  
  - Containment  
  - Eradication  
  - Recovery  
  - Lessons Learned  

---

##  User Interface Overview

The UI is intentionally minimalistic and SOC-friendly, featuring a clean dark theme for comfortable long-session use.

###  1. Incident Selection Dropdown
Users choose their incident type via a clean dropdown menu.

**(Insert screenshot here)**  
`![Incident Dropdown Placeholder](screenshots/incident_dropdown.png)`

---

###  2. Metadata Overview (Severity, Impact, SLA)
Once an incident is selected, the tool displays a metadata grid summarizing:
- Severity (Critical / High / Medium)  
- Expected Impact  
- SLA and response time requirements  

**(Insert screenshot here)**  
`![Metadata Grid Placeholder](screenshots/metadata_grid.png)`

---

###  3. MITRE ATT&CK Mapping Table
The app highlights relevant MITRE IDs and techniques tied to the selected incident.

**(Insert screenshot here)**  
`![MITRE Table Placeholder](screenshots/mitre_table.png)`

---

###  4. Complete IR Phases
Each incident includes a detailed breakdown of every response phase, written in SOC-ready language.

**(Insert screenshot here)**  
`![IR Phases Placeholder](screenshots/ir_phases.png)`

---

###  5. PDF Export
A one-click **“Download as PDF”** button generates a professional PDF version of the entire playbook.  
No temporary files are stored — PDFs stream directly from memory.

**(Insert screenshot here)**  
`![PDF Export Placeholder](screenshots/pdf_export.png)`

---

##  Purpose

This project demonstrates:
- Cybersecurity domain knowledge  
- Ability to convert IR processes into structured workflows  
- MITRE ATT&CK familiarity  
- Python/Flask full-stack development  
- Secure PDF generation  
- Frontend design with a clean, minimal UI  
- Dockerized deployment

Perfect for inclusion in cybersecurity portfolios, SOC/IR engineering interviews, or lab environments.

---

##  Live Workflow Summary

1. User selects incident type  
2. Application retrieves structured IR data  
3. Metadata + MITRE + phases are rendered dynamically  
4. Optional PDF export formats the playbook professionally  
5. No data is stored — all generation is ephemeral  

---

##  Screenshots

Create a folder called `screenshots/` in the repo and drop your images in later.

