from sage_map_builder.planning.map_plan import MissionIntent
from sage_map_builder.planning.mission_generation_report import inspect_mission_intent


def test_report_allows_supported_mission_intent():
    report = inspect_mission_intent(MissionIntent(objectives=["defend"], waves=[{"owner": "USA"}]))
    assert report.supported is True
    assert report.objectives == 1
    assert report.waves == 1
    assert report.scripts == 0
    assert report.blockers == ()


def test_report_exposes_script_blocker():
    report = inspect_mission_intent(MissionIntent(scripts=[{"name": "wave"}]))
    assert report.supported is False
    assert report.scripts == 1
    assert report.blockers
