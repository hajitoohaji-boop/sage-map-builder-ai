from sage_map_builder.map.evidence import make_evidence
from research.map_samples.section_evidence import boundaries, section_evidence


def test_boundaries_are_only_observed_marker_positions():
    data = b"AAAAEAR\x00BBBB CkMpCCCC"
    assert boundaries(data, (b"EAR\x00", b"CkMp")) == (0, 4, 13, len(data))


def test_section_evidence_is_deterministic_and_opaque():
    data = b"AAAACkMpBBBB"
    sections = section_evidence(data, (b"CkMp",))
    assert [(s.start, s.end, s.length) for s in sections] == [(0, 4, 4), (4, 12, 8)]
    assert sections[0].preview_hex == "41 41 41 41"
    assert len(sections[0].sha256) == 64
