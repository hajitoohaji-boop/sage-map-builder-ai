"""Deterministic compiler from a validated generation plan to MapDocument."""
from __future__ import annotations

from sage_map_builder.map.builder import add_asset_object, add_waypoint, build_document
from sage_map_builder.map.document import MapDocument
from sage_map_builder.mods.asset_index import AssetIndex
from sage_map_builder.planner.mission_plan import MissionPlan
from .map_plan import MapGenerationPlan
from .plan_validator import validate_plan


class PlanCompileError(ValueError):
    """Raised when a plan cannot be compiled without inventing mod data."""


def compile_plan(
    plan: MapGenerationPlan,
    *,
    asset_index: AssetIndex,
    mission: MissionPlan,
) -> MapDocument:
    issues = validate_plan(plan)
    errors = [issue for issue in issues if issue.level == "error"]
    if errors:
        raise PlanCompileError("; ".join(issue.message for issue in errors))
    if plan.unresolved:
        raise PlanCompileError("plan contains unresolved assets: " + ", ".join(plan.unresolved))

    document = build_document(
        title=plan.intent.title or plan.intent.description[:80] or "Generated Map",
        width=plan.intent.width,
        height=plan.intent.height,
        mission=mission,
        asset_index=asset_index,
    )
    for placement in plan.placements:
        if placement.kind.casefold() == "waypoint":
            add_waypoint(document, placement.template, placement.x, placement.y, placement.z)
            continue
        owner = placement.owner or "PlyrCivilian"
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
