# Remediation Plan — Active Directory gMSA Password Extraction Abuse

## Immediate Actions

- Review PrincipalsAllowedToRetrieveManagedPassword for every gMSA and reduce scope aggressively.
- Do not place gMSAs in Domain Admins or equivalent privileged groups.
- Separate service identity from administrative identity.
- Constrain where gMSAs can log on and which hosts may use them.
- Rotate exposed managed accounts and review downstream systems that trusted those accounts.

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
