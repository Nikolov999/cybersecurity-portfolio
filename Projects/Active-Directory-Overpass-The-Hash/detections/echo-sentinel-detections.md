# EchoSentinel Detection Notes — Active Directory Overpass-the-Hash + Delegation Abuse

## Detection Strategy

The detections below are written in a **platform-neutral** format so they can be adapted into EchoSentinel correlation rules, parsers, saved searches, or alert logic. I could not verify any public EchoSentinel rule syntax, so the content is intentionally portable rather than vendor-specific.

## Core Signals

- Look for Kerberos TGT requests that follow hash-based compromise indicators on the same identity or host.
- Alert on administrative SMB or service-creation activity from workstations that do not usually perform remote administration.
- Detect 4768/4769 patterns inconsistent with the account’s normal host affinity, service usage, or logon hours.
- Correlate DCSync indicators with prior lateral movement and privilege escalation events.
- Review delegation-related account changes and service-ticket patterns for high-value SPNs.

## Recommended Log Sources

- Windows Security
- Sysmon
- PowerShell Operational
- Windows Defender / EDR telemetry
- Directory Service logs on DCs
- Kerberos authentication logs from domain controllers

## Event Coverage

Typical Windows events worth correlating in this case study:

| Event ID | Why it matters |
|---|---|
| 4624 | Successful logon, including abnormal host-to-host access |
| 4648 | Explicit credential use |
| 4672 | Special privileges assigned at logon |
| 4688 | Suspicious process creation |
| 4662 | Directory object access, including replication abuse and ACL changes |
| 4728 / 4729 | Member added to / removed from privileged groups |
| 4732 / 4733 | Member added to / removed from local security-enabled groups |
| 4768 | Kerberos TGT requests |
| 4769 | Kerberos service ticket requests |
| 4776 | NTLM authentication validation |
| Sysmon 1 | Process creation |
| Sysmon 10 | Process access, useful for LSASS access detection |

## Example Correlation Ideas

### 1. Ticket/Authentication Anomaly
Trigger when:
- a low-frequency admin account suddenly generates multiple Kerberos events from a new host
- followed by remote logon or service creation on a server
- within a short correlation window

### 2. Privilege Escalation Chain
Trigger when:
- directory ACL changes or privileged group changes occur
- followed by privileged logons, replication access, or secrets dumping behavior
- from the same user or host

### 3. Replication Abuse
Trigger when:
- 4662 events contain replication-related access on a DC
- and the source is not an approved domain controller or sanctioned identity-management platform

### 4. Service Account Misuse
Trigger when:
- a service account or gMSA authenticates interactively
- or initiates remote admin activity from a workstation
- or appears in a host baseline where it does not normally execute

## Tuning Notes

- baseline admin workstations separately from user workstations
- maintain allowlists for legitimate replication platforms
- enrich accounts with tags such as `tier0`, `service_account`, `gmsa`, `sensitive`
- capture host role metadata so EchoSentinel can distinguish workstations from servers and DCs
- use suppression windows carefully; these attack chains often unfold in bursts

## Severity Guidance

| Condition | Suggested Severity |
|---|---|
| Single suspicious Kerberos anomaly | Medium |
| Kerberos anomaly + remote admin evidence | High |
| Privileged group change on protected object | High |
| DCSync from non-DC source | Critical |
| krbtgt-related compromise indicators | Critical |

## Analyst Triage Checklist

1. Confirm source host, account, and target system.
2. Determine whether the source host is approved for administration.
3. Review adjacent Kerberos, NTLM, process, and PowerShell events.
4. Check whether the user entered a privileged group or modified a protected object.
5. Contain the identity and host before broader credential hygiene actions.
