"""Loading and feature helpers shared by the notebook and the pipeline."""

from pathlib import Path

import pandas as pd


def load_raw(path: str | Path) -> pd.DataFrame:
    """Read the raw Wine Quality CSV (semicolon-separated, UCI format)."""
    return pd.read_csv(path, sep=";")


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Lowercase column names and replace spaces with underscores."""
    out = df.copy()
    out.columns = [str(c).strip().lower().replace(" ", "_") for c in out.columns]
    return out


def make_target(df: pd.DataFrame, threshold: int = 7) -> pd.DataFrame:
    """Add the binary target ``good`` (1 if quality >= threshold, else 0)."""
    out = df.copy()
    out["good"] = (out["quality"] >= threshold).astype(int)
    return out
