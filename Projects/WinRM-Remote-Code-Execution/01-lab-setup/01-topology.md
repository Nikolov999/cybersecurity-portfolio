\# Lab Topology



\## Network

Single flat LAN segment (`192.168.1.0/24`) for controlled, observable traffic.



\## Nodes

\- \*\*EchoSentinel (host / SIEM):\*\* `192.168.1.27`

&nbsp; - Central visibility and alerting

\- \*\*Kali (attacker):\*\* `192.168.1.13`

&nbsp; - Initiates WinRM connections and remote commands

\- \*\*Windows 10 (target):\*\* `192.168.1.32`

&nbsp; - WinRM enabled, EchoSentinel installed and instrumented for telemetry



\## Ports

\- \*\*WinRM HTTP:\*\* `5985/tcp`



\## Traffic Direction

\- Attacker → Target: WinRM session + remote execution

\- Target → EchoSentinel: log forwarding / agent telemetry (implementation-specific)

