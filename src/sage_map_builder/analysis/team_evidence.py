"""Evidence model for observed World Builder teams."""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any

@dataclass(frozen=True)
class TeamEvidence:
    name: str
    owner: str | None = None
    singleton: bool | None = None
    production_priority: int | None = None
    unit_limits: tuple[int | None, ...] = ()
    max_instances: int | None = None
    description: str | None = None
    properties: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def normalize_observed_team(record: dict[str, Any]) -> TeamEvidence:
    if not record.get("name"):
        raise ValueError("observed team requires a name")
    limits = tuple(record.get("unit_limits") or ())
    return TeamEvidence(
        name=str(record["name"]), owner=record.get("owner"),
        singleton=record.get("singleton"),
        production_priority=record.get("production_priority"),
        unit_limits=limits,
        max_instances=record.get("max_instances"),
        description=record.get("description"),
        properties=dict(record.get("properties") or {}),
    )
