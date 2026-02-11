import logging
import re
from typing import Optional

LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s - %(message)s"


def setup_logging():
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)


_RE_LOGON_TYPE = re.compile(r"(?:Logon\s*Type|LogonType)\s*[:=]\s*(\d+)", re.IGNORECASE)
_RE_WORKSTATION = re.compile(r"(?:Workstation\s*Name|Source\s*Workstation)\s*[:=]\s*([^\r\n]+)", re.IGNORECASE)
_RE_TARGET_SERVER = re.compile(r"(?:Destination\s*Host|Target\s*Server|Computer)\s*[:=]\s*([^\r\n]+)", re.IGNORECASE)
_RE_TASK_NAME = re.compile(r"(?:Task\s*Name|TaskName)\s*[:=]\s*([^\r\n]+)", re.IGNORECASE)
_RE_SERVICE_NAME = re.compile(r"(?:Service\s*Name|ServiceName)\s*[:=]\s*([^\r\n]+)", re.IGNORECASE)
_RE_IMAGE = re.compile(r"(?:Image|Process\s*Name)\s*[:=]\s*([^\r\n]+)", re.IGNORECASE)
_RE_PARENT_IMAGE = re.compile(r"(?:Parent\s*Image|ParentImage)\s*[:=]\s*([^\r\n]+)", re.IGNORECASE)
_RE_COMMAND_LINE = re.compile(r"(?:Command\s*Line|CommandLine)\s*[:=]\s*([^\r\n]+)", re.IGNORECASE)
_RE_DLL_SIGNED = re.compile(r"(?:Signed|Signature\s*Status)\s*[:=]\s*(\w+)", re.IGNORECASE)
_RE_LOADED_IMAGE = re.compile(r"(?:ImageLoaded|Loaded\s*Image)\s*[:=]\s*([^\r\n]+)", re.IGNORECASE)
_RE_TARGET = re.compile(r"(?:Target\s*Server|TargetServer|Target\s*Machine)\s*[:=]\s*([^\r\n]+)", re.IGNORECASE)


def parse_int(regex: re.Pattern, raw: str) -> Optional[int]:
    if not raw:
        return None
    m = regex.search(raw)
    if not m:
        return None
    try:
        return int(m.group(1).strip())
    except Exception:
        return None


def parse_str(regex: re.Pattern, raw: str) -> Optional[str]:
    if not raw:
        return None
    m = regex.search(raw)
    if not m:
        return None
    s = (m.group(1) or "").strip()
    return s or None


def parse_logon_type(raw: str) -> Optional[int]:
    return parse_int(_RE_LOGON_TYPE, raw)


def parse_workstation(raw: str) -> Optional[str]:
    return parse_str(_RE_WORKSTATION, raw)


def parse_target(raw: str) -> Optional[str]:
    return parse_str(_RE_TARGET, raw) or parse_str(_RE_TARGET_SERVER, raw)


def parse_task_name(raw: str) -> Optional[str]:
    return parse_str(_RE_TASK_NAME, raw)


def parse_service_name(raw: str) -> Optional[str]:
    return parse_str(_RE_SERVICE_NAME, raw)


def parse_image(raw: str) -> Optional[str]:
    return parse_str(_RE_IMAGE, raw)


def parse_parent_image(raw: str) -> Optional[str]:
    return parse_str(_RE_PARENT_IMAGE, raw)


def parse_command_line(raw: str) -> Optional[str]:
    return parse_str(_RE_COMMAND_LINE, raw)


def parse_loaded_image(raw: str) -> Optional[str]:
    return parse_str(_RE_LOADED_IMAGE, raw)


def parse_signed_flag(raw: str) -> Optional[str]:
    v = parse_str(_RE_DLL_SIGNED, raw)
    return v.lower() if v else None


def contains_any(haystack: str, needles: list[str]) -> bool:
    h = (haystack or "").lower()
    return any(n.lower() in h for n in needles if n)