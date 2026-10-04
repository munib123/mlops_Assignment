# MLOps Assignment: Wine Quality Prediction

Collaborative Git-based Machine Learning engineering project adhering to rigorous MLOps practices, including DVC data and pipeline versioning, pre-commit enforcement, branch protection, CI automation, and reproducible release workflows.

## Project Overview

- **Dataset**: UCI Red Wine Quality (`data/raw/winequality-red.csv`, semicolon-separated)
  - UCI Archive: [Wine Quality Dataset](https://archive.ics.uci.edu/dataset/186/wine+quality)
- **Target**: Binary classification where `good = 1` if `quality >= 7` else `0`. The original `quality` column is strictly excluded from features to prevent data leakage.
- **Starter Code Reference**: [Kaggle Red Wine Quality Prediction](https://www.kaggle.com/code/bhumikasingh/red-wine-quality-prediction)

## Setup & Environment

This project utilizes `uv` for reproducible Python package management and virtual environment orchestration.

1. **Clone the repository**:
   ```bash
   git clone https://github.com/munib123/mlops_Assignment.git
   cd mlops_Assignment
   ```

2. **Sync dependencies**:
   ```bash
   uv sync
   ```

3. **Install pre-commit hooks**:
   ```bash
   uv run pre-commit install
   ```

## Running the Code

Execute the baseline training module from the repository root:

```bash
uv run python -m src.train
```

Run unit tests:

```bash
uv run pytest
```

Run code formatting and linting checks:

```bash
uv run ruff check .
uv run ruff format --check .
```
