"""Compare probe JSON reports without assigning speculative field meanings."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def compare(left: dict, right: dict) -> dict:
    lw = {row["offset"]: row for row in left["u32_words_first_512"]}
    rw = {row["offset"]: row for row in right["u32_words_first_512"]}
    offsets = sorted(set(lw) & set(rw))
    equal = []
    different = []
    for offset in offsets:
        a, b = lw[offset], rw[offset]
        item = {
            "offset": offset,
            "left_little_u32": a["little_u32"],
            "right_little_u32": b["little_u32"],
            "left_big_u32": a["big_u32"],
            "right_big_u32": b["big_u32"],
        }
        (equal if a == b else different).append(item)
    return {
        "left": left["file"],
        "right": right["file"],
        "same_u32_records": equal,
        "different_u32_records": different,
        "same_record_count": len(equal),
        "different_record_count": len(different),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("left", type=Path)
    parser.add_argument("right", type=Path)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()
    left = json.loads(args.left.read_text(encoding="utf-8"))
    right = json.loads(args.right.read_text(encoding="utf-8"))
    result = compare(left, right)
    text = json.dumps(result, indent=2, ensure_ascii=False)
    if args.output:
        args.output.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
