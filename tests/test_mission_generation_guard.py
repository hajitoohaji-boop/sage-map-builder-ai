import pytest

from sage_map_builder.planning.map_plan import MissionIntent
from sage_map_builder.planning.mission_generation_guard import validate_mission_generation_intent


def test_empty_scripts_are_allowed():
    validate_mission_generation_intent(MissionIntent())


def test_scripts_are_not_silently_dropped():
    with pytest.raises(ValueError, match="script generation is not supported"):
        validate_mission_generation_intent(MissionIntent(scripts=[{"name": "WAVE 1"}]))
