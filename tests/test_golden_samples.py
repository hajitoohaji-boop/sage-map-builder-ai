from pathlib import Path
from sage_map_builder.pipeline.golden_samples import verify_sample


def test_known_sample_verification(tmp_path: Path):
    p = tmp_path / "MY MAP.map"
    p.write_bytes(b"EAR\x00" + b"x" * (28712 - 4))
    result = verify_sample(p)
    assert result["known_name"]
    assert result["size_matches"]
    assert result["starts_with_ear"]
    assert result["verified"] is False  # CkMp is intentionally required too.


def test_unknown_sample_is_not_verified(tmp_path: Path):
    p = tmp_path / "unknown.map"
    p.write_bytes(b"EAR\x00CkMp")
    result = verify_sample(p)
    assert result["known_name"] is False
    assert result["verified"] is False
