from sage_map_builder.map.header_word_compare import compare_header_words


def test_same_and_different_words_are_classified():
    left = b"EAR\0" + (1).to_bytes(4, "little") + (2).to_bytes(4, "little")
    right = b"EAR\0" + (1).to_bytes(4, "little") + (5).to_bytes(4, "little")
    rows = compare_header_words(left, right)
    assert rows[0]["status"] == "same"
    assert rows[1]["status"] == "same"
    assert rows[2]["status"] == "different"
    assert rows[2]["little_difference"] == 3


def test_right_only_word_is_reported():
    rows = compare_header_words(b"EAR\0", b"EAR\0" + b"\x01\x00\x00\x00")
    assert rows[-1]["status"] == "right_only"
