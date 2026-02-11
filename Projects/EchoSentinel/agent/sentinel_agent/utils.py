import logging
import socket
from datetime import datetime, timezone

LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s - %(message)s"


def setup_logging():
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


def hostname() -> str:
    return socket.gethostname()


def utc_now() -> datetime:
    return datetime.now(timezone.utc)