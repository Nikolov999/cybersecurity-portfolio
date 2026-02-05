# Detection reality (no tuning)

## What Wazuh detected

* Events list:

Feb 3, 2026 @ 20:20:53.112 | Administrator | Rule ID: 67028 | Special Privileges Assigned to Logon | Severity: N/A



Feb 3, 2026 @ 20:20:53.114 | Administrator | Rule ID: 6 | Successful Remote Logon Detected | Severity: N/A



Feb 3, 2026 @ 20:20:53.171 | Administrator | Rule ID: 60137 | Windows User Logoff | Severity: N/A

## What was not detected (expected gaps)

* No direct alert for SMB credential file read
* No direct alert stating “credentials harvested”
* Possible weak/noisy signals only

## Why this is expected

Legitimate protocols + valid credentials often appear normal; SIEM visibility is partial by default.

## Evidence pointers

* evidence/wazuh/alerts.json
