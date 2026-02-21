# Configuration Changes



### Baseline vs Hardened State



---



## Authentication Controls



| Setting | Before | After |

|----------|---------|--------|

| Network Level Authentication | Disabled | Enabled |

| Security Layer | Negotiate | TLS |

| Account Lockout | Not Configured | 5 Attempts |



---



## Exposure Controls



| Setting | Before | After |

|----------|---------|--------|

| Firewall Scope | Any Source | Management IP Only |

| RDP Port | 3389 | 3389 (Restricted) |

| Administrator Account | Default | Renamed/Disabled |



---



## Service Configuration



Verify service state:



```powershell

Get-Service TermService


