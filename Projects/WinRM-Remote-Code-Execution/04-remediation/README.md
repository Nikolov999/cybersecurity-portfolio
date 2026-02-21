# Remediation Summary



## Goal

Reduce WinRM abuse risk while maintaining legitimate manageability and preserving detection telemetry.



## Implemented Controls (Lab)

- Disabled weak auth (Basic) and disallow unencrypted traffic

- Prefer HTTPS listener (5986) for encrypted WinRM

- Restrict inbound WinRM with firewall allowlist:

 - Allowed only EchoSentinel host `192.168.1.27`

 - Blocked attacker host `192.168.1.13` (and all others)



