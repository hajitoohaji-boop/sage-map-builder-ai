"""Conservative candidate-field engine for binary map research.

A candidate is evidence, never a semantic fact. Promotion to a verified field
requires an explicit rule and independent confirmation.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
import json
from pathlib import Path
from typing import Literal


Status = Literal["candidate", "rejected", "verified"]


@dataclass(frozen=True)
class FieldObservation:
    offset: int
    left_raw: str
    right_raw: str
    left_little_u32: int
    right_little_u32: int
    status: Status
    reason: str


def generate_candidates(left_words: list[dict], right_words: list[dict]) -> list[FieldObservation]:
    right = {int(row["offset"]): row for row in right_words}
    result: list[FieldObservation] = []
    for row in left_words:
        other = right.get(int(row["offset"]))
        if other is None:
            continue
        same = row["raw_hex"] == other["raw_hex"]
        result.append(FieldObservation(
            offset=int(row["offset"]),
            left_raw=row["raw_hex"],
            right_raw=other["raw_hex"],
            left_little_u32=int(row["little_u32"]),
            right_little_u32=int(other["little_u32"]),
            status="candidate",
            reason="same raw bytes across samples" if same else "same offset with differing raw bytes",
        ))
    return result


def write_candidates(candidates: list[FieldObservation], output: str | Path) -> None:
    Path(output).write_text(
        json.dumps([asdict(item) for item in candidates], indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
