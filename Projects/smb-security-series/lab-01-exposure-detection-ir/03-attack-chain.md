\# Attack chain 



\## Step 1 — Access exposed SMB share

\- Source: lab-attacker 10.10.10.10

\- Target: C:\\Creds\\creds.txt(Host:lab-win-client)

\- Outcome: directory listed + credential file read



\## Step 2 — Extract credentials

\- Credentials obtained from file creds.txt



\## Step 3 — Credential reuse

\- Target host: lab-win-server (10.10.10.50)

\- Auth mechanism: SMB

\- Evidence: Windows Security log / Wazuh alert



\## Step 4 — Remote execution proof

\- Mechanism: PsExec

\- Stopped here since condition was reached, further exploitation was unnecessary for the purpose of this lab.

