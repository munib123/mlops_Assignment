# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.5
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # 01 - Exploratory data analysis: Wine Quality (red)
#
# Dataset: [UCI Wine Quality](https://archive.ics.uci.edu/dataset/186/wine+quality), red wine,
# tracked with DVC at `data/raw/winequality-red.csv` (run `uv run dvc pull` first).
#
# Target: `good = 1` if `quality >= 7`, else `0`. `quality` is never used as a feature.
# Loading, cleaning and validation live in `src/` and are tested in `tests/`.

# %%
import sys
from pathlib import Path


def find_repo_root(start: Path) -> Path:
    for path in [start, *start.parents]:
        if (path / "pyproject.toml").exists():
            return path
    raise FileNotFoundError("pyproject.toml not found above " + str(start))


ROOT = find_repo_root(Path.cwd())
sys.path.insert(0, str(ROOT))

import matplotlib.pyplot as plt

from src.features import clean_column_names, load_raw, make_target
from src.validate_data import validate

RAW = ROOT / "data" / "raw" / "winequality-red.csv"

# %% [markdown]
# ## Load, clean and validate

# %%
df = make_target(clean_column_names(load_raw(RAW)))
problems = validate(df.drop(columns=["good"]))
print("shape:", df.shape)
print("validation problems:", problems or "none")

# %%
print(df.dtypes.to_string())

# %% [markdown]
# ## Nulls and duplicates

# %%
print("null values per column:")
print(df.isna().sum())
n_dupes = int(df.duplicated().sum())
print(f"\nexact duplicate rows: {n_dupes} of {len(df)} ({n_dupes / len(df):.1%})")

# %% [markdown]
# ## Summary statistics

# %%
df.describe().T.round(3)

# %% [markdown]
# ## Class balance

# %%
counts = df["good"].value_counts().sort_index()
print(counts.to_string())
print(f"share of good wines: {df['good'].mean():.1%}")
print("\nquality distribution:")
print(df["quality"].value_counts().sort_index().to_string())

# %% [markdown]
# ## Plots

# %%
fig, ax = plt.subplots(figsize=(6, 3.5))
df["quality"].value_counts().sort_index().plot.bar(ax=ax, color="#4c72b0")
ax.axvline(3.5, color="black", linestyle="--", linewidth=1)
ax.set_xlabel("quality score")
ax.set_ylabel("number of wines")
ax.set_title("Quality scores; right of the dashed line = good (>= 7)")
plt.tight_layout()
plt.show()

# %%
corr = df.drop(columns=["quality"]).corr()["good"].drop("good").sort_values()
fig, ax = plt.subplots(figsize=(6, 4))
corr.plot.barh(ax=ax, color=["#c44e52" if v < 0 else "#55a868" for v in corr])
ax.set_xlabel("correlation with good")
ax.set_title("Feature correlation with the target")
plt.tight_layout()
plt.show()

# %%
fig, axes = plt.subplots(1, 2, figsize=(9, 3.5))
for ax, col in zip(axes, ["alcohol", "volatile_acidity"], strict=True):
    for label, group in df.groupby("good"):
        ax.hist(group[col], bins=30, alpha=0.6, density=True, label=f"good = {label}")
    ax.set_xlabel(col)
    ax.set_ylabel("density")
    ax.legend()
fig.suptitle("Strongest positive and negative features by class")
plt.tight_layout()
plt.show()

# %% [markdown]
# ## Findings
#
# 1. The file has 1,599 rows and 12 columns, no null values, and every value is inside the ranges
#    checked by `src/validate_data.py`.
# 2. **240 rows (15.0%) are exact duplicates.** With a random split, copies of the same wine can
#    land in both train and test and inflate the scores. This motivates the data-update PR that
#    removes them.
# 3. The target is imbalanced: only 217 wines (13.6%) are good, so we report F1 for the positive
#    class and ROC AUC rather than relying on accuracy alone.
# 4. Alcohol has the strongest positive correlation with good (0.41), followed by citric acid (0.22)
#    and sulphates (0.20).
# 5. Volatile acidity has the strongest negative correlation (-0.27), followed by density (-0.15)
#    and total sulfur dioxide (-0.14).
