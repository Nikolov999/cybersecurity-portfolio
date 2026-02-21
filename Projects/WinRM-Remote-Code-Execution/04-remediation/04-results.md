# Results (Before vs After)



## Before Hardening (Permissive)

- WinRM over HTTP `5985` reachable from LAN

- Kali (`192.168.1.13`) can authenticate and execute commands (with valid credentials)

- Telemetry observed:

 - WinRM Operational activity

 - Security 4624 logons from `192.168.1.13`

 - `wsmprovhost.exe` process chain

 - PowerShell 4104 script blocks (if enabled)



## After Hardening (Constrained)

- Weak auth disabled, unencrypted traffic disallowed

- HTTPS listener optionally enabled

- Firewall allowlist restricts WinRM inbound:

 - Allowed: `192.168.1.27` (EchoSentinel host)

 - Blocked: `192.168.1.13` (Kali attacker)



Expected outcome:

- Kali attempts fail at network boundary (preferred) or authentication boundary

- EchoSentinel still ingests logs and detections remain operational



