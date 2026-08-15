"""Root document model for the independent SAGE map engine."""

from pydantic import BaseModel, ConfigDict, Field

from .metadata import MapMetadata
from .world import Vector3, Waypoint, WorldObject


class MapDocument(BaseModel):
    """Complete in-memory representation of a map at the current stage."""

    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    metadata: MapMetadata
    waypoints: list[Waypoint] = Field(default_factory=list)
    objects: list[WorldObject] = Field(default_factory=list)

    def add_waypoint(self, waypoint: Waypoint) -> None:
        if any(item.name == waypoint.name for item in self.waypoints):
            raise ValueError(f"duplicate waypoint name: {waypoint.name}")
        self.waypoints.append(waypoint)

    def add_object(self, obj: WorldObject) -> None:
        if any(item.id == obj.id for item in self.objects):
            raise ValueError(f"duplicate object id: {obj.id}")
        self.objects.append(obj)

    @classmethod
    def empty(cls, title: str, width: int, height: int) -> "MapDocument":
        return cls(metadata=MapMetadata(title=title, width=width, height=height))


__all__ = ["MapDocument", "Vector3"]
