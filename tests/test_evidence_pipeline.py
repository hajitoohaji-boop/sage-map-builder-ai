from pathlib import Path
from sage_map_builder.pipeline.evidence_pipeline import analyze_samples, write_evidence_pipeline


def test_pipeline_combines_two_samples(tmp_path: Path):
    a = tmp_path / "a.map"
    b = tmp_path / "b.map"
    a.write_bytes(b"EAR\x00" + b"a" * 8 + b"CkMp" + b"1")
    b.write_bytes(b"EAR\x00" + b"b" * 8 + b"CkMp" + b"2")
    result = analyze_samples([a, b])
    assert result["schema_version"] == 1
    assert len(result["samples"]) == 2
    assert result["comparison"] is not None
    assert result["samples"][0]["semantic_interpretation"] is None


def test_pipeline_writes_json(tmp_path: Path):
    a = tmp_path / "a.map"
    a.write_bytes(b"EAR\x00" + b"x" * 12 + b"CkMp")
    out = tmp_path / "evidence.json"
    result = write_evidence_pipeline([a], out)
    assert out.exists()
    assert result["samples"][0]["sample"]["file"] == "a.map"
