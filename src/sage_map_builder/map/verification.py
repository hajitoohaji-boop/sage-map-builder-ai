"""Explicit verification rules for binary-map field candidates."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from .hypotheses import FieldObservation


RuleResult = Literal["verified", "rejected", "candidate"]


@dataclass(frozen=True)
class VerificationRule:
    name: str
    description: str


RAW_EQUALITY = VerificationRule(
    "raw_equality",
    "Both samples contain identical raw bytes at the same offset.",
)


def apply_rule(observation: FieldObservation, rule: VerificationRule = RAW_EQUALITY) -> tuple[RuleResult, str]:
    if rule.name == "raw_equality":
        if observation.left_raw == observation.right_raw:
            return "candidate", "Raw equality is confirmed, but semantic meaning is not proven."
        return "rejected", "Raw bytes differ between samples."
    raise ValueError(f"unknown verification rule: {rule.name}")


def verify_observations(observations: list[FieldObservation], rule: VerificationRule = RAW_EQUALITY) -> list[FieldObservation]:
    results: list[FieldObservation] = []
    for item in observations:
        status, reason = apply_rule(item, rule)
        results.append(FieldObservation(
            offset=item.offset,
            left_raw=item.left_raw,
            right_raw=item.right_raw,
            left_little_u32=item.left_little_u32,
            right_little_u32=item.right_little_u32,
            status=status,
            reason=reason,
        ))
    return results
