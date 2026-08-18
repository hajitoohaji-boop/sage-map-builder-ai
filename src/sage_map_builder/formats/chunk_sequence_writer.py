"""Lossless writer for RawChunk sequences."""
from __future__ import annotations
from .chunk_sequence_reader import RawChunk


def write_sequence(chunks: tuple[RawChunk, ...]) -> bytes:
    out = bytearray()
    for chunk in chunks:
        if chunk.header.data_size != len(chunk.payload):
            raise ValueError("RawChunk header size does not match payload")
        out.extend(chunk.header.pack())
        out.extend(chunk.payload)
    return bytes(out)
