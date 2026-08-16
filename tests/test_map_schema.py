import pytest

from sage_map_builder.map.schema import BinarySpan, MapEvidence, OpaqueSection


def test_binary_span_end():
    assert BinarySpan(10, 5).end == 15


def test_evidence_rejects_out_of_bounds_span():
    evidence = MapEvidence(10, b"EAR\0", (), (BinarySpan(8, 3),))
    with pytest.raises(ValueError):
        evidence.validate()


def test_opaque_section_requires_exact_size():
    section = OpaqueSection(BinarySpan(0, 4), b"abc")
    with pytest.raises(ValueError):
        section.validate(10)
