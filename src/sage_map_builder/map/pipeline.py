"""Deterministic binary-analysis pipeline for SAGE map samples."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .schema import BinarySpan, MapEvidence


@dataclass(frozen=True)
class MapProbeResult:
    path: str
    evidence: MapEvidence
    head: bytes


def probe_bytes(data: bytes, path: str = "<memory>") -> MapProbeResult:
    if not data:
        raise ValueError("map file is empty")
    magic = data[:4]
    marker = b"CkMp"
    offsets: list[int] = []
    start = 0
    while True:
        index = data.find(marker, start)
        if index < 0:
            break
        offsets.append(index)
        start = index + 1
    evidence = MapEvidence(len(data), magic, tuple(offsets))
    evidence.validate()
    return MapProbeResult(path, evidence, data[:512])


def probe_file(path: str | Path) -> MapProbeResult:
    file_path = Path(path)
    return probe_bytes(file_path.read_bytes(), str(file_path))


def common_canonical_offsets(*results: MapProbeResult) -> tuple[int, ...]:
    if not results:
        return ()
    common = set(results[0].evidence.ckmP_offsets)
    for result in results[1:]:
        common.intersection_update(result.evidence.ckmP_offsets)
    return tuple(sorted(common))
