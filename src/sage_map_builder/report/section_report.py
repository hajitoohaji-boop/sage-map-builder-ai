"""Stable JSON section report produced from one MapReader result."""

from __future__ import annotations

from dataclasses import asdict
import json
from pathlib import Path
from typing import Any

from ..map.reader import MapReaderResult


def build_section_report(result: MapReaderResult) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "file": result.file_name,
        "file_size": len(result.data),
        "header": {
            "magic_hex": result.header.magic.hex(" "),
            "ckmp_offsets": list(result.header.ckmP_offsets),
        },
        "header_words": [asdict(word) for word in result.header_words],
        "regions": [
            {"start": r.start, "end": r.end, "size": r.size, "source": r.source}
            for r in result.regions
        ],
    }


def write_section_report(result: MapReaderResult, output: str | Path) -> None:
    Path(output).write_text(
        json.dumps(build_section_report(result), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
