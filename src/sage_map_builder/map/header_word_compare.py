"""Compare raw 32-bit header words without assigning semantic meanings."""

from __future__ import annotations

from dataclasses import asdict
import json
from pathlib import Path
from typing import Any

from .header_words import extract_header_words


def compare_header_words(left: bytes, right: bytes, *, limit: int = 512) -> list[dict[str, Any]]:
    a = extract_header_words(left, limit=limit)
    b = extract_header_words(right, limit=limit)
    by_offset = {word.offset: word for word in b}
    rows: list[dict[str, Any]] = []
    for word in a:
        other = by_offset.get(word.offset)
        if other is None:
            rows.append({"offset": word.offset, "status": "left_only", "left": asdict(word), "right": None})
            continue
        rows.append({
            "offset": word.offset,
            "status": "same" if word.raw_hex == other.raw_hex else "different",
            "left": asdict(word),
            "right": asdict(other),
            "little_difference": other.little_u32 - word.little_u32,
            "big_difference": other.big_u32 - word.big_u32,
        })
    left_offsets = {word.offset for word in a}
    for word in b:
        if word.offset not in left_offsets:
            rows.append({"offset": word.offset, "status": "right_only", "left": None, "right": asdict(word)})
    return rows


def write_header_comparison(left: bytes, right: bytes, output: str | Path, *, limit: int = 512) -> None:
    Path(output).write_text(
        json.dumps(compare_header_words(left, right, limit=limit), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
