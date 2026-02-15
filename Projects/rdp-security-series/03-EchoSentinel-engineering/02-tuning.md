\# RDP Security Series – 03 Detection Engineering  

\## 02 – Tuning Strategy



This section documents threshold tuning applied to reduce false positives during RDP attack simulation.



---



\# Threshold Tuning



Defaults defined in settings: :contentReference\[oaicite:11]{index=11}



| Rule | Default | RDP Lab Tuning |

|------|---------|----------------|

| brute\_fail\_threshold | 5 | Kept |

| brute\_fail\_window\_seconds | 120 | Reduced to 90 |

| rdp\_brute\_fail\_threshold | 3 | Kept |

| rdp\_brute\_window\_seconds | 60 | Kept |

| spray\_fail\_threshold | 15 | Increased to 20 |

| spray\_distinct\_user\_threshold | 6 | Kept |



Reason:

Reduce noise from lab password retries.



---



\# Allowlisting



Admin users:

\- admin\_users\_csv :contentReference\[oaicite:12]{index=12}



4672 suppression:

\- allow\_4672\_users\_csv :contentReference\[oaicite:13]{index=13}



Management IP tuning:

\- management\_ips\_csv :contentReference\[oaicite:14]{index=14}



---



\# Suppression Windows



Low: 15 minutes  

Medium: 30 minutes  

High: 30 minutes :contentReference\[oaicite:15]{index=15}



Prevents duplicate RDP brute alerts.



---



\# Baseline-Based Tuning



BaselineUserIP :contentReference\[oaicite:16]{index=16}  

BaselineUserHost :contentReference\[oaicite:17]{index=17}  

BaselineHostPair :contentReference\[oaicite:18]{index=18}  



Purpose:

Suppress expected admin workstation → server RDP traffic after first observation.



---



\# Risk Adjustment



Risk computed via compute\_risk(): :contentReference\[oaicite:19]{index=19}



Boosts applied:

+15 if privileged user  

+10 if first\_seen anomaly  

+5–10 if recurring  



Result:

RDP brute on critical server surfaces as high-risk immediately.



---



