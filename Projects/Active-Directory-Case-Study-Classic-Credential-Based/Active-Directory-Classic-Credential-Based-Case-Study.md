# EchoSentinel Active Directory Attack Reconstruction

Source set used:
- Screenshots extracted from `Screenshots.zip`
- Supporting scenario notes: fileciteturn0file0

## Executive summary

The screenshots show a full AD intrusion chain against `WIN-EVGH6IS9JPB.lab.local` in `LAB.LOCAL`, with the attacker operating from `192.168.1.13` and, in at least one NTLM validation event, workstation name `kali`.

The sequence visible in EchoSentinel is:

1. Anonymous SMB/network reconnaissance against the domain controller.
2. Kerberos ticket activity for `j.smith`, including RC4 service ticket requests consistent with Kerberoasting.
3. Successful NTLM/network authentication as `Bobo` from `192.168.1.13`.
4. Execution activity on the host, including `net.exe`, `net1.exe`, `cmd.exe`, `WmiPrvSE.exe`, and `mimikatz.exe`.
5. LSASS access by `mimikatz.exe`.
6. Service / scheduled-task / permission-modification alerts in EchoSentinel.
7. Later authentication and privilege events involving `WIN-EVGH6IS9JPB$` and `Administrator@LAB.LOCAL`.
8. Directory Service object access (`4662`) events strongly consistent with DCSync / replication-right abuse.
9. Follow-on credential use alert (`4648`) visible in EchoSentinel alerts.

## Environment / infrastructure identified

- **Hostname / computer:** `WIN-EVGH6IS9JPB.lab.local`
- **Short host:** `WIN-EVGH6IS9JPB`
- **Domain:** `LAB.LOCAL`
- **Likely domain controller role:** supported by Kerberos (`4768`, `4769`) and Directory Service access (`4662`) activity shown in the screenshots.
- **Attacker source IP:** `192.168.1.13`
- **Attacker workstation name observed:** `kali` (event `4776` for `j.smith`)

## Identities observed

- `ANONYMOUS LOGON`
- `j.smith`
- `j.smith@LAB.LOCAL`
- `Bobo`
- `Administrator`
- `Administrator@LAB.LOCAL`
- `WIN-EVGH6IS9JPB$`
- `WIN-EVGH6IS9JPB$@LAB.LOCAL`
- `LOCAL SERVICE`

## Timeline reconstruction

Times below are from the screenshots and should be treated as the visible timeline captured in EchoSentinel, not necessarily the complete raw-log timeline.

### Phase 1 — Reconnaissance / enumeration

**08:06:44–08:06:47**
- `5145` on `WIN-EVGH6IS9JPB` for `WIN-EVGH6IS9JPB$`
- `4624` on `WIN-EVGH6IS9JPB` for `ANONYMOUS LOGON`
- `4627` on `WIN-EVGH6IS9JPB` for `ANONYMOUS LOGON`
- `4689` on `WIN-EVGH6IS9JPB` for `WIN-EVGH6IS9JPB$`
- `5140` on `WIN-EVGH6IS9JPB` for `ANONYMOUS LOGON`

**Interpretation**
- This is the visible start of the intrusion chain.
- `4624` with **LogonType 3**, `AuthenticationPackageName: NTLM`, source `192.168.1.13`, target user `ANONYMOUS LOGON`, and `5140`/`5145` show anonymous SMB/file-share style probing.
- EchoSentinel also raised `ES-LAT-001 Network logon (4624 LogonType=3)` for this stage.

### Phase 2 — Kerberos-based account discovery / roasting setup

**08:07:34** — `4768`, DB ID `41858`
- User: `j.smith`
- Service: `krbtgt`
- TicketEncryptionType: `0x12`
- IP: `192.168.1.13`
- Port: `49985`

**08:08:01** — `4768`, DB ID `41882`
- User: `j.smith`
- Service: `krbtgt`
- TicketEncryptionType: `0x17`
- IP: `192.168.1.13`
- Port: `34708`

**08:09:15** — `4768`, DB ID `41923`
- User: `j.smith`
- Service: `krbtgt`
- TicketEncryptionType: `0x17`
- IP: `192.168.1.13`
- Port: `44818`

**08:09:15** — `4769`, DB ID `41924`
- User: `j.smith@LAB.LOCAL`
- Service: `Bobo`
- TicketEncryptionType: `0x17`
- IP: `192.168.1.13`
- Port: `44820`

**08:09:15** — `4769`, DB ID `41925`
- User: `j.smith@LAB.LOCAL`
- Service: `vagran` (as shown in screenshot; likely intended to be `vagrant`)
- TicketEncryptionType: `0x17`
- IP: `192.168.1.13`
- Port: `44834`

**08:09:15** — `4769`, DB ID `41926`
- User: `j.smith@LAB.LOCAL`
- Service: `j.smith`
- TicketEncryptionType: `0x17`
- IP: `192.168.1.13`
- Port: `44850`

**Correlated hunt view around 08:09**
- Multiple `4662` events are visible at `08:09:47`
- Another `4662` appears at `08:10:38`

**Interpretation**
- The repeated `4768`/`4769` pattern from the same source IP, especially `4769` with **RC4 (`0x17`)**, matches Kerberoasting-style service ticket collection.
- EchoSentinel explicitly raised **`ES-AD-001 Kerberoasting indicator (4769 RC4)`** at **08:09:15** for `j.smith@LAB.LOCAL`.
- This is the clearest detection pivot from “recon” into “credential access”.

### Phase 3 — Password validation / credential compromise

**08:11:16** — `4776`, DB ID `41974`
- Target user: `j.smith`
- Package: `MICROSOFT_AUTHENTICATION_PACKAGE_V1_0`
- Workstation: `kali`
- Status: `0x0`

**08:15:49** — `4776`, DB ID `42142`
- Target user: `Bobo`
- Package: `MICROSOFT_AUTHENTICATION_PACKAGE_V1_0`
- Status: `0x0`

**08:15:49.8377309Z** — `4624`
- Target user: `Bobo`
- Domain: `LAB`
- LogonType: `3`
- LogonProcess: `NtLmSsp`
- AuthenticationPackage: `NTLM`
- PackageName: `NTLM V2`
- Source IP: `192.168.1.13`
- Source port: `56436`

**Interpretation**
- `4776` with success (`Status 0x0`) for `j.smith` from workstation `kali` indicates NTLM credential validation.
- `4776` success for `Bobo` followed immediately by `4624` network logon from `192.168.1.13` indicates the attacker successfully authenticated as the service/user account `Bobo`.
- EchoSentinel raised:
  - `ES-LAT-001 Network logon (4624 LogonType=3)` at **08:15:49** for `Bobo`
  - `ES-AUTH-008 Special privileges assigned at logon (4672)` at **08:15:49** for `Bobo`

### Phase 4 — Remote execution / foothold consolidation

**08:15:57** — `4688`, DB ID `42169`
- New process: `C:\Windows\System32\wbem\WmiPrvSE.exe`
- Parent: `C:\Windows\System32\svchost.exe`
- Subject user: `WIN-EVGH6IS9JPB$`
- Target user: `LOCAL SERVICE`

**08:16:05** — EchoSentinel alert only
- `ES-PERS-001 New service installed (4697)`
- Host: `WIN-EVGH6IS9JPB`
- User: `Bobo`

**08:16:16** — `4688`, DB ID `42209`
- New process: `C:\Windows\SysWOW64\cmd.exe`
- Parent: `C:\Windows\GUvaKgMe.exe`

**08:16:44** — `4688`, DB ID `42218`
- New process: `C:\Windows\SysWOW64\net.exe`
- Parent: `C:\Windows\SysWOW64\cmd.exe`

**08:16:47** — `4688`, DB ID `42219`
- New process: `C:\Windows\SysWOW64\net1.exe`
- Parent: `C:\Windows\SysWOW64\net.exe`

**Interpretation**
- The `4697` alert plus `4688` process chain indicate remote execution and service-based foothold establishment.
- `cmd.exe -> net.exe -> net1.exe` strongly suggests account/group/service enumeration or manipulation after compromise.
- The random-looking parent executable `C:\Windows\GUvaKgMe.exe` is suspicious and may be a dropped loader or renamed tool.

### Phase 5 — Tasking / service persistence activity

**08:17:30** — `4688`, DB ID `42233`
- New process: `C:\Tools\x64\mimikatz.exe`
- Parent: `C:\Windows\SysWOW64\cmd.exe`

**08:17:46** — EchoSentinel alert only
- `ES-PERS-003 Scheduled task created (4698)`
- Host: `WIN-EVGH6IS9JPB`
- User: `WIN-EVGH6IS9JPB$`

**08:17:49** — `4688`, DB ID `42241`
- New process: `C:\ProgramData\Microsoft\Windows Defender\Platform\4.18.26010.5-0\MpCmdRun.exe`
- Parent: `...\MsMpEng.exe`

**Interpretation**
- `mimikatz.exe` execution is direct evidence of credential-dumping intent.
- The scheduled-task alert at `08:17:46` shows a persistence or execution mechanism was created shortly after foothold establishment.
- `MpCmdRun.exe` suggests Defender interaction, possibly scan/remediation/response to the tooling, but the screenshots do not prove intent either way.

### Phase 6 — Credential dumping / LSASS access

**08:18:03** — `4663`, DB ID `42248`
- Object type: `Process`
- Object name: `\Device\HarddiskVolume2\Windows\System32\lsass.exe`
- Process name: `C:\Tools\x64\mimikatz.exe`
- AccessMask: `0x10`

**Interpretation**
- This is the strongest host-level credential dumping indicator in the set.
- `mimikatz.exe` accessed `lsass.exe`, which aligns with `sekurlsa::logonpasswords` / credential extraction behavior.

### Phase 7 — Continued logons / elevated context / service-account activity

**08:18:56–08:19:58**
- Repeated `4624` events in hunt view for user `WIN-EVGH6IS9JPB$`

**08:22:04** — `4688`, DB ID `42340`
- New process: long `TiWorker.exe` path under `WinSxS`

**08:22:30** — `4688`, DB ID `42346`
- New process: `C:\Windows\System32\wbem\WmiPrvSE.exe`
- Parent: `svchost.exe`
- Target user shown as `WIN-EVGH6IS9JPB$`

**08:25:47** — `4688`, DB ID `42423`
- New process: `C:\Windows\System32\LogonUI.exe`
- Parent: `winlogon.exe`

**08:25:51** — `4688`, DB ID `42426`
- New process: `C:\Windows\System32\taskhostw.exe`
- Target user: `Administrator`

**08:26:14** — `4688`, DB ID `42457`
- New process: `C:\Windows\System32\wbem\WmiPrvSE.exe`
- Target user: `LOCAL SERVICE`

**08:27:17** — `4688`, DB ID `42477`
- New process: `C:\Windows\System32\wbem\WmiPrvSE.exe`

**Interpretation**
- This block indicates the compromise moved into an elevated or administrative context.
- `taskhostw.exe` targeting `Administrator` is a useful pivot suggesting administrator-level session creation or code execution in that context.

### Phase 8 — Re-authentication as Bobo and privilege-changing activity

**08:33:17** — `4624` visible in detail view (event ID faint in screenshot, event body clearly shows logon fields)
- User: `Bobo`
- LogonType: `3`
- Auth: `NTLM / NTLM V2`
- Source IP: `192.168.1.13`
- Source port: `35858`

**08:34:06** — `4688`, DB ID `42623`
- New process: `C:\Windows\SysWOW64\cmd.exe`
- Parent: `C:\Windows\sqZWiSCg.exe`

**08:34:06** — `4688`, DB ID `42624`
- New process: `C:\Windows\System32\conhost.exe`
- Parent: `C:\Windows\SysWOW64\cmd.exe`

**08:34:51** — `4688`, DB ID `42630`
- New process: `C:\Tools\x64\mimikatz.exe`
- Parent: `C:\Windows\SysWOW64\cmd.exe`

**08:35:55** — EchoSentinel alert only
- `ES-SMB-003 File/share permission modified (4670)`
- Severity: `high`
- Host: `WIN-EVGH6IS9JPB`
- User: `WIN-EVGH6IS9JPB$`
- Risk: `95`

**08:35:56** — EchoSentinel alerts
- `ES-AUTH-008 Special privileges assigned at logon (4672)`
- `ES-LAT-001 Network logon (4624 LogonType=3)`
- `ES-AUTH-004 Rapid IP change for same user`
- Host: `WIN-EVGH6IS9JPB`
- User: `WIN-EVGH6IS9JPB$`

**Interpretation**
- The attacker re-entered with `Bobo`, spawned another suspicious process chain, and executed `mimikatz.exe` again.
- The high-risk `4670` alert indicates ACL / permission modification. In the context of the lab scenario, this lines up with **ACL abuse / privilege escalation**.
- The `4672` + `4624` cluster for the machine account shows a privileged logon context becoming active around the same time.

### Phase 9 — DCSync / directory replication abuse

**08:36:59** — `4662` burst, DB IDs `42668`, `42669`, `42670`, `42671`
- Object server: `DS`
- OperationType: `Object Access`
- AccessMask: `0x100`
- Multiple replication-related GUIDs / properties shown, including:
  - `{1131f6aa-9c07-11d1-f79f-00c04fc2dcd2}`
  - `{1131f6ad-9c07-11d1-f79f-00c04fc2dcd2}`
  - `{89e95b76-444d-4c62-991a-0facbeda640c}`
  - `{19195a5b-6da0-11d0-afd3-00c04fd930c9}`

**Interpretation**
- This is the clearest **DCSync / replication-right abuse** evidence in the screenshots.
- Multiple `4662` events with DS object access and replication GUIDs are the classic Windows logging footprint for DCSync.
- This stage likely corresponds to replication of sensitive directory secrets, including administrator and potentially `krbtgt`, matching the lab notes.

### Phase 10 — Explicit credentials / follow-on privileged auth

**08:37:08** — EchoSentinel alerts
- `ES-LAT-001 Network logon (4624 LogonType=3)`
- `ES-AUTH-004 Rapid IP change for same user`
- User: `WIN-EVGH6IS9JPB$`

**08:41:41** — EchoSentinel alert
- `ES-AUTH-007 Explicit credentials used (4648)`
- Host: `WIN-EVGH6IS9JPB`
- User: `WIN-EVGH6IS9JPB$`

**08:41:41** — `4768`, DB ID `42799`
- User: `WIN-EVGH6IS9JPB$`
- Service: `krbtgt`
- TicketEncryptionType: `0x12`
- PreAuthType: `2`
- Address: `::1`

**08:41:41** — `4769`, DB ID `42800`
- User: `WIN-EVGH6IS9JPB$@LAB.LOCAL`
- Service: `WIN-EVGH6IS9JPB$`
- TicketEncryptionType: `0x12`
- Address: `::1`

**08:42:10** — hunt view entries
- `4768` for `WIN-EVGH6IS9JPB$`
- `4769` for `WIN-EVGH6IS9JPB$@LAB.LOCAL`
- `4624`
- `4624`

**08:43:24** — hunt view
- `4688`

**08:43:30** — hunt view
- `4624`

**08:46:15–08:47:34** — hunt view
- repeated `4624`

**08:48:35** — hunt view
- `4769` for `Administrator@LAB.LOCAL`

**08:49:36** — hunt view
- `4769` for `Administrator@LAB.LOCAL`

**Interpretation**
- `4648` indicates a process used explicit credentials.
- The later `4769` service ticket activity for `Administrator@LAB.LOCAL` indicates the attacker reached high privilege and is now requesting tickets in an administrator context.
- This is consistent with the late-stage scenario outcome: privilege escalation to domain-admin-equivalent control after credential theft and directory abuse.

## Alert inventory visible in EchoSentinel

From the alerts list screenshots:

| Alert ID | Time | Severity | Rule | Host | User | Risk |
|---|---|---:|---|---|---|---:|
| 856 | 07/03/2026 08:06:45 | medium | `ES-LAT-001 Network logon (4624 LogonType=3)` | `WIN-EVGH6IS9JPB` | `ANONYMOUS LOGON` | 70 |
| 857 | 07/03/2026 08:09:15 | medium | `ES-LAT-001 Network logon (4624 LogonType=3)` | `WIN-EVGH6IS9JPB` | `j.smith` | 70 |
| 858 | 07/03/2026 08:09:15 | medium | `ES-AD-001 Kerberoasting indicator (4769 RC4)` | `WIN-EVGH6IS9JPB` | `j.smith@LAB.LOCAL` | 65 |
| 859 | 07/03/2026 08:15:49 | medium | `ES-AUTH-008 Special privileges assigned at logon (4672)` | `WIN-EVGH6IS9JPB` | `Bobo` | 70 |
| 860 | 07/03/2026 08:15:49 | medium | `ES-LAT-001 Network logon (4624 LogonType=3)` | `WIN-EVGH6IS9JPB` | `Bobo` | 70 |
| 861 | 07/03/2026 08:16:05 | medium | `ES-PERS-001 New service installed (4697)` | `WIN-EVGH6IS9JPB` | `Bobo` | 60 |
| 862 | 07/03/2026 08:17:46 | medium | `ES-PERS-003 Scheduled task created (4698)` | `WIN-EVGH6IS9JPB` | `WIN-EVGH6IS9JPB$` | 60 |
| 863 | 07/03/2026 08:35:55 | high | `ES-SMB-003 File/share permission modified (4670)` | `WIN-EVGH6IS9JPB` | `WIN-EVGH6IS9JPB$` | 95 |
| 864 | 07/03/2026 08:35:56 | medium | `ES-AUTH-008 Special privileges assigned at logon (4672)` | `WIN-EVGH6IS9JPB` | `WIN-EVGH6IS9JPB$` | 70 |
| 865 | 07/03/2026 08:35:56 | medium | `ES-AUTH-004 Rapid IP change for same user` | `WIN-EVGH6IS9JPB` | `WIN-EVGH6IS9JPB$` | 70 |
| 866 | 07/03/2026 08:35:56 | medium | `ES-LAT-001 Network logon (4624 LogonType=3)` | `WIN-EVGH6IS9JPB` | `WIN-EVGH6IS9JPB$` | 70 |
| 867 | 07/03/2026 08:36:17 | medium | `ES-LAT-001 Network logon (4624 LogonType=3)` | `WIN-EVGH6IS9JPB` | `WIN-EVGH6IS9JPB$` | 70 |
| 868 | 07/03/2026 08:37:08 | medium | `ES-AUTH-004 Rapid IP change for same user` | `WIN-EVGH6IS9JPB` | `WIN-EVGH6IS9JPB$` | 70 |
| 869 | 07/03/2026 08:37:08 | medium | `ES-LAT-001 Network logon (4624 LogonType=3)` | `WIN-EVGH6IS9JPB` | `WIN-EVGH6IS9JPB$` | 70 |
| 870 | 07/03/2026 08:41:41 | medium | `ES-AUTH-007 Explicit credentials used (4648)` | `WIN-EVGH6IS9JPB` | `WIN-EVGH6IS9JPB$` | 70 |

## Event IDs observed and what they mean in this chain

| Event ID | Meaning in this case | Why it matters |
|---|---|---|
| `4624` | Successful logon | Used to prove anonymous access, Bobo access, machine-account access, and later privileged sessions |
| `4627` | Group membership information tied to logon | Supports the anonymous / session establishment cluster |
| `4648` | Explicit credentials used | Indicates credential material was supplied to a process for authentication |
| `4662` | Directory Service object access | In this set, the replication GUIDs make it strong DCSync evidence |
| `4663` | Object access | Here it shows `mimikatz.exe` touching `lsass.exe` |
| `4670` | Permissions on an object were changed | Matches ACL / permission abuse and is one of the strongest escalation indicators in the alert set |
| `4672` | Special privileges assigned at logon | Marks privileged logon sessions for `Bobo` and later `WIN-EVGH6IS9JPB$` |
| `4688` | New process created | Shows execution chain: WMI, cmd, net, net1, conhost, mimikatz |
| `4689` | Process ended | Present early in the timeline as part of the recon cluster |
| `4697` | Service installed | Persistence / remote execution indicator |
| `4698` | Scheduled task created | Persistence / remote execution indicator |
| `4768` | Kerberos TGT requested | Supports user / machine Kerberos auth activity and pre-roasting stages |
| `4769` | Kerberos service ticket requested | Key signal for Kerberoasting and later high-privilege ticket activity |
| `4776` | NTLM credential validation | Shows successful password validation for `j.smith` and `Bobo` |
| `5140` | Network share accessed | Early SMB reconnaissance |
| `5145` | Detailed share access check | Early anonymous SMB enumeration |

## Process execution chain observed

Visible suspicious / noteworthy processes:

- `C:\Windows\System32\wbem\WmiPrvSE.exe`
- `C:\Windows\SysWOW64\cmd.exe`
- `C:\Windows\SysWOW64\net.exe`
- `C:\Windows\SysWOW64\net1.exe`
- `C:\Windows\System32\conhost.exe`
- `C:\Tools\x64\mimikatz.exe`
- `C:\ProgramData\Microsoft\Windows Defender\Platform\4.18.26010.5-0\MpCmdRun.exe`
- `C:\Windows\System32\taskhostw.exe`
- `C:\Windows\System32\LogonUI.exe`
- `C:\Windows\sqZWiSCg.exe` (parent of suspicious `cmd.exe` execution)
- `C:\Windows\GUvaKgMe.exe` (parent of suspicious `cmd.exe` execution)

## Attack-path correlation to the scenario steps

### 1. Network reconnaissance / service enumeration
**Evidence**
- `4624` / `4627` / `5140` / `5145` with `ANONYMOUS LOGON`
- Source IP `192.168.1.13`

**Detection**
- Alert `856` (`ES-LAT-001`)

### 2. Username / account discovery and Kerberos abuse
**Evidence**
- `4768` for `j.smith`
- `4769` RC4 service tickets for `Bobo`, `vagran`, `j.smith`

**Detection**
- Alert `858` (`ES-AD-001 Kerberoasting indicator (4769 RC4)`)

### 3. Password cracking / credential validation
**Evidence**
- `4776` success for `j.smith` from workstation `kali`
- `4776` success for `Bobo`

**Detection correlation**
- Leads directly into `4624` network logon for `Bobo`

### 4. Service account compromise
**Evidence**
- `4624` successful NTLM logon as `Bobo` from `192.168.1.13`

**Detection**
- Alert `860` (`ES-LAT-001`)
- Alert `859` (`ES-AUTH-008`, privileged logon)

### 5. Remote execution / foothold
**Evidence**
- `4688` process chain (`cmd.exe`, `net.exe`, `net1.exe`, `WmiPrvSE.exe`)
- `4697` new service installed
- `4698` scheduled task created

**Detection**
- Alerts `861`, `862`

### 6. Credential dumping
**Evidence**
- `4688` for `C:\Tools\x64\mimikatz.exe`
- `4663` access to `lsass.exe` by `mimikatz.exe`

**Detection**
- No dedicated “mimikatz” alert is visible in the screenshots, but the raw events are conclusive.

### 7. ACL abuse / privilege escalation
**Evidence**
- `4670` high-risk permission modification alert
- Privileged logons with `4672`
- Follow-on admin-context execution and later `Administrator@LAB.LOCAL` ticket activity

**Detection**
- Alert `863` (`ES-SMB-003 File/share permission modified (4670)`) — strongest explicit escalation alert in the set
- Alerts `864`, `865`, `866`, `867`, `868`, `869`

### 8. DCSync
**Evidence**
- Burst of `4662` events with DS replication GUIDs at `08:36:59`

**Detection correlation**
- The screenshots do not show a dedicated DCSync-named alert.
- The correlation is analytic: `4662` + replication GUIDs + prior privilege-escalation context = strong DCSync evidence.

### 9. Domain-admin / late-stage privileged operations
**Evidence**
- `4769` service tickets for `Administrator@LAB.LOCAL` at `08:48:35` and `08:49:36`
- `4648` explicit credentials used at `08:41:41`

**Detection**
- Alert `870` (`ES-AUTH-007 Explicit credentials used (4648)`)

### 10. Golden-ticket persistence
**Evidence status**
- **Not directly evidenced in the screenshots.**
- The lab notes support this as the scenario end state, but the screenshot set does not show a definitive golden-ticket artifact such as forged-ticket-specific telemetry.

## What can be stated with high confidence

- The attacker source is `192.168.1.13`.
- The attacker used anonymous SMB/network access first.
- `j.smith` activity from `192.168.1.13` generated RC4 `4769` service-ticket requests consistent with Kerberoasting.
- Credentials for `Bobo` were successfully validated and then used for network logon.
- `mimikatz.exe` executed on the target.
- `mimikatz.exe` accessed `lsass.exe`.
- A new service and a scheduled task were created.
- Object permissions were modified (`4670`).
- DS replication-style `4662` events occurred with replication GUIDs, strongly consistent with DCSync.
- Later privileged activity involved `Administrator@LAB.LOCAL`.

## What is likely but not fully proven by the screenshots alone

- `vagran` is probably `vagrant` and is an OCR / rendering artifact.
- The scenario almost certainly reaches Domain Admin / DCSync / `krbtgt` compromise, but only DCSync is directly supported by the screenshots.
- Golden Ticket persistence is part of the exercise notes, but there is no direct screenshot proof of ticket forgery or pass-the-ticket in EchoSentinel.

## Concise attacker action list

1. Enumerated SMB / shares anonymously from `192.168.1.13`.
2. Requested Kerberos TGTs / service tickets for `j.smith`.
3. Requested RC4 service tickets for roastable targets (`Bobo`, `vagran`, `j.smith`).
4. Validated credentials via NTLM from workstation `kali`.
5. Authenticated successfully as `Bobo` from `192.168.1.13`.
6. Established execution on the target via service / WMI / command shell activity.
7. Ran `net.exe` / `net1.exe` for follow-on host / account manipulation.
8. Created a service and scheduled task.
9. Executed `mimikatz.exe`.
10. Accessed `lsass.exe`.
11. Modified permissions / ACLs (`4670`).
12. Performed DS replication-style access consistent with DCSync.
13. Used explicit credentials and later operated in `Administrator@LAB.LOCAL` context.
