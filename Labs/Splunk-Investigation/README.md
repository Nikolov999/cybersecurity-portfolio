# Brute-Force Detection in Splunk

**Goal:** Detect and respond to brute-force authentication attempts.

## Tools Used
- Splunk Enterprise  
- Sysmon  
- Windows Security Logs  

## Steps
1. Built an index for `wineventlog:security` and parsed Event ID 4625.
2. Created correlation searches to detect >5 failed logins in 2 minutes.
3. Set up a dashboard and triggered an alert for repeated IPs.

📸 **Dashboard Preview:**  
![splunk-dashboard](./dashboard-screenshot.png)

## Result
- Alert triggered successfully.
- Documented detection logic for SOC analysts.

