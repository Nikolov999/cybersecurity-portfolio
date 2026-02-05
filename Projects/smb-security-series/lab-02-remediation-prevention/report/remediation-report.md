# \# Remediation Report — SMB Credential Exposure

# 

# \## Summary

# The remediation addressed the root causes identified in Lab 1: plaintext credential exposure via an SMB share, over-broad access permissions, and excessive privilege assigned to a reusable identity. Changes were implemented to eliminate credential exposure, enforce least privilege on the share, and reduce the blast radius of the affected account, while maintaining normal operational functionality.

# 

# ---

# 

# \## Before

# 

# \### Risk statement

# A Windows SMB share was misconfigured with overly permissive Share and NTFS permissions and contained a plaintext file with valid credentials. These credentials belonged to an account with administrative access on another system, enabling credential reuse and lateral movement using legitimate mechanisms without exploitation.

# 

# \### Evidence pointers

# \- Lab 1 incident report

# \- `lab-01-exposure-detection-ir/02-misconfiguration.md`

# \- Wazuh alerts and Windows Security logs from the Server 2022 host

# \- Timeline documenting SMB access followed by remote execution

# 

# ---

# 

# \## Changes applied

# 

# \### Share + NTFS

# \- Removed broad principals (e.g. `Everyone`, `Users`) from SMB Share permissions.

# \- Restricted Share access to explicitly required users/groups only.

# \- Updated NTFS permissions to align with least privilege and match intended access.

# \- Disabled guest/anonymous access to the share.

# 

# \### Secret handling

# \- Removed plaintext credential file from the SMB share.

# \- Verified no credentials or sensitive configuration files remained accessible via SMB.

# \- Documented approved approach for secret storage outside of file shares.

# 

# ---

# 

# \## After

# 

# \### Expected behavior confirmed

# \- Unauthorized users can no longer list or read the SMB share.

# \- No plaintext credentials are accessible via network shares.

# \- The previously exposed account no longer has unnecessary administrative access on the target system.

# \- Normal, intended access to the share (where applicable) continues to function.

# 

# \### Evidence pointers

# \- Updated Share and NTFS permission screenshots/notes

# \- Validation checks showing access denied from attacker context

# \- Configuration notes under `lab-02-remediation-prevention/evidence/after/`

# 

# ---

# 

# \## Residual risk

# \- Credential exposure remains possible through other channels (e.g. email, scripts, documentation) if secrets are mishandled elsewhere.

# \- Legitimate credentials reused across systems can still enable lateral movement if over-privileged identities exist.

# \- Detection gaps remain for silent credential exposure events until additional auditing and detection engineering are implemented (addressed in Lab 3).

# 

# ---



