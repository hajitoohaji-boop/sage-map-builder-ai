"""Deterministic JSON serialization for MapDocument."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any
from .map_document import MapDocument


def document_to_json(document: MapDocument) -> str:
    return json.dumps(document.to_dict(), ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def write_document_json(document: MapDocument, path: str | Path) -> None:
    Path(path).write_text(document_to_json(document), encoding="utf-8")


def document_from_dict(data: dict[str, Any]) -> MapDocument:
    dimensions = data.get("dimensions", {})
    from .map_document import MapDimensions, MapRegion
    regions = [MapRegion(int(r["start"]), int(r["end"]), str(r["source"])) for r in data.get("regions", [])]
    opaque = [MapRegion(int(r["start"]), int(r["end"]), str(r["source"])) for r in data.get("opaque_sections", [])]
    return MapDocument(
        file_name=str(data["file_name"]),
        raw_size=int(data["raw_size"]),
        dimensions=MapDimensions(dimensions.get("width"), dimensions.get("height")),
        regions=regions,
        waypoints=list(data.get("waypoints", [])),
        objects=list(data.get("objects", [])),
        scripts=list(data.get("scripts", [])),
        opaque_sections=opaque,
    )


def read_document_json(path: str | Path) -> MapDocument:
    return document_from_dict(json.loads(Path(path).read_text(encoding="utf-8")))
