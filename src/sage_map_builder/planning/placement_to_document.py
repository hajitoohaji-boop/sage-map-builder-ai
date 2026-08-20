"""Apply validated placement intents to the engine-owned MapDocument."""
from __future__ import annotations

from sage_map_builder.map.builder import add_asset_object, add_waypoint
from sage_map_builder.map.document import MapDocument
from sage_map_builder.mods.asset_index import AssetIndex
from sage_map_builder.planning.map_plan import PlacementIntent


def apply_placements(
    document: MapDocument,
    placements: list[PlacementIntent],
    *,
    asset_index: AssetIndex,
) -> MapDocument:
    """Apply placements in order; validation in the builder remains authoritative."""
    for placement in placements:
        if placement.kind.casefold() == "waypoint":
            add_waypoint(document, placement.template, placement.x, placement.y, placement.z)
        else:
            owner = (placement.owner or "").strip()
            if not owner:
                raise ValueError(f"placement owner is required: {placement.template}")
            add_asset_object(
                document,
                asset_index,
                placement.template,
                owner,
                placement.x,
                placement.y,
                placement.z,
            )
    document.validate()
    return document
