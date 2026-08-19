from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SAMPLES = {
    "MY MAP.map": (28712, "7d4e1e0b21febd33a460f88a557c4a1e0b3fbb7c"),
    "CONTRA Custom Campaign The Battle for Lake Town.map": (
        147237,
        "b33c1ae19eea4c694bc8398571021e1cf1163e8c",
    ),
}


def test_golden_samples_exist_and_match_recorded_size():
    for name, (expected_size, _sha) in SAMPLES.items():
        data = (ROOT / name).read_bytes()
        assert len(data) == expected_size, name
        assert data[:4] == b"EAR\x00", name


def test_golden_samples_match_git_blob_sha():
    for name, (_expected_size, expected_sha) in SAMPLES.items():
        data = (ROOT / name).read_bytes()
        blob_header = f"blob {len(data)}\0".encode("ascii")
        actual_sha = hashlib.sha1(blob_header + data).hexdigest()
        assert actual_sha == expected_sha, name
