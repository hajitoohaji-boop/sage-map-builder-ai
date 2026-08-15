import pytest

from sage_map_builder.io import BinaryReader, BinaryReaderError


def test_reader_tracks_position_and_remaining() -> None:
    reader = BinaryReader(b"\x01\x02\x03")
    assert reader.size == 3
    assert reader.position == 0
    assert reader.remaining == 3
    assert reader.read_u8() == 1
    assert reader.position == 1
    assert reader.remaining == 2


def test_reader_uses_little_endian_for_unsigned_integers() -> None:
    reader = BinaryReader(b"\x34\x12\x78\x56\x34\x12")
    assert reader.read_u16() == 0x1234
    assert reader.read_u32() == 0x12345678


def test_reader_reads_float() -> None:
    reader = BinaryReader(b"\x00\x00\x20\x40")
    assert reader.read_f32() == pytest.approx(2.5)


def test_reader_rejects_truncated_read() -> None:
    reader = BinaryReader(b"\x01")
    with pytest.raises(BinaryReaderError):
        reader.read_u16()


def test_reader_rejects_invalid_seek() -> None:
    reader = BinaryReader(b"abc")
    with pytest.raises(BinaryReaderError):
        reader.seek(4)


def test_reader_requires_bytes() -> None:
    with pytest.raises(TypeError):
        BinaryReader(bytearray(b"abc"))  # type: ignore[arg-type]
