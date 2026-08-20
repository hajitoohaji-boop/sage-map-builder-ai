"""Compile the validated mission portion of a MapGenerationPlan.

Only already-structured mission dictionaries are accepted; this layer never
turns free prose into players, bases, waves, or units.
"""
from __future__ import annotations

from typing import Any

from sage_map_builder.planner.mission_plan import BasePlan, MissionPlan, PlayerPlan, WavePlan
from .map_plan import MapGenerationPlan


class MissionCompileError(ValueError):
    pass


def _required(data: dict[str, Any], key: str) -> Any:
    value = data.get(key)
    if value is None or (isinstance(value, str) and not value.strip()):
        raise MissionCompileError(f"mission field is required: {key}")
    return value


def compile_mission(plan: MapGenerationPlan, *, title: str | None = None) -> MissionPlan:
    """Build a MissionPlan from explicit structured mission facts in *plan*.

    The compiler intentionally does not infer players from prose. A player,
    base, or wave must already be represented as a structured dictionary.
    """
    mission_data = plan.mission
    mission = MissionPlan(title=title or plan.intent.title or "Generated Mission")
    mission.objectives.extend(mission_data.objectives or plan.intent.objectives)

    for raw in mission_data.scripts:
        kind = raw.get("kind")
        if kind == "player":
            mission.players.append(PlayerPlan(
                name=str(_required(raw, "name")),
                faction=str(_required(raw, "faction")),
            ))
        elif kind == "base":
            mission.bases.append(BasePlan(
                owner=str(_required(raw, "owner")),
                name=str(_required(raw, "name")),
                x=float(_required(raw, "x")),
                y=float(_required(raw, "y")),
            ))
        elif kind:
            raise MissionCompileError(f"unsupported structured mission kind: {kind}")

    for raw in mission_data.waves:
        owner = str(_required(raw, "owner"))
        units = raw.get("units")
        if not isinstance(units, (list, tuple)) or not units:
            raise MissionCompileError("wave units must be a non-empty list")
        delay = int(raw.get("delay_seconds", 0))
        if delay < 0:
            raise MissionCompileError("wave delay cannot be negative")
        mission.waves.append(WavePlan(owner=owner, units=tuple(map(str, units)), delay_seconds=delay))

    mission.validate()
    return mission
