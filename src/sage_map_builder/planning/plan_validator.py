"""Deterministic validation for description-derived map plans."""
from __future__ import annotations
from dataclasses import dataclass
from .map_plan import MapGenerationPlan

@dataclass(frozen=True)
class ValidationIssue:
    level: str
    code: str
    message: str


def validate_plan(plan: MapGenerationPlan) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    try:
        plan.validate()
    except ValueError as exc:
        return [ValidationIssue("error", "INVALID_PLAN", str(exc))]
    seen: set[tuple[str, float, float, float]] = set()
    for item in plan.placements:
        key = (item.template, item.x, item.y, item.z)
        if key in seen:
            issues.append(ValidationIssue("error", "DUPLICATE_PLACEMENT", f"duplicate placement: {item.template}"))
        seen.add(key)
        if not (0 <= item.x <= plan.intent.width and 0 <= item.y <= plan.intent.height):
            issues.append(ValidationIssue("error", "OUT_OF_BOUNDS", f"placement outside map: {item.template}"))
    for entry in plan.unresolved:
        issues.append(ValidationIssue("warning", "UNRESOLVED", entry))
    return issues
