"""Small, non-semantic summary for a verified WaypointsList payload."""
from __future__ import annotations
from .waypoints_chunk import WaypointLink


def summarize_waypoint_links(links: list[WaypointLink]) -> dict[str, int]:
    return {"link_count": len(links)}
