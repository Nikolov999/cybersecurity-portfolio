# Active Directory Advanced ACL Abuse (WriteOwner on Domain Admins)

## Overview

Demonstrated an ACL-driven privilege escalation path in a controlled lab. A low-privileged user had WriteOwner exposure over a high-value AD group, which enabled ownership takeover, rights expansion, group membership abuse, and domain-control impact validation.

This repository is written as a **portfolio case study**, not as an operator playbook. It documents the lab scenario, the defensive value of the exercise, how I detected it in **EchoSentinel**, and the remediation actions required after validation.

## Scope

- Environment: isolated Active Directory lab: 
   - Windows Server 2022 VM
   - Kali Linux VM
- Goal: validate detection coverage, understand blast radius, and document remediation
- Outcome: reproducible purple-team case study for portfolio use
- Safety: step-by-step exploitation commands and live secrets are intentionally excluded

## ATT&CK Mapping

| Technique ID | Technique |
|---|---|
| T1484.001 | Domain Policy Modification |
| T1098 | Account Manipulation |
| T1069.002 | Domain Groups |
| T1003.006 | DCSync |
| T1558.001 | Golden Ticket |

## Lab Context

- Domain: `LAB.LOCAL`
- DC: `192.168.1.31`
- Example low-priv user used in the lab: `bobo`
- Supporting tooling referenced in the engagement: Impacket, Mimikatz, CrackMapExec, PowerShell-based AD tooling, and internal tooling where applicable

## Attack Summary

1. Used Argus to enumerate and visualize an attack path involving WriteOwner over a privileged AD group.
2. Validated that directory ACL misconfiguration alone was sufficient for privilege escalation.
3. Demonstrated ownership and DACL abuse in a lab-safe sequence.
4. Confirmed privileged group membership changes and resulting access expansion.
5. Assessed downstream domain compromise risk tied to replication secrets and forged-ticket persistence.


## Argus Usage

This case study includes **Argus**, my AD attack-path enumeration CLI, as part of the discovery phase.

Argus was used to:
- enumerate effective rights in the domain
- visualize attack paths to privileged objects
- surface the `WriteOwner` relationship on a protected group
- export graph data for presentation and validation

This strengthened the project by tying offensive validation to graph-driven privilege-path analysis rather than manual guesswork alone.

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
