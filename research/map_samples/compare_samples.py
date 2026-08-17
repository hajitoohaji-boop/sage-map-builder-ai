"""Deterministic cross-sample comparison without semantic guesses."""
from __future__ import annotations
import json
from pathlib import Path


def compare(left: dict, right: dict) -> dict:
    lw = left["u32_words_first_512"]
    rw = right["u32_words_first_512"]
    rows = []
    for a, b in zip(lw, rw):
        rows.append({
            "offset": a["offset"],
            "same": a == b,
            "left": a,
            "right": b,
        })
    return {
        "left": left["file"],
        "right": right["file"],
        "common_prefix_bytes": min(left["size"], right["size"]),
        "u32_comparison_count": len(rows),
        "same_u32_count": sum(r["same"] for r in rows),
        "different_u32_count": sum(not r["same"] for r in rows),
        "rows": rows,
        "shared_markers": {
            marker: sorted(set(left["markers"].get(marker, [])) & set(right["markers"].get(marker, [])))
            for marker in set(left["markers"]) | set(right["markers"])
        },
    }


def compare_files(left_path: Path, right_path: Path) -> dict:
    return compare(json.loads(left_path.read_text(encoding="utf-8")), json.loads(right_path.read_text(encoding="utf-8")))


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("left", type=Path)
    parser.add_argument("right", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = compare_files(args.left, args.right)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
