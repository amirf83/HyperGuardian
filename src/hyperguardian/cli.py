from __future__ import annotations

import argparse
from datetime import datetime, timezone

from .report import build_report, write_report
from .scanner import scan_network
from .utils import parse_ports


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="hyperguardian", description="Agentless network audit MVP")
    sub = parser.add_subparsers(dest="command", required=True)

    scan = sub.add_parser("scan", help="Scan a CIDR for open ports and basic service banners")
    scan.add_argument("--cidr", required=True, help="CIDR to scan (e.g., 192.168.1.0/24)")
    scan.add_argument("--ports", required=True, help="Ports list (e.g., 22,80,443 or 1-1024)")
    scan.add_argument("--timeout", type=float, default=0.6, help="Socket timeout in seconds")
    scan.add_argument("--workers", type=int, default=200, help="Concurrent workers")
    scan.add_argument("--out", default="report.json", help="Output JSON report path")
    return parser


def run_scan(args: argparse.Namespace) -> int:
    ports = parse_ports(args.ports)
    if not ports:
        raise SystemExit("No ports provided")
    started_at = datetime.now(timezone.utc)
    hosts = scan_network(args.cidr, ports, args.timeout, args.workers)
    finished_at = datetime.now(timezone.utc)
    report = build_report(args.cidr, ports, hosts, started_at, finished_at)
    write_report(args.out, report)
    print(f"Scan finished. Report saved to {args.out}")
    return 0


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "scan":
        return run_scan(args)
    return 0
