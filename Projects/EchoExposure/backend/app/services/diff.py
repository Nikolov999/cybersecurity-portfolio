def diff_scans(old: dict, new: dict):
    added_ports = list(set(new.get("ports", [])) - set(old.get("ports", [])))
    removed_ports = list(set(old.get("ports", [])) - set(new.get("ports", [])))

    return {
        "added_ports": added_ports,
        "removed_ports": removed_ports
    }
