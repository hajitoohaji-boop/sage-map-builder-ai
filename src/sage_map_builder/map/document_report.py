"""Deterministic, JSON-safe summary of a MapDocument before binary writing."""
from __future__ import annotations
from typing import Any
from .document import MapDocument


def document_summary(document: MapDocument) -> dict[str, Any]:
    document.validate()
    return {
        "title": document.title,
        "dimensions": {"width": document.width, "height": document.height},
        "objects": [
            {"asset": obj.asset.name, "owner": obj.owner, "x": obj.x, "y": obj.y, "z": obj.z}
            for obj in document.objects
        ],
        "waypoints": [
            {"name": point.name, "x": point.x, "y": point.y, "z": point.z}
            for point in document.waypoints
        ],
        "mission_present": document.mission is not None,
    }
