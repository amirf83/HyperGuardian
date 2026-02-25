# HyperGuardian

HyperGuardian is a lightweight, agentless network audit MVP designed for internal SME networks. It discovers hosts in a CIDR, scans selected TCP ports, fingerprints basic services (HTTP/SSH), and produces a JSON report.

## Features (MVP)
- Agentless TCP discovery on a CIDR
- Configurable port list
- Service fingerprinting (HTTP/SSH)
- JSON reporting with timestamps and scan metadata

## Install (local)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Quick start
```bash
hyperguardian scan --cidr 192.168.1.0/24 --ports 22,80,443 --out report.json
```

## Example output
```json
{
  "meta": {
    "started_at": "2026-02-25T12:00:00Z",
    "finished_at": "2026-02-25T12:01:10Z",
    "cidr": "192.168.1.0/24",
    "ports": [22, 80, 443]
  },
  "hosts": [
    {
      "ip": "192.168.1.10",
      "open_ports": [22, 80],
      "services": {
        "22": {"name": "ssh", "banner": "SSH-2.0-OpenSSH_8.2"},
        "80": {"name": "http", "banner": "HTTP/1.1 200 OK"}
      }
    }
  ]
}
```

## Notes
- This MVP avoids false positives by only reporting what is observed.
- Future steps: active vuln validation plugins and misconfiguration checks.