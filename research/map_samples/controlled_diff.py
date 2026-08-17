"""Compare two map binaries for controlled-change experiments.

This tool intentionally reports byte-level changes only. It never infers a
semantic field from a changed offset.
"""
from __future__ import annotations
from pathlib import Path
import hashlib
import json


def diff_bytes(original: bytes, modified: bytes) -> dict:
    common = min(len(original), len(modified))
    changed = [i for i in range(common) if original[i] != modified[i]]
    added = list(range(common, len(modified))) if len(modified) > common else []
    removed = list(range(common, len(original))) if len(original) > common else []
    ranges = []
    for offsets in (changed, added, removed):
        if not offsets:
            continue
        start = prev = offsets[0]
        for offset in offsets[1:]:
            if offset != prev + 1:
                ranges.append({"start": start, "end": prev, "length": prev - start + 1})
                start = offset
            prev = offset
        ranges.append({"start": start, "end": prev, "length": prev - start + 1})
    return {
        "original_size": len(original),
        "modified_size": len(modified),
        "original_sha256": hashlib.sha256(original).hexdigest(),
        "modified_sha256": hashlib.sha256(modified).hexdigest(),
        "changed_byte_count": len(changed),
        "added_byte_count": len(added),
        "removed_byte_count": len(removed),
        "changed_ranges": ranges,
        "semantic_interpretation": None,
    }


def write_diff(original_path: Path, modified_path: Path, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    result = diff_bytes(original_path.read_bytes(), modified_path.read_bytes())
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
