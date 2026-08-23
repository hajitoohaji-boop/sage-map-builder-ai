import struct

from sage_map_builder.formats.chunk_identity_table import identity
from sage_map_builder.formats.chunk_index import ChunkIndex
from sage_map_builder.formats.chunk_stream import scan
from sage_map_builder.formats.order_evidence import score


def test_order_evidence_is_strong_only_at_expected_position():
    data = struct.pack("<HH", 4, 1) + b"x"
    occurrence = ChunkIndex.from_spans(scan(data)).items[0]
    evidence = score(identity("HeightMapData", 4), occurrence)
    assert evidence.strong
    assert evidence.distance == 0
