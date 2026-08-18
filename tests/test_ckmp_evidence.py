from sage_map_builder.analysis.ckmp_evidence import first_ckmp_evidence, find_ckmp_evidence


def test_ckmp_evidence_records_observed_following_u32_only():
    data = b"EAR\x00" + b"x" * 10 + b"CkMp" + b"\x21\x00\x00\x00" + b"tail"
    evidence = first_ckmp_evidence(data)
    assert evidence is not None
    assert evidence.marker_offset == 14
    assert evidence.following_u32 == 33
    assert evidence.following_bytes == b"\x21\x00\x00\x00"


def test_ckmp_scanner_keeps_all_occurrences():
    data = b"CkMp\x01\x00\x00\x00---CkMp\x02\x00\x00\x00"
    items = find_ckmp_evidence(data)
    assert [item.marker_offset for item in items] == [0, 11]
    assert [item.following_u32 for item in items] == [1, 2]


def test_truncated_ckmp_does_not_invent_a_value():
    evidence = first_ckmp_evidence(b"abcCkMp\x01\x02")
    assert evidence is not None
    assert evidence.following_u32 is None
    assert evidence.following_bytes == b"\x01\x02"
