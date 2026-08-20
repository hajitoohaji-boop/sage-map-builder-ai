"""Resolve explicit wave unit names against the real mod asset index."""
from __future__ import annotations

from sage_map_builder.mods.asset_index import AssetIndex
from sage_map_builder.planner.mission_plan import MissionPlan

_UNIT_KINDS = {"object", "unit", "aircraft", "vehicle", "infantry"}


def resolve_wave_assets(mission: MissionPlan, asset_index: AssetIndex) -> MissionPlan:
    """Validate every explicit wave unit against the loaded mod assets.

    Names are never rewritten or invented. An unknown name is reported in
    ``mission.unresolved`` when that field exists; otherwise a ValueError is
    raised so an invalid mission cannot silently reach the map writer.
    """
    unresolved: list[str] = []
    for wave_index, wave in enumerate(mission.waves):
        for unit_name in wave.units:
            asset = asset_index.find(unit_name)
            if asset is None or asset.kind not in _UNIT_KINDS:
                unresolved.append(f"wave[{wave_index}].unit:{unit_name}")

    if unresolved:
        if hasattr(mission, "unresolved"):
            mission.unresolved.extend(unresolved)  # type: ignore[attr-defined]
        raise ValueError("Unresolved wave assets: " + ", ".join(unresolved))

    return mission
