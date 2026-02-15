\# RDP Security Series – Detection Engineering (EchoSentinel)



This module documents how EchoSentinel was tuned to detect, correlate, and score RDP abuse scenarios.



---



\## Core Focus



\- RDP brute force detection

\- Password spray detection

\- Privileged RDP monitoring

\- Baseline anomaly detection

\- Brute→Success correlation



---



\## Architecture Components Used



\- Deterministic rule engine :contentReference\[oaicite:25]{index=25}

\- Correlation layer :contentReference\[oaicite:26]{index=26}

\- Baseline tables :contentReference\[oaicite:27]{index=27}

\- Risk scoring engine :contentReference\[oaicite:28]{index=28}

\- Threshold tuning via settings :contentReference\[oaicite:29]{index=29}



---



\## Evidence Stored



\- Raw Windows event logs (4624, 4625, 4648, 4672)

\- Alert records from alerts table :contentReference\[oaicite:30]{index=30}

\- Validation scenario run data

\- Risk score comparisons pre/post tuning

\- Screenshot of detection timeline

\- Correlation ID evidence for ES-CORR-001



---



\## Conclusion



EchoSentinel was tuned to provide deterministic, explainable, and risk-aware detection coverage for RDP abuse techniques aligned to MITRE ATT\&CK.



Portfolio-grade SOC validation complete.

