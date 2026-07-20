from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

from .config import ARTIFACTS_DIR, REPORTS_DIR
from .data_utils import download_dataset, extract_dataset
from .features import FEATURE_COLUMNS, load_and_prepare_dataset

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
LOGGER = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train an HHAR activity classifier.")
    parser.add_argument("--sample-fraction", type=float, default=0.05, help="Fraction of rows to sample from each file.")
    parser.add_argument(
        "--max-rows-per-sensor",
        type=int,
        default=200000,
        help="Maximum number of rows to load from each sensor CSV for faster experimentation.",
    )
    parser.add_argument("--random-state", type=int, default=42, help="Random state for reproducibility.")
    parser.add_argument("--force-download", action="store_true", help="Download the dataset archive again.")
    return parser.parse_args()


def save_confusion_matrix(y_true, y_pred, labels: list[str], output_path: Path) -> None:
    matrix = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(10, 7))
    sns.heatmap(matrix, annot=True, fmt="d", cmap="Blues", xticklabels=labels, yticklabels=labels)
    plt.title("HHAR Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.tight_layout()
    plt.savefig(output_path, dpi=160)
    plt.close()


def main() -> None:
    args = parse_args()

    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    archive_path = download_dataset(force_download=args.force_download)
    extracted_dir = extract_dataset(archive_path)

    accelerometer_path = extracted_dir / "Phones_accelerometer.csv"
    gyroscope_path = extracted_dir / "Phones_gyroscope.csv"

    dataset = load_and_prepare_dataset(
        accelerometer_path=str(accelerometer_path),
        gyroscope_path=str(gyroscope_path),
        sample_fraction=args.sample_fraction,
        random_state=args.random_state,
        max_rows_per_sensor=args.max_rows_per_sensor,
    )

    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(dataset.target)

    X_train, X_test, y_train, y_test = train_test_split(
        dataset.features,
        y_encoded,
        test_size=0.2,
        random_state=args.random_state,
        stratify=y_encoded,
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = RandomForestClassifier(
        n_estimators=250,
        max_depth=18,
        min_samples_split=8,
        min_samples_leaf=3,
        n_jobs=-1,
        random_state=args.random_state,
        class_weight="balanced_subsample",
    )
    model.fit(X_train_scaled, y_train)

    predictions = model.predict(X_test_scaled)
    class_names = label_encoder.inverse_transform(sorted(set(y_encoded)))

    accuracy = accuracy_score(y_test, predictions)
    macro_f1 = f1_score(y_test, predictions, average="macro")
    report_dict = classification_report(y_test, predictions, target_names=class_names, output_dict=True)

    metrics = {
        "accuracy": accuracy,
        "macro_f1": macro_f1,
        "sample_fraction": args.sample_fraction,
        "max_rows_per_sensor": args.max_rows_per_sensor,
        "random_state": args.random_state,
        "feature_columns": FEATURE_COLUMNS,
        "classes": class_names.tolist(),
    }

    joblib.dump(model, ARTIFACTS_DIR / "hhar_random_forest.joblib")
    joblib.dump(scaler, ARTIFACTS_DIR / "hhar_scaler.joblib")
    joblib.dump(label_encoder, ARTIFACTS_DIR / "hhar_label_encoder.joblib")

    with (ARTIFACTS_DIR / "metrics.json").open("w", encoding="utf-8") as file_handle:
        json.dump(metrics, file_handle, indent=2)

    pd.DataFrame(report_dict).transpose().to_csv(REPORTS_DIR / "classification_report.csv", index=True)
    save_confusion_matrix(y_test, predictions, class_names.tolist(), REPORTS_DIR / "confusion_matrix.png")

    LOGGER.info("Training complete. Accuracy: %.4f | Macro F1: %.4f", accuracy, macro_f1)
    LOGGER.info("Artifacts written to %s", ARTIFACTS_DIR)


if __name__ == "__main__":
    main()
