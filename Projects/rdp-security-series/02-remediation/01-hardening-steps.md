# RDP Security Series – 02 Remediation  

## 01 – Hardening Steps



## Objective

Reduce RDP attack surface and eliminate weaknesses identified during brute-force, credential abuse, and lateral movement simulations.



---



## 1. Enforce Network Level Authentication (NLA)



Network Level Authentication ensures authentication occurs before a full RDP session is established.



\*\*PowerShell:\*\*

```powershell

Set-ItemProperty `

-Path "HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Terminal Server\\WinStations\\RDP-Tcp" `

-Name "UserAuthentication" -Value 1

```

---

## 2. Enforce TLS Encryption


Force RDP to use SSL/TLS instead of native RDP security.

```
Set-ItemProperty `
-Path "HKLM:\SYSTEM\CurrentControlSet\Control\Terminal Server\WinStations\RDP-Tcp" `
-Name "SecurityLayer" -Value 2

```

Values:

- 0 = RDP Security

- 1 = Negotiate

- 2 = SSL (TLS)

Expected: 2

---

## 3. Enable Account Lockout Policy


Configure via Local Security Policy:

- Lockout threshold: 5 invalid attempts

- Lockout duration: 15 minutes

- Reset counter: 15 minutes

Powershell Validation:

```

net accounts

```

---

## 4. Restrict RDP via Windows Firewall


Limit access to specific management IPs only.

```

New-NetFirewallRule `
-DisplayName "Allow RDP From Management Host" `
-Direction Inbound `
-Protocol TCP `
-LocalPort 3389 `
-RemoteAddress 10.10.10.5 `
-Action Allow

```

---

## 5. Rename or Disable Built-in Administrator

``` Powershell

Rename-LocalUser -Name "Administrator" -NewName "svc_admin_local"

```

``` Powershell

Disable-LocalUser -Name "Administrator"

```

---

## 6. Enable Security Event Logging


Ensure auditing is enabled for:

- Logon success (4624)

- Logon failure (4625)

- RDP connection (1149)

- Session reconnect/disconnect (4778 / 4779)

``` Powershell

auditpol /set /category:"Logon/Logoff" /success:enable /failure:enable

```

---

## 7. Disable RDP If Not Required

```Powershell

Set-ItemProperty `
-Path "HKLM:\SYSTEM\CurrentControlSet\Control\Terminal Server" `
-Name "fDenyTSConnections" -Value 1

```

---

## Security Impact

- Reduced brute-force success rate

- Enforced pre-authentication validation

- Limited remote lateral movement paths

- Improved detection telemetry for SIEM ingestion