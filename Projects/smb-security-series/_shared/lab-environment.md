# Lab Environment 

## Network
- Lab subnet(s):10.10.10.0/24
- DNS / AD (if any):N/A
- Time source / timezone used in reports:London Time(UTC 0)

## Systems
- Wazuh Manager: wazuh-vm (10.10.10.30)
- Share host (Windows): lab-win-client (10.10.10.100) — Wazuh agent installed: yes
- Target host (Windows): lab-win-server (10.10.10.50) — Wazuh agent installed: yes
- Attacker VM (Kali/Ubuntu): lab-attacker (10.10.10.10)

## Logging assumptions
- Windows Security log enabled
- Sysmon installed: yes
- Wazuh agent configuration notes:
