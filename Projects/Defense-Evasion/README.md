# EchoSentinel  Defense Evasion & Log Tampering Case Study

## Overview
This repository presents a controlled lab simulation of coordinated defense evasion via WinRM remote access.

The scenario demonstrates:

- Remote privileged logon (4624 / 4672)
- Microsoft Defender configuration tampering (5007 / 5001)
- Audit policy modification (4719)
- Sysmon driver unload (telemetry degradation)
- Correlated detection via ES-DE-001 rule

This project validates behavioral correlation over single-event detection.

---

## Attack Chain Summary

1. WinRM Remote Logon (Type 3)
2. Privileged Token Assigned
3. Defender Configuration Drift
4. Audit Policy Change
5. Sensor Removal (SysmonDrv unload)

EchoSentinel correlates these events into a single high-severity alert.

---

## Repository Structure

- /evidence  Raw exported hunt data and screenshots
- /analysis  Timeline and event breakdown
- /detection  Rule logic and correlation explanation
- /remediation  Response strategy
- CASE_REPORT.md  Executive case summary
