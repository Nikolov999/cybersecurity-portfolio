\# Configuration Changes (WinRM Secure Baseline)



Run on Windows 10 `192.168.1.32` in elevated PowerShell.



\## 1) Disable Basic Auth + Disallow Unencrypted

```powershell

winrm set winrm/config/service/auth '@{Basic="false"}'

winrm set winrm/config/service '@{AllowUnencrypted="false"}'

