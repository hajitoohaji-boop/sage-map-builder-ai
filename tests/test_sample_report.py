import hashlib
from pathlib import Path
from sage_map_builder.report.sample_report import build_sample_report


def test_sample_report_is_evidence_only(tmp_path: Path):
    p = tmp_path / "sample.map"
    data = b"EAR\x00abcdefghCkMp1234"
    p.write_bytes(data)
    report = build_sample_report(p)
    assert report["sample"]["size"] == len(data)
    assert report["sample"]["sha256"] == hashlib.sha256(data).hexdigest()
    assert report["markers"]["EAR\u0000"] == [0]
    assert report["markers"]["CkMp"] == [12]
    assert report["semantic_interpretation"] is None
    assert report["sections"]
