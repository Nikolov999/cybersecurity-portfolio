# Project 4  HTTP Exfiltration (Noisy Variant)

Technique: HTTP exfil using certutil  
Target: LAB-WIN-CLIENT  
User: vagrant  
C2: http://192.168.1.13:8000

Telemetry validated:
- Security 4688
- Sysmon 1 (Process Create)
- Privileged Object Access
- Successful Logon (Type 3)
- HTTP outbound via certutil

Screenshots stored in /evidence
