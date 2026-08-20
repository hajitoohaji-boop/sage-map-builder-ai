"""Conservative extraction of explicitly labeled mission facts."""
from __future__ import annotations
import re
from sage_map_builder.planner.mission_plan import MissionPlan, PlayerPlan, BasePlan, WavePlan

_FIELD = re.compile(r"(?im)^\s*(players?|players|players|factions?|bases?|waves?|objectives?|هدف|اللاعبون|الفصائل|القواعد|الموجات)\s*[:：]\s*(.+)$")

def _parts(value: str) -> tuple[str, ...]:
    return tuple(x.strip() for x in re.split(r"[,،;؛]", value) if x.strip())

def extract_mission_facts(text: str) -> dict[str, tuple[str, ...]]:
    facts: dict[str, tuple[str, ...]] = {}
    for match in _FIELD.finditer(text):
        key = match.group(1).casefold()
        value = _parts(match.group(2))
        if key in {"player", "players", "players", "اللاعبون"}:
            facts["players"] = value
        elif key in {"faction", "factions", "الفصائل"}:
            facts["factions"] = value
        elif key in {"base", "bases", "القواعد"}:
            facts["bases"] = value
        elif key in {"wave", "waves", "الموجات"}:
            facts["waves"] = value
        elif key in {"objective", "objectives", "هدف"}:
            facts["objectives"] = value
    return facts

def apply_explicit_mission_facts(plan: MissionPlan, facts: dict[str, tuple[str, ...]]) -> MissionPlan:
    players = facts.get("players", ())
    factions = facts.get("factions", ())
    if players and factions and len(players) == len(factions):
        plan.players = [PlayerPlan(name=p, faction=f) for p, f in zip(players, factions)]
    if facts.get("objectives"):
        plan.objectives = list(facts["objectives"])
    return plan
