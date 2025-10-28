ATTACKER-DEFENDER LAB

Author: Bobo Nikolov
Date: 27-10-2025
Status: In Progress (Defender / SecurityOnion phase next)

---

- Objective
Build isolated attacker <> victim lab to demonstrate reconnaissance, initial access, execution, persistence, and privilege escalation — then add a defender (SecurityOnion) to capture telemetry and create detections.

- Architecture and Scope
"lab_attacker" - Kali Linux(Internal Network(labnet)/NAT)IP 10.10.10.10
"lab_victim" - Ubuntu Linux(Internal Network(labnet)/Internal Network(intnet))IP 10.10.10.20
"Network" - Internal Network only(Isolated)
"Snapshot" - Created before testing and reverted again for repeatability.

NOTE: All work is performed on my VM's only!

1. ENUMERATION 
(In linux terminal)Run:
nmap -sS -sV 10.10.10.20
(evidence/2025-10-27_05-52_AM_Screenshot_Enumeration_ .png)
