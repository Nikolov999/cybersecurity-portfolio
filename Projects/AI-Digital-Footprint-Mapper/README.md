# AI Digital Footprint Mapper

A desktop application for analyzing digital footprints, internal network exposure, and risk levels using a modern GUI and a local LLM (Ollama). The tool is designed for internal lab use, allowing safe experimentation, automated data enrichment, and security insights without sending any data to external services.

---

## Purpose

Modern organizations and individuals leave large digital footprints across domains, emails, social accounts, services, and network infrastructure. Understanding this footprint is critical for assessing exposure, identifying attack vectors, and improving security posture.

This application centralizes footprint analysis into a single workflow that integrates:

- YAML-based footprint ingestion

- Internal network scanning

- Risk scoring and attack surface analysis

- Historical comparison

- Graph visualization

- Local AI-driven recommendations

All processing runs locally inside an Ubuntu (Defender) VM, making it safe and suitable for experimentation.

---

## Key Features

### Digital Footprint Loading (YAML)

The application can load a YAML file describing:

- People

- Email accounts

- Domains

- Social accounts

- IP addresses

- Services

- Ownership and relationship mappings

The YAML file is parsed into an interconnected asset graph representing the digital footprint.

---

### Internal Network Scanning

The application integrates Nmap to scan internal or lab networks. Results are automatically converted into assets, such as:

- Hosts

- Open ports

- Services

- Versions

This provides real-time visibility into internal exposure.

### Risk Scoring Engine

A built-in heuristic model assigns a risk score to each asset based on:

- Service type

- Exposure level

- Authentication weakness

- Breach indicators

- Asset value

- Protocol age or insecurity

Assets receive:

- A score (0–100)

- A set of risk tags explaining the reasoning

- Graph Visualization

- A built-in graph viewer displays:

- Nodes for assets

- Edges representing relationships (ownership, hosting, usage)

- Node shapes by type

- Color-coded visualization for clarity

- Modern Dark Mode GUI

The interface includes:

- Asset table with filtering

- Risk threshold slider

- Service and asset type filters

- YAML loading tools

- Scan execution

- Graph view window

- Assistant panel

- Historical scan list

- Scan History and Time-Series Tracking

Each analysis or scan is saved as a JSON snapshot containing:

- Timestamp

- Source (YAML or Nmap)

- Asset count

- Average risk

- Maximum risk

### Asset summaries

The history viewer helps identify changes over time, such as new assets or increasing exposure.

Local LLM Assistant (Ollama)

The assistant uses a local LLM to provide insights such as:

- Highest-risk assets

- Changes between scans

- Summary of the attack surface

- Recommendations for hardening

- Identification of dangerous services

The assistant receives a structured summary of the current graph and scan history, ensuring fully local, offline operation.

### Requirements:
System Requirements:

- Ubuntu Linux (VM or host)

- Python 3.10+

- Tkinter

- Nmap

- Ollama installed locally

- Install system packages:
```bash 
sudo apt update
sudo apt install nmap python3-tk
```
- Python Dependencies

Install inside your virtual environment:
```bash
pip install matplotlib networkx pyyaml rich requests
```
Ollama (Local LLM)

Install Ollama:
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Pull a model (example):
```bash
ollama pull llama3
```

Ensure the server is running:
```bash
ollama serve
```
Running the Application

Launch the GUI with:
```bash
python3 footprint_gui.py
```

Use the interface to:

- Load YAML files

- Analyze configurations

- Run internal network scans

- Visualize graphs

- Ask questions through the assistant

- View and compare historical scans

### File Summary

footprint_gui.py
Main graphical user interface, risk filter controls, assistant panel, graph viewer, and history UI.

footprint_mapper.py
Asset graph engine, YAML loader, risk scoring logic, Nmap parser, and snapshot creator.

llm_client.py
Lightweight wrapper for communicating with a local Ollama model through its chat API.

scan_history/
Automatically created directory where scan snapshots are stored as JSON files.

Intended Use:

- This project is intended for:

- Cybersecurity learning

- Lab experiments

- Internal footprint analysis

- Attack surface mapping

- Visualization and risk understanding

- AI-assisted security insight generation

All use should remain inside controlled lab environments.
External or unauthorized scanning is not supported or endorsed.
