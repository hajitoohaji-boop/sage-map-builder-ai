from sage_map_builder.formats.chunk_identity_table import identity
from sage_map_builder.formats.evidence_bundle import CandidateEvidence
from sage_map_builder.formats.evidence_matrix import build_matrix
from sage_map_builder.formats.sample_evidence import SampleEvidence
from sage_map_builder.formats.chunk_index import ChunkIndex
from sage_map_builder.formats.chunk_stream import scan
from sage_map_builder.formats.chunk_fingerprint import fingerprint
import struct


def make_evidence(sample: str, label: str, version: int) -> CandidateEvidence:
    data = struct.pack('<HH', version, 1) + b'x'
    item = ChunkIndex.from_spans(scan(data)).items[0]
    return CandidateEvidence(identity(label, version), item, fingerprint(data, item.span), True, True, sample)


def test_matrix_compares_known_identity_across_two_samples():
    left = SampleEvidence('a.map', (make_evidence('a.map', 'HeightMapData', 4),))
    right = SampleEvidence('b.map', (make_evidence('b.map', 'HeightMapData', 4),))
    cell = next(c for c in build_matrix(left, right) if c.identity.label == 'HeightMapData')
    assert cell.comparable
    assert cell.score == 4
