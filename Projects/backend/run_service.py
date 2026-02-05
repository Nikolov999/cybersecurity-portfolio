import os
import sys
from pathlib import Path

def _fix_path():
    # PyInstaller: add folder containing executable to sys.path
    if getattr(sys, "frozen", False):
        base = Path(sys.executable).resolve().parent
        sys.path.insert(0, str(base))
    else:
        root = Path(__file__).resolve().parents[0]
        sys.path.insert(0, str(root))

_fix_path()

def main():
    os.environ.setdefault("PYTHONUNBUFFERED", "1")

    # Service-safe data dir override
    # Inno/NSSM will set ECHOEXPOSURE_DATA_DIR, but keep a fallback
    os.environ.setdefault("ECHOEXPOSURE_DATA_DIR",
        str(Path(os.environ.get("PROGRAMDATA", r"C:\ProgramData")) / "EchoPentest" / "EchoExposure" / "data")
    )

    import uvicorn
    from app.main import app

    uvicorn.run(app, host="127.0.0.1", port=9000, log_level="info")

if __name__ == "__main__":
    main()
