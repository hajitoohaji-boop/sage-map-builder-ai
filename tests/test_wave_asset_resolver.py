from sage_map_builder.mods.asset_index import AssetIndex
from sage_map_builder.mods.assets import NormalizedAsset
from sage_map_builder.planner.mission_plan import MissionPlan, WavePlan, PlayerPlan
from sage_map_builder.planning.wave_asset_resolver import resolve_wave_assets


def test_resolves_explicit_unit_names_from_asset_index():
    assets = AssetIndex((
        NormalizedAsset(name="Crusader", kind="vehicle", source="test", properties={}),
    ))
    mission = MissionPlan(title="Test", players=[PlayerPlan(name="USA", faction="America")])
    mission.waves = [WavePlan(owner="USA", units=("Crusader",), delay_seconds=30)]
    assert resolve_wave_assets(mission, assets) is mission


def test_rejects_unknown_wave_unit():
    assets = AssetIndex(())
    mission = MissionPlan(title="Test", players=[PlayerPlan(name="USA", faction="America")])
    mission.waves = [WavePlan(owner="USA", units=("UnknownUnit",), delay_seconds=30)]
    try:
        resolve_wave_assets(mission, assets)
    except ValueError as exc:
        assert "UnknownUnit" in str(exc)
    else:
        raise AssertionError("unknown unit must be rejected")
