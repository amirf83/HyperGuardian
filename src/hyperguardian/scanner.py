from __future__ import annotations

import ipaddress
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List

from .fingerprint import fingerprint_service


def _is_port_open(host: str, port: int, timeout: float) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except Exception:
        return False


def scan_host(host: str, ports: List[int], timeout: float) -> Dict:
    open_ports: List[int] = []
    services: Dict[str, dict] = {}
    for port in ports:
        if _is_port_open(host, port, timeout):
            open_ports.append(port)
            services[str(port)] = fingerprint_service(host, port)
    if not open_ports:
        return {}
    return {"ip": host, "open_ports": open_ports, "services": services}


def scan_network(cidr: str, ports: List[int], timeout: float, workers: int = 200) -> List[Dict]:
    network = ipaddress.ip_network(cidr, strict=False)
    hosts = [str(ip) for ip in network.hosts()]
    results: List[Dict] = []
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(scan_host, host, ports, timeout): host for host in hosts}
        for future in as_completed(futures):
            data = future.result()
            if data:
                results.append(data)
    return sorted(results, key=lambda item: item["ip"])
