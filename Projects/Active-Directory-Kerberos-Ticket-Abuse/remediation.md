# Remediation Plan — Active Directory Kerberos Ticket Abuse

## Immediate Actions

- Tier administrative accounts and restrict where privileged tickets can exist.
- Disable unconstrained delegation and review delegation exposure across service accounts.
- Restrict and monitor WinRM, PowerShell remoting, and remote admin tooling.
- Harden LSASS with Credential Guard or equivalent protections.
- Audit replication permissions and remove DCSync-capable rights from non-essential principals.
- Rotate affected service-account passwords and reset krbtgt twice if ticket forgery risk is confirmed.

## Containment Priorities

1. Isolate affected hosts.
2. Disable or reset exposed accounts.
3. Invalidate compromised sessions and tickets.
4. Review group membership, delegation, ACLs, and replication rights.
5. Expand scope to adjacent systems touched by the same identities.

## Recovery Notes

- Resetting user passwords alone is not sufficient if Kerberos ticket material or replication secrets were exposed.
- If forged-ticket risk exists, perform a controlled **double reset of `krbtgt`** with change management and replication validation.
- Rebuild trust boundaries for any account that held administrative or replication-equivalent rights.

## Preventive Controls

- privileged access workstations for admin activity
- strong tiering between users, servers, and domain controllers
- gMSA and service-account least privilege
- continuous ACL review on privileged AD objects
- SIEM detections tied to authentication abuse, not only malware signatures
- regular attack-path analysis using tools such as BloodHound or Argus

## Metrics To Track

- count of principals with replication rights
- count of principals with WriteDACL / WriteOwner on privileged objects
- count of service accounts with interactive logon rights
- count of gMSAs with excessive password-reader scope
- time to detect and time to contain privileged-authentication anomalies
