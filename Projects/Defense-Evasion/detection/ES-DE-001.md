# Detection Engineering  ES-DE-001

## Rule Logic

Trigger when:

- 4624 (LogonType 3)
- AND 4672
- AND one or more:
  - 4719
  - 5007 / 5001
  - 7036 / 7040
  - SysmonDrv unload

Within 15 minutes.

## Objective

Detect intent, not isolated activity.

## MITRE Mapping

- T1562  Impair Defenses
- T1021.006  WinRM
- T1078  Valid Accounts
