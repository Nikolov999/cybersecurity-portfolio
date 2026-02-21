# Validation Test Cases



All tests target Windows 10 `192.168.1.32`.

EchoSentinel is `192.168.1.27`.

Attacker Kali is `192.168.1.13`.



## Test Case 1 — Successful WinRM Session (Pre-Hardening)

- Source: Kali `192.168.1.13`

- Action:

 - `evil-winrm` connect and run `whoami`

- Expected:

 - WinRM Operational entries on target

 - Security 4624 on target with source IP `192.168.1.13`

 - `wsmprovhost.exe` evidence

 - Optional: 4104 script block content



## Test Case 2 — Remote Command Execution Burst (Pre-Hardening)

- Source: Kali `192.168.1.13`

- Action:

 - Execute 5 commands in 60 seconds (`hostname`, `ipconfig`, `whoami`, `netstat`, `systeminfo`)

- Expected:

 - Multiple process creations tied to provider host

 - 4104 entries containing commands (if enabled)

 - EchoSentinel alert for WinRM RCE pattern



## Test Case 3 — Failed WinRM After Hardening (Firewall Allowlist)

- Source: Kali `192.168.1.13`

- Action:

 - Attempt `evil-winrm` to target

- Expected:

 - Connection failure (blocked/refused)

 - No 4624 from Kali for WinRM session

 - Optional: firewall log evidence if enabled



## Test Case 4 — Allowed Management Host Access (Post-Hardening)

- Source: EchoSentinel host `192.168.1.27`

- Action:

 - WinRM management attempt (if you use it as an admin station)

- Expected:

 - Success only from allowlisted IP

 - Corresponding logs visible in EchoSentinel



## Test Case 5 — Content-Level Proof (PowerShell 4104)

- Source: whichever host successfully remotes (pre-hardening or allowlisted)

- Action:

 - Execute a distinct script block string: `Write-Output "WINRM\_VALIDATION\_4104"`

- Expected:

 - 4104 contains the unique marker

&nbsp; - EchoSentinel can pivot from alert to raw script block evidence


