"""Verification helpers for the repository's two known real samples."""
from __future__ import annotations
import hashlib
from pathlib import Path

EXPECTED = {
    "MY MAP.map": {"size": 28712, "sha256": None},
    "CONTRA Custom Campaign The Battle for Lake Town.map": {"size": 147237, "sha256": None},
}


def verify_sample(path: str | Path) -> dict:
    path = Path(path)
    data = path.read_bytes()
    result = {
        "file": path.name,
        "size": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "starts_with_ear": data[:4] == b"EAR\x00",
        "has_ckmp": b"CkMp" in data,
        "known_name": path.name in EXPECTED,
    }
    expected = EXPECTED.get(path.name)
    result["expected_size"] = expected["size"] if expected else None
    result["size_matches"] = expected is not None and result["size"] == expected["size"]
    result["verified"] = result["size_matches"] and result["starts_with_ear"] and result["has_ckmp"]
    return result
