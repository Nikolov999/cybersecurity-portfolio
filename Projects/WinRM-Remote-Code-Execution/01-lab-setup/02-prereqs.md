\# Prerequisites



\## On Windows 10 Target (192.168.1.32)

\- Local admin (or authorized remote management) account for testing:

&nbsp; - labadmin

\- WinRM enabled (HTTP for initial testing; HTTPS for hardened state)

\- Event logging enabled:

&nbsp; - WinRM Operational channel

&nbsp; - Security auditing (logon + process creation)

&nbsp; - PowerShell Script Block logging (recommended)

&nbsp; - Sysmon configured (process creation + network)



\## On Kali Attacker (192.168.1.13)

Install tools:

```bash

sudo apt update

sudo apt install -y evil-winrm ruby-full

