\# Threat Model



\## Why WinRM Matters

WinRM is a legitimate remote management protocol. In intrusions, WinRM becomes a high-signal lateral movement and remote execution channel after credential access.



\## Attacker Goal

\- Use valid credentials to:

&nbsp; - Execute commands remotely

&nbsp; - Enumerate system state

&nbsp; - Stage payloads or run living-off-the-land commands



\## Common Preconditions

\- Credential theft/reuse (local admin, reused password, password spraying)

\- WinRM enabled and reachable on the network

\- Firewall allows inbound 5985/5986

\- Account has rights for remote management (often local admin)



\## Key Risks

\- Low friction remote execution without dropping binaries (depending on technique)

\- Remote PowerShell enables fast discovery and staging

\- Can blend with legitimate admin activity unless baselined and scoped



\## Defender Assumptions (This Lab)

\- Target Windows 10 produces:

&nbsp; - WinRM operational events

&nbsp; - Security logon/process creation events (4688 requires auditing enabled)

\- EchoSentinel from it's agent ingests events from the Windows 10 target and can query/correlate.



\## High Value Detections

\- WinRM session creation + source IP correlation

\- `wsmprovhost.exe` spawning PowerShell/CMD

\- Script block content indicating remote execution commands or download/execute patterns

\- Unusual remote management from non-admin workstation subnets (here: `192.168.1.13`)

