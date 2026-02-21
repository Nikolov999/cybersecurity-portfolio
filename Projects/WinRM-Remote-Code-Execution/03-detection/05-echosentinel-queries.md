 # EchoSentinel Queries (WinRM RCE)



These are generic query patterns. Adapt field names to your EchoSentinel schema.



 ## Query 1 — WinRM Operational Activity on Target

Filter:

 - `host _ip = 192.168.1.32`

 - `channel = Microsoft-Windows-WinRM/Operational`

 - `time in attack window`



Example (pseudo):

```text

host _ip:192.168.1.32 AND channel:"Microsoft-Windows-WinRM/Operational"


