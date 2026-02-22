# Local Privilege Escalation Indicators

Behavior-focused privilege escalation validation as a continuation of:

1) SMB credential abuse (initial access / credential exposure)
2) WinRM lateral movement (remote PowerShell session)
3) Privilege consolidation on the target (this project)

This project avoids exploit PoCs and instead validates what a SOC actually detects:
- Group membership change to local Administrators (4732)
- Elevated token issuance (4672)
- Post-elevation privileged service/object activity (4673 / 4674)

## Lab Context

- Attacker: Kali (WinRM client)
- Target: Windows host
- Telemetry: Windows Security + WinRM + PowerShell logs ingested into EchoSentinel

## Attack Flow (High Level)

1. Establish WinRM session on target using compromised credentials
2. Baseline identity + groups + privileges (`whoami`, `whoami /groups`, `whoami /priv`)
3. Add user to local Administrators (privilege consolidation)
4. Re-logon / token refresh to materialize elevated privileges
5. Validate privileged activity via Security events:
   - 4732: local admin group modification
   - 4672: special privileges assigned to logon
   - 4673: privileged service called
   - 4674: privileged object access

## Evidence

| Step | Screenshot | What it shows |
|---|---|---|
| 1 | evidence/screenshots/01-winrm-logon.png | WinRM session established (post-lateral movement starting point) |
| 2 | evidence/screenshots/03-whoami.png | Baseline identity |
| 3 | evidence/screenshots/05-whoami-groups.png | Baseline group memberships |
| 4 | evidence/screenshots/06-whoami-priv.png | Baseline token privileges |
| 5 | evidence/screenshots/07-add-to-local-admins.png | Privilege consolidation action (add to local Administrators) |
| 6 | evidence/screenshots/08-verify-local-admins.png | Group membership verified |
| 7 | evidence/screenshots/09-verify-priv-after-elevation.png | Elevated token/privileges verified after refresh |
| 8 | evidence/screenshots/11-event-4674-privileged-object-access.png | Post-elevation privileged object access (4674) |
| 9 | evidence/screenshots/12-event-4673-privileged-service-called.png | Post-elevation privileged service invocation (4673) |

## Key Detection Logic (EchoSentinel)

- Alert when a non-baselined account is added to local Administrators (4732 / 4728/4729/4733 variants)
- Confirm elevation via 4672 for the same user/session
- Enrich with 4673/4674 to demonstrate active use of elevated rights

See: `detections/detection-pack.md`

## Remediation

Remove unauthorized admin membership and validate least-privilege.

See: `remediation/remediation.md`
