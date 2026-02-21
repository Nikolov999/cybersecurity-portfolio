# Rules Created (EchoSentinel)



This document lists every rule created and tuned specifically for RDP abuse detection.



All rules originate from EchoSentinel’s deterministic rule engine and correlation layer.



---



# PACK 1 – Authentication & RDP Abuse



---



## ES-AUTH-001  

Brute Force Suspected (4625 threshold)



Trigger:

- Event ID: 4625

- Same hostname

- Same username

- Same source_ip

- ≥ brute_fail_threshold within brute_fail_window_seconds



Threshold defaults:

- 5 failures within 120 seconds :contentReference[oaicite:0]{index=0}



MITRE:

- Credential Access – T1110



Severity:

- Medium



---



## ES-AUTH-002  

Password Spray Suspected



Trigger:

- Event ID: 4625

- Same source_ip

- ≥ 15 failures

- ≥ 6 distinct usernames

- Within 300 seconds :contentReference[oaicite:1]{index=1}



MITRE:

- Credential Access – T1110



Severity:

- High



---



## ES-AUTH-003  

RDP Brute Force (LogonType = 10)



Trigger:

- Event ID: 4625

- LogonType = 10 (RemoteInteractive)

- Same source_ip + username

- ≥ 3 failures within 60 seconds :contentReference[oaicite:2]{index=2}



MITRE:

- Credential Access – T1110



Severity:

- High



Purpose:

This is the primary RDP-focused brute-force detection.



---



## ES-AUTH-004  

Rapid IP Change for Same User



Trigger:

- Event ID: 4624

- Same username

- ≥ 2 distinct source IPs

- Within 600 seconds :contentReference[oaicite:3]{index=3}



MITRE:

- Defense Evasion – T1078



Severity:

- Medium (High if admin user)



---



## ES-AUTH-005  

Privileged User Network/RDP Logon



Trigger:

- Event ID: 4624

- LogonType 3 or 10

- Username in admin_users list :contentReference[oaicite:4]{index=4}



MITRE:

- Privilege Escalation – T1078



Severity:

- Medium



---



## ES-AUTH-006  

First-Seen Source IP for User



Trigger:

- Event ID: 4624

- BaselineUserIP table indicates first occurrence :contentReference[oaicite:5]{index=5}



MITRE:

- Credential Access – T1078



Severity:

- Low / Medium (if privileged)



Baseline persistence model:

BaselineUserIP table :contentReference[oaicite:6]{index=6}



---



## ES-AUTH-007  

Explicit Credentials Used (4648)



Trigger:

- Event ID: 4648

- Explicit credential usage detected



MITRE:

- Credential Access – T1078



Severity:

- Medium/High



---



## ES-AUTH-008  

Special Privileges Assigned (4672)



Trigger:

- Event ID: 4672

- User NOT in allow_4672_users list :contentReference[oaicite:7]{index=7}



MITRE:

- Privilege Escalation – T1068



Severity:

- Medium



---



# CORRELATION RULE



---



## ES-CORR-001  

Brute Force → Success (4625 → 4624)



Logic:

- ≥ 5 failures within 10 minutes

- Followed by successful 4624

- Same user + same source_ip :contentReference[oaicite:8]{index=8}



MITRE:

- Credential Access – T1110



Severity:

- High



Purpose:

Detects successful compromise after brute force.



---



# SUPPRESSION LOGIC



Severity-based suppression window:



- Low: 900 seconds

- Medium: 1800 seconds

- High: 1800 seconds :contentReference[oaicite:9]{index=9}



Prevents alert storms during active brute-force testing.



---



# RISK SCORING MODEL



Risk score derived from:



- Severity score

- Asset criticality

- Privileged user boost

- First-seen anomaly boost

- Recurrence factor :contentReference[oaicite:10]{index=10}



Ensures RDP compromise on critical server scores significantly higher than lab noise.




