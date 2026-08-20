"""Resolve explicit placement templates against the real mod asset index."""
from __future__ import annotations

from sage_map_builder.mods.asset_index import AssetIndex
from .map_plan import MapGenerationPlan


def resolve_plan_placements(plan: MapGenerationPlan, asset_index: AssetIndex) -> MapGenerationPlan:
    """Reject unknown object templates before the map compiler runs.

    Waypoints are engine-level placements and are intentionally exempt from
    asset lookup. Every other placement must name an asset present in the
    loaded mod registry. No aliases or inferred objects are created here.
    """
    unresolved: list[str] = []
    for index, placement in enumerate(plan.placements):
        if placement.kind.casefold() == "waypoint":
            if not placement.template.strip():
                unresolved.append(f"placement[{index}].waypoint:")
            continue
        if asset_index.find(placement.template) is None:
            unresolved.append(f"placement[{index}].asset:{placement.template}")
        if placement.owner is not None and not placement.owner.strip():
            unresolved.append(f"placement[{index}].owner:")

    if unresolved:
        plan.unresolved.extend(unresolved)
        raise ValueError("Unresolved placements: " + ", ".join(unresolved))

    return plan
