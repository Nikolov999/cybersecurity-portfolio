## Executive summary
A Windows host exposed an SMB share with overly broad permissions. A plaintext credential file on the share was accessed and those credentials were reused to authenticate to a second host and execute a single remote command.

**Key point:** No single alert was sufficient; confidence emerged through temporal correlation and contextual reasoning.

## Impact
- Credentials exposed and reused
- Remote execution proof on one host
- Primary risk: lateral movement potential

## Root cause
Misconfigured SMB share permissions and insecure secret handling (plaintext creds stored on share).

## High-level response
- Disabled/rotated exposed creds
- Restricted share permissions (Share + NTFS)
- Verified scope limited to single target
