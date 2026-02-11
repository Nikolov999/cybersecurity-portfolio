from fastapi import FastAPI
from .db import Base, engine
from .api import router
from .utils import setup_logging

setup_logging()

app = FastAPI(title="EchoSentinel Backend", version="1.0.0")

Base.metadata.create_all(bind=engine)

app.include_router(router)