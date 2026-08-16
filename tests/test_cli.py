import json
from sage_map_builder.cli import main


def test_cli_writes_json_report(tmp_path):
    (tmp_path / "sample.map").write_bytes(b"EAR\0" + b"x" * 12 + b"CkMp" + b"data")
    output = tmp_path / "report.json"
    assert main([str(tmp_path), "-o", str(output)]) == 0
    report = json.loads(output.read_text(encoding="utf-8"))
    assert report["sample_count"] == 1
