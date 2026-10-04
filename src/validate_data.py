"""Data checks for the Wine Quality dataset.

Usage: uv run python -m src.validate_data <csv>
Prints a report and exits 1 if any problem is found.
"""

import argparse
import sys
from pathlib import Path

import pandas as pd
from pandas.api.types import is_bool_dtype, is_integer_dtype, is_numeric_dtype

from src.features import clean_column_names, load_raw

CHEMISTRY_COLUMNS = [
    "fixed_acidity",
    "volatile_acidity",
    "citric_acid",
    "residual_sugar",
    "chlorides",
    "free_sulfur_dioxide",
    "total_sulfur_dioxide",
    "density",
    "ph",
    "sulphates",
    "alcohol",
]
EXPECTED_COLUMNS = [*CHEMISTRY_COLUMNS, "quality"]

# Bounds are set around the observed min/max of the raw file, with headroom.
VALUE_RANGES = {
    "fixed_acidity": (0, 20),
    "volatile_acidity": (0, 2),
    "citric_acid": (0, 1.5),
    "residual_sugar": (0, 20),
    "chlorides": (0, 1),
    "free_sulfur_dioxide": (0, 100),
    "total_sulfur_dioxide": (0, 400),
    "density": (0.98, 1.01),
    "ph": (2, 5),
    "sulphates": (0, 3),
    "alcohol": (5, 20),
    "quality": (0, 10),
}
MIN_ROWS = 100


def validate(df: pd.DataFrame) -> list[str]:
    """Return a list of problems; an empty list means the data is valid."""
    problems: list[str] = []

    missing = [c for c in EXPECTED_COLUMNS if c not in df.columns]
    extra = [c for c in df.columns if c not in EXPECTED_COLUMNS]
    if missing:
        problems.append(f"missing columns: {missing}")
    if extra:
        problems.append(f"unexpected columns: {extra}")

    for col in CHEMISTRY_COLUMNS:
        if col in df.columns and (not is_numeric_dtype(df[col]) or is_bool_dtype(df[col])):
            problems.append(f"{col}: expected numeric dtype, got {df[col].dtype}")
    if "quality" in df.columns and not is_integer_dtype(df["quality"]):
        problems.append(f"quality: expected integer dtype, got {df['quality'].dtype}")

    nulls = df.isna().sum()
    for col, count in nulls[nulls > 0].items():
        problems.append(f"{col}: {count} null value(s)")

    for col, (low, high) in VALUE_RANGES.items():
        if col not in df.columns:
            continue
        values = pd.to_numeric(df[col], errors="coerce")
        bad = int(((values < low) | (values > high)).sum())
        if bad:
            problems.append(f"{col}: {bad} value(s) outside [{low}, {high}]")

    if len(df) < MIN_ROWS:
        problems.append(f"only {len(df)} rows, expected at least {MIN_ROWS}")

    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate a raw Wine Quality CSV.")
    parser.add_argument("csv", type=Path, help="path to a semicolon-separated CSV")
    args = parser.parse_args(argv)

    df = clean_column_names(load_raw(args.csv))
    problems = validate(df)
    print(f"Validated {args.csv}: {len(df)} rows, {len(df.columns)} columns")
    if problems:
        print(f"FAILED with {len(problems)} problem(s):")
        for problem in problems:
            print(f"  - {problem}")
        return 1
    print("OK: schema, nulls, value ranges and row count all pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
