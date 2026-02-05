# Misconfiguration (root cause)

## SMB share
- Share host: lab-win-client (10.10.10.100)
- Share name: Creds
- Share permissions (before): <e.g., Everyone: Read>
- NTFS permissions (before): <e.g., Users/Everyone: Read>

## Secret exposure
- File name: <creds.txt>
- Location: C:\Creds\creds.txt
- Contains: *************(username) + ***********(password)

## Evidence pointers
- Permissions screenshots: evidence/share-host/screenshots/
- Notes: evidence/share-host/config-screens.md
