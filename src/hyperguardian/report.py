from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Dict, List


def build_report(cidr: str, ports: List[int], hosts: List[Dict], started_at: datetime, finished_at: datetime) -> Dict:
    return {
        "meta": {
            "started_at": started_at.astimezone(timezone.utc).isoformat(),
            "finished_at": finished_at.astimezone(timezone.utc).isoformat(),
            "cidr": cidr,
            "ports": ports,
        },
        "hosts": hosts,
    }


def write_report(path: str, report: Dict) -> None:
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2)
        handle.write("\n")
