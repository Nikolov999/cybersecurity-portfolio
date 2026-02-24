# Attack Narrative (Pre-Exfil Phase)

## Objective
Establish a WinRM session, execute commands remotely, stage data locally into a single directory, and prepare a compressed archive **without** performing outbound transfer.

## Behavioral Stages

### Stage 1  Initial Access (WinRM)
- Remote network logon to target using WinRM
- Creates a session context for remote execution

**Anchor telemetry:** Security 4624 (Type 3), source IP = attacker

### Stage 2  Remote Execution Baseline
- WinRM provider host (wsmprovhost.exe) spawns child processes
- Confirms command execution occurs inside remote management channel

**Anchor telemetry:** Sysmon 1 child process where parent is wsmprovhost.exe -Embedding

### Stage 3  Staging
- Files are aggregated from multiple user locations into one destination:
  - C:\Users\Public\staging\

**Anchor telemetry:** burst file writes (if Sysmon FileCreate is enabled) + concentrated destination

### Stage 4  Compression Preparation
- PowerShell archive tooling loads compression assembly and/or module
- Archive artifact is created (zip) under public path

**Anchor telemetry:** PowerShell Operational 4103 with Add-Type / archive module usage

### Stage 5  Session End
- Logoff event closes correlation window

**Anchor telemetry:** Security 4634

## Sequence Model (Detection-Friendly)

4624 Type 3
 wsmprovhost.exe observed
 child process execution (Sysmon 1)
 staging behavior (concentration)
 compression prep (PS 4103)
 archive artifact created
 4634 session end
