# 🔍 Detecting RDP Brute-Force in Splunk

There’s something oddly satisfying about catching a brute-force attack in your logs — that exact moment when all those failed login attempts line up and the pattern clicks.  

This one focuses on **RDP brute-force** detection using Splunk. It’s one of those fundamental detections every SOC should have, but it’s also a perfect exercise to sharpen your log analysis mindset.

---

## 🧠 Thinking Like a Defender

When I approach any detection, I start by asking:
- *What behavior am I actually trying to catch?*
- *How does it look in the logs?*
- *And how can I translate that into something Splunk understands?*

For RDP brute-force, the behavior is simple — someone (or something) repeatedly tries to log into an account via Remote Desktop and fails.  
On Windows, that means a storm of **Event ID 4625** (Failed Logon) events, specifically with **LogonType 10** (remote interactive logon).

---

## 📊 Building the Detection

So the logic goes like this:  
> *Find accounts that have multiple failed logons from the same IP within a short window.*

In Splunk, that turns into something readable and logical:

```spl
index=wineventlog EventCode=4625 LogonType=10
| stats count as failed by Account_Name, IpAddress
| where failed > 5
| sort -failed

