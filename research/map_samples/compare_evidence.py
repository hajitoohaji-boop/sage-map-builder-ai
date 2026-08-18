"""Compare two deterministic real-map evidence reports.

No semantic labels are inferred from matching offsets. The report only shows
observations that are equal/different between the two samples.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def compare(left: dict, right: dict) -> dict:
    left_markers = {(row["label"], row["version"], row["offset"]): row for row in left["source_chunk_markers"]}
    right_markers = {(row["label"], row["version"], row["offset"]): row for row in right["source_chunk_markers"]}
    common = sorted(set(left_markers) & set(right_markers))
    return {
        "left": left["file"],
        "right": right["file"],
        "same_prefix_hex": left["prefix_hex"] == right["prefix_hex"],
        "same_ckmp_marker_offsets": [
            item["marker_offset"] for item in left["ckmp"]
            if item["marker_offset"] in {x["marker_offset"] for x in right["ckmp"]}
        ],
        "same_source_marker_records": [left_markers[key] for key in common],
        "common_source_marker_count": len(common),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare two map evidence JSON reports")
    parser.add_argument("left", type=Path)
    parser.add_argument("right", type=Path)
    parser.add_argument("-o", "--output", type=Path, required=True)
    args = parser.parse_args()

    left = json.loads(args.left.read_text(encoding="utf-8"))
    right = json.loads(args.right.read_text(encoding="utf-8"))
    result = compare(left, right)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
