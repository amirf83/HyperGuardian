from __future__ import annotations

import socket
import ssl
from typing import Optional


def _read_banner(sock: socket.socket, size: int = 256) -> str:
    sock.settimeout(1.5)
    try:
        data = sock.recv(size)
    except Exception:
        return ""
    return data.decode(errors="ignore").strip()


def fingerprint_ssh(host: str, port: int) -> Optional[str]:
    try:
        with socket.create_connection((host, port), timeout=1.5) as sock:
            banner = _read_banner(sock)
            return banner or None
    except Exception:
        return None


def fingerprint_http(host: str, port: int, use_tls: bool) -> Optional[str]:
    request = f"HEAD / HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
    try:
        if use_tls:
            context = ssl.create_default_context()
            with socket.create_connection((host, port), timeout=2) as sock:
                with context.wrap_socket(sock, server_hostname=host) as tls_sock:
                    tls_sock.sendall(request.encode())
                    banner = _read_banner(tls_sock, 512)
        else:
            with socket.create_connection((host, port), timeout=2) as sock:
                sock.sendall(request.encode())
                banner = _read_banner(sock, 512)
        return banner.split("\r\n")[0] if banner else None
    except Exception:
        return None


def fingerprint_service(host: str, port: int) -> dict:
    if port == 22:
        banner = fingerprint_ssh(host, port)
        return {"name": "ssh", "banner": banner} if banner else {"name": "ssh"}
    if port in {80, 8080}:
        banner = fingerprint_http(host, port, use_tls=False)
        return {"name": "http", "banner": banner} if banner else {"name": "http"}
    if port in {443, 8443}:
        banner = fingerprint_http(host, port, use_tls=True)
        return {"name": "https", "banner": banner} if banner else {"name": "https"}
    return {"name": "unknown"}
