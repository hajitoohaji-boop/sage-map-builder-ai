from sage_map_builder.map.hypotheses import FieldObservation
from sage_map_builder.map.verification import apply_rule, verify_observations


def observation(a: str, b: str) -> FieldObservation:
    return FieldObservation(4, a, b, 1, 2, "candidate", "raw")


def test_equal_bytes_remain_candidate_not_verified():
    status, reason = apply_rule(observation("01 00 00 00", "01 00 00 00"))
    assert status == "candidate"
    assert "semantic meaning" in reason


def test_different_bytes_are_rejected():
    status, _ = apply_rule(observation("01 00 00 00", "02 00 00 00"))
    assert status == "rejected"


def test_batch_verification():
    result = verify_observations([observation("aa", "aa"), observation("aa", "bb")])
    assert [item.status for item in result] == ["candidate", "rejected"]
