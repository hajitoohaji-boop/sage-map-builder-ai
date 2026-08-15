"""Engine-owned map document model, independent of AI and World Builder."""

from __future__ import annotations

from dataclasses import dataclass, field

from sage_map_builder.mods.assets import NormalizedAsset
from sage_map_builder.planner.mission_plan import MissionPlan


@dataclass(frozen=True)
class MapObject:
    asset: NormalizedAsset
    owner: str
    x: float
    y: float
    z: float = 0.0


@dataclass(frozen=True)
class Waypoint:
    name: str
    x: float
    y: float
    z: float = 0.0


@dataclass
class MapDocument:
    title: str
    width: int
    height: int
    objects: list[MapObject] = field(default_factory=list)
    waypoints: list[Waypoint] = field(default_factory=list)
    mission: MissionPlan | None = None

    def validate(self) -> None:
        if self.width <= 0 or self.height <= 0:
            raise ValueError("map dimensions must be positive")
        if self.width % 64 or self.height % 64:
            raise ValueError("map dimensions must be multiples of 64")
        if not self.title.strip():
            raise ValueError("map title cannot be empty")
        waypoint_names = [point.name.casefold() for point in self.waypoints]
        if len(waypoint_names) != len(set(waypoint_names)):
            raise ValueError("duplicate waypoint name")
        for obj in self.objects:
            if not obj.owner.strip():
                raise ValueError("map object owner cannot be empty")
            if not (0 <= obj.x <= self.width and 0 <= obj.y <= self.height):
                raise ValueError(f"object outside map bounds: {obj.asset.name}")
        for point in self.waypoints:
            if not (0 <= point.x <= self.width and 0 <= point.y <= self.height):
                raise ValueError(f"waypoint outside map bounds: {point.name}")
        if self.mission is not None:
            self.mission.validate()
