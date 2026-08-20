"""Convert explicit wave intent dictionaries into validated WavePlan objects."""
from __future__ import annotations

from sage_map_builder.planner.mission_plan import MissionPlan, WavePlan


def wave_intent_to_plan(mission: MissionPlan, waves: list[dict[str, object]]) -> MissionPlan:
    """Append only fully explicit waves; never infer owner, units, or delay.

    Required fields are ``owner`` and ``units``. ``delay_seconds`` is required
    as well so that a missing timing value cannot silently change gameplay.
    """
    converted: list[WavePlan] = []
    for index, raw in enumerate(waves):
        owner = raw.get("owner")
        units = raw.get("units")
        delay = raw.get("delay_seconds")
        if not isinstance(owner, str) or not owner.strip():
            raise ValueError(f"wave {index}: owner must be an explicit non-empty string")
        if not isinstance(units, (list, tuple)) or not units or not all(isinstance(x, str) and x.strip() for x in units):
            raise ValueError(f"wave {index}: units must be a non-empty list of explicit names")
        if isinstance(delay, bool) or not isinstance(delay, int) or delay < 0:
            raise ValueError(f"wave {index}: delay_seconds must be a non-negative integer")
        converted.append(WavePlan(owner=owner.strip(), units=tuple(x.strip() for x in units), delay_seconds=delay))

    mission.waves.extend(converted)
    mission.validate()
    return mission
