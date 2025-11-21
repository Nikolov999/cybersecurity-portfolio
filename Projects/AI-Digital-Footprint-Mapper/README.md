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

![YAML Scanning]()
![YAML Scanning]()

---

### Internal Network Scanning

The application integrates Nmap to scan internal or lab networks. Results are automatically converted into assets, such as:

- Hosts

- Open ports

- Services

- Versions

This provides real-time visibility into internal exposure.

![Network-Mapper]()
![Network-Mapper]()

---

### Assistant Panel 

The llm_client.py module serves as the communication backbone between the application and its integrated large language model. Designed with simplicity and modularity in mind, this file abstracts away all of the networking details required to interact with a locally hosted LLM through the Ollama runtime. Rather than embedding API logic throughout the codebase, the application relies on this single, isolated module to send prompts and receive model-generated responses.

At its core, the module defines a lightweight function named call_llm, which accepts a text prompt, packages it into an appropriate JSON payload, and sends it to the Ollama chat API endpoint via an HTTP POST request. The default configuration targets http://localhost:11434/api/chat and uses the llama3 model, though both the endpoint and model name can be easily swapped out without affecting the rest of the application. This design choice allows the system to be flexible and future-proof: switching to a different model or even a different backend, such as LM Studio or OpenAI, can be accomplished simply by modifying this file alone.

The function also includes foundational error handling. Network issues, malformed responses, and unexpected conditions are all captured and raised as a custom exception, LLMError. This ensures that the GUI can cleanly report errors back to the user without crashing or exposing low-level stack traces. Because the GUI only needs to call a single function—rather than dealing with HTTP requests or JSON parsing—the higher-level application code remains clean, readable, and focused on user interaction and data visualization.

In practice, llm_client.py acts as the “voice” of the assistant portion of the software. Whenever the user asks a question, the application gathers contextual information (such as risk summaries or historical scan data), constructs a prompt, and passes it to the LLM through this module. The function then returns the model’s response as plain text, ready to be displayed in the assistant chat panel. The entire conversational workflow depends on this small but essential component.

In essence, llm_client.py is the glue that binds the analytical capabilities of the application with the generative reasoning power of a local LLM. By isolating the API communication logic into a dedicated module, the project gains clarity, extensibility, and reliability, while ensuring that all AI inference remains fully local and under the user’s control.

---

![Assistant-Example]()

---

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

---

### File Summary

footprint_gui.py
Main graphical user interface, risk filter controls, assistant panel, graph viewer, and history UI.

footprint_mapper.py
Asset graph engine, YAML loader, risk scoring logic, Nmap parser, and snapshot creator.

llm_client.py
Lightweight wrapper for communicating with a local Ollama model through its chat API.

scan_history/
Automatically created directory where scan snapshots are stored as JSON files.

---

**Creator:**
- Bobo Nikolov (project owner, developer, tester)

---

### Intended Use:

- This project is intended for:

- Cybersecurity learning

- Lab experiments

- Internal footprint analysis

- Attack surface mapping

- Visualization and risk understanding

- AI-assisted security insight generation

All use should remain inside controlled lab environments.
External or unauthorized scanning is not supported or endorsed.

