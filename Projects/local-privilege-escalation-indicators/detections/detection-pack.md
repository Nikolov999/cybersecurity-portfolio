# Detection Pack  Local Privilege Escalation Indicators

## Goal
Detect privilege escalation behavior after authenticated lateral movement (WinRM), without exploit signatures.

## Primary Signals (Windows Security)

### 1) Local Administrators Membership Changes
- 4732: member added to local security group
- 4733: member removed from local security group
- 4728/4729/4756/4757: group membership changes (domain/global/universal variants)

High fidelity condition:
- Target group == "Administrators"
- Subject user not in admin baseline
- Source context aligned to remote management session (WinRM)

### 2) Elevated Token Issuance
- 4672: special privileges assigned to new logon

Use allowlist:
- Known admin/service accounts
Flag:
- New/rare accounts receiving 4672

### 3) Post-Elevation Privileged Activity
- 4673: privileged service called
- 4674: operation attempted on a privileged object

Use as enrichment:
- Demonstrate active use of elevated rights following admin group modification.

## Correlation (Narrative)
4732 (add admin)  4672 (elevated token)  4673/4674 (privileged usage)
