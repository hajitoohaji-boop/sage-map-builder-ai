"""Raw 32-bit header-word extraction; semantic meaning is intentionally unknown."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import struct
from pathlib import Path


@dataclass(frozen=True)
class HeaderWord:
    offset: int
    raw_hex: str
    little_u32: int
    big_u32: int


def extract_header_words(data: bytes, *, limit: int = 512) -> tuple[HeaderWord, ...]:
    if limit < 4:
        raise ValueError("limit must be at least 4")
    end = min(len(data), limit)
    end -= end % 4
    return tuple(
        HeaderWord(
            offset=offset,
            raw_hex=data[offset:offset + 4].hex(" "),
            little_u32=struct.unpack_from("<I", data, offset)[0],
            big_u32=struct.unpack_from(">I", data, offset)[0],
        )
        for offset in range(0, end, 4)
    )


def write_header_words(data: bytes, output: str | Path, *, limit: int = 512) -> None:
    words = extract_header_words(data, limit=limit)
    Path(output).write_text(
        json.dumps([asdict(word) for word in words], indent=2) + "\n",
        encoding="utf-8",
    )
