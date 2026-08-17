"""Deterministic marker scanner for binary samples.

It reports observations only; marker names have no semantic interpretation here.
"""
from __future__ import annotations
from dataclasses import asdict
from pathlib import Path
import hashlib
import json

DEFAULT_MARKERS = (b"EAR\x00", b"CkMp", b"MBar", b"WayP", b"SCPT")


def scan(data: bytes, markers=DEFAULT_MARKERS) -> dict:
    found = {}
    for marker in markers:
        positions = []
        start = 0
        while True:
            pos = data.find(marker, start)
            if pos < 0:
                break
            positions.append(pos)
            start = pos + 1
        found[marker.decode("ascii", errors="replace")] = positions
    return {"size": len(data), "sha256": hashlib.sha256(data).hexdigest(), "markers": found}


def scan_file(path: Path) -> dict:
    result = scan(path.read_bytes())
    result["file"] = path.name
    return result


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = {"samples": [scan_file(p) for p in args.files]}
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
