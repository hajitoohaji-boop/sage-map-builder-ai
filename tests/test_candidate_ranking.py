import struct

from sage_map_builder.formats.candidate_ranking import rank
from sage_map_builder.formats.chunk_identity_table import identity
from sage_map_builder.formats.chunk_index import ChunkIndex
from sage_map_builder.formats.chunk_stream import scan


def test_candidate_ranking_is_deterministic():
    data = (
        struct.pack("<HH", 7, 1) + b"a"
        + struct.pack("<HH", 4, 1) + b"b"
    )
    index = ChunkIndex.from_spans(scan(data))
    result = rank(identity("HeightMapData", 4), tuple(item for item in index.items if item.span.header.version == 4))
    assert result[0].occurrence.ordinal == 1
    assert result[0].distance == 1
