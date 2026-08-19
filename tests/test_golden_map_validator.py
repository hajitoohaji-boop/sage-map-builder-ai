from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "research" / "map_samples" / "validate_golden_samples.py"

spec = importlib.util.spec_from_file_location("validate_golden_samples", MODULE)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_golden_sample_validator_has_no_errors():
    assert module.validate(ROOT) == []
