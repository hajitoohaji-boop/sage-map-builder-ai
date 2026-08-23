import struct

from sage_map_builder.formats.chunk_index import ChunkIndex
from sage_map_builder.formats.chunk_stream import scan


def test_index_assigns_stable_ordinals_and_filters_version():
    data = (
        struct.pack("<HH", 4, 1) + b"a"
        + struct.pack("<HH", 7, 2) + b"bc"
        + struct.pack("<HH", 4, 3) + b"xyz"
    )
    index = ChunkIndex.from_spans(scan(data))
    assert [x.ordinal for x in index.by_version(4)] == [0, 2]
    assert index.items[1].span.header.data_size == 2
