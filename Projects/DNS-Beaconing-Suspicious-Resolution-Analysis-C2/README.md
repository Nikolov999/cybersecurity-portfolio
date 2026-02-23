# DNS Beaconing & Suspicious Resolution Analysis (C2)

## Overview

This project simulates DNS-based Command-and-Control (C2) beaconing behavior
and analyzes Windows DNS telemetry using EchoSentinel.

The objective is to detect periodic DNS resolution patterns
that resemble real-world C2 infrastructure communication.

---

## Lab Environment

- Target Host: lab-win-client
- DNS Resolver: 8.8.8.8
- Domain Used: echopentest.com
- Log Source: Microsoft-Windows-DNS-Client/Operational
- Optional: Sysmon Event ID 22

---

## Key Telemetry Observed

- Event ID 3006  DNS Query Issued
- Event ID 3008  Query Completed (Success)
- Event ID 3010  Query Failure
- Event ID 3018  Timeout Condition

Repeated queries occurred at ~510 second intervals,
demonstrating beacon-like periodic DNS activity.

See the evidence/ folder for screenshots.
