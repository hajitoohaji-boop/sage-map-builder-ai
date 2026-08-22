"""Small status model for binary MAP codec readiness."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class CodecStatus(str, Enum):
    OPAQUE = "opaque"
    EVIDENCE = "evidence"
    VERIFIED = "verified"


@dataclass(frozen=True)
class CodecReadiness:
    label: str
    version: int
    status: CodecStatus
    source_backed: bool
    sample_backed: bool
    round_trip_tested: bool

    @property
    def ready(self) -> bool:
        return (
            self.status is CodecStatus.VERIFIED
            and self.source_backed
            and self.sample_backed
            and self.round_trip_tested
        )
