# 02  Remediation

## Objective
Contain and remove scheduled-task persistence and confirm no recurrence.

## Immediate Actions
1. Export task XML for evidence
2. Disable task
3. Delete task
4. Remove payload script
5. Verify no additional tasks created in same time window

## Evidence to Capture
- Task properties (name, triggers, action)
- Deletion/disable events (TaskScheduler log if enabled; Sysmon process execution of schtasks delete)
- Confirmation that task file is removed from:
  - `C:\Windows\System32\Tasks\WindowsUpdateCheck`
- Confirmation `C:\Users\Public\updater.ps1` removed
