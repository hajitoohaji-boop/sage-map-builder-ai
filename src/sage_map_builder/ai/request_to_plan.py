"""Deterministic bridge from a natural-language request to a generation plan."""
from __future__ import annotations
from .request import MapRequest
from .request_parser import request_to_intent
from .mission_facts import extract_mission_facts
from sage_map_builder.planning.map_plan import MapGenerationPlan


def request_to_plan(request: MapRequest) -> MapGenerationPlan:
    """Build a plan from explicit facts only; never infer game assets."""
    intent = request_to_intent(request)
    facts = extract_mission_facts(request.text)
    if facts.get("factions"):
        intent.factions = list(facts["factions"])
    if facts.get("objectives"):
        intent.objectives = list(facts["objectives"])
    plan = MapGenerationPlan(intent=intent)
    if facts.get("objectives"):
        plan.mission.objectives = list(facts["objectives"])
    plan.validate()
    return plan
