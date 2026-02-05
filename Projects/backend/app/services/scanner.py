import asyncio
import socket

COMMON_PORTS = {
    80: "http",
    443: "https",
    22: "ssh",
    21: "ftp",
    25: "smtp",
    3389: "rdp",
    3306: "mysql",
    8080: "http-alt",
}


def severity_for_port(port: int) -> str:
    if port in (21, 22, 3389):
        return "high"
    if port in (80, 443, 8080):
        return "medium"
    return "low"


def risk_score(ports: list[int]) -> int:
    score = 0
    for p in ports:
        if p in (21, 22, 3389):
            score += 30
        elif p in (80, 443, 8080):
            score += 10
        else:
            score += 5
    return min(score, 100)


async def scan_target(target: str):
    result = {
        "target": target,
        "resolved_ip": None,
        "ports": [],
        "services": [],
        "risk_score": 0,
        "tags": [],
    }

    try:
        result["resolved_ip"] = socket.gethostbyname(target)
    except Exception:
        pass

    ports_to_check = [21, 22, 80, 443, 3389, 8080]
    found_ports: list[int] = []

    for port in ports_to_check:
        try:
            conn = asyncio.open_connection(target, port)
            reader, writer = await asyncio.wait_for(conn, timeout=1)
            found_ports.append(port)
            writer.close()
            await writer.wait_closed()
        except Exception:
            pass

    services = []
    tags: list[str] = []

    for p in found_ports:
        services.append(
            {
                "port": p,
                "service": COMMON_PORTS.get(p, "unknown"),
                "severity": severity_for_port(p),
            }
        )

        if p in (21, 22, 3389):
            tags.append("remote-access")
        if p in (80, 443, 8080):
            tags.append("web")

    result["ports"] = found_ports
    result["services"] = services
    result["risk_score"] = risk_score(found_ports)
    result["tags"] = sorted(list(set(tags)))

    return result
