# Remediation Plan — Active Directory Overpass-the-Hash + Delegation Abuse

## Immediate Actions

- Enforce strong controls around NTLM exposure, including local admin password randomization and credential isolation.
- Reduce or eliminate legacy NTLM where feasible.
- Review and minimize delegation, especially privileged accounts and sensitive services.
- Restrict remote service creation, PsExec-like execution paths, and admin share access.
- Protect domain replication permissions and monitor for privilege escalation on replication-capable accounts.

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
