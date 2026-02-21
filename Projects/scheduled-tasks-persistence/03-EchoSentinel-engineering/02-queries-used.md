# 02  Queries Used (Copy/Paste)

## Find schtasks create/run
channel:"Microsoft-Windows-Sysmon/Operational" event_id:1 image:"C:\Windows\System32\schtasks.exe"

## Find task file written
channel:"Microsoft-Windows-Sysmon/Operational" event_id:11 target_filename:"C:\Windows\System32\Tasks\WindowsUpdateCheck"

## Find payload script created
channel:"Microsoft-Windows-Sysmon/Operational" event_id:11 target_filename:"C:\Users\Public\updater.ps1"

## Find WinRM-auth context
channel:"Security" event_id:4624
channel:"Security" event_id:4672
