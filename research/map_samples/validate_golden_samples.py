"""Validate the repository's golden map samples without interpreting payload bytes."""
from __future__ import annotations

import hashlib
from pathlib import Path

SAMPLES = {
    "MY MAP.map": (28712, "7d4e1e0b21febd33a460f88a557c4a1e0b3fbb7c"),
    "CONTRA Custom Campaign The Battle for Lake Town.map": (
        147237,
        "b33c1ae19eea4c694bc8398571021e1cf1163e8c",
    ),
}


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    for name, (size, sha) in SAMPLES.items():
        path = root / name
        if not path.is_file():
            errors.append(f"missing: {name}")
            continue
        data = path.read_bytes()
        if len(data) != size:
            errors.append(f"size mismatch: {name}")
        if git_blob_sha(data) != sha:
            errors.append(f"sha mismatch: {name}")
        if data[:4] != b"EAR\x00":
            errors.append(f"missing EAR header: {name}")
    return errors
