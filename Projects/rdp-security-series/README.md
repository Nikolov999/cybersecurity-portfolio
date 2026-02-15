\# RDP Security Series  

\## End-to-End Detection Engineering, Remediation \& Validation



This project documents a complete offensive → defensive → engineering → validation cycle focused on securing Remote Desktop Protocol (RDP).



It demonstrates:



\- Realistic attack simulation  

\- Detection rule creation  

\- SIEM tuning (EchoSentinel)  

\- Hardening \& remediation  

\- Retest and validation  

\- Measurable security improvement  



This is not a theoretical write-up.  

Every phase was executed in a controlled lab and validated against real telemetry.



---



\# Project Architecture



Environment:



\- Attacker: Kali Linux VM  

\- Victim: Windows 8/10 VM (Bridged)  

\- Monitoring: EchoSentinel (custom-built SIEM)  

\- Network: Segmented lab (host + bridged VMs)  



Telemetry Sources:



\- Security Log (4624, 4625, 4648, 4672, 4740, etc.)

\- System Log (Service activity)

\- Sysmon (Process + command-line context)



---



\# Folder Overview



---



\# 01 – Detection \& Incident Response



Focus:

Offensive simulation and initial detection gaps.



Activities:



\- RDP brute force testing

\- Password spray simulation

\- Brute → successful login validation

\- Privileged RDP monitoring

\- Log analysis of:

&nbsp; - 4625 (Failed logon)

&nbsp; - 4624 (Successful logon)

&nbsp; - LogonType 10 (RemoteInteractive)



Findings:



\- Unlimited login attempts

\- No account lockout

\- Broad firewall exposure

\- No correlation detection

\- Weak visibility on admin RDP activity



Outcome:



Defined detection requirements for EchoSentinel rule engineering.



---



\# 02 – Remediation



Focus:

Hardening the RDP attack surface.



Controls Implemented:



\- Network Level Authentication (NLA)

\- TLS enforcement (SecurityLayer = 2)

\- Account lockout (5 attempts / 15 min)

\- Firewall restriction to management IP

\- Administrator account renaming

\- Event auditing enforcement



Security Impact:



\- Brute force viability reduced

\- Spray effectiveness limited

\- Remote exposure narrowed

\- Logging fidelity improved



Residual Risk Reduced:

Medium → Low



---



\# 03 – EchoSentinel Engineering



Focus:

Detection engineering and SIEM tuning.



Core Detection Packs Built:



Authentication \& Access:



\- ES-AUTH-001 – Brute force suspected

\- ES-AUTH-002 – Password spray

\- ES-AUTH-003 – RDP brute force (LogonType=10)

\- ES-AUTH-004 – Rapid IP change

\- ES-AUTH-005 – Privileged RDP logon

\- ES-AUTH-006 – First-seen user/IP

\- ES-AUTH-007 – Explicit credential usage (4648)

\- ES-AUTH-008 – Special privileges assigned (4672)



Correlation Layer:



\- ES-CORR-001 – Brute force → success (4625 → 4624)



Engineering Features Implemented:



\- Threshold-based detection

\- Severity-based suppression windows

\- Persistent baseline tables:

&nbsp; - User/IP

&nbsp; - User/Host

&nbsp; - Host/Host

\- Recurrence tracking (24h window)

\- Deterministic risk scoring model

\- MITRE ATT\&CK mapping



Tuning Applied:



\- Adjusted brute thresholds

\- Spray distinct-user logic refinement

\- Admin allowlisting

\- Suppression window calibration

\- Risk weight adjustments



Result:



\- High signal-to-noise ratio

\- Alert storms eliminated

\- Risk prioritization aligned with asset criticality

\- Fully explainable detection logic



---



\# 04 – Validation \& Retest



Focus:

Confirm detection + mitigation effectiveness.



Retest Scenarios:



1\. RDP brute force

2\. Password spray

3\. Brute → successful login

4\. Privileged RDP access

5\. New workstation login anomaly



Detection Verification:



\- All attack paths detected

\- Correlation fired correctly

\- Duplicate alerts suppressed

\- Risk scores adjusted dynamically

\- MITRE mapping confirmed



Mitigation Verification:



\- Account lockout triggered correctly

\- Firewall restrictions blocked unauthorized hosts

\- TLS enforced secure sessions

\- Default admin no longer bruteable



Measured Outcomes:



\- Detection accuracy: High

\- Noise level: Controlled

\- Correlation reliability: Confirmed

\- Risk prioritization: Effective

\- Exposure reduction: Significant



---



\# Security Improvements Achieved



Before:



\- Open RDP surface

\- Unlimited login attempts

\- No detection correlation

\- No anomaly tracking

\- Weak admin monitoring



After:



\- Rate-limited authentication

\- Account lockout enforcement

\- RDP brute detection

\- Password spray detection

\- Correlated compromise detection

\- Privileged session monitoring

\- Baseline anomaly detection

\- Risk-scored alert prioritization

\- Controlled alert suppression

\- Hardened remote access exposure



---



\# Detection Engineering Principles Applied



\- Deterministic logic over black-box scoring

\- Explicit thresholds

\- Transparent suppression model

\- Baseline persistence

\- Correlation layering

\- Risk contextualization (asset + privilege + anomaly)

\- MITRE-aligned mapping

\- Measurable validation through retest



---



\# Portfolio Value



This project demonstrates:



\- Offensive security understanding

\- Defensive engineering capability

\- SIEM rule creation

\- False positive tuning

\- Correlation design

\- Risk scoring implementation

\- Mitigation validation

\- End-to-end SOC workflow design



It reflects a Purple Team mindset:



Attack → Observe → Engineer → Harden → Retest → Measure.



---



\# Final Assessment



RDP attack surface: Hardened  

Detection coverage: Comprehensive  

Correlation: Functional  

False positives: Controlled  

Risk scoring: Context-aware  

Validation: Successful  



EchoSentinel validated against realistic RDP abuse scenarios in a controlled lab environment.



End-to-end lifecycle complete.

