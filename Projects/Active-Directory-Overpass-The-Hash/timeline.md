# Timeline — Active Directory Overpass-the-Hash + Delegation Abuse

## High-Level Sequence

| Step | Description |
|---|---|
| 1 | Started from previously recovered NTLM material in a controlled domain. |
| 2 | Converted password-equivalent material into Kerberos authentication. |
| 3 | Used Kerberos-backed remote execution for lateral movement in the lab. |
| 4 | Validated escalation impact through privileged account exposure and ticket reuse scenarios. |
| 5 | Mapped the role of delegation in expanding the blast radius. |

## Evidence To Preserve

- authentication logs from domain controllers
- endpoint telemetry from source and target hosts
- PowerShell and process execution logs
- screenshots and console captures for the portfolio walkthrough
- any exported Argus graph artifacts where applicable
