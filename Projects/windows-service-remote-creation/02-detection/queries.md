# Simple hunt queries (manual)

## Find sc.exe service creation
Filter:
- channel: Microsoft-Windows-Sysmon/Operational
- event_id: 1
- image endswith: \sc.exe
- command_line contains: " create "

## Find service ImagePath registry edits
Filter:
- channel: Microsoft-Windows-Sysmon/Operational
- event_id: 13
- target_object contains: "\System\CurrentControlSet\Services\"
- target_object contains: "\ImagePath"

## Find payload staged in ProgramData
Filter:
- channel: Microsoft-Windows-Sysmon/Operational
- event_id: 11
- target_filename startswith: "C:\ProgramData\"
