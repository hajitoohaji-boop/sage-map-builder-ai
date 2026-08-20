"""Deterministic extraction of explicit plan facts from a MapRequest.

This module intentionally extracts only facts that can be represented without
inventing game/mod semantics. Unknown natural-language requirements remain in
``unresolved`` for a later evidence-backed resolver.
"""
from __future__ import annotations
import re
from sage_map_builder.planning.map_plan import MapGenerationPlan, MapIntent
from .request import MapRequest
from .request_parser import detect_language

_OBJECTIVE_RE = re.compile(r"(?:objective|هدف)\s*[:：]\s*(.+)", re.IGNORECASE)


def request_to_plan(request: MapRequest) -> MapGenerationPlan:
    request.validate()
    language = detect_language(request.text) if request.language == "auto" else request.language
    dimensions = re.search(r"(?P<w>\d{2,3})\s*[x×]\s*(?P<h>\d{2,3})", request.text)
    width = int(dimensions.group("w")) if dimensions else 256
    height = int(dimensions.group("h")) if dimensions else 256
    objectives: list[str] = []
    match = _OBJECTIVE_RE.search(request.text)
    if match:
        objectives.append(match.group(1).strip())
    intent = MapIntent(
        title=request.hints.get("title", ""),
        width=width,
        height=height,
        description=request.text,
        objectives=objectives,
        constraints=[f"language:{language}"],
    )
    plan = MapGenerationPlan(intent=intent)
    plan.validate()
    return plan
