"""Extract only explicitly labeled facts from a MapRequest.

No game/mod names are inferred from prose. Facts are accepted only through
explicit ``key: value`` fields so later resolution can use AssetIndex safely.
"""
from __future__ import annotations
import re
from sage_map_builder.planning.map_plan import MapGenerationPlan

_FIELD_RE = re.compile(r"(?im)^\s*(factions?|players?|constraints?|objective|هدف)\s*[:：]\s*(.+?)\s*$")


def _split(value: str) -> list[str]:
    return [item.strip() for item in re.split(r"[,،;؛]", value) if item.strip()]


def apply_explicit_facts(plan: MapGenerationPlan) -> MapGenerationPlan:
    """Return the same plan with only explicitly labeled facts added."""
    for key, value in _FIELD_RE.findall(plan.intent.description):
        normalized = key.casefold()
        if normalized in {"faction", "factions", "player", "players"}:
            for item in _split(value):
                if item not in plan.intent.factions:
                    plan.intent.factions.append(item)
        elif normalized in {"constraint", "constraints"}:
            for item in _split(value):
                if item not in plan.intent.constraints:
                    plan.intent.constraints.append(item)
        else:
            if value.strip() and value.strip() not in plan.intent.objectives:
                plan.intent.objectives.append(value.strip())
    plan.validate()
    return plan
