"""Translate the currently supported MissionIntent fields into MissionPlan.

This adapter deliberately does not infer players, bases, waves, or scripts.
MissionIntent currently carries objectives, waves, and scripts; objectives are
safe to transfer directly, while the richer mission fields require explicit
schemas and asset resolution before they can be compiled.
"""
from __future__ import annotations

from sage_map_builder.planner.mission_plan import MissionPlan
from sage_map_builder.planning.map_plan import MissionIntent


def mission_intent_to_plan(intent: MissionIntent, *, title: str = "Mission") -> MissionPlan:
    plan = MissionPlan(title=title)
    plan.objectives = list(intent.objectives)
    plan.validate()
    return plan
