# AI-Phishing Analyzer (Prototype)

## Motivation

Phishing remains the most common and effective initial attack vector used by cybercriminals against individuals, companies, and critical infrastructure. Despite advancements in security tools, many organizations still fall victim to credential theft, financial fraud, and malware infections that begin with a single deceptive email. Traditional filtering solutions catch a large portion of these threats, but attackers continually evolve their techniques, leveraging social engineering, spoofed domains, and forged authentication headers to bypass defenses. The purpose of this prototype was to build an accessible, transparent, and extensible phishing detection system that combines AI-driven analysis with traditional security heuristics. By understanding how phishing attacks are constructed and evaluated, this project aims to provide both a practical defensive tool and a learning platform for anyone interested in cybersecurity, email forensics, or threat detection.

## This prototype app is an advanced AI-powered phishing detection system built for security research, demonstrations, and portfolio purposes.  
This prototype integrates:

- FastAPI backend  
- Transformer-based AI model (HuggingFace)  
- Custom heuristic engine (URLs, IP detection, TLD analysis, brand impersonation)  
- Email header authentication checks (SPF, DKIM, DMARC, Return-Path mismatch)  
- Streamlit frontend for analysis and visualization  
- Docker containerization  
- Optional Linux desktop launcher  

---

## Features

### AI Email Scoring
- Transformer-based text classification model  
- Scores emails from 0 to 100  
- Labels: "Likely Phishing" or "Likely Legit"

### Heuristic Engine
- Urgency and pressure-language detection  
- Raw IP URL detection  
- Suspicious TLD analysis (.xyz, .top, .click, etc.)  
- Brand impersonation checks (PayPal, Microsoft, Apple, etc.)  
- Suspicious sender-domain patterns  

### Header & Authentication Analysis
- SPF softfail/fail detection  
- DKIM failure detection  
- DMARC failure detection  
- Return-Path vs From-domain mismatch  
- Full raw-header processing  

### Streamlit Frontend
- Analyzer tab  
- Dashboard tab (analysis history + charts)  
- Raw Email tab (paste full email source)  

### Dockerized Deployment
- Complete application runs inside a single container  
- Exposes FastAPI (8000) and Streamlit UI (8501)  

### Optional Desktop Launcher (Linux)
- Start the analyzer like a standard application from your desktop  

---

# Project Folder Structure

```
AI-Phishing-Analyzer/
│
├── main.py                    # FastAPI backend
├── phishing_model.py          # AI + heuristics + header analysis
├── streamlit_app.py           # Streamlit UI
│
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker build file
├── .dockerignore              # Optional
│
├── analysis_history.jsonl     # Automatically generated log
│
├── start_phishing_detector.sh # Optional desktop launcher script
├── phishing-detector.desktop  # Optional GNOME launcher entry
│
└── README.md                  # Project documentation
```

---

# Installation

The prototype can be run in two different modes:

- Method A: Docker container (recommended)  
- Method B: Python virtual environment  

---

# Method A — Docker Deployment

### Install Docker (Ubuntu)

```bash
sudo apt update
sudo apt install -y docker.io
sudo systemctl enable --now docker
```

### Build the image

```bash
docker build -t phishing-detector .
```

### Run the container

```bash
docker run --rm -p 8000:8000 -p 8501:8501 phishing-detector
```

### Access the application

- Streamlit UI: http://127.0.0.1:8501  
- FastAPI: http://127.0.0.1:8000  

---

# Method B — Python Virtual Environment

### Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Run the backend

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Run the frontend

```bash
streamlit run streamlit_app.py --server.address 0.0.0.0 --server.port 8501
```

### Access UI

http://127.0.0.1:8501

---

# Analyzer

The "Analyzer" tab allows you to enter the mail's sender and body without looking for the message source.
It's results won't be as detailed as the ones when you use the raw email analyzer. Showing just breif message like:

- Risk score
- Display body link, if there is any

---

![Analyzer Tab](Projects/AI-Phishing-Analyzer-Prototype/Screenshots/Analyzer-Screenshot.png)

---

# Raw Email Analyzer

The "Raw Email" tab allows you to paste the complete message source (headers + body).  
This performs:

- SPF fail detection  
- DKIM fail detection  
- DMARC fail detection  
- Return-Path mismatch detection  
- Suspicious forwarding chain analysis  
- Full body + header scoring  

Example raw email:

```
Return-Path: <bounce-service@pp-security-alerts.com>
Received: from smtp4.shadow-host.net (185.199.221.55)
Authentication-Results: dkim=fail; spf=softfail; dmarc=fail
From: PayPal Support <no-reply@paypal.com>
Subject: URGENT: Unusual activity detected
Content-Type: text/html

<a href="http://185.199.221.55/paypal/verify/login">CLICK HERE TO VERIFY</a>
```

---

![Raw Email Example](Projects/AI-Phishing-Analyzer-Prototype/Screenshots/Raw-Email-Screenshot-1.png)

---

![Raw Email Example](Projects/AI-Phishing-Analyzer-Prototype/Screenshots/Raw-Email-Screenshot-2.png)

---

# Dashboard

The dashboard provides:

- Recent analysis entries  
- Score distribution chart  
- Timeline of previous scans  
- Sender and subject history  

History is saved in:

```
analysis_history.jsonl
```
---

![Dashboard](Projects/AI-Phishing-Analyzer-Prototype/Screenshots/Dashboard-Screenshot.png)

---

# Architecture Overview

```
         +------------------------+
         |      Streamlit UI      |
         | Analyzer / Dashboard   |
         | Raw Email Viewer       |
         +------------+-----------+
                      |
                      | HTTP (JSON)
                      v
             +---------------------+
             |       FastAPI       |
             |     REST Backend    |
             +----------+----------+
                        |
               +--------+--------+
               |  phishing_model |
               |  AI + Heuristics|
               +-----------------+
               | Transformer     |
               | URL checks      |
               | TLD rules       |
               | Header checks   |
               +-----------------+
```

---

# Desktop Launcher (Optional)

### Start Script (start_phishing_detector.sh)

```bash
#!/bin/bash
APP_DIR="$HOME/phishing-detector"
cd "$APP_DIR" || exit 1

CONTAINER_NAME="phishing-detector-app"

if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
  docker run -d --name "$CONTAINER_NAME" -p 8000:8000 -p 8501:8501 phishing-detector
fi

xdg-open http://127.0.0.1:8501 >/dev/null 2>&1 &
```

### Desktop Entry (phishing-detector.desktop)

```ini
[Desktop Entry]
Type=Application
Name=AI-Phishing Analyzer (Prototype)
Exec=/home/USERNAME/start_phishing_detector.sh
Icon=utilities-terminal
Terminal=false
Categories=Utility;Security;
```

---

# Credits

This prototype was created collaboratively as a personal cybersecurity and AI learning project.

**Creator:**
- Bobo Nikolov (project owner, developer, tester)

---

# Notes

This project is intended as a prototype and should not be used in production environments without further security hardening, model fine-tuning, and integration testing. After I implement and configure all these I will make a link that you guys can only curl and have it downloaded on your own VM's or Host.

