"""Smoke test for project setup verification."""

from pathlib import Path


def test_smoke_setup() -> None:
    repo_root = Path(__file__).resolve().parent.parent
    raw_data = repo_root / "data" / "raw" / "winequality-red.csv"
    assert repo_root.exists()
    assert (repo_root / "src" / "train.py").exists()
    assert raw_data.exists()
