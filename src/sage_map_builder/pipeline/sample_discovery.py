"""Discover map samples without assigning semantic roles."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class MapSample:
    path: str
    size: int
    magic_hex: str
    valid_magic: bool


def discover_maps(root: str | Path, recursive: bool = True) -> tuple[MapSample, ...]:
    base = Path(root)
    paths = base.rglob("*.map") if recursive else base.glob("*.map")
    found: list[MapSample] = []
    for path in sorted(paths):
        if not path.is_file():
            continue
        data = path.read_bytes()
        found.append(MapSample(str(path), len(data), data[:4].hex(" "), data[:4] == b"EAR\0"))
    return tuple(found)
