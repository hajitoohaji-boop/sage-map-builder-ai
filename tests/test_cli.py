import json
from pathlib import Path
from sage_map_builder.cli import main


def test_cli_writes_json_report(tmp_path: Path):
    (tmp_path / "sample.map").write_bytes(b"EAR\0" + b"x" * 12 + b"CkMp" + b"data")
    output = tmp_path / "report.json"
    assert main([str(tmp_path), "-o", str(output)]) == 0
    report = json.loads(output.read_text(encoding="utf-8"))
    assert report["sample_count"] == 1


def test_cli_builds_evidence_report(tmp_path: Path):
    source = tmp_path / "sample.map"
    output = tmp_path / "evidence.json"
    source.write_bytes(b"EAR\0CkMp")
    assert main(["report", str(source), "-o", str(output)]) == 0
    report = json.loads(output.read_text(encoding="utf-8"))
    assert report["semantic_interpretation"] is None


def test_cli_preserves_bytes(tmp_path: Path):
    source = tmp_path / "a.map"
    output = tmp_path / "b.map"
    source.write_bytes(b"EAR\0binary")
    assert main(["preserve", str(source), str(output)]) == 0
    assert output.read_bytes() == source.read_bytes()
