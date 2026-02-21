# 01  Detection Logic (Portfolio-Grade)

## Rule Idea A  WinRM-driven Scheduled Task Creation
Trigger when all are true:
- Sysmon Event ID 1
- Image ends with `\schtasks.exe`
- CommandLine contains `/create`
- ParentImage contains `\wsmprovhost.exe` (WinRM host)

Add severity if:
- CommandLine contains `/ru SYSTEM`
- CommandLine contains `/sc ONLOGON` or `/sc ONSTART`

## Rule Idea B  Task Artifact Written
Trigger when:
- Sysmon Event ID 11
- TargetFilename starts with:
  - `C:\Windows\System32\Tasks\`
- Filename matches suspicious naming pattern (e.g., mimics update tools)

## Rule Idea C  Immediate Execution After Creation
Trigger when:
- Sysmon Event ID 1 with `/run`
- Same task name as recent `/create` within short window

## Fields To Collect (EchoSentinel Normalization)
- hostname
- username
- channel
- event_id
- image / parent_image
- command_line
- target_filename
- integrity_level
- logon_type (for Security 4624)
- record_id
- timestamp
