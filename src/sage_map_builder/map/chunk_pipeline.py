"""Connect evidence-based map regions to DataChunk probes."""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path

from sage_map_builder.formats.chunk_probe import ChunkProbe, probe_regions
from .reader import MapReader, MapReaderResult

@dataclass(frozen=True)
class ChunkPipelineResult:
    reader: MapReaderResult
    probes: tuple[ChunkProbe, ...]


def probe_map_bytes(data: bytes, file_name: str = "<memory>") -> ChunkPipelineResult:
    reader = MapReader().read_bytes(data, file_name)
    regions = [(r.start, r.end) for r in reader.regions]
    probes = probe_regions(data, regions)
    return ChunkPipelineResult(reader, probes)


def probe_map_file(path: str | Path) -> ChunkPipelineResult:
    p = Path(path)
    return probe_map_bytes(p.read_bytes(), p.name)
