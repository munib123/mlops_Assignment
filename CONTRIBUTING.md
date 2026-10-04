# Contributing Guidelines

Welcome to the ML Collab project. All contributors must adhere to these branching conventions, commit standards, and merge policies.

---

## 1. Branching Strategy

We follow a three-tier branch hierarchy: `dev` → `staging` → `main`.

- **`main`**: Production branch containing tagged model releases (e.g. `model-v1.0`). No direct pushes allowed.
- **`staging`**: Pre-release verification branch where candidate releases are validated and independently reproduced.
- **`dev`**: Active integration branch where features, data updates, and fixes land via reviewed pull requests.

### Branch Naming Conventions
- `feat/<name>`: New model or pipeline features, starting from `origin/dev` and merging into `dev`.
- `data/<name>`: Dataset versioning, cleaning, or validation updates, starting from `origin/dev` and merging into `dev`.
- `exp/<member>-<idea>`: Exploratory experiment sweeps (e.g. `exp/abdullah-gradient-boosting`). These branches are pushed to GitHub for visibility but are never merged into `dev`.
- `fix/<name>`: Bug fixes or hotfixes starting from `origin/main` (for hotfixes) or `origin/dev`.

---

## 2. Commit Standards

We enforce [Conventional Commits](https://www.conventionalcommits.org/):
- `feat:` New features or pipeline additions (e.g., `feat: add scaling step`)
- `data:` Dataset additions or updates (e.g., `data: remove duplicate rows`)
- `exp:` Experiment tracking code or logs (e.g., `exp: try max_depth=8`)
- `fix:` Bug fixes (e.g., `fix: resolve max_depth conflict after rebase`)
- `test:` Adding or modifying tests (e.g., `test: add pipeline integration tests`)
- `docs:` Documentation updates (e.g., `docs: update CONTRIBUTING.md`)
- `ci:` Continuous integration changes (e.g., `ci: configure GitHub Actions workflow`)
- `chore:` Maintenance tasks or pipeline lock updates (e.g., `chore: record baseline pipeline outputs`)
- `build:` Dependency or packaging updates (e.g., `build: pin environment with uv`)

Keep commits atomic, descriptive, and focused on one logical change.

---

## 3. Merge Policy

- **PRs into `dev` and `fix/` PRs**: Must use **Squash and merge**.
- **Promotions (`dev` → `staging`, `staging` → `main`, and `main` → `dev`)**: Must use **Create a merge commit**.
  - **Never** squash promotion PRs.
  - **Never** delete `dev`, `staging`, or `main`.

---

## 4. Collaboration Rules & Guardrails

1. **No direct pushes**: Never push directly to `dev`, `staging`, or `main`. All work enters through Pull Requests.
2. **Review requirements**: Every PR requires at least 1 approval from a designated peer reviewer.
3. **Reviewer merges**: The author **never** merges their own PR; only the reviewer merges upon successful review.
4. **Data & model versioning**: Run `uv run dvc push` **before** `git push` whenever data or model artifacts change.
5. **Committed experiments**: Never run experiments on uncommitted code. Commit code and configuration changes prior to running DVC experiments.
6. **Rebase before PR**: Always rebase on the latest `origin/dev` before submitting a PR:
   ```bash
   git fetch origin && git rebase origin/dev
   ```
7. **Lock file exclusivity**: Only one open PR may modify `pyproject.toml` or `uv.lock` at a time to prevent dependency conflicts.
8. **Pre-commit hooks**: Ensure hooks are installed once per clone before making commits:
   ```bash
   uv run pre-commit install
   ```
