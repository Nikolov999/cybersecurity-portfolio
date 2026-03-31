# Timeline — Active Directory Kerberos Ticket Abuse

## High-Level Sequence

| Step | Description |
|---|---|
| 1 | Authenticated to the domain with a standard user in a lab environment. |
| 2 | Generated a Kerberos TGT and used ticket-based authentication for remote access. |
| 3 | Enumerated and exported in-memory tickets from the compromised endpoint. |
| 4 | Demonstrated ticket injection and session validation. |
| 5 | Validated downstream impact by identifying service-account credential exposure and replication-risk paths. |

## Evidence To Preserve

- authentication logs from domain controllers
- endpoint telemetry from source and target hosts
- PowerShell and process execution logs
- screenshots and console captures for the portfolio walkthrough
- any exported Argus graph artifacts where applicable
