\# Remediation Summary



\## Goal

Reduce WinRM abuse risk while maintaining legitimate manageability and preserving detection telemetry.



\## Implemented Controls (Lab)

\- Disable weak auth (Basic) and disallow unencrypted traffic

\- Prefer HTTPS listener (5986) for encrypted WinRM

\- Restrict inbound WinRM with firewall allowlist:

&nbsp; - Allow only EchoSentinel host `192.168.1.27`

&nbsp; - Block attacker host `192.168.1.13` (and all others)



\## Verification

\- Pre-hardening: Kali can execute commands (credentialed)

\- Post-hardening: Kali is blocked; allowed management host can still operate



\## What To Show in Portfolio

\- Before/after diagrams

\- Config snippets (winrm settings + firewall rules)

\- EchoSentinel detections and raw logs

