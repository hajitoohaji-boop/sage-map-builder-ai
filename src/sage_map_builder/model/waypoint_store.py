"""Waypoint collection operations for MapDocument."""
from __future__ import annotations
from .map_document import MapDocument
from .waypoint import Waypoint, validate_waypoint


def add_waypoint(document: MapDocument, waypoint: Waypoint) -> None:
    validate_waypoint(waypoint, document.dimensions.width, document.dimensions.height)
    if any(item.get("name") == waypoint.name for item in document.waypoints):
        raise ValueError(f"duplicate waypoint name: {waypoint.name}")
    document.waypoints.append({"name": waypoint.name, "x": waypoint.x, "y": waypoint.y, "z": waypoint.z})


def remove_waypoint(document: MapDocument, name: str) -> None:
    before = len(document.waypoints)
    document.waypoints[:] = [item for item in document.waypoints if item.get("name") != name]
    if len(document.waypoints) == before:
        raise KeyError(name)
