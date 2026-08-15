"""Independent validation pass for map documents."""

from __future__ import annotations

from dataclasses import dataclass

from .document import MapDocument


@dataclass(frozen=True)
class ValidationIssue:
    code: str
    message: str


def validate_document(document: MapDocument) -> tuple[ValidationIssue, ...]:
    issues: list[ValidationIssue] = []
    try:
        document.validate()
    except ValueError as exc:
        issues.append(ValidationIssue("MAP_INVALID", str(exc)))
    return tuple(issues)


def require_valid(document: MapDocument) -> None:
    issues = validate_document(document)
    if issues:
        raise ValueError("; ".join(issue.message for issue in issues))
