from sage_map_builder.analysis.controlled_diff import diff_bytes


def test_controlled_diff_groups_contiguous_changes():
    result = diff_bytes(b"abcdef", b"abXYefZZ")
    assert result["changed_byte_count"] == 2
    assert result["added_byte_count"] == 2
    assert result["removed_byte_count"] == 0
    assert {tuple((r["start"], r["end"])) for r in result["changed_ranges"]} == {(2, 3), (6, 7)}
    assert result["semantic_interpretation"] is None


def test_controlled_diff_identical_files_have_no_changes():
    result = diff_bytes(b"same", b"same")
    assert result["changed_byte_count"] == 0
    assert result["added_byte_count"] == 0
    assert result["removed_byte_count"] == 0
    assert result["changed_ranges"] == []
