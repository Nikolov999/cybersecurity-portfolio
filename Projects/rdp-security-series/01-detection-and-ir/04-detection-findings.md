# Detection Findings



Wazuh successfully detected RDP activity.



Relevant Windows Event IDs:

- 4625 — Failed Logon

- 4624 — Successful Logon

- Logon Type 10 — Remote Interactive (RDP)



Observed Indicators:

- Burst of failed logons from attacker IP

- Successful logon following failures

- Remote session established



EchoSentinel Alerts:

Default rules triggered on authentication failures and logon activity.



Analysis:

Event correlation showed a clear pattern of credential guessing followed by access.


