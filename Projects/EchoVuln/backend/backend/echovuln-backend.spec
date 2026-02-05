# echovuln-backend.spec

block_cipher = None

a = Analysis(
    ["run_backend.py"],
    pathex=["."],
    binaries=[],
    datas=[
        ("app", "app"),
    ],
    hiddenimports=[
        "sqlalchemy",
        "sqlalchemy.orm",
        "sqlalchemy.ext.declarative",
        "fastapi",
        "uvicorn",
        "pydantic",
        "app",
        "app.main",
        "app.db",
        "app.db.models",
        "app.core.security",
        "app.routers.keys",
        "app.core.auth",
        "app.core.config",
        "app.routers.os_snapshots",
        "app.routers.agents_enroll",
        "app.services.ingest_v2",
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="echovuln-backend",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name="echovuln-backend",
)
