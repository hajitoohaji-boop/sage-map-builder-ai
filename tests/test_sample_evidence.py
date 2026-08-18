from sage_map_builder.analysis.sample_evidence import collect_sample_evidence, sample_evidence_dict


def test_sample_evidence_is_deterministic_and_nonsemantic():
    data = b"EAR\x00" + b"x" * 10 + b"CkMp" + b"\x21\x00\x00\x00"
    report = collect_sample_evidence(data, "sample.map")
    assert report.file_name == "sample.map"
    assert report.size == len(data)
    assert report.prefix_hex.startswith("45 41 52 00")
    assert report.ckmp[0].following_u32 == 33
    assert report.source_chunk_markers == ()


def test_sample_evidence_dict_contains_hash_and_observations():
    result = sample_evidence_dict(b"EAR\x00CkMp\x01\x00\x00\x00", "x.map")
    assert result["file"] == "x.map"
    assert len(result["sha256"]) == 64
    assert result["ckmp"][0]["following_u32"] == 1
    assert "semantic_interpretation" not in result
