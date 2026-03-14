# ARGUS

**Active Directory Review Framework**  
**Author:** Bobo Nikolov, EchoPentest

---

## Quick Install 

If you wish to try it out please visit: https://github.com/Nikolov999/argus

---

ARGUS is a modular, read-only Active Directory security assessment toolkit written in Go. It is designed for configuration auditing, exposure review, and defensive reporting in enterprise environments.

## Why this project exists

Active Directory environments accumulate configuration drift, privilege sprawl, legacy Kerberos settings, unmanaged delegation, inconsistent GPOs, and broad administrative exposure. ARGUS was built to provide a fast, operator-friendly CLI for reviewing those conditions through a structured, extensible framework.

---

## Core design goals

- Read-only assessment
- Enterprise-friendly CLI output
- Clear module separation
- JSON and HTML reporting
- Modular architecture for future expansion
- Defensive review only

---

## Features

- Kerberos exposure analysis
- Delegation auditing
- AD CS certificate surface review
- Privileged group scope analysis
- GPO enumeration
- Domain trust analysis
- Remote management surface discovery
- SMB exposure review
- ACL delegation indicators
- Tier 0 inventory
- Privilege sprawl review
- JSON / HTML reporting

---

## Modules

| Module | Description |
|---|---|
| `enum` | Domain inventory counts |
| `tierzero` | Tier 0 asset and identity inventory |
| `gpoenum` | Group Policy Object inventory |
| `trustaudit` | Domain trust inventory |
| `kerb` | Kerberos exposure review |
| `misconfig` | Read-only misconfiguration review |
| `shareaudit` | SMB exposure inventory |
| `lateralmap` | Remote administration surface inventory |
| `aclexposure` | Dangerous ACL rights exposure review |
| `sprawl` | Privilege sprawl review |
| `privmap` | Privileged group membership map |
| `adminscope` | Privileged group scope review |
| `blast` | Defender-oriented blast radius prioritization |
| `adminsd` | AdminSDHolder and SDProp drift review |
| `serviceimpact` | Service account privilege and dependency review |
| `daattacksurface` | Domain controller exposure inventory |
| `aclaudit` | Delegation and protected-object ACL indicators |
| `delegaudit` | Delegation configuration review |
| `adcs` | Basic AD CS review scaffold |
| `certsurface` | Certificate template surface review |
| `auto` | Combined core assessment |



---

## Example

```bash
argus auto -d corp.local -dc 10.10.10.5 -u 'CORP\auditor' -p 'Password123!'
Example output
Active Directory Review Framework
by EchoPentest

ARGUS EXECUTIVE SUMMARY

Users: 1532
Groups: 221
Computers: 412
Pre-auth disabled: 2
SPN accounts: 31
Privileged SPN accounts: 1
Legacy encryption review items: 6
Misconfiguration findings: 4
AD CS templates reviewed: 3
```

---

## Installation

### Build locally
go build -o argus ./cmd/argus

### Install globally
sudo cp argus /usr/local/bin/argus
sudo chmod +x /usr/local/bin/argus
hash -r

---

## Usage

### Inventory
argus enum -d corp.local -dc 10.10.10.5 -u 'CORP\auditor' -p 'Password123!'

### Kerberos review
argus kerb -d corp.local -dc 10.10.10.5 -u 'CORP\auditor' -p 'Password123!' --password-age

### GPO review
argus gpoenum -d corp.local -dc 10.10.10.5 -u 'CORP\auditor' -p 'Password123!'

### Tier 0 inventory
argus tierzero -d corp.local -dc 10.10.10.5 -u 'CORP\auditor' -p 'Password123!'

### Privilege sprawl review
argus sprawl -d corp.local -dc 10.10.10.5 -u 'CORP\auditor' -p 'Password123!'

### Reporting
argus kerb -d corp.local -dc 10.10.10.5 -u 'CORP\auditor' -p 'Password123!' --json kerb.json
argus auto -d corp.local -dc 10.10.10.5 -u 'CORP\auditor' -p 'Password123!' --html review.html

### Reporting outputs

- Human-readable CLI output

- JSON artifact for automation

- HTML report for review and sharing

### HTML Reporting

Each module can export structured HTML reports suitable for documentation or client reporting.

Example:

```bash
argus kerb -d corp.local -dc 10.10.10.5 --html kerberos_report.html
```

---

## Architecture summary

LDAP collectors
      ↓
data models
      ↓
audit modules
      ↓
report engine
      ↓
CLI interface

More detail is available in docs/architecture.md.

---

## Safe scope

ARGUS is designed for defensive assessment and reporting. It does not perform:

- credential extraction

- ticket requests for cracking

- exploit generation

- attack-path generation

- abuse command generation

- privilege escalation workflows

### Repository layout
argus/
├── cmd/
├── internal/
├── docs/
├── examples/
├── .github/workflows/
├── go.mod
├── README.md
├── LICENSE
└── CHANGELOG.md
### What this project demonstrates

- Go development

- Active Directory internals

- LDAP collection patterns

- network exposure review

- modular CLI architecture

- reporting design

- security engineering mindset

---

## Screenshots

### Kerberos Security Review

![Kerberos CLI](docs/screenshots/kerb.png)

### Kerberos HTML Report

![Kerberos HTML Report](docs/screenshots/kerb-html-report.png)

## Privilege Sprawl Review

![Sprawl](screenshots/sprawl.png)

### Lateral Mapping

![Auto Summary](docs/screenshots/lateralmap.png)


---

## Author

Bobo Nikolov, EchoPentest
