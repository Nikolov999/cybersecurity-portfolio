\# Triage \& scoping



\## Initial signal

\- What drew attention: Unauthorized event detected on Wazuh.

\- Time window:Feb 3, 2026 @ 20:20:53



\## Questions answered

\- Which source IP accessed the share? 

* Source IP listed as 10.10.10.1 which makes it unreliable.
* Which account was used on the target host? Account not - listed only the alias WORKSTATION.



\## Scope

\- Affected hosts: Administrator(lab-win-client) and same user on Active Directory, lab-win-server.

\- Confirmed actions: Initial Access

\- Ruled out (persistence/extra hosts/data exfil):

