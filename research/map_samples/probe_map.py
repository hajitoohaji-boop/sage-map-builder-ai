"""CLI binary probe for SAGE map samples.

This tool never modifies a sample. It emits deterministic JSON containing only
observed bytes and integer interpretations; semantic field names are deliberately
not guessed here.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import struct
from pathlib import Path


def probe(path: Path) -> dict[str, object]:
    data = path.read_bytes()
    words: list[dict[str, int]] = []
    limit = min(len(data), 512)
    for offset in range(0, limit - 3, 4):
        le = struct.unpack_from("<I", data, offset)[0]
        be = struct.unpack_from(">I", data, offset)[0]
        words.append({"offset": offset, "little_u32": le, "big_u32": be})
    markers = {}
    for marker in (b"EAR\x00", b"CkMp"):
        positions: list[int] = []
        start = 0
        while True:
            pos = data.find(marker, start)
            if pos < 0:
                break
            positions.append(pos)
            start = pos + 1
        markers[marker.decode("latin-1").replace("\x00", "\\0")] = positions
    return {
        "file": path.name,
        "size": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "first_32_hex": data[:32].hex(" "),
        "markers": markers,
        "u32_words_first_512": words,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("maps", nargs="+", type=Path)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()
    report = {str(path): probe(path) for path in args.maps}
    text = json.dumps(report, indent=2, ensure_ascii=False)
    if args.output:
        args.output.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
