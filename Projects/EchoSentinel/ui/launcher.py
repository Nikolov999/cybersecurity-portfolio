import os
import sys
import time
import socket
import subprocess
from pathlib import Path

import requests
import webview


APP_TITLE = "EchoSentinel"
HOST = os.getenv("ECHOS_UI_HOST", "127.0.0.1")
PORT_START = int(os.getenv("ECHOS_UI_PORT", "8510"))
STREAMLIT_APP = os.getenv("ECHOS_UI_APP", "app.py")

STREAMLIT_ENV = {
    "STREAMLIT_BROWSER_GATHER_USAGE_STATS": "false",
    "STREAMLIT_SERVER_HEADLESS": "true",
    "STREAMLIT_SERVER_ENABLECORS": "false",
    "STREAMLIT_SERVER_ENABLEXSRFPROTECTION": "false",
    "STREAMLIT_GLOBAL_DEVELOPMENT_MODE": "false",
}


def pick_port(start: int) -> int:
    for p in range(start, start + 40):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.15)
            if s.connect_ex((HOST, p)) != 0:
                return p
    return start


def wait_http(url: str, timeout_s: int = 30) -> bool:
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        try:
            r = requests.get(url, timeout=1.0)
            if r.status_code < 500:
                return True
        except Exception:
            pass
        time.sleep(0.25)
    return False


def start_streamlit(app_path: Path, port: int) -> subprocess.Popen:
    env = os.environ.copy()
    env.update(STREAMLIT_ENV)

    cmd = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        str(app_path),
        "--server.address",
        HOST,
        "--server.port",
        str(port),
        "--server.fileWatcherType",
        "none",
        "--client.showSidebarNavigation",
        "false",
    ]

    creationflags = 0
    if os.name == "nt":
        creationflags = subprocess.CREATE_NO_WINDOW  # type: ignore[attr-defined]

    return subprocess.Popen(
        cmd,
        cwd=str(app_path.parent),
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL,
        creationflags=creationflags,
    )


def main():
    here = Path(__file__).resolve().parent
    app_path = (here / STREAMLIT_APP).resolve()

    port = pick_port(PORT_START)
    url = f"http://{HOST}:{port}"

    proc = start_streamlit(app_path, port)
    if not wait_http(url, timeout_s=35):
        try:
            proc.terminate()
        except Exception:
            pass
        raise SystemExit("EchoSentinel UI failed to start")

    window = webview.create_window(
        APP_TITLE,
        url,
        width=1280,
        height=820,
        min_size=(1100, 720),
        resizable=True,
        background_color="#000000",
    )

    def _cleanup():
        try:
            proc.terminate()
        except Exception:
            pass

    try:
        webview.start(gui="edgechromium", debug=False)
    finally:
        _cleanup()


if __name__ == "__main__":
    main()