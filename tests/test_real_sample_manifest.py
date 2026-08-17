import hashlib
import json
from pathlib import Path


def test_manifest_contains_two_verified_samples_and_observations():
    manifest = json.loads(Path("research/map_samples/sample_manifest.json").read_text(encoding="utf-8"))
    samples = manifest["samples"]
    assert len(samples) == 2
    names = {s["file"] for s in samples}
    assert names == {"MY MAP.map", "CONTRA Custom Campaign The Battle for Lake Town.map"}
    for sample in samples:
        assert sample["size"] > 0
        assert len(sample["sha256"]) == 64
        assert sample["first_bytes_hex"].lower() == "45 41 52 00"
        assert "CkMp" in sample["verified_markers"]


def test_binary_samples_are_verified_if_present_in_checkout():
    manifest = json.loads(Path("research/map_samples/sample_manifest.json").read_text(encoding="utf-8"))
    root = Path(".")
    for sample in manifest["samples"]:
        path = root / sample["file"]
        if not path.exists():
            continue
        data = path.read_bytes()
        assert len(data) == sample["size"]
        assert hashlib.sha256(data).hexdigest() == sample["sha256"]
        assert data[:4] == bytes.fromhex("45 41 52 00")
        assert b"CkMp" in data
