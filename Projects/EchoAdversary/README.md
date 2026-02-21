# EchoAdversary

**EchoAdversary** is a lab-focused **adversary simulation** tool designed for **purple-team validation**.

It executes controlled, repeatable technique simulations against a chosen target so you can verify:
- what telemetry is produced
- what detections fire (or don’t)
- how fast alerts arrive
- what evidence an analyst can pivot on inside **EchoSentinel**

This is **not** a real-world exploitation framework. It is a **signal generator** for defensive validation in isolated lab environments.

---

## Why It Exists

Most lab “attacks” are one-off scripts that prove nothing beyond “it worked once”.

EchoAdversary exists to make activity:
- **repeatable**
- **measurable**
- **comparable** across runs

Paired with EchoSentinel, you get a full loop:
- simulate → observe → detect → investigate → score

---

## Core Capabilities

- **Technique replay**: run the same simulation multiple times with consistent behavior
- **Target selection**: run against a chosen VM (IP/hostname) instead of only localhost
- **Evidence-first workflow**: produce artifacts that defenders can validate (auth, privilege, service creation, execution patterns)
- **Purple-team pairing**: validate outcomes in EchoSentinel (events, alerts, cases, validation tab)

---

## What It Simulates

EchoAdversary focuses on techniques that produce high-value defender telemetry.

Typical themes:
- Authentication patterns (success/failure bursts)
- Privileged session indicators
- Service creation / persistence-style artifacts
- SMB/RDP lateral movement patterns (lab-safe)

The goal is reliable telemetry for detection engineering, not “stealth”.

---

## Architecture

EchoAdversary is structured as:
- **UI layer** (operator control + scenario selection)
- **Engine layer** (scenario execution + safety checks)
- **Scenario modules** (each technique is its own module with clear inputs/outputs)
