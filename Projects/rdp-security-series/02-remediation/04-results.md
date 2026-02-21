# RDP Security Series – 02 Remediation  

## 04 – Results



### Testing Methodology



- Brute-force simulation from attacker VM

- Credential spray attempt

- Privileged RDP session test

- Log validation via EchoSentinel



---



## Observed Improvements



### Before Hardening



- Unlimited login attempts

- Broad firewall exposure

- Default admin account active

- No account lockout enforcement



---



### After Hardening



| Control | Result |

|----------|--------|

| NLA | Blocks unauthenticated session creation |

| Account Lockout | Attacker blocked after 5 attempts |

| Firewall Restriction | External VM access denied |

| Admin Rename | Reduced automated attack success |

| TLS Enforcement | Secure channel enforced |



---



## Detection Improvements (EchoSentinel)



Events Observed:

- 4625 spikes during brute force

- 4740 (Account Lockout)

- 1149 connection attempts

- Correlated source IP detection



---



## Risk Reduction



- Brute force viability reduced

- Credential spray effectiveness minimized

- Lateral movement contained

- Logging visibility improved



---



## Overall Assessment



Residual Risk: Medium → Low  

Exposure Surface: Reduced  

Detection Capability: Enhanced  



Hardening successful.


