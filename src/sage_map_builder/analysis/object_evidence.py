"""Evidence records for observed map objects.

These records deliberately preserve observed values without assigning semantic
meaning that has not been proven by the source or a real map sample.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any

@dataclass(frozen=True)
class ObjectEvidence:
    template: str
    owner: str | None = None
    x: float | None = None
    y: float | None = None
    z: float | None = None
    angle: float | None = None
    health: float | None = None
    team: str | None = None
    unique_id: int | None = None
    properties: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def normalize_observed_object(record: dict[str, Any]) -> ObjectEvidence:
    if not record.get("template"):
        raise ValueError("observed object requires a template")
    return ObjectEvidence(
        template=str(record["template"]),
        owner=record.get("owner"),
        x=record.get("x"), y=record.get("y"), z=record.get("z"),
        angle=record.get("angle"), health=record.get("health"),
        team=record.get("team"), unique_id=record.get("unique_id"),
        properties=dict(record.get("properties") or {}),
    )
