# Timeline — Active Directory Advanced ACL Abuse (WriteOwner on Domain Admins)

## High-Level Sequence

| Step | Description |
|---|---|
| 1 | Used Argus to enumerate and visualize an attack path involving WriteOwner over a privileged AD group. |
| 2 | Validated that directory ACL misconfiguration alone was sufficient for privilege escalation. |
| 3 | Demonstrated ownership and DACL abuse in a lab-safe sequence. |
| 4 | Confirmed privileged group membership changes and resulting access expansion. |
| 5 | Assessed downstream domain compromise risk tied to replication secrets and forged-ticket persistence. |

## Evidence To Preserve

- authentication logs from domain controllers
- endpoint telemetry from source and target hosts
- PowerShell and process execution logs
- screenshots and console captures for the portfolio walkthrough
- any exported Argus graph artifacts where applicable
