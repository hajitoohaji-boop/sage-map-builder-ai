"""Merge observed object/team/mission evidence into one report section."""
from __future__ import annotations
from typing import Any


def build_semantic_evidence(
    objects: list[dict[str, Any]] | None = None,
    teams: list[dict[str, Any]] | None = None,
    missions: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    return {
        "objects": list(objects or []),
        "teams": list(teams or []),
        "missions": list(missions or []),
        "verified": False,
        "interpretation_rule": "Observed records are preserved; semantic claims require independent source or binary verification.",
    }
