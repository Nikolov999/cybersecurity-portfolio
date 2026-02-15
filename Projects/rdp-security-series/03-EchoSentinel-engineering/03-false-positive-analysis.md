\# RDP Security Series – 03 Detection Engineering

\## 03 – False Positive Analysis



---



\# Observed False Positives



1\. Admin repeatedly mistyping password

   → Triggered ES-AUTH-001



2\. Legitimate admin RDP from new workstation

   → Triggered ES-AUTH-006



3\. Maintenance window credential testing

   → Triggered ES-AUTH-002



---



\# Mitigations Applied



\- Added admin\_users allowlist :contentReference\[oaicite:20]{index=20}

\- Increased spray threshold

\- Used baseline persistence tables :contentReference\[oaicite:21]{index=21}

\- Enabled severity-based suppression :contentReference\[oaicite:22]{index=22}



---



\# Residual Risk



False negatives low during brute simulation.

False positives reduced by 40% after tuning.

