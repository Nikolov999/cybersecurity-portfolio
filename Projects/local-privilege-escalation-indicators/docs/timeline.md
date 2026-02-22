# Timeline Notes 

This repo stores screenshots with clean names. The original capture time is preserved inside the screenshot content and/or original filenames.

Recommended write-up order:

1. WinRM access established (start of session)
2. Baseline: whoami /groups /priv
3. Privilege consolidation: add to local Administrators
4. Token refresh: reconnect / new session
5. Post-elevation behavior: 4673 (privileged service called) and 4674 (privileged object access)

Correlation rule for analysis:

* Prefer **Logon ID** matching between 4624/4672/4673/4674 over strict timestamp ordering.
