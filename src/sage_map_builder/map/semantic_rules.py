"""Conservative semantic checks for common map-header hypotheses."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


SemanticStatus = Literal["supported", "rejected", "unknown"]


@dataclass(frozen=True)
class SemanticCheck:
    name: str
    status: SemanticStatus
    reason: str


def check_dimension(value: int, *, minimum: int = 64, maximum: int = 512) -> SemanticCheck:
    """Check whether a raw integer is plausible as a SAGE map dimension.

    This is only a plausibility check. It never proves that the field is a
    width or height; that requires independent structural evidence.
    """
    if minimum <= value <= maximum and value % 64 == 0:
        return SemanticCheck("dimension", "supported", "value is within the supported range and is divisible by 64")
    return SemanticCheck("dimension", "rejected", "value does not satisfy the supported dimension constraints")


def check_dimension_pair(width: int, height: int) -> SemanticCheck:
    if check_dimension(width).status != "supported":
        return SemanticCheck("dimension_pair", "rejected", "width is not a supported dimension")
    if check_dimension(height).status != "supported":
        return SemanticCheck("dimension_pair", "rejected", "height is not a supported dimension")
    return SemanticCheck("dimension_pair", "supported", "both values satisfy dimension constraints")
