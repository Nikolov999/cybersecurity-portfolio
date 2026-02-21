# Tuning Strategy



This section documents threshold tuning applied to reduce false positives during RDP attack simulation.



---



# Threshold Tuning



Defaults defined in settings: :contentReference[oaicite:11]{index=11}



| Rule | Default | RDP Lab Tuning |

|------|---------|----------------|

| brute_fail_threshold | 5 | Kept |

| brute_fail_window_seconds | 120 | Reduced to 90 |

| rdp_brute_fail_threshold | 3 | Kept |

| rdp_brute_window_seconds | 60 | Kept |

| spray_fail_threshold | 15 | Increased to 20 |

| spray_distinct_user_threshold | 6 | Kept |



Reason:

Reduce noise from lab password retries.



---



# Allowlisting



Admin users:

- admin_users_csv :contentReference[oaicite:12]{index=12}



4672 suppression:

- allow_4672_users_csv :contentReference[oaicite:13]{index=13}



Management IP tuning:

- management_ips_csv :contentReference[oaicite:14]{index=14}



---



# Suppression Windows



Low: 15 minutes  

Medium: 30 minutes  

High: 30 minutes :contentReference[oaicite:15]{index=15}



Prevents duplicate RDP brute alerts.



---



# Baseline-Based Tuning



BaselineUserIP :contentReference[oaicite:16]{index=16}  

BaselineUserHost :contentReference[oaicite:17]{index=17}  

BaselineHostPair :contentReference[oaicite:18]{index=18}  



Purpose:

Suppress expected admin workstation → server RDP traffic after first observation.



---



# Risk Adjustment



Risk computed via compute_risk(): :contentReference[oaicite:19]{index=19}



Boosts applied:

+15 if privileged user  

+10 if first_seen anomaly  

+5–10 if recurring  



Result:

RDP brute on critical server surfaces as high-risk immediately.



---




