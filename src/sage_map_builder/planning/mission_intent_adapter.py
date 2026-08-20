"""Translate validated mission intent into the engine MissionPlan without inference."""
from __future__ import annotations

from sage_map_builder.planner.mission_plan import MissionPlan, PlayerPlan
from sage_map_builder.planning.map_plan import MissionIntent


def mission_intent_to_plan(intent: MissionIntent, *, title: str = "Mission") -> MissionPlan:
    """Build only facts explicitly represented by MissionIntent.

    Placement-derived bases and waves remain untouched here; they require
    their concrete schemas and asset resolution before they can be compiled.
    """
    plan = MissionPlan(title=title)
    if intent.objectives:
        plan.objectives = list(intent.objectives)
    if intent.players:
        plan.players = [PlayerPlan(name=name, faction=faction) for name, faction in intent.players]
    plan.validate()
    return plan
