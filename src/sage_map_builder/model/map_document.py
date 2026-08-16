"""Neutral internal model for a Generals/Zero Hour map.

Unknown binary fields remain opaque; this model is not a guess-based parser.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class MapDimensions:
    width: int | None = None
    height: int | None = None


@dataclass(frozen=True)
class MapRegion:
    start: int
    end: int
    source: str


@dataclass
class MapDocument:
    file_name: str
    raw_size: int
    dimensions: MapDimensions = field(default_factory=MapDimensions)
    regions: list[MapRegion] = field(default_factory=list)
    waypoints: list[dict[str, Any]] = field(default_factory=list)
    objects: list[dict[str, Any]] = field(default_factory=list)
    scripts: list[dict[str, Any]] = field(default_factory=list)
    opaque_sections: list[MapRegion] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": 1,
            "file_name": self.file_name,
            "raw_size": self.raw_size,
            "dimensions": {"width": self.dimensions.width, "height": self.dimensions.height},
            "regions": [r.__dict__ for r in self.regions],
            "waypoints": self.waypoints,
            "objects": self.objects,
            "scripts": self.scripts,
            "opaque_sections": [r.__dict__ for r in self.opaque_sections],
        }
