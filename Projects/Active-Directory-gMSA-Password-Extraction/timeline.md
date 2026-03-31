# Timeline — Active Directory gMSA Password Extraction Abuse

## High-Level Sequence

| Step | Description |
|---|---|
| 1 | Enumerated a gMSA exposure path in the lab. |
| 2 | Recovered managed-account password material through authorized readers in the attack scenario. |
| 3 | Validated how excessive privileges on the gMSA expanded the compromise path. |
| 4 | Assessed the operational impact of using a managed service account for high-privilege administration. |
| 5 | Documented domain-level consequences and recovery requirements. |

## Evidence To Preserve

- authentication logs from domain controllers
- endpoint telemetry from source and target hosts
- PowerShell and process execution logs
- screenshots and console captures for the portfolio walkthrough
- any exported Argus graph artifacts where applicable
