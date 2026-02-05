# \# SMB Credential Abuse — Detection, Remediation \& Validation Series

# 

# This repository documents a four-lab defensive security series focused on

# credential exposure via SMB misconfiguration and its downstream impact.

# 

# The goal is not exploitation, but \*\*realistic blue-team detection, response,

# and validation\*\* using default telemetry and minimal tooling.

# 

# ---

# 

# \## Lab Overview

# 

# \### Lab 1 — Detection \& Incident Response

# \*\*Scenario:\*\*  

# A misconfigured SMB share exposed plaintext credentials which were abused for

# privileged access and remote execution.

# 

# \*\*Focus:\*\*

# \- Incident reconstruction

# \- Analyst reasoning without tuned detections

# \- Identification of visibility gaps

# 

# \*\*Outcome:\*\*

# \- Credential abuse occurred

# \- Limited detection fidelity

# \- Manual log correlation required

# 

# ---

# 

# \### Lab 2 — Remediation

# \*\*Scenario:\*\*  

# The root cause (credential exposure via SMB share) was remediated.

# 

# \*\*Focus:\*\*

# \- Share and NTFS permission hardening

# \- Secret removal and hygiene

# \- Verification of corrected behavior

# 

# \*\*Outcome:\*\*

# \- Credential exposure eliminated

# \- Attack path disrupted at source

# 

# ---

# 

# \### Lab 3 — Detection Engineering

# \*\*Scenario:\*\*  

# Custom Wazuh rules were engineered to detect the behavioral chain of

# credential-based lateral movement.

# 

# \*\*Focus:\*\*

# \- Network logons (Type 3)

# \- Privileged logon assignment (4672)

# \- SMB-based remote execution via service creation

# \- Correlation across events

# 

# \*\*Outcome:\*\*

# \- High-confidence detection of lateral movement behavior

# \- Reduced reliance on protocol-specific logging

# 

# ---

# 

# \### Lab 4 — Validation (Purple Team)

# \*\*Scenario:\*\*  

# The original attack path from Lab 1 was replayed after remediation and

# detection engineering.

# 

# \*\*Focus:\*\*

# \- Control effectiveness

# \- Detection reliability

# \- Analyst confidence

# 

# \*\*Outcome:\*\*

# \- Attack prevented or constrained

# \- Detection chain fired consistently

# \- Incident resolved with minimal response

# 

# ---

# 

# \## Why This Series Matters

# 

# This project demonstrates:

# \- Realistic enterprise misconfiguration

# \- Identity-based attack detection challenges

# \- Analyst-level reasoning over alert chasing

# \- Full defensive lifecycle: detect → fix → engineer → validate

# 

# No artificial exploits. No excessive tooling. No theater.

# 

# ---

# 

# \## Technologies Used

# \- Windows 10 / Windows Server 2022

# \- Wazuh (agent + manager)

# \- Native Windows logging

# \- SMB / NTLM authentication

# \- PsExec-style execution (benign command)

# 

# ---

# 

# \## Author

# EchoPentest  

# Blue Team • Detection Engineering • Incident Response

