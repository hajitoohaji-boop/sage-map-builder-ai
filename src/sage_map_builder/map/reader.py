"""Safe, evidence-preserving binary map reader."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .header_evidence import HeaderEvidence, extract_header_evidence
from .region_detection import ByteRegion, bounded_regions
from .header_words import HeaderWord, extract_header_words


@dataclass(frozen=True)
class MapReaderResult:
    file_name: str
    data: bytes
    header: HeaderEvidence
    header_words: tuple[HeaderWord, ...]
    regions: tuple[ByteRegion, ...]


class MapReader:
    """Read a .map as bytes without inventing semantic fields."""

    def read_bytes(self, data: bytes, file_name: str = "<memory>") -> MapReaderResult:
        header = extract_header_evidence(data)
        words = extract_header_words(data)
        regions = bounded_regions(data, list(header.ckmP_offsets))
        return MapReaderResult(file_name, data, header, words, regions)

    def read_file(self, path: str | Path) -> MapReaderResult:
        p = Path(path)
        return self.read_bytes(p.read_bytes(), p.name)
