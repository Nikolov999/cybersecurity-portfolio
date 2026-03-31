# Active Directory Kerberos Ticket Abuse

## Overview

Documented a full Kerberos ticket abuse path in a controlled AD lab: valid-domain-user foothold, TGT acquisition, pass-the-ticket, ticket harvesting, service-account credential exposure, and domain-impact assessment.

This repository is written as a **portfolio case study**, not as an operator playbook. It documents the lab scenario, the defensive value of the exercise, how I detected it in **EchoSentinel**, and the remediation actions required after validation.

## Scope

- Environment: isolated Active Directory lab
- Goal: validate detection coverage, understand blast radius, and document remediation
- Outcome: reproducible purple-team case study for portfolio use
- Safety: step-by-step exploitation commands and live secrets are intentionally excluded

## ATT&CK Mapping

| Technique ID | Technique |
|---|---|
| T1550.003 | Pass the Ticket |
| T1558 | Steal or Forge Kerberos Tickets |
| T1003.001 | LSASS Memory |
| T1003.006 | DCSync |
| T1021.006 | WinRM |

## Lab Context

- Domain: `LAB.LOCAL`
- DC: `192.168.1.31`
- Example low-priv user used in the lab: `bobo`
- Supporting tooling referenced in the engagement: Impacket, Mimikatz, CrackMapExec, PowerShell-based AD tooling, and internal tooling where applicable

## Attack Summary

1. Authenticated to the domain with a standard user in a lab environment.
2. Generated a Kerberos TGT and used ticket-based authentication for remote access.
3. Enumerated and exported in-memory tickets from the compromised endpoint.
4. Demonstrated ticket injection and session validation.
5. Validated downstream impact by identifying service-account credential exposure and replication-risk paths.


## What EchoSentinel Was Expected To Catch

Primary detection goals for this scenario:

- authentication pattern shifts
- abnormal privileged access emergence
- replication abuse indicators
- remote execution or lateral movement anomalies
- privileged object or directory control changes where applicable

See `detections/echo-sentinel-detections.md` for the detailed logic.

## Remediation Focus

This scenario was used to validate:

- preventive identity hardening
- privilege separation
- service-account control
- ACL hygiene
- detection engineering for authentication abuse and directory compromise

See `remediation.md` for the control plan.

## Repository Layout

```text
.
├── README.md
├── timeline.md
├── remediation.md
├── detections/
│   └── echo-sentinel-detections.md
└── recordings/
    └── .gitkeep
```

## Recording Notes

Place screen captures or walkthrough videos in `recordings/`.

## Portfolio Value

This project shows:
- offensive understanding in a controlled AD lab
- defensive engineering through SIEM content design
- remediation planning tied to the attack path
- ability to communicate technical findings in a clean repo format
