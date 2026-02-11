$env:SENTINEL_DB_PATH = "$(Resolve-Path .)\sentinel.db"
$env:SENTINEL_API_KEY = "CHANGE_ME_LONG_RANDOM"
$env:SENTINEL_HOST = "0.0.0.0"
$env:SENTINEL_PORT = "8345"
python -m uvicorn app.main:app --host $env:SENTINEL_HOST --port $env:SENTINEL_PORT