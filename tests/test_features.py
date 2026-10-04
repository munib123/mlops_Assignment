from pathlib import Path

import pandas as pd

from src.features import clean_column_names, load_raw, make_target

SAMPLE = Path(__file__).parent / "data" / "sample.csv"


def test_load_raw_reads_semicolon_csv():
    df = load_raw(SAMPLE)
    assert len(df) == 300
    assert "fixed acidity" in df.columns
    assert len(df.columns) == 12


def test_clean_column_names():
    df = pd.DataFrame(columns=["Fixed Acidity", "pH", "total sulfur dioxide"])
    assert list(clean_column_names(df).columns) == [
        "fixed_acidity",
        "ph",
        "total_sulfur_dioxide",
    ]


def test_clean_column_names_does_not_mutate_input():
    df = pd.DataFrame(columns=["Fixed Acidity"])
    clean_column_names(df)
    assert list(df.columns) == ["Fixed Acidity"]


def test_make_target_threshold():
    df = pd.DataFrame({"quality": [3, 6, 7, 8]})
    assert make_target(df)["good"].tolist() == [0, 0, 1, 1]
    assert make_target(df, threshold=6)["good"].tolist() == [0, 1, 1, 1]
    assert make_target(df)["good"].dtype.kind == "i"
