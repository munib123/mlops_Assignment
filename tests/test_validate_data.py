from pathlib import Path

import numpy as np
import pytest

from src.features import clean_column_names, load_raw
from src.validate_data import main, validate

SAMPLE = Path(__file__).parent / "data" / "sample.csv"


@pytest.fixture
def clean_df():
    return clean_column_names(load_raw(SAMPLE))


def test_clean_frame_passes(clean_df):
    assert validate(clean_df) == []


def test_null_is_caught(clean_df):
    clean_df.loc[0, "alcohol"] = np.nan
    problems = validate(clean_df)
    assert any("alcohol" in p and "null" in p for p in problems)


def test_out_of_range_is_caught(clean_df):
    clean_df.loc[0, "ph"] = 9.0
    problems = validate(clean_df)
    assert any("ph" in p and "outside" in p for p in problems)


def test_negative_chemistry_is_caught(clean_df):
    clean_df.loc[0, "chlorides"] = -0.1
    assert any("chlorides" in p for p in validate(clean_df))


def test_missing_column_is_caught(clean_df):
    problems = validate(clean_df.drop(columns=["density"]))
    assert any("missing columns" in p for p in problems)


def test_too_few_rows_is_caught(clean_df):
    assert any("rows" in p for p in validate(clean_df.head(10)))


def test_cli_exit_codes(tmp_path, clean_df):
    assert main([str(SAMPLE)]) == 0
    bad = load_raw(SAMPLE)
    bad.loc[0, "pH"] = 9.0
    bad_path = tmp_path / "bad.csv"
    bad.to_csv(bad_path, sep=";", index=False)
    assert main([str(bad_path)]) == 1
