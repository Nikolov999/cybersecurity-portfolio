#  Network Traffic Analysis

**Goal:** Identify and investigate suspicious network activity captured in PCAP files.

##  Tools Used
- Wireshark  
- Zeek  
- VirusTotal (for domain/IP enrichment)

##  Scenario
A suspicious user workstation was reported for high outbound traffic. A network capture was taken for analysis.

##  Analysis Process
1. Loaded the PCAP into Wireshark and filtered by `tcp.stream eq 3` and `dns`.
2. Identified repeated connections to external IP `185.141.x.x` on port 4444.
3. Extracted payloads and analyzed Zeek logs for anomalies.
4. Used VirusTotal to confirm the domain was associated with known C2 infrastructure.

## ✅ Outcome
- Confirmed active beaconing pattern.
- Created a Splunk detection rule for similar traffic signatures.
- Recommended blocking IPs at the firewall.

📸 **Screenshots:**  
![pcap](./pcap-analysis.png)

