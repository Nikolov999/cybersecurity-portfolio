\# RDP Security Series – 03 Detection Engineering  

\## 04 – Results



---



\# Test Scenarios



1\. RDP brute force from Kali

2\. Password spray across multiple users

3\. Successful login after brute

4\. Admin lateral RDP

5\. First-seen workstation



---



\# Detection Coverage



| Attack | Rule Triggered | Result |

|--------|---------------|--------|

| RDP brute | ES-AUTH-003 | Detected |

| Spray | ES-AUTH-002 | Detected |

| Brute→Success | ES-CORR-001 | Detected |

| Admin RDP | ES-AUTH-005 | Detected |

| New workstation | ES-AUTH-006 | Detected |



---



\# Scoring Impact



Risk computation leveraged:



\- severity\_to\_score() :contentReference\[oaicite:23]{index=23}

\- compute\_risk() :contentReference\[oaicite:24]{index=24}



High-value server compromise generated risk\_score > 85.



---



\# Overall Outcome



Detection Accuracy: High  

Noise: Controlled  

RDP Abuse Visibility: Comprehensive  



EchoSentinel successfully validated against controlled RDP attack simulation.



---



