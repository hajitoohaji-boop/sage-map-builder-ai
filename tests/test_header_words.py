from sage_map_builder.map.header_words import extract_header_words


def test_extracts_raw_words_without_semantic_guessing():
    data = b"EAR\0" + bytes(range(4, 16))
    words = extract_header_words(data)
    assert words[0].offset == 0
    assert words[0].raw_hex == "45 41 52 00"
    assert words[0].little_u32 == 0x00524145
    assert words[0].big_u32 == 0x45415200


def test_limit_is_aligned_to_four_bytes():
    words = extract_header_words(bytes(range(20)), limit=10)
    assert [word.offset for word in words] == [0, 4, 8]
