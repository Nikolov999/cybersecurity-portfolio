# Incident Response: Compromised Workstation

**Goal:** Perform triage, containment, and documentation after detecting a compromised Windows host.

## Tools Used
- Sysmon  
- Windows Event Viewer  
- Splunk  
- Autoruns / Process Explorer  
- PowerShell  

## Scenario
SOC received an alert for suspicious PowerShell activity (`cmd.exe` spawning `powershell.exe`).  
The host was reportedly sending traffic to external IPs on unusual ports.

## Investigation Steps
1. Pulled Sysmon logs (Event IDs 1, 3, 11) and Windows Security Logs (4624, 4688).  
2. Discovered process chain: `outlook.exe → powershell.exe → certutil.exe`.  
3. Extracted persistence entries from the Registry (Run keys).  
4. Contained the host and acquired a memory image for deeper analysis.  
5. Conducted IOC lookups using VirusTotal and Hybrid Analysis.

📸 **Screenshot (example):**  
_Add an image here showing your Splunk search or process tree._

## ✅ Outcome
- Confirmed malicious PowerShell downloader.  
- Removed persistence and cleaned registry keys.  
- Updated the internal IR playbook with detection signatures.  
- Created new Splunk correlation rule: *certutil download via PowerShell*.

[⬅ Back to Portfolio](https://nikolov999.github.io/cybersecurity-portfolio/)
