# Remediation

## 1) Remove Unauthorized Local Admin
Ran on target (admin context):

- Remove user from local Administrators:
  - `net localgroup Administrators vagrant /delete`

## 2) Validate
- Confirm group membership:
  - `net localgroup Administrators`

## 3) Prevent Recurrence
- Enforce least privilege (no daily-driver admin accounts)
- Restrict WinRM to management subnet + strong auth
- Monitor + alert on 4732/4672 with baselines
