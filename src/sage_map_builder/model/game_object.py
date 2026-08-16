"""Neutral placed-object model for map editing."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class GameObject:
    object_id: str
    template: str
    x: float
    y: float
    z: float = 0.0
    owner: str | None = None

    def __post_init__(self) -> None:
        if not self.object_id.strip():
            raise ValueError("object_id must not be empty")
        if not self.template.strip():
            raise ValueError("template must not be empty")
        if not all(isinstance(v, (int, float)) for v in (self.x, self.y, self.z)):
            raise TypeError("object coordinates must be numeric")
