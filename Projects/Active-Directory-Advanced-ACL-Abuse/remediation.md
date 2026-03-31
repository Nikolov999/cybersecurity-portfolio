# Remediation Plan — Active Directory Advanced ACL Abuse (WriteOwner on Domain Admins)

## Immediate Actions

- Audit ACLs on high-value objects, especially Domain Admins, Enterprise Admins, AdminSDHolder, and privileged OUs.
- Remove WriteOwner, WriteDACL, GenericAll, and equivalent rights from non-administrative principals.
- Use BloodHound/Argus-style attack-path analysis as a recurring control, not a one-time assessment.
- Enable protected groups monitoring and rapid approval workflows for membership changes.
- Revert unauthorized ACL modifications, re-evaluate inheritance settings, and rotate privileged credentials after containment.

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
