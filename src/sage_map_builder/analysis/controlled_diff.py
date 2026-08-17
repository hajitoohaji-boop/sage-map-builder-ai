"""Controlled byte-level diff used for one-change map experiments."""
from __future__ import annotations
import hashlib


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
