from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


FEATURE_COLUMNS = [
    "acc_x",
    "acc_y",
    "acc_z",
    "gyro_x",
    "gyro_y",
    "gyro_z",
    "acc_magnitude",
    "gyro_magnitude",
]


@dataclass
class DatasetBundle:
    features: pd.DataFrame
    target: pd.Series


def _clean_sensor_frame(frame: pd.DataFrame, prefix: str) -> pd.DataFrame:
    renamed = frame.rename(
        columns={
            "x": f"{prefix}_x",
            "y": f"{prefix}_y",
            "z": f"{prefix}_z",
            "gt": "activity",
            "Creation_Time": "timestamp",
        }
    )
    renamed = renamed[["timestamp", f"{prefix}_x", f"{prefix}_y", f"{prefix}_z", "User", "Device", "activity"]]
    renamed = renamed.dropna()
    renamed = renamed[renamed["activity"].str.lower() != "null"]
    renamed["timestamp"] = pd.to_numeric(renamed["timestamp"], errors="coerce")
    renamed = renamed.dropna(subset=["timestamp"])
    renamed = renamed.sort_values(["User", "Device", "timestamp"]).reset_index(drop=True)
    return renamed


def load_and_prepare_dataset(
    accelerometer_path: str,
    gyroscope_path: str,
    sample_fraction: float,
    random_state: int,
    max_rows_per_sensor: int | None = None,
) -> DatasetBundle:
    use_columns = ["Creation_Time", "x", "y", "z", "User", "Device", "gt"]
    accel_df = pd.read_csv(accelerometer_path, usecols=use_columns, nrows=max_rows_per_sensor)
    gyro_df = pd.read_csv(gyroscope_path, usecols=use_columns, nrows=max_rows_per_sensor)

    accel_df = _clean_sensor_frame(accel_df, prefix="acc")
    gyro_df = _clean_sensor_frame(gyro_df, prefix="gyro")

    if 0 < sample_fraction < 1:
        accel_df = accel_df.sample(frac=sample_fraction, random_state=random_state).sort_values(
            ["User", "Device", "timestamp"]
        )
        gyro_df = gyro_df.sample(frac=sample_fraction, random_state=random_state).sort_values(
            ["User", "Device", "timestamp"]
        )

    merged_partitions = []

    for (user, device), accel_group in accel_df.groupby(["User", "Device"], sort=False):
        gyro_group = gyro_df[(gyro_df["User"] == user) & (gyro_df["Device"] == device)]
        if gyro_group.empty:
            continue

        joined = pd.merge_asof(
            accel_group.sort_values("timestamp"),
            gyro_group.sort_values("timestamp"),
            on="timestamp",
            by=["User", "Device"],
            direction="nearest",
            suffixes=("", "_gyro"),
        )
        joined = joined[joined["activity"] == joined["activity_gyro"]]
        merged_partitions.append(joined)

    if not merged_partitions:
        raise ValueError("No aligned accelerometer and gyroscope samples were found.")

    dataset = pd.concat(merged_partitions, ignore_index=True)
    dataset["acc_magnitude"] = np.sqrt(dataset["acc_x"] ** 2 + dataset["acc_y"] ** 2 + dataset["acc_z"] ** 2)
    dataset["gyro_magnitude"] = np.sqrt(dataset["gyro_x"] ** 2 + dataset["gyro_y"] ** 2 + dataset["gyro_z"] ** 2)

    features = dataset[FEATURE_COLUMNS].copy()
    target = dataset["activity"].copy()
    return DatasetBundle(features=features, target=target)


def engineer_single_prediction_features(sample: dict[str, float]) -> pd.DataFrame:
    acc_magnitude = float(np.sqrt(sample["acc_x"] ** 2 + sample["acc_y"] ** 2 + sample["acc_z"] ** 2))
    gyro_magnitude = float(np.sqrt(sample["gyro_x"] ** 2 + sample["gyro_y"] ** 2 + sample["gyro_z"] ** 2))

    return pd.DataFrame(
        [
            {
                "acc_x": sample["acc_x"],
                "acc_y": sample["acc_y"],
                "acc_z": sample["acc_z"],
                "gyro_x": sample["gyro_x"],
                "gyro_y": sample["gyro_y"],
                "gyro_z": sample["gyro_z"],
                "acc_magnitude": acc_magnitude,
                "gyro_magnitude": gyro_magnitude,
            }
        ]
    )
