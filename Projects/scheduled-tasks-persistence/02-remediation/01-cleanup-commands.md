# 01  Cleanup Commands (Local on Target)

## Run these on the Windows target (admin)

### Confirm task exists
schtasks /query /tn "WindowsUpdateCheck" /v /fo LIST

### Export task XML (evidence)
schtasks /query /tn "WindowsUpdateCheck" /xml > C:\Users\Public\WindowsUpdateCheck.xml

### Disable task (containment)
schtasks /change /tn "WindowsUpdateCheck" /disable

### Delete task (eradication)
schtasks /delete /tn "WindowsUpdateCheck" /f

### Remove payload
del /f /q C:\Users\Public\updater.ps1

### Remove exported XML after you store it in evidence
del /f /q C:\Users\Public\WindowsUpdateCheck.xml
