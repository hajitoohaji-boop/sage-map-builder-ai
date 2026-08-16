import pytest
from sage_map_builder.map.reader import MapReader
from sage_map_builder.model.edit_session import EditSession
from sage_map_builder.model.from_reader import document_from_reader


def make_session():
    raw = b"EAR\0abcdefghij"
    doc = document_from_reader(MapReader().read_bytes(raw, "sample.map"))
    return EditSession.start(doc, raw), raw


def test_edit_preview_and_commit():
    session, raw = make_session()
    session.patch(4, b"XYZ")
    assert session.preview_bytes() == b"EAR\0XYZdefghij"
    assert session.commit_bytes() == session.preview_bytes()


def test_rollback_restores_original():
    session, raw = make_session()
    session.patch(4, b"XYZ")
    session.rollback()
    assert session.preview_bytes() == raw


def test_wrong_document_size_is_rejected():
    session, raw = make_session()
    with pytest.raises(ValueError):
        EditSession.start(session.document, raw + b"x")
