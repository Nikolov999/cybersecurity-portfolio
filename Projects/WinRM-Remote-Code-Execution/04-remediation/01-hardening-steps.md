\# Hardening Steps (WinRM)



Target: Windows 10 `192.168.1.32`



\## Step 1 — Reduce Exposure

If WinRM is not required, disable it:

```powershell

Stop-Service WinRM

Set-Service WinRM -StartupType Disabled

