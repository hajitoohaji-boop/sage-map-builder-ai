"""Unified cross-sample report built only from observable evidence."""
from __future__ import annotations
from pathlib import Path
import hashlib
import json


def compare_bytes(left: bytes, right: bytes) -> dict:
    count = min(len(left), len(right))
    equal = sum(left[i] == right[i] for i in range(count))
    return {
        "common_length": count,
        "equal_byte_count": equal,
        "different_byte_count": count - equal,
        "left_size": len(left),
        "right_size": len(right),
        "left_sha256": hashlib.sha256(left).hexdigest(),
        "right_sha256": hashlib.sha256(right).hexdigest(),
    }


def build_compare_report(left_path: Path, right_path: Path) -> dict:
    left, right = left_path.read_bytes(), right_path.read_bytes()
    return {
        "schema_version": 1,
        "left": left_path.name,
        "right": right_path.name,
        "comparison": compare_bytes(left, right),
        "semantic_interpretation": None,
        "interpretation_rule": "Byte equality/difference is evidence only; it does not identify field meaning.",
    }


def write_compare_report(left_path: Path, right_path: Path, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(build_compare_report(left_path, right_path), indent=2) + "\n", encoding="utf-8")
