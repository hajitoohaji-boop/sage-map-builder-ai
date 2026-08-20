"""Guard mission generation against unsupported script intent."""
from __future__ import annotations

from sage_map_builder.planning.map_plan import MissionIntent


def validate_mission_generation_intent(intent: MissionIntent) -> None:
    """Reject script intent until a concrete MissionDocument script model exists.

    Waves can be compiled by ``wave_intent_adapter``. Script dictionaries cannot
    yet be represented by ``MissionPlan``/``MapDocument`` without inventing a
    schema, so generation must fail explicitly rather than silently dropping them.
    """
    if intent.scripts:
        raise ValueError(
            "mission script generation is not supported yet: "
            "script intent requires a concrete deterministic script model"
        )
