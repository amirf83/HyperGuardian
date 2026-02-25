from __future__ import annotations

from typing import Iterable, List


def parse_ports(ports: str) -> List[int]:
    cleaned = ports.replace(" ", "")
    if not cleaned:
        return []
    result: List[int] = []
    for item in cleaned.split(","):
        if "-" in item:
            start, end = item.split("-", 1)
            result.extend(range(int(start), int(end) + 1))
        else:
            result.append(int(item))
    return sorted(set(result))


def chunks(items: Iterable[str], size: int) -> Iterable[list[str]]:
    batch: list[str] = []
    for item in items:
        batch.append(item)
        if len(batch) >= size:
            yield batch
            batch = []
    if batch:
        yield batch
