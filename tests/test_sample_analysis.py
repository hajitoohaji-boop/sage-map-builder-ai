import pytest

from sage_map_builder.analysis import compare_bytes, fingerprint


def test_fingerprint_is_stable() -> None:
    result = fingerprint(b"abc")
    assert result.size == 3
    assert result.sha256 == "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"


def test_compare_bytes_reports_changes_and_length() -> None:
    result = compare_bytes(b"abc", b"axcde")
    assert [(item.offset, item.left, item.right) for item in result] == [
        (1, ord("b"), ord("x")),
        (3, None, ord("d")),
        (4, None, ord("e")),
    ]


def test_compare_bytes_limit() -> None:
    result = compare_bytes(b"abc", b"xyz", limit=2)
    assert len(result) == 2


def test_compare_bytes_rejects_negative_limit() -> None:
    with pytest.raises(ValueError):
        compare_bytes(b"a", b"b", limit=-1)
