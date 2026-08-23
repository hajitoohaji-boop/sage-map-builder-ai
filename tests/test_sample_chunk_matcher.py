import struct

from sage_map_builder.formats.chunk_index import ChunkIndex
from sage_map_builder.formats.chunk_stream import scan
from sage_map_builder.formats.sample_chunk_matcher import candidates


def test_candidates_are_version_based_and_do_not_claim_semantics():
    data = struct.pack("<HH", 4, 2) + b"ab" + struct.pack("<HH", 1, 1) + b"x"
    result = candidates(ChunkIndex.from_spans(scan(data)))
    assert len(result) == 2
    assert result[0].identity.label == "HeightMapData"
    assert result[0].identity.semantic_status == "opaque"
