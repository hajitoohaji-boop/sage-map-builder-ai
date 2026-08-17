"""Cross-reference validation for the deterministic map domain model."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class ValidationIssue:
    severity: str
    code: str
    message: str
    reference: str | None = None


def validate_document(document) -> tuple[ValidationIssue, ...]:
    issues: list[ValidationIssue] = []
    waypoint_names = {w.get("name") for w in document.waypoints}
    object_ids = {o.get("object_id") for o in document.objects}
    script_names = {s.get("name") for s in document.scripts}

    for waypoint in document.waypoints:
        if not waypoint.get("name"):
            issues.append(ValidationIssue("error", "WAYPOINT_NAME", "Waypoint has no name"))
    for obj in document.objects:
        if not obj.get("object_id"):
            issues.append(ValidationIssue("error", "OBJECT_ID", "Object has no object_id"))
        if not obj.get("template"):
            issues.append(ValidationIssue("error", "OBJECT_TEMPLATE", "Object has no template", obj.get("object_id")))
    for script in document.scripts:
        if not script.get("name"):
            issues.append(ValidationIssue("error", "SCRIPT_NAME", "Script has no name"))
        for action in script.get("actions", []):
            args = action.get("args", {})
            waypoint = args.get("waypoint")
            if waypoint is not None and waypoint not in waypoint_names:
                issues.append(ValidationIssue("error", "UNKNOWN_WAYPOINT", f"Script references unknown waypoint: {waypoint}", script.get("name")))
            obj = args.get("object_id")
            if obj is not None and obj not in object_ids:
                issues.append(ValidationIssue("error", "UNKNOWN_OBJECT", f"Script references unknown object: {obj}", script.get("name")))
    return tuple(issues)
