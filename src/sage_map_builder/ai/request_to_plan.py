"""Deterministic bridge from a natural-language request to a generation plan."""
from __future__ import annotations
from .request import MapRequest
from .request_parser import request_to_intent
from sage_map_builder.planning.map_plan import MapGenerationPlan


def request_to_plan(request: MapRequest) -> MapGenerationPlan:
    """Build only the facts explicitly extracted by the conservative parser.

    No factions, placements, objectives, scripts, waves, assets, or terrain are
    invented here. Such details must be supplied by a later evidence-backed
    planner or remain unresolved.
    """
    intent = request_to_intent(request)
    plan = MapGenerationPlan(intent=intent)
    plan.validate()
    return plan
