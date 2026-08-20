"""Deterministic reporting for supported and unsupported mission intent."""
from __future__ import annotations

from dataclasses import dataclass
from sage_map_builder.planning.map_plan import MissionIntent


@dataclass(frozen=True)
class MissionGenerationReport:
    objectives: int
    waves: int
    scripts: int
    supported: bool
    blockers: tuple[str, ...]


def inspect_mission_intent(intent: MissionIntent) -> MissionGenerationReport:
    blockers: list[str] = []
    if intent.scripts:
        blockers.append("script intent has no deterministic MissionPlan representation")
    return MissionGenerationReport(
        objectives=len(intent.objectives),
        waves=len(intent.waves),
        scripts=len(intent.scripts),
        supported=not blockers,
        blockers=tuple(blockers),
    )
