"""Core world-space models used independently of World Builder."""

from pydantic import BaseModel, ConfigDict, Field


class Vector3(BaseModel):
    """A position in SAGE world space."""

    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    x: float
    y: float
    z: float


class Waypoint(BaseModel):
    """A named mission waypoint."""

    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    name: str = Field(min_length=1)
    position: Vector3


class WorldObject(BaseModel):
    """A minimal engine-independent representation of a world object."""

    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    id: str = Field(min_length=1)
    template_name: str = Field(min_length=1)
    position: Vector3
    angle: float = 0.0
    owner: str | None = None
