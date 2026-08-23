import struct

from sage_map_builder.formats.chunk_fingerprint import fingerprint
from sage_map_builder.formats.chunk_identity_table import identity
from sage_map_builder.formats.chunk_index import ChunkIndex
from sage_map_builder.formats.chunk_stream import scan
from sage_map_builder.formats.evidence_bundle import CandidateEvidence


def test_candidate_evidence_is_deterministic_and_bounded():
    data = struct.pack("<HH", 4, 3) + b"abc"
    indexed = ChunkIndex.from_spans(scan(data)).items[0]
    spec = identity("HeightMapData", 4)
    item = CandidateEvidence(spec, indexed, fingerprint(data, indexed.span), True, True, "sample.map")
    assert item.score == 2
    assert item.promotable
    assert len(item.fingerprint.sha256) == 64
