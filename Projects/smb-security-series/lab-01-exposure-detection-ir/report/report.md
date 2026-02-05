# Credential Exposure via SMB Misconfiguration — Incident Report



## 1\. Executive summary

A Windows host exposed an SMB share with overly broad permissions. A plaintext credential file on the share was accessed and those credentials were reused to authenticate to a second host and execute a single remote command.

**Key point:** No single alert was sufficient; confidence emerged through temporal correlation and contextual reasoning.



## 2\. Impact

* Credentials exposed and reused
* Remote execution proof on one host
* Primary risk: lateral movement potential



## 3\. Root cause

* Misconfigured SMB permissions (Share + NTFS)
* Plaintext secrets stored on share



## 4\. Detection reality (no tuning)

* What fired: No alerts fired, Wazuh was on purpose in it's default mode. Events did show of Login, Privileges Assigned and Logoff.
* What didn't: Process creation (Psexec), Anonymous SMB login, SMB share being accessed on the share-host, or SMB file being downloaded from the share.
* Why: Wazuh by default isn't configured to show SMB shares status or access.



## 5\. Analyst reasoning

* Correlation chain:

  * SMB access (T0/T1)
  * New auth pattern (T2)
  * Remote execution proof (T3)

* Confidence statement:
  No single alert was sufficient; confidence emerged through temporal correlation and contextual reasoning.



## 6\. Response

* Containment: Disable exposed accounts, remove SMB shares access, review other systems for reuse.
* Recovery: Restraints matters the most, no full network shutdown or system reimage. The goal is containing the incident without causing full system shutdown.



## 7\. Lessons learned

Prevention:

* Remove plaintext secrets from shares
* Least privilege for Share + NTFS
* Access review for shared resources



COMING UP IN THE NEXT LAB OF THIS SERIES!!

