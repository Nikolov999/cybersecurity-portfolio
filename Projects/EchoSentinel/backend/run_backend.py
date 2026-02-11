import os
import uvicorn

if __name__ == "__main__":
    host = os.getenv("SENTINEL_HOST", "127.0.0.1")
    port = int(os.getenv("SENTINEL_PORT", "8345"))
    uvicorn.run("main:app", host=host, port=port, log_level="info")