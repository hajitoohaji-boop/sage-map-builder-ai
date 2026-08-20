"""Conservative request parser; it extracts only explicit dimensions/language."""
from __future__ import annotations
import re
from .request import MapRequest
from sage_map_builder.planning.map_plan import MapIntent

_DIMENSIONS = re.compile(r"(?P<w>\d{2,3})\s*[x×]\s*(?P<h>\d{2,3})")


def detect_language(text: str) -> str:
    return "ar" if re.search(r"[\u0600-\u06ff]", text) else "en"


def request_to_intent(request: MapRequest) -> MapIntent:
    request.validate()
    language = detect_language(request.text) if request.language == "auto" else request.language
    match = _DIMENSIONS.search(request.text)
    width = int(match.group("w")) if match else 256
    height = int(match.group("h")) if match else 256
    return MapIntent(
        title=request.hints.get("title", ""),
        width=width,
        height=height,
        description=request.text,
        constraints=[f"language:{language}"],
    )
