"""Deterministic construction helpers for MapDocument."""

from __future__ import annotations

from sage_map_builder.map.document import MapDocument, MapObject, Waypoint
from sage_map_builder.mods.asset_index import AssetIndex
from sage_map_builder.planner.mission_plan import MissionPlan


def build_document(
    *,
    title: str,
    width: int,
    height: int,
    mission: MissionPlan,
    asset_index: AssetIndex,
) -> MapDocument:
    """Create a validated empty document tied to the requested mission.

    Asset resolution is explicit: callers must resolve an asset through the
    supplied index before an object can be added. This prevents invented mod
    object names from silently entering the map.
    """
    document = MapDocument(title=title, width=width, height=height, mission=mission)
    document.validate()
    return document


def add_waypoint(document: MapDocument, name: str, x: float, y: float, z: float = 0.0) -> Waypoint:
    waypoint = Waypoint(name, x, y, z)
    document.waypoints.append(waypoint)
    document.validate()
    return waypoint


def add_asset_object(
    document: MapDocument,
    asset_index: AssetIndex,
    asset_name: str,
    owner: str,
    x: float,
    y: float,
    z: float = 0.0,
) -> MapObject:
    asset = asset_index.find(asset_name)
    if asset is None:
        raise KeyError(f"asset not found in loaded mod: {asset_name}")
    obj = MapObject(asset, owner, x, y, z)
    document.objects.append(obj)
    try:
        document.validate()
    except Exception:
        document.objects.pop()
        raise
    return obj
