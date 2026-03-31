# Active Directory gMSA Password Extraction Abuse

## Overview

Analyzed the risk of over-privileged gMSA usage in a lab. Demonstrated how readable gMSA password material can become a direct path to privileged access, remote execution, and domain-wide impact when account scope is poorly controlled.

This repository is written as a **portfolio case study**, not as an operator playbook. It documents the lab scenario, the defensive value of the exercise, how I detected it in **EchoSentinel**, and the remediation actions required after validation.

## Scope

- Environment: isolated Active Directory lab
- Goal: validate detection coverage, understand blast radius, and document remediation
- Outcome: reproducible purple-team case study for portfolio use
- Safety: step-by-step exploitation commands and live secrets are intentionally excluded

## ATT&CK Mapping

| Technique ID | Technique |
|---|---|
| T1078 | Valid Accounts |
| T1003 | OS Credential Dumping |
| T1550.002 | Pass the Hash |
| T1021.002 | SMB/Windows Admin Shares |
| T1003.006 | DCSync |

## Lab Context

- Domain: `LAB.LOCAL`
- DC: `192.168.1.31`
- Example low-priv user used in the lab: `bobo`
- Supporting tooling referenced in the engagement: Impacket, Mimikatz, CrackMapExec, PowerShell-based AD tooling, and internal tooling where applicable

## Attack Summary

1. Enumerated a gMSA exposure path in the lab.
2. Recovered managed-account password material through authorized readers in the attack scenario.
3. Validated how excessive privileges on the gMSA expanded the compromise path.
4. Assessed the operational impact of using a managed service account for high-privilege administration.
5. Documented domain-level consequences and recovery requirements.


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
