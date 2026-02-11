# IMPORTANT:
# - Backend binds to 0.0.0.0 (listen on all interfaces)
# - Agent must CONNECT to a real address (loopback for same PC, or the backend PC's LAN IP/DNS)
# Set BACKEND_HOST to the backend machine's reachable IP or DNS name.
$env:BACKEND_HOST = "127.0.0.1"

$env:SENTINEL_AGENT_BACKEND_URL = "http://$env:BACKEND_HOST`:8345"
$env:SENTINEL_AGENT_API_KEY = "CHANGE_ME_LONG_RANDOM"
$env:SENTINEL_AGENT_POLL_SECONDS = "5"
$env:SENTINEL_AGENT_CHANNELS = "Security,Microsoft-Windows-Sysmon/Operational"
$env:SENTINEL_AGENT_EVENT_IDS = "4624,4625,4634,4697,4698,1"

python -m sentinel_agent.main