"""Training script refactored from starter notebook."""

from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split


def main() -> None:
    repo_root = Path(__file__).resolve().parent.parent
    data_path = repo_root / "data" / "raw" / "winequality-red.csv"

    df = pd.read_csv(data_path, sep=";")
    df["good"] = (df["quality"] >= 7).astype(int)

    features = df.drop(columns=["quality", "good"])
    target = df["good"]

    x_train, x_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=0.2,
        random_state=42,
        stratify=target,
    )

    clf = RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42)
    clf.fit(x_train, y_train)

    predictions = clf.predict(x_test)
    acc = accuracy_score(y_test, predictions)
    f1 = f1_score(y_test, predictions)

    print(f"Accuracy: {acc:.4f}")
    print(f"F1: {f1:.4f}")


if __name__ == "__main__":
    main()
