"""Generate deterministic evidence JSON for a real .map sample.

Usage:
    python research/map_samples/collect_evidence.py "MY MAP.map" -o my-map-evidence.json

This command reads the actual bytes. It does not modify the source map and does
not assign semantic meaning to offsets.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from sage_map_builder.analysis.sample_evidence import sample_evidence_dict


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect evidence from one real SAGE map")
    parser.add_argument("map", type=Path)
    parser.add_argument("-o", "--output", type=Path, required=True)
    args = parser.parse_args()

    data = args.map.read_bytes()
    report = sample_evidence_dict(data, args.map.name)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
